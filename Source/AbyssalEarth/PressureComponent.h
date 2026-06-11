#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PressureComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalPressureChangedSignature, float, PressurePercent, bool, bAboveRating);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalPressureCriticalSignature);

/**
 * Depth pressure survival vital (roadmap B4). Pressure is set externally by
 * a depth-tracking system (e.g. AAbyssalPlayerCharacter reads Z-position and
 * calls SetCurrentDepth each frame). When pressure exceeds PressureRating,
 * the owner takes damage via UGameplayStatics::ApplyDamage routed into
 * UAbyssalHealthComponent. PressureRating rises with suit upgrade items.
 *
 * "Depth" is expressed in metres below sea level (positive = deeper).
 * Pressure (atm) = 1 + Depth / 10.  Only depths past PressureSafeDepth matter.
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UPressureComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UPressureComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /**
     * Set the owner's current depth in metres (positive = deeper).
     * Call every frame from the owning character based on world Z position.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void SetCurrentDepth(float DepthMetres);

    /** Add to the suit's pressure rating (e.g. from upgrade items). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void AddPressureRating(float Delta);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void ResetPressure();

    /** Current depth in metres. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetCurrentDepth() const { return CurrentDepth; }

    /** Pressure in atm at current depth. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetCurrentPressureAtm() const;

    /** Pressure as 0..100 percent of the danger range above PressureSafeDepth. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetPressurePercent() const;

    /** True when depth exceeds the suit's effective rating. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    bool IsAbovePressureRating() const { return bAboveRating; }

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalPressureChangedSignature OnPressureChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalPressureCriticalSignature OnPressureCritical;

    /** Depth (m) below which pressure starts to matter. Defaults to 6000 m. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float PressureSafeDepth = 6000.0f;

    /** Suit's base pressure rating in atm. Exceeding this causes damage. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float PressureRating = 620.0f;

    /** Damage per second while above rating. Scales with overpressure magnitude. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float OverpressureDamagePerSecond = 10.0f;

protected:
    virtual void BeginPlay() override;

private:
    void ApplyOverpressureDamage(float DeltaTime);
    void UpdatePressureState();

    UPROPERTY()
    float CurrentDepth = 0.0f;

    UPROPERTY()
    bool bAboveRating = false;
};
