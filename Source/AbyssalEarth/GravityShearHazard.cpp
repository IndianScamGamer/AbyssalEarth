#include "GravityShearHazard.h"
#include "Components/BoxComponent.h"
#include "AbyssalTraversalComponent.h"

AGravityShearHazard::AGravityShearHazard()
{
    DamageMode = EHazardDamageMode::None;
    IdleDuration = 3.0f;
    WarningDuration = 1.0f;
    ActiveDuration = 5.0f;
    CooldownDuration = 0.0f;
    bStartActive = true;

    SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
    SetRootComponent(SceneRoot);

    ShearVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("ShearVolume"));
    ShearVolume->SetupAttachment(RootComponent);
    ShearVolume->SetBoxExtent(FVector(200.0f, 200.0f, 200.0f));
    ShearVolume->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    ShearVolume->SetCollisionResponseToAllChannels(ECR_Overlap);
    ShearVolume->OnComponentBeginOverlap.AddDynamic(this, &AGravityShearHazard::OnShearOverlapBegin);
}

void AGravityShearHazard::OnPhaseChanged(EHazardPhase NewPhase)
{
    Super::OnPhaseChanged(NewPhase);
    ShearVolume->SetCollisionEnabled(
        NewPhase == EHazardPhase::Active ? ECollisionEnabled::QueryOnly : ECollisionEnabled::NoCollision);
}

void AGravityShearHazard::OnShearOverlapBegin(UPrimitiveComponent* /*OverlappedComp*/, AActor* OtherActor,
    UPrimitiveComponent* /*OtherComp*/, int32 /*OtherBodyIndex*/, bool /*bFromSweep*/, const FHitResult& /*SweepResult*/)
{
    if (!OtherActor)
    {
        return;
    }

    if (UAbyssalTraversalComponent* Traversal = OtherActor->FindComponentByClass<UAbyssalTraversalComponent>())
    {
        Traversal->RequestGravityReorientation(GravityDirection, ReorientDuration);
    }
}
