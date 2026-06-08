#include "StaminaComponent.h"

UStaminaComponent::UStaminaComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UStaminaComponent::BeginPlay()
{
    Super::BeginPlay();
    OnStaminaChanged.Broadcast(GetStaminaPercent());
}

void UStaminaComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (bExerting && CanExert())
    {
        TimeSinceExertion = 0.0f;
        SetStamina(Stamina - DrainRate * DeltaTime);
    }
    else
    {
        TimeSinceExertion += DeltaTime;
        if (Stamina < 1.0f && TimeSinceExertion >= RegenDelay)
        {
            SetStamina(Stamina + RegenRate * DeltaTime);
        }
    }
}

void UStaminaComponent::SetExerting(bool bInExerting)
{
    bExerting = bInExerting;
    if (bExerting)
    {
        TimeSinceExertion = 0.0f;
    }
}

bool UStaminaComponent::TryConsumeStamina(float Cost)
{
    if (Cost <= 0.0f)
    {
        return true;
    }

    if (bExhausted || Stamina < Cost)
    {
        return false;
    }

    TimeSinceExertion = 0.0f;
    SetStamina(Stamina - Cost);
    return true;
}

void UStaminaComponent::RestoreStamina()
{
    SetStamina(1.0f);
}

bool UStaminaComponent::CanExert() const
{
    return !bExhausted && Stamina > 0.0f;
}

void UStaminaComponent::SetStamina(float NewStamina)
{
    const float Clamped = FMath::Clamp(NewStamina, 0.0f, 1.0f);
    if (!FMath::IsNearlyEqual(Clamped, Stamina))
    {
        Stamina = Clamped;
        OnStaminaChanged.Broadcast(GetStaminaPercent());
    }

    if (!bExhausted && Stamina <= 0.0f)
    {
        bExhausted = true;
        bExerting = false;
        OnExhausted.Broadcast();
    }
    else if (bExhausted && Stamina >= ExhaustionRecoveryThreshold)
    {
        bExhausted = false;
        OnRecovered.Broadcast();
    }
}
