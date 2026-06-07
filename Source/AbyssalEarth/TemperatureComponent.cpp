#include "TemperatureComponent.h"
#include "GameFramework/Actor.h"
#include "GameFramework/DamageType.h"
#include "Kismet/GameplayStatics.h"

UTemperatureComponent::UTemperatureComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UTemperatureComponent::BeginPlay()
{
    Super::BeginPlay();
    OnTemperatureChanged.Broadcast(GetHeatPercent(), bInHeatZone);
}

void UTemperatureComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    const float InsulationFactor = 1.0f - FMath::Clamp(Insulation, 0.0f, 1.0f);
    if (bInHeatZone)
    {
        SetHeatExposure(HeatExposure + HeatGainRate * InsulationFactor * DeltaTime);
    }
    else if (HeatExposure > 0.0f)
    {
        SetHeatExposure(HeatExposure - CoolRate * DeltaTime);
    }

    if (bOverheating)
    {
        ApplyOverheatDamage(DeltaTime);
    }
}

void UTemperatureComponent::SetInHeatZone(bool bInZone)
{
    if (bInHeatZone != bInZone)
    {
        bInHeatZone = bInZone;
        OnTemperatureChanged.Broadcast(GetHeatPercent(), bInHeatZone);
    }
}

void UTemperatureComponent::AddHeatExposure(float Delta)
{
    const float InsulationFactor = 1.0f - FMath::Clamp(Insulation, 0.0f, 1.0f);
    // Insulation only reduces incoming heat, never cooling.
    const float Scaled = Delta > 0.0f ? Delta * InsulationFactor : Delta;
    SetHeatExposure(HeatExposure + Scaled);
}

void UTemperatureComponent::ResetTemperature()
{
    SetHeatExposure(0.0f);
}

void UTemperatureComponent::SetHeatExposure(float NewExposure)
{
    const float Clamped = FMath::Clamp(NewExposure, 0.0f, 1.0f);
    if (!FMath::IsNearlyEqual(Clamped, HeatExposure))
    {
        HeatExposure = Clamped;
        OnTemperatureChanged.Broadcast(GetHeatPercent(), bInHeatZone);
    }

    const bool bShouldOverheat = HeatExposure >= OverheatThreshold;
    if (bShouldOverheat != bOverheating)
    {
        bOverheating = bShouldOverheat;
        if (bOverheating)
        {
            OnOverheatBegan.Broadcast();
        }
        else
        {
            OnOverheatEnded.Broadcast();
        }
    }
}

void UTemperatureComponent::ApplyOverheatDamage(float DeltaTime)
{
    AActor* Owner = GetOwner();
    if (!Owner || OverheatDamagePerSecond <= 0.0f)
    {
        return;
    }

    // Engine damage path (matches AEmberVentHazard); routes into UAbyssalHealthComponent.
    UGameplayStatics::ApplyDamage(Owner, OverheatDamagePerSecond * DeltaTime, nullptr, Owner, UDamageType::StaticClass());
}

float UTemperatureComponent::GetHeatExposure() const
{
    return HeatExposure;
}

float UTemperatureComponent::GetHeatPercent() const
{
    return HeatExposure * 100.0f;
}

bool UTemperatureComponent::IsOverheating() const
{
    return bOverheating;
}

bool UTemperatureComponent::IsInHeatZone() const
{
    return bInHeatZone;
}
