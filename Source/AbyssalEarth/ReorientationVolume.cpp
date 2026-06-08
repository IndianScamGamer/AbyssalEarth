#include "ReorientationVolume.h"
#include "AbyssalTraversalComponent.h"
#include "Components/BoxComponent.h"

AReorientationVolume::AReorientationVolume()
{
    PrimaryActorTick.bCanEverTick = false;

    TriggerBox = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerBox"));
    RootComponent = TriggerBox;
    TriggerBox->SetBoxExtent(FVector(200.0f, 200.0f, 200.0f));
    TriggerBox->SetCollisionProfileName(TEXT("Trigger"));
}

void AReorientationVolume::BeginPlay()
{
    Super::BeginPlay();
    TriggerBox->OnComponentBeginOverlap.AddDynamic(this, &AReorientationVolume::HandleOverlapBegin);
}

void AReorientationVolume::HandleOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp,
    int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    if (!OtherActor || OtherActor == this)
    {
        return;
    }

    UAbyssalTraversalComponent* Traversal = OtherActor->FindComponentByClass<UAbyssalTraversalComponent>();
    if (!Traversal)
    {
        return;
    }

    Traversal->RequestGravityReorientation(GravityDirection, ReorientDuration);
    BP_OnReoriented(OtherActor);
}
