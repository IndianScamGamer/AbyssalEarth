#include "AbyssalHealthComponent.h"
#include "GameFramework/Actor.h"

UAbyssalHealthComponent::UAbyssalHealthComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UAbyssalHealthComponent::BeginPlay()
{
    Super::BeginPlay();
    CurrentHealth = MaxHealth;

    if (AActor* Owner = GetOwner())
    {
        Owner->OnTakeAnyDamage.AddDynamic(this, &UAbyssalHealthComponent::HandleTakeAnyDamage);
    }

    OnHealthChanged.Broadcast(this, CurrentHealth, 0.0f);
}

void UAbyssalHealthComponent::Heal(float Amount)
{
    if (bIsDead || Amount <= 0.0f)
    {
        return;
    }
    SetHealth(CurrentHealth + Amount);
}

void UAbyssalHealthComponent::ApplyDirectDamage(float Amount)
{
    if (bIsDead || Amount <= 0.0f)
    {
        return;
    }
    const float Effective = FMath::Max(0.0f, Amount - ArmorRating);
    if (Effective <= 0.0f)
    {
        return;
    }
    OnDamaged.Broadcast(this, Effective);
    SetHealth(CurrentHealth - Effective);
}

void UAbyssalHealthComponent::Respawn()
{
    bIsDead = false;
    SetHealth(MaxHealth);
}

void UAbyssalHealthComponent::Kill()
{
    if (bIsDead)
    {
        return;
    }
    SetHealth(0.0f);
}

float UAbyssalHealthComponent::GetHealthPercent() const
{
    return MaxHealth > 0.0f ? FMath::Clamp(CurrentHealth / MaxHealth, 0.0f, 1.0f) : 0.0f;
}

void UAbyssalHealthComponent::HandleTakeAnyDamage(AActor* /*DamagedActor*/, float Damage,
    const UDamageType* /*DamageType*/, AController* /*InstigatedBy*/, AActor* /*DamageCauser*/)
{
    if (bIsDead || Damage <= 0.0f)
    {
        return;
    }
    const float Effective = FMath::Max(0.0f, Damage - ArmorRating);
    if (Effective <= 0.0f)
    {
        return;
    }
    OnDamaged.Broadcast(this, Effective);
    SetHealth(CurrentHealth - Effective);
}

void UAbyssalHealthComponent::SetHealth(float NewHealth)
{
    const float Old = CurrentHealth;
    CurrentHealth = FMath::Clamp(NewHealth, 0.0f, MaxHealth);
    const float Delta = CurrentHealth - Old;

    if (!FMath::IsNearlyZero(Delta))
    {
        OnHealthChanged.Broadcast(this, CurrentHealth, Delta);
    }

    if (CurrentHealth <= 0.0f && !bIsDead)
    {
        bIsDead = true;
        OnDeath.Broadcast(this);
    }
}
