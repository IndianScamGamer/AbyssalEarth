#include "GravityShearHazard.h"
#include "Components/BoxComponent.h"
#include "AbyssalTraversalComponent.h"

AGravityShearHazard::AGravityShearHazard()
{
    DamageMode = EHazardDamageMode::None;
    WarningDuration = 1.0f;
    ActiveDuration = 5.0f;
    CooldownDuration = 3.0f;
    bAutoActivate = true;

    ShearVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("ShearVolume"));
    ShearVolume->SetupAttachment(RootComponent);
    ShearVolume->SetBoxExtent(FVector(200.0f, 200.0f, 200.0f));
    ShearVolume->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    ShearVolume->SetCollisionResponseToAllChannels(ECR_Overlap);
    ShearVolume->OnComponentBeginOverlap.AddDynamic(this, &AGravityShearHazard::OnShearOverlapBegin);
}

void AGravityShearHazard::BeginPlay()
{
    Super::BeginPlay();
}

void AGravityShearHazard::OnActivePhaseBegin_Implementation()
{
    Super::OnActivePhaseBegin_Implementation();
    ShearVolume->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
}

void AGravityShearHazard::OnCooldownPhaseBegin_Implementation()
{
    Super::OnCooldownPhaseBegin_Implementation();
    ShearVolume->SetCollisionEnabled(ECollisionEnabled::NoCollision);
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
