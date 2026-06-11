#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/EngineTypes.h"
#include "OxygenComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalOxygenChangedSignature, float, OxygenPercent, bool, bSubmerged);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalSuffocationBeganSignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalSuffocationEndedSignature);

/**
 * Breathable-air survival vital (roadmap B3). Oxygen (0..1) drains while the owner
 * is submerged or in a low-oxygen zone and refills while breathing. At zero it
 * applies periodic suffocation damage through the engine damage system
 * (UGameplayStatics::ApplyDamage), the same path AEmberVentHazard/UTemperatureComponent
 * use, routing into UAbyssalHealthComponent. AirCapacityBonus foreshadows rebreather
 * upgrades (extends effective drain time).
 *
 * Map use: Inner Sea (underwater sections), and any sealed/low-air pocket.
 * Vitals are transient (reset on load), like health — not persisted.
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UOxygenComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UOxygenComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /** Enter/leave a submerged or low-oxygen zone. Water/air volumes call this on the player's component. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void SetSubmerged(bool bInSubmerged);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void RefillOxygen();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetOxygen() const { return Oxygen; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetOxygenPercent() const { return Oxygen * 100.0f; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    bool IsSuffocating() const { return bSuffocating; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    bool IsSubmerged() const { return bSubmerged; }

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalOxygenChangedSignature OnOxygenChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalSuffocationBeganSignature OnSuffocationBegan;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalSuffocationEndedSignature OnSuffocationEnded;

    /** Oxygen fraction drained per second while submerged (before AirCapacityBonus). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float OxygenDrainRate = 0.10f;

    /** Oxygen fraction refilled per second while breathing. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float OxygenRefillRate = 0.40f;

    /** Suffocation damage per second applied while oxygen is depleted. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float SuffocationDamagePerSecond = 15.0f;

    /** 0 = base lungs, 1 = double effective air (halves drain). Raised by rebreather upgrades. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0", ClampMax="1.0"))
    float AirCapacityBonus = 0.0f;

protected:
    virtual void BeginPlay() override;

private:
    void SetOxygen(float NewOxygen);
    void ApplySuffocationDamage(float DeltaTime);

    UPROPERTY()
    float Oxygen = 1.0f;

    UPROPERTY()
    bool bSubmerged = false;

    UPROPERTY()
    bool bSuffocating = false;
};
