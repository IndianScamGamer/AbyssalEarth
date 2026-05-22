#include "EmberVentHazard.h"
#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"

AEmberVentHazard::AEmberVentHazard()
{
    PrimaryActorTick.bCanEverTick = false;

    SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
    SetRootComponent(SceneRoot);

    VentMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("VentMesh"));
    VentMesh->SetupAttachment(SceneRoot);
    VentMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);

    VentLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("VentLight"));
    VentLight->SetupAttachment(SceneRoot);
    VentLight->SetIntensity(0.0f);
    VentLight->SetLightColor(FLinearColor(1.0f, 0.45f, 0.15f));
    VentLight->SetAttenuationRadius(700.0f);
}

void AEmberVentHazard::BeginPlay()
{
    Super::BeginPlay();

    if (bStartActive)
    {
        SetVentActive(true);
    }
    else
    {
        CurrentPhase = EEmberVentPhase::Idle;
        BroadcastPhaseEvent(CurrentPhase);
    }
}

void AEmberVentHazard::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    ClearTimers();
    Super::EndPlay(EndPlayReason);
}

void AEmberVentHazard::SetVentActive(bool bNewActive)
{
    if (bVentActive == bNewActive)
    {
        return;
    }

    bVentActive = bNewActive;

    if (!bVentActive)
    {
        ClearTimers();
        if (CurrentPhase != EEmberVentPhase::Idle)
        {
            EnterPhase(EEmberVentPhase::Idle);
        }
        return;
    }

    EEmberVentPhase StartPhase = EEmberVentPhase::Idle;
    float OverrideElapsed = 0.0f;

    const float Offset = bRandomizeInitialPhaseOffset
        ? FMath::FRand()
        : FMath::Clamp(InitialPhaseOffset, 0.0f, 1.0f);

    const float Total = FMath::Max(IdleDuration + WarningDuration + EruptDuration + CooldownDuration, KINDA_SMALL_NUMBER);
    float TargetTime = Offset * Total;

    if (TargetTime < IdleDuration)
    {
        StartPhase = EEmberVentPhase::Idle;
        OverrideElapsed = TargetTime;
    }
    else if ((TargetTime -= IdleDuration) < WarningDuration)
    {
        StartPhase = EEmberVentPhase::Warning;
        OverrideElapsed = TargetTime;
    }
    else if ((TargetTime -= WarningDuration) < EruptDuration)
    {
        StartPhase = EEmberVentPhase::Erupting;
        OverrideElapsed = TargetTime;
    }
    else
    {
        StartPhase = EEmberVentPhase::Cooldown;
        OverrideElapsed = FMath::Max(TargetTime - EruptDuration, 0.0f);
    }

    EnterPhase(StartPhase);

    if (UWorld* World = GetWorld())
    {
        const float Remaining = FMath::Max(GetPhaseDuration(StartPhase) - OverrideElapsed, KINDA_SMALL_NUMBER);
        PhaseStartTime = World->GetTimeSeconds() - OverrideElapsed;
        World->GetTimerManager().ClearTimer(PhaseTimerHandle);
        World->GetTimerManager().SetTimer(PhaseTimerHandle, this, &AEmberVentHazard::AdvancePhase, Remaining, false);
    }
}

bool AEmberVentHazard::IsVentActive() const
{
    return bVentActive;
}

EEmberVentPhase AEmberVentHazard::GetCurrentPhase() const
{
    return CurrentPhase;
}

float AEmberVentHazard::GetTimeInCurrentPhase() const
{
    const UWorld* World = GetWorld();
    if (!World)
    {
        return 0.0f;
    }
    return FMath::Max(World->GetTimeSeconds() - PhaseStartTime, 0.0f);
}

float AEmberVentHazard::GetCurrentPhaseDuration() const
{
    return GetPhaseDuration(CurrentPhase);
}

