#include "StructuralHazards.h"
#include "Components/BoxComponent.h"
#include "Components/SphereComponent.h"
#include "GameFramework/Character.h"
#include "Kismet/GameplayStatics.h"

// ---------------------------------------------------------------------------
// ABrittleWalkwaySection
// ---------------------------------------------------------------------------

ABrittleWalkwaySection::ABrittleWalkwaySection()
{
    DamageMode = EHazardDamageMode::None;
    IdleDuration = 0.0f;     // Activation jumps straight to Warning
    WarningDuration = 0.5f;  // Creak before the drop
    ActiveDuration = 1.0f;   // Collapse window
    // CooldownDuration is set from RespawnDelay in BeginPlay
    bStartActive = false;    // Activated by integrity reaching zero, not on spawn

    SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
    SetRootComponent(SceneRoot);

    WeightTrigger = CreateDefaultSubobject<UBoxComponent>(TEXT("WeightTrigger"));
    WeightTrigger->SetupAttachment(RootComponent);
    WeightTrigger->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    WeightTrigger->SetCollisionResponseToAllChannels(ECR_Ignore);
    WeightTrigger->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
    WeightTrigger->OnComponentBeginOverlap.AddDynamic(this, &ABrittleWalkwaySection::OnPawnStepped);
}

void ABrittleWalkwaySection::BeginPlay()
{
    CurrentIntegrity = MaxIntegrity;
    CooldownDuration = RespawnDelay;
    Super::BeginPlay();
}

void ABrittleWalkwaySection::OnPawnStepped(UPrimitiveComponent* /*OverlappedComp*/, AActor* OtherActor,
    UPrimitiveComponent* /*OtherComp*/, int32 /*OtherBodyIndex*/, bool /*bFromSweep*/, const FHitResult& /*SweepResult*/)
{
    if (!OtherActor || !Cast<ACharacter>(OtherActor) || IsHazardActive())
    {
        return;
    }

    CurrentIntegrity = FMath::Max(0, CurrentIntegrity - 1);
    BP_OnIntegrityChanged(CurrentIntegrity);

    if (CurrentIntegrity <= 0)
    {
        SetHazardActive(true); // Idle(0s) -> Warning -> Active (collapse)
    }
}

void ABrittleWalkwaySection::OnPhaseChanged(EHazardPhase NewPhase)
{
    Super::OnPhaseChanged(NewPhase);

    switch (NewPhase)
    {
        case EHazardPhase::Active:
            // The floor gives way
            bCollapsedOnce = true;
            SetWalkwaySolid(false);
            break;

        case EHazardPhase::Cooldown:
            if (RespawnDelay <= 0.0f)
            {
                // One-shot: stay collapsed forever
                SetHazardActive(false);
            }
            break;

        case EHazardPhase::Idle:
            if (bCollapsedOnce && RespawnDelay > 0.0f)
            {
                // Cycle wrapped after cooldown: restore the walkway
                CurrentIntegrity = MaxIntegrity;
                BP_OnIntegrityChanged(CurrentIntegrity);
                SetWalkwaySolid(true);
                SetHazardActive(false); // Wait for the next integrity depletion
            }
            break;

        default:
            break;
    }
}

void ABrittleWalkwaySection::SetWalkwaySolid(bool bSolid)
{
    if (UPrimitiveComponent* Root = Cast<UPrimitiveComponent>(GetRootComponent()))
    {
        Root->SetCollisionEnabled(bSolid ? ECollisionEnabled::QueryAndPhysics : ECollisionEnabled::NoCollision);
    }
    WeightTrigger->SetCollisionEnabled(bSolid ? ECollisionEnabled::QueryOnly : ECollisionEnabled::NoCollision);
}

// ---------------------------------------------------------------------------
// ACeilingFragmentHazard
// ---------------------------------------------------------------------------

ACeilingFragmentHazard::ACeilingFragmentHazard()
{
    DamageMode = EHazardDamageMode::None; // Impact damage applied manually on drop
    IdleDuration = 0.0f;
    WarningDuration = 0.4f; // Brief shake before the drop
    ActiveDuration = 2.0f;  // Fall + settle
    CooldownDuration = 0.0f;
    bStartActive = false;

    SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
    SetRootComponent(SceneRoot);

    ProximityTrigger = CreateDefaultSubobject<USphereComponent>(TEXT("ProximityTrigger"));
    ProximityTrigger->SetupAttachment(RootComponent);
    ProximityTrigger->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    ProximityTrigger->SetCollisionResponseToAllChannels(ECR_Ignore);
    ProximityTrigger->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
    ProximityTrigger->OnComponentBeginOverlap.AddDynamic(this, &ACeilingFragmentHazard::OnProximityOverlap);
}

void ACeilingFragmentHazard::BeginPlay()
{
    ProximityTrigger->SetSphereRadius(ProximityRadius);
    Super::BeginPlay();
}

void ACeilingFragmentHazard::OnProximityOverlap(UPrimitiveComponent* /*OverlappedComp*/, AActor* OtherActor,
    UPrimitiveComponent* /*OtherComp*/, int32 /*OtherBodyIndex*/, bool /*bFromSweep*/, const FHitResult& /*SweepResult*/)
{
    if (bTriggered || !OtherActor || !Cast<ACharacter>(OtherActor))
    {
        return;
    }
    bTriggered = true;
    ProximityTrigger->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    SetHazardActive(true); // Idle(0s) -> Warning (shake) -> Active (drop)
}

void ACeilingFragmentHazard::OnPhaseChanged(EHazardPhase NewPhase)
{
    Super::OnPhaseChanged(NewPhase);

    switch (NewPhase)
    {
        case EHazardPhase::Active:
        {
            // Let the fragment mesh fall under physics
            if (UPrimitiveComponent* Root = Cast<UPrimitiveComponent>(GetRootComponent()))
            {
                Root->SetSimulatePhysics(true);
            }

            TArray<AActor*> IgnoredActors;
            IgnoredActors.Add(this);
            UGameplayStatics::ApplyRadialDamage(this, ImpactDamage, GetActorLocation(),
                ImpactRadius, HazardDamageType, IgnoredActors, this, nullptr, true);
            break;
        }

        case EHazardPhase::Cooldown:
            // One-shot: fall happened, deactivate permanently
            SetHazardActive(false);
            break;

        default:
            break;
    }
}
