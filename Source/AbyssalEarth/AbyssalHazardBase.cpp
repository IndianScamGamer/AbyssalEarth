#include "AbyssalHazardBase.h"
#include "Components/PrimitiveComponent.h"
#include "GameFramework/DamageType.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"

AAbyssalHazardBase::AAbyssalHazardBase()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AAbyssalHazardBase::BeginPlay()
{
    Super::BeginPlay();

    if (bStartActive)
    {
        if (bRandomizeInitialPhaseOffset)
        {
            // Skip into a random fraction of Idle so nearby hazards are staggered.
            const float OffsetSeconds = FMath::FRandRange(0.0f, IdleDuration);
            GetWorldTimerManager().SetTimer(PhaseTimerHandle,
                this, &AAbyssalHazardBase::AdvancePhase,
                FMath::Max(IdleDuration - OffsetSeconds, KINDA_SMALL_NUMBER),
                false);
            CurrentPhase = EHazardPhase::Idle;
            PhaseStartTime = GetWorld()->GetTimeSeconds() - OffsetSeconds;
            bHazardActive = true;
            OnHazardIdle();
        }
        else
        {
            const float OffsetSeconds = InitialPhaseOffset * IdleDuration;
            GetWorldTimerManager().SetTimer(PhaseTimerHandle,
                this, &AAbyssalHazardBase::AdvancePhase,
                FMath::Max(IdleDuration - OffsetSeconds, KINDA_SMALL_NUMBER),
                false);
            CurrentPhase = EHazardPhase::Idle;
            PhaseStartTime = GetWorld()->GetTimeSeconds() - OffsetSeconds;
            bHazardActive = true;
            OnHazardIdle();
        }
        OnHazardActivated.Broadcast();
    }
}

void AAbyssalHazardBase::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    ClearTimers();
    Super::EndPlay(EndPlayReason);
}

void AAbyssalHazardBase::SetHazardActive(bool bNewActive)
{
    if (bHazardActive == bNewActive)
    {
        return;
    }

    bHazardActive = bNewActive;

    if (bHazardActive)
    {
        EnterPhase(EHazardPhase::Idle);
        OnHazardActivated.Broadcast();
    }
    else
    {
        ClearTimers();
        CurrentPhase = EHazardPhase::Idle;
        OnHazardDeactivated.Broadcast();
    }
}

float AAbyssalHazardBase::GetPhaseProgress() const
{
    const float Duration = GetPhaseDuration(CurrentPhase);
    if (Duration <= 0.0f)
    {
        return 1.0f;
    }
    return FMath::Clamp(GetTimeInCurrentPhase() / Duration, 0.0f, 1.0f);
}

float AAbyssalHazardBase::GetTimeInCurrentPhase() const
{
    return GetWorld() ? (GetWorld()->GetTimeSeconds() - PhaseStartTime) : 0.0f;
}

void AAbyssalHazardBase::RegisterDamagePrimitive(UPrimitiveComponent* Primitive)
{
    if (!Primitive)
    {
        return;
    }

    DamagePrimitives.AddUnique(Primitive);

    if (DamageMode == EHazardDamageMode::Overlap)
    {
        Primitive->OnComponentBeginOverlap.AddDynamic(this, &AAbyssalHazardBase::HandleOverlapBegin);
        Primitive->OnComponentEndOverlap.AddDynamic(this, &AAbyssalHazardBase::HandleOverlapEnd);
    }
}

void AAbyssalHazardBase::UnregisterDamagePrimitive(UPrimitiveComponent* Primitive)
{
    if (!Primitive)
    {
        return;
    }

    DamagePrimitives.Remove(Primitive);

    Primitive->OnComponentBeginOverlap.RemoveDynamic(this, &AAbyssalHazardBase::HandleOverlapBegin);
    Primitive->OnComponentEndOverlap.RemoveDynamic(this, &AAbyssalHazardBase::HandleOverlapEnd);
}

// -----------------------------------------------------------------------------
// Internal phase machine
// -----------------------------------------------------------------------------

