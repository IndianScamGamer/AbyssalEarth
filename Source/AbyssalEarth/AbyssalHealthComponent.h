#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "AbyssalHealthComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FAbyssalHealthChangedSignature,
    class UAbyssalHealthComponent*, HealthComp, float, NewHealth, float, Delta);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalDamagedSignature,
    class UAbyssalHealthComponent*, HealthComp, float, DamageApplied);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalDeathSignature,
    class UAbyssalHealthComponent*, HealthComp);

/**
 * Centralised health and death component (roadmap I1). All survival vitals
 * (UOxygenComponent, UTemperatureComponent, UPressureComponent, StaminaComponent)
 * route damage through UGameplayStatics::ApplyDamage, which triggers
 * AActor::OnTakeAnyDamage. This component binds that delegate and applies
 * damage after ArmorRating reduction. MaxHealth and ArmorRating are raised
 * by suit upgrades. Death state is final until explicitly reset (respawn).
 *
 * Attach to AAbyssalPlayerCharacter (and any damageable creature).
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UAbyssalHealthComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UAbyssalHealthComponent();

    virtual void BeginPlay() override;

    /** Heal the owner. Clamped to MaxHealth. Does nothing if dead. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Health")
    void Heal(float Amount);

    /** Apply direct damage (bypasses AActor damage system — use for non-engine sources). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Health")
    void ApplyDirectDamage(float Amount);

    /** Restore to full health and clear dead state. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Health")
    void Respawn();

    /** Instantly kill the owner. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Health")
    void Kill();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Health")
    float GetCurrentHealth() const { return CurrentHealth; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Health")
    float GetMaxHealth() const { return MaxHealth; }

    /** Current health as a 0..1 fraction. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Health")
    float GetHealthPercent() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Health")
    bool IsDead() const { return bIsDead; }

    // Delegates
    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Health")
    FAbyssalHealthChangedSignature OnHealthChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Health")
    FAbyssalDamagedSignature OnDamaged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Health")
    FAbyssalDeathSignature OnDeath;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Health", meta=(ClampMin="1.0"))
    float MaxHealth = 100.0f;

    /**
     * Flat damage reduction per hit (not percentage). Raised by suit upgrades.
     * Applied before the damage is deducted: effective_damage = max(0, raw - Armor).
     */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Health", meta=(ClampMin="0.0"))
    float ArmorRating = 0.0f;

protected:
    UFUNCTION()
    void HandleTakeAnyDamage(AActor* DamagedActor, float Damage, const UDamageType* DamageType,
        AController* InstigatedBy, AActor* DamageCauser);

private:
    void SetHealth(float NewHealth);

    UPROPERTY()
    float CurrentHealth = 0.0f;

    UPROPERTY()
    bool bIsDead = false;
};
