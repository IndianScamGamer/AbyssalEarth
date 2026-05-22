#include "BeaconActor.h"
#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"

ABeaconActor::ABeaconActor()
{
    PrimaryActorTick.bCanEverTick = false;

    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    SetRootComponent(Mesh);

    Light = CreateDefaultSubobject<UPointLightComponent>(TEXT("Light"));
    Light->SetupAttachment(Mesh);
    Light->SetIntensity(3500.0f);
    Light->SetAttenuationRadius(650.0f);
    ApplyBeaconVisuals();
}

void ABeaconActor::BeginPlay()
{
    Super::BeginPlay();

    if (!BeaconId.IsValid())
    {
        BeaconId = FGuid::NewGuid();
    }

    ApplyBeaconVisuals();
}

void ABeaconActor::InitializeBeacon(FGuid InBeaconId, FLinearColor InLightColor)
{
    BeaconId = InBeaconId.IsValid() ? InBeaconId : FGuid::NewGuid();
    BeaconLightColor = InLightColor;
    ApplyBeaconVisuals();
}

FGuid ABeaconActor::GetBeaconId() const
{
    return BeaconId;
}

FLinearColor ABeaconActor::GetBeaconLightColor() const
{
    return BeaconLightColor;
}

void ABeaconActor::ApplyBeaconVisuals()
{
    if (Light)
    {
        Light->SetLightColor(BeaconLightColor);
    }
}