void AAbyssalHazardBase::EnterPhase(EHazardPhase NewPhase)
{
    CurrentPhase = NewPhase;
    PhaseStartTime = GetWorld()->GetTimeSeconds();

    BroadcastPhaseEvent(NewPhase);

    const float Duration = GetPhaseDuration(NewPhase);

    if (NewPhase == EHazardPhase::Active)
    {
        StartDamageTick();
    }
    else
    {
        StopDamageTick();
    }

    if (Duration > 0.0f)
    {
        GetWorldTimerManager().SetTimer(PhaseTimerHandle,
            this, &AAbyssalHazardBase::AdvancePhase,
            Duration, false);
    }
    else
    {
        // Instantaneous phase — advance next frame via zero-duration timer.
        GetWorldTimerManager().SetTimerForNextTick(this, &AAbyssalHazardBase::AdvancePhase);
    }
}

void AAbyssalHazardBase::AdvancePhase()
{
    if (!bHazardActive)
    {
        return;
    }
    EnterPhase(GetNextPhase(CurrentPhase));
}

void AAbyssalHazardBase::StartDamageTick()
{
    if (DamageMode == EHazardDamageMode::None)
    {
        return;
    }

    GetWorldTimerManager().SetTimer(DamageTimerHandle,
        this, &AAbyssalHazardBase::TickDamage,
        DamageTickInterval, true, 0.0f);
}

void AAbyssalHazardBase::StopDamageTick()
{
    GetWorldTimerManager().ClearTimer(DamageTimerHandle);
    OverlappingActors.Empty();
}

void AAbyssalHazardBase::TickDamage()
{
    if (!bHazardActive || CurrentPhase != EHazardPhase::Active)
    {
        return;
    }

    const float DeltaDamage = DamagePerSecond * DamageTickInterval;
    OnActiveDamageTick(DeltaDamage);

    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    if (DamageMode == EHazardDamageMode::Radial)
    {
        UGameplayStatics::ApplyRadialDamage(
            World,
            DeltaDamage,
            GetActorLocation(),
            DamageRadius,
            HazardDamageType,
            TArray<AActor*>{ this },
            this,
            GetInstigatorController(),
            false);
    }
    else if (DamageMode == EHazardDamageMode::Overlap)
    {
        for (AActor* Target : OverlappingActors)
        {
            if (IsValid(Target))
            {
                UGameplayStatics::ApplyDamage(
                    Target,
                    DeltaDamage,
                    GetInstigatorController(),
                    this,
                    HazardDamageType);
            }
        }
    }
}

void AAbyssalHazardBase::ClearTimers()
{
    GetWorldTimerManager().ClearTimer(PhaseTimerHandle);
    GetWorldTimerManager().ClearTimer(DamageTimerHandle);
}

float AAbyssalHazardBase::GetPhaseDuration(EHazardPhase Phase) const
{
    switch (Phase)
    {
    case EHazardPhase::Idle:     return IdleDuration;
    case EHazardPhase::Warning:  return WarningDuration;
    case EHazardPhase::Active:   return ActiveDuration;
    case EHazardPhase::Cooldown: return CooldownDuration;
    default:                     return IdleDuration;
    }
}

EHazardPhase AAbyssalHazardBase::GetNextPhase(EHazardPhase Phase) const
{
    switch (Phase)
    {
    case EHazardPhase::Idle:     return EHazardPhase::Warning;
    case EHazardPhase::Warning:  return EHazardPhase::Active;
    case EHazardPhase::Active:   return EHazardPhase::Cooldown;
    case EHazardPhase::Cooldown: return EHazardPhase::Idle;
    default:                     return EHazardPhase::Idle;
    }
}

void AAbyssalHazardBase::BroadcastPhaseEvent(EHazardPhase Phase)
{
    OnHazardPhaseChanged.Broadcast(Phase);

    switch (Phase)
    {
    case EHazardPhase::Idle:     OnHazardIdle();     break;
    case EHazardPhase::Warning:  OnHazardWarning();  break;
    case EHazardPhase::Active:   OnHazardActive();   break;
    case EHazardPhase::Cooldown: OnHazardCooldown(); break;
    default: break;
    }
}

// -----------------------------------------------------------------------------
// Overlap tracking (Overlap damage mode)
// -----------------------------------------------------------------------------

void AAbyssalHazardBase::HandleOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
    UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    if (OtherActor && OtherActor != this)
    {
        OverlappingActors.Add(OtherActor);
    }
}

void AAbyssalHazardBase::HandleOverlapEnd(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
    UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
    if (OtherActor)
    {
        OverlappingActors.Remove(OtherActor);
    }
}
