#include "AbyssalHealthComponent.h"
#include "GameFramework/Actor.h"
#include "GameFramework/DamageType.h"

UAbyssalHealthComponent::UAbyssalHealthComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UAbyssalHealthComponent::BeginPlay()
{
    Super::BeginPlay();

    MaxHealth = FMath::Max(MaxHealth, 1.0f);
    CurrentHealth = bStartAtMaxHealth ? MaxHealth : FMath::Clamp(CurrentHealth, 0.0f, MaxHealth);
    bDead = CurrentHealth <= 0.0f;

    if (AActor* Owner = GetOwner())
    {
        Owner->OnTakeAnyDamage.AddDynamic(this, &UAbyssalHealthComponent::HandleOwnerTakeAnyDamage);
    }

    OnHealthChanged.Broadcast(CurrentHealth, MaxHealth, 0.0f);
}

void UAbyssalHealthComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (AActor* Owner = GetOwner())
    {
        Owner->OnTakeAnyDamage.RemoveDynamic(this, &UAbyssalHealthComponent::HandleOwnerTakeAnyDamage);
    }

    Super::EndPlay(EndPlayReason);
}

float UAbyssalHealthComponent::ApplyHealthDamage(float DamageAmount, AActor* DamageCauser)
{
    if (DamageAmount <= 0.0f || (bDead && !bCanTakeDamageWhenDead))
    {
        return CurrentHealth;
    }

    const float PreviousHealth = CurrentHealth;
    SetCurrentHealth(CurrentHealth - DamageAmount, DamageCauser);

    const float AppliedDamage = PreviousHealth - CurrentHealth;
    if (AppliedDamage > 0.0f)
    {
        OnDamaged.Broadcast(AppliedDamage, DamageCauser, CurrentHealth);
    }

    return CurrentHealth;
}

float UAbyssalHealthComponent::Heal(float HealAmount)
{
    if (HealAmount <= 0.0f || bDead)
    {
        return CurrentHealth;
    }

    SetCurrentHealth(CurrentHealth + HealAmount);
    return CurrentHealth;
}

void UAbyssalHealthComponent::RestoreFullHealth()
{
    bDead = false;
    SetCurrentHealth(MaxHealth);
}

void UAbyssalHealthComponent::Kill(AActor* DamageCauser)
{
    SetCurrentHealth(0.0f, DamageCauser);
}

float UAbyssalHealthComponent::GetCurrentHealth() const
{
    return CurrentHealth;
}

float UAbyssalHealthComponent::GetMaxHealth() const
{
    return MaxHealth;
}

float UAbyssalHealthComponent::GetHealthPercent() const
{
    return MaxHealth > KINDA_SMALL_NUMBER ? CurrentHealth / MaxHealth : 0.0f;
}

bool UAbyssalHealthComponent::IsDead() const
{
    return bDead;
}

void UAbyssalHealthComponent::HandleOwnerTakeAnyDamage(AActor* DamagedActor, float Damage, const UDamageType* DamageType, AController* InstigatedBy, AActor* DamageCauser)
{
    if (Damage <= 0.0f)
    {
        return;
    }

    UE_LOG(LogTemp, Verbose, TEXT("[AbyssalEarth] %s took %.2f damage from %s (type %s)"),
        DamagedActor ? *DamagedActor->GetName() : TEXT("<unknown>"),
        Damage,
        DamageCauser ? *DamageCauser->GetName() : TEXT("<unknown>"),
        DamageType ? *DamageType->GetName() : TEXT("<none>"));

    ApplyHealthDamage(Damage, DamageCauser);
}

void UAbyssalHealthComponent::SetCurrentHealth(float NewHealth, AActor* DamageCauser)
{
    const float PreviousHealth = CurrentHealth;
    CurrentHealth = FMath::Clamp(NewHealth, 0.0f, MaxHealth);
    const float Delta = CurrentHealth - PreviousHealth;

    if (!FMath::IsNearlyZero(Delta))
    {
        OnHealthChanged.Broadcast(CurrentHealth, MaxHealth, Delta);
    }

    if (!bDead && CurrentHealth <= 0.0f)
    {
        bDead = true;
        OnDeath.Broadcast(GetOwner(), DamageCauser);
    }
}
