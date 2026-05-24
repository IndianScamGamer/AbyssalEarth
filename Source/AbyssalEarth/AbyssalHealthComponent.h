#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "AbyssalHealthComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FAbyssalHealthChangedSignature, float, CurrentHealth, float, MaxHealth, float, Delta);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FAbyssalDamagedSignature, float, DamageAmount, AActor*, DamageCauser, float, CurrentHealth);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalDeathSignature, AActor*, KilledActor, AActor*, DamageCauser);

UCLASS(ClassGroup = (AbyssalEarth), BlueprintType, Blueprintable, meta = (BlueprintSpawnableComponent))
class ABYSSALEARTH_API UAbyssalHealthComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UAbyssalHealthComponent();

    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Health")
    float ApplyHealthDamage(float DamageAmount, AActor* DamageCauser = nullptr);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Health")
    float Heal(float HealAmount);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Health")
    void RestoreFullHealth();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Health")
    void Kill(AActor* DamageCauser = nullptr);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Health")
    float GetCurrentHealth() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Health")
    float GetMaxHealth() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Health")
    float GetHealthPercent() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Health")
    bool IsDead() const;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Health", meta = (ClampMin = "1.0"))
    float MaxHealth = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Health")
    bool bStartAtMaxHealth = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Health")
    bool bCanTakeDamageWhenDead = false;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Health")
    FAbyssalHealthChangedSignature OnHealthChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Health")
    FAbyssalDamagedSignature OnDamaged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Health")
    FAbyssalDeathSignature OnDeath;

private:
    UPROPERTY(VisibleInstanceOnly, Category = "Abyssal Earth|Health")
    float CurrentHealth = 100.0f;

    UPROPERTY(VisibleInstanceOnly, Category = "Abyssal Earth|Health")
    bool bDead = false;

    UFUNCTION()
    void HandleOwnerTakeAnyDamage(AActor* DamagedActor, float Damage, const class UDamageType* DamageType, class AController* InstigatedBy, AActor* DamageCauser);

    void SetCurrentHealth(float NewHealth, AActor* DamageCauser = nullptr);
};
