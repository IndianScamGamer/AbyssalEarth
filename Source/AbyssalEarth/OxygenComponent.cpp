#include "OxygenComponent.h"
#include "GameFramework/Actor.h"
#include "GameFramework/DamageType.h"
#include "Kismet/GameplayStatics.h"

UOxygenComponent::UOxygenComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UOxygenComponent::BeginPlay()
{
    Super::BeginPlay();
    OnOxygenChanged.Broadcast(GetOxygenPercent(), bSubmerged);
}

void UOxygenComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (bSubmerged)
    {
        // AirCapacityBonus extends air: bonus 1.0 halves the effective drain.
        const float CapacityFactor = 1.0f / (1.0f + FMath::Clamp(AirCapacityBonus, 0.0f, 1.0f));
        SetOxygen(Oxygen - OxygenDrainRate * CapacityFactor * DeltaTime);
    }
    else if (Oxygen < 1.0f)
    {
        SetOxygen(Oxygen + OxygenRefillRate * DeltaTime);
    }

    if (bSuffocating)
    {
        ApplySuffocationDamage(DeltaTime);
    }
}

void UOxygenComponent::SetSubmerged(bool bInSubmerged)
{
    if (bSubmerged != bInSubmerged)
    {
        bSubmerged = bInSubmerged;
        OnOxygenChanged.Broadcast(GetOxygenPercent(), bSubmerged);
    }
}

void UOxygenComponent::RefillOxygen()
{
    SetOxygen(1.0f);
}

void UOxygenComponent::SetOxygen(float NewOxygen)
{
    const float Clamped = FMath::Clamp(NewOxygen, 0.0f, 1.0f);
    if (!FMath::IsNearlyEqual(Clamped, Oxygen))
    {
        Oxygen = Clamped;
        OnOxygenChanged.Broadcast(GetOxygenPercent(), bSubmerged);
    }

    const bool bShouldSuffocate = Oxygen <= 0.0f;
    if (bShouldSuffocate != bSuffocating)
    {
        bSuffocating = bShouldSuffocate;
        if (bSuffocating)
        {
            OnSuffocationBegan.Broadcast();
        }
        else
        {
            OnSuffocationEnded.Broadcast();
        }
    }
}

void UOxygenComponent::ApplySuffocationDamage(float DeltaTime)
{
    AActor* Owner = GetOwner();
    if (!Owner || SuffocationDamagePerSecond <= 0.0f)
    {
        return;
    }

    // Engine damage path (matches AEmberVentHazard); routes into UAbyssalHealthComponent.
    UGameplayStatics::ApplyDamage(Owner, SuffocationDamagePerSecond * DeltaTime, nullptr, Owner, UDamageType::StaticClass());
}