float AEmberVentHazard::GetCurrentPhaseProgress() const
{
    const float Duration = GetCurrentPhaseDuration();
    if (Duration <= KINDA_SMALL_NUMBER)
    {
        return 1.0f;
    }
    return FMath::Clamp(GetTimeInCurrentPhase() / Duration, 0.0f, 1.0f);
}

void AEmberVentHazard::EnterPhase(EEmberVentPhase NewPhase)
{
    CurrentPhase = NewPhase;

    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    PhaseStartTime = World->GetTimeSeconds();

    World->GetTimerManager().ClearTimer(DamageTimerHandle);
    if (CurrentPhase == EEmberVentPhase::Erupting && DamagePerSecond > 0.0f)
    {
        World->GetTimerManager().SetTimer(DamageTimerHandle, this, &AEmberVentHazard::TickDamage, DamageTickInterval, true, 0.0f);
    }

    BroadcastPhaseEvent(CurrentPhase);

    if (bVentActive)
    {
        const float Duration = FMath::Max(GetPhaseDuration(CurrentPhase), KINDA_SMALL_NUMBER);
        World->GetTimerManager().ClearTimer(PhaseTimerHandle);
        World->GetTimerManager().SetTimer(PhaseTimerHandle, this, &AEmberVentHazard::AdvancePhase, Duration, false);
    }
}

void AEmberVentHazard::AdvancePhase()
{
    if (!bVentActive)
    {
        return;
    }
    EnterPhase(GetNextPhase(CurrentPhase));
}

void AEmberVentHazard::TickDamage()
{
    if (CurrentPhase != EEmberVentPhase::Erupting)
    {
        return;
    }

    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    const float DamageThisTick = DamagePerSecond * DamageTickInterval;
    TSubclassOf<UDamageType> DamageType = EruptDamageType ? EruptDamageType : TSubclassOf<UDamageType>(UDamageType::StaticClass());

    static const TArray<AActor*> IgnoreActors;
    UGameplayStatics::ApplyRadialDamage(
        World,
        DamageThisTick,
        GetActorLocation(),
        DamageRadius,
        DamageType,
        IgnoreActors,
        this,
        nullptr,
        false,
        ECC_Visibility);
}

void AEmberVentHazard::ClearTimers()
{
    if (UWorld* World = GetWorld())
    {
        World->GetTimerManager().ClearTimer(PhaseTimerHandle);
        World->GetTimerManager().ClearTimer(DamageTimerHandle);
    }
}

float AEmberVentHazard::GetPhaseDuration(EEmberVentPhase Phase) const
{
    switch (Phase)
    {
    case EEmberVentPhase::Idle:     return IdleDuration;
    case EEmberVentPhase::Warning:  return WarningDuration;
    case EEmberVentPhase::Erupting: return EruptDuration;
    case EEmberVentPhase::Cooldown: return CooldownDuration;
    default:                        return 0.0f;
    }
}

EEmberVentPhase AEmberVentHazard::GetNextPhase(EEmberVentPhase Phase) const
{
    switch (Phase)
    {
    case EEmberVentPhase::Idle:     return EEmberVentPhase::Warning;
    case EEmberVentPhase::Warning:  return EEmberVentPhase::Erupting;
    case EEmberVentPhase::Erupting: return EEmberVentPhase::Cooldown;
    case EEmberVentPhase::Cooldown: return EEmberVentPhase::Idle;
    default:                        return EEmberVentPhase::Idle;
    }
}

void AEmberVentHazard::BroadcastPhaseEvent(EEmberVentPhase Phase)
{
    switch (Phase)
    {
    case EEmberVentPhase::Idle:     OnVentIdle();     break;
    case EEmberVentPhase::Warning:  OnVentWarning();  break;
    case EEmberVentPhase::Erupting: OnVentErupting(); break;
    case EEmberVentPhase::Cooldown: OnVentCooldown(); break;
    default: break;
    }

    OnVentPhaseChanged.Broadcast(Phase);
}
