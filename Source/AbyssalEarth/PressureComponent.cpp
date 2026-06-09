#include "PressureComponent.h"
#include "GameFramework/Actor.h"
#include "GameFramework/DamageType.h"
#include "Kismet/GameplayStatics.h"

UPressureComponent::UPressureComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UPressureComponent::BeginPlay()
{
    Super::BeginPlay();
    OnPressureChanged.Broadcast(GetPressurePercent(), bAboveRating);
}

void UPressureComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    if (bAboveRating)
    {
        ApplyOverpressureDamage(DeltaTime);
    }
}

void UPressureComponent::SetCurrentDepth(float DepthMetres)
{
    const float Clamped = FMath::Max(0.0f, DepthMetres);
    if (FMath::IsNearlyEqual(Clamped, CurrentDepth))
    {
        return;
    }
    CurrentDepth = Clamped;
    UpdatePressureState();
}

void UPressureComponent::AddPressureRating(float Delta)
{
    PressureRating = FMath::Max(0.0f, PressureRating + Delta);
    UpdatePressureState();
}

void UPressureComponent::ResetPressure()
{
    CurrentDepth = 0.0f;
    bAboveRating = false;
    OnPressureChanged.Broadcast(0.0f, false);
}

float UPressureComponent::GetCurrentPressureAtm() const
{
    // Standard seawater: 1 atm per 10 m depth
    return 1.0f + CurrentDepth / 10.0f;
}

float UPressureComponent::GetPressurePercent() const
{
    if (CurrentDepth <= PressureSafeDepth)
    {
        return 0.0f;
    }
    // Express danger as % of one extra rating-unit past safe depth
    const float DangerRange = FMath::Max(1.0f, PressureRating - GetCurrentPressureAtm() + 1.0f);
    return FMath::Clamp((GetCurrentPressureAtm() - (1.0f + PressureSafeDepth / 10.0f)) / DangerRange * 100.0f, 0.0f, 100.0f);
}

void UPressureComponent::UpdatePressureState()
{
    const float CurrentAtm = GetCurrentPressureAtm();
    const bool bShouldBeAbove = (CurrentDepth > PressureSafeDepth) && (CurrentAtm > PressureRating);

    if (bShouldBeAbove != bAboveRating)
    {
        bAboveRating = bShouldBeAbove;
        if (bAboveRating)
        {
            OnPressureCritical.Broadcast();
        }
    }

    OnPressureChanged.Broadcast(GetPressurePercent(), bAboveRating);
}

void UPressureComponent::ApplyOverpressureDamage(float DeltaTime)
{
    AActor* Owner = GetOwner();
    if (!Owner || OverpressureDamagePerSecond <= 0.0f)
    {
        return;
    }

    // Scale damage by how far over the rating the current pressure is
    const float Overpressure = FMath::Max(0.0f, GetCurrentPressureAtm() - PressureRating);
    const float ScaledDamage = OverpressureDamagePerSecond * (1.0f + Overpressure / 10.0f) * DeltaTime;
    UGameplayStatics::ApplyDamage(Owner, ScaledDamage, nullptr, Owner, UDamageType::StaticClass());
}
