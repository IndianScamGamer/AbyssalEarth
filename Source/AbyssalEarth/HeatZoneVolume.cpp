#include "HeatZoneVolume.h"
#include "TemperatureComponent.h"
#include "Components/BoxComponent.h"

AHeatZoneVolume::AHeatZoneVolume()
{
    PrimaryActorTick.bCanEverTick = false;

    HeatVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("HeatVolume"));
    SetRootComponent(HeatVolume);
    HeatVolume->SetBoxExtent(FVector(400.0f, 400.0f, 200.0f));
    HeatVolume->SetCollisionProfileName(TEXT("Trigger"));
}

void AHeatZoneVolume::BeginPlay()
{
    Super::BeginPlay();

    if (HeatVolume)
    {
        HeatVolume->OnComponentBeginOverlap.AddDynamic(this, &AHeatZoneVolume::HandleBeginOverlap);
        HeatVolume->OnComponentEndOverlap.AddDynamic(this, &AHeatZoneVolume::HandleEndOverlap);
    }
}

void AHeatZoneVolume::HandleBeginOverlap(
    UPrimitiveComponent* OverlappedComponent,
    AActor* OtherActor,
    UPrimitiveComponent* OtherComp,
    int32 OtherBodyIndex,
    bool bFromSweep,
    const FHitResult& SweepResult)
{
    if (!OtherActor)
    {
        return;
    }

    if (UTemperatureComponent* Temperature = OtherActor->FindComponentByClass<UTemperatureComponent>())
    {
        Temperature->SetInHeatZone(true);
    }
}

void AHeatZoneVolume::HandleEndOverlap(
    UPrimitiveComponent* OverlappedComponent,
    AActor* OtherActor,
    UPrimitiveComponent* OtherComp,
    int32 OtherBodyIndex)
{
    if (!OtherActor)
    {
        return;
    }

    if (UTemperatureComponent* Temperature = OtherActor->FindComponentByClass<UTemperatureComponent>())
    {
        Temperature->SetInHeatZone(false);
    }
}
