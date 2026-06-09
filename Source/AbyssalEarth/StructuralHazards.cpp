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
    WarningDuration = 0.5f;
    ActiveDuration = 1.0f;
    CooldownDuration = 0.0f;
    bAutoActivate = false; // Activated by integrity reaching zero, not a timer

    WeightTrigger = CreateDefaultSubobject<UBoxComponent>(TEXT("WeightTrigger"));
    WeightTrigger->SetupAttachment(RootComponent);
    WeightTrigger->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    WeightTrigger->SetCollisionResponseToAllChannels(ECR_Ignore);
    WeightTrigger->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
    WeightTrigger->OnComponentBeginOverlap.AddDynamic(this, &ABrittleWalkwaySection::OnPawnLanded);
}

void ABrittleWalkwaySection::BeginPlay()
{
    Super::BeginPlay();
    CurrentIntegrity = MaxIntegrity;
}

void ABrittleWalkwaySection::OnPawnLanded(UPrimitiveComponent* /*OverlappedComp*/, AActor* OtherActor,
    UPrimitiveComponent* /*OtherComp*/, int32 /*OtherBodyIndex*/, bool /*bFromSweep*/, const FHitResult& /*SweepResult*/)
{
    if (!OtherActor || !Cast<ACharacter>(OtherActor))
    {
        return;
    }
    if (CurrentState == EHazardPhase::Active || CurrentState == EHazardPhase::Cooldown)
    {
        return;
    }

    CurrentIntegrity = FMath::Max(0, CurrentIntegrity - 1);
    BP_OnIntegrityChanged(CurrentIntegrity);

    if (CurrentIntegrity <= 0)
    {
        ActivateHazard();
    }
}

void ABrittleWalkwaySection::OnActivePhaseBegin_Implementation()
{
    Super::OnActivePhaseBegin_Implementation();
    // Disable the walkway mesh collision so the player falls through
    if (UPrimitiveComponent* Root = Cast<UPrimitiveComponent>(GetRootComponent()))
    {
        Root->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    }
    WeightTrigger->SetCollisionEnabled(ECollisionEnabled::NoCollision);
}

void ABrittleWalkwaySection::OnIdlePhaseBegin_Implementation()
{
    Super::OnIdlePhaseBegin_Implementation();
    // Respawn: restore integrity and collision
    CurrentIntegrity = MaxIntegrity;
    BP_OnIntegrityChanged(CurrentIntegrity);
    if (UPrimitiveComponent* Root = Cast<UPrimitiveComponent>(GetRootComponent()))
    {
        Root->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
    }
    WeightTrigger->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
}

// ---------------------------------------------------------------------------
// ACeilingFragmentHazard
// ---------------------------------------------------------------------------

ACeilingFragmentHazard::ACeilingFragmentHazard()
{
    DamageMode = EHazardDamageMode::None; // We apply radial damage manually on landing
    WarningDuration = 0.4f; // Brief shake before drop
    ActiveDuration = 2.0f; // Fall + settle
    CooldownDuration = 0.0f;
    bAutoActivate = false;

    ProximityTrigger = CreateDefaultSubobject<USphereComponent>(TEXT("ProximityTrigger"));
    ProximityTrigger->SetupAttachment(RootComponent);
    ProximityTrigger->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    ProximityTrigger->SetCollisionResponseToAllChannels(ECR_Ignore);
    ProximityTrigger->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
    ProximityTrigger->OnComponentBeginOverlap.AddDynamic(this, &ACeilingFragmentHazard::OnProximityOverlap);
}

void ACeilingFragmentHazard::BeginPlay()
{
    Super::BeginPlay();
    ProximityTrigger->SetSphereRadius(ProximityRadius);
    FallOrigin = GetActorLocation();
}

void ACeilingFragmentHazard::OnProximityOverlap(UPrimitiveComponent* /*OverlappedComp*/, AActor* OtherActor,
    UPrimitiveComponent* /*OtherComp*/, int32 /*OtherBodyIndex*/, bool /*bFromSweep*/, const FHitResult& /*SweepResult*/)
{
    if (!OtherActor || !Cast<ACharacter>(OtherActor))
    {
        return;
    }
    if (CurrentState != EHazardPhase::Idle)
    {
        return;
    }
    // Disable trigger so it only fires once per cycle
    ProximityTrigger->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    ActivateHazard();
}

void ACeilingFragmentHazard::OnWarningPhaseBegin_Implementation()
{
    Super::OnWarningPhaseBegin_Implementation();
    // BP handles camera shake / rumble
}

void ACeilingFragmentHazard::OnActivePhaseBegin_Implementation()
{
    Super::OnActivePhaseBegin_Implementation();

    // Enable physics so the fragment mesh falls naturally
    if (UPrimitiveComponent* Root = Cast<UPrimitiveComponent>(GetRootComponent()))
    {
        Root->SetSimulatePhysics(true);
    }

    // Impact damage is applied by an OnHit binding set up in the Blueprint subclass,
    // or via a sweep at ActiveDuration end. Exposed as ImpactDamage/ImpactRadius for BP use.
    TArray<AActor*> IgnoredActors;
    IgnoredActors.Add(this);
    UGameplayStatics::ApplyRadialDamage(this, ImpactDamage, GetActorLocation(),
        ImpactRadius, nullptr, IgnoredActors, this, nullptr, true);
}
