#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/EngineTypes.h"
#include "StaminaComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalStaminaChangedSignature, float, StaminaPercent);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalExhaustedSignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalRecoveredSignature);

/**
 * Exertion survival vital (roadmap B3). Stamina (0..1) drains while the owner is
 * exerting (sprinting, climbing, swimming against current) and regenerates after a
 * short recovery delay once exertion stops. Hitting zero raises an exhaustion gate:
 * CanExert() returns false until stamina recovers past ExhaustionRecoveryThreshold,
 * which the character movement code should poll before allowing sprint.
 *
 * Discrete actions (dodge, climb-jump) call TryConsumeStamina(Cost). No damage path
 * — stamina only gates traversal. Transient (reset on load), like health.
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UStaminaComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UStaminaComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /** Begin/stop continuous exertion (sprint, climb). Movement code drives this. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void SetExerting(bool bInExerting);

    /** Spend a discrete chunk of stamina (e.g. dodge). Returns false (and spends nothing) if insufficient or exhausted. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    bool TryConsumeStamina(float Cost);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void RestoreStamina();

    /** Whether the owner may currently start/continue exerting (false while exhausted). */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    bool CanExert() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetStamina() const { return Stamina; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetStaminaPercent() const { return Stamina * 100.0f; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    bool IsExhausted() const { return bExhausted; }

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalStaminaChangedSignature OnStaminaChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalExhaustedSignature OnExhausted;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalRecoveredSignature OnRecovered;

    /** Stamina fraction drained per second while exerting. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float DrainRate = 0.25f;

    /** Stamina fraction regenerated per second while resting. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float RegenRate = 0.20f;

    /** Seconds to wait after exertion stops before regen begins. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float RegenDelay = 1.0f;

    /** Once exhausted, stamina must climb above this fraction before exertion is allowed again. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0", ClampMax="1.0"))
    float ExhaustionRecoveryThreshold = 0.25f;

protected:
    virtual void BeginPlay() override;

private:
    void SetStamina(float NewStamina);

    UPROPERTY()
    float Stamina = 1.0f;

    UPROPERTY()
    bool bExerting = false;

    UPROPERTY()
    bool bExhausted = false;

    float TimeSinceExertion = 0.0f;
};
