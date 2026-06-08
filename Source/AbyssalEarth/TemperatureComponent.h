#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/EngineTypes.h"
#include "TemperatureComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalTemperatureChangedSignature, float, HeatPercent, bool, bInHeatZone);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalOverheatBeganSignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalOverheatEndedSignature);

/**
 * Heat-exposure survival vital (roadmap B3). Exposure (0..1) rises while the owner
 * is in a heat zone and falls while in safe/cool areas. At/above the overheat
 * threshold it applies periodic damage to the owner through the engine damage system
 * (UGameplayStatics::ApplyDamage), the same path AEmberVentHazard uses, which routes
 * into UAbyssalHealthComponent. Insulation scales incoming heat to foreshadow suit
 * upgrades / equipment.
 *
 * Single-purpose for now (heat); oxygen/stamina vitals can follow this pattern or be
 * generalized later. NOTE: exposure is not yet persisted (pending save rework, A1).
 * Map use: Mantle Garden (heat fields), and any future heat hazard.
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UTemperatureComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UTemperatureComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /** Enter/leave a heat zone. Heat volumes call this on the player's component. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void SetInHeatZone(bool bInZone);

    /** Add an instantaneous chunk of heat exposure (positive heats, negative cools). Positive amounts are scaled by insulation. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void AddHeatExposure(float Delta);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Survival")
    void ResetTemperature();

    /** Current exposure on a 0..1 scale. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetHeatExposure() const;

    /** Current exposure on a 0..100 scale for HUD readouts. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    float GetHeatPercent() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    bool IsOverheating() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Survival")
    bool IsInHeatZone() const;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalTemperatureChangedSignature OnTemperatureChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalOverheatBeganSignature OnOverheatBegan;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Survival")
    FAbyssalOverheatEndedSignature OnOverheatEnded;

    /** Heat exposure gained per second while in a heat zone (before insulation). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float HeatGainRate = 0.12f;

    /** Heat exposure lost per second while not in a heat zone. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float CoolRate = 0.18f;

    /** Exposure (0..1) at/above which the owner takes overheating damage. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0", ClampMax="1.0"))
    float OverheatThreshold = 0.85f;

    /** Damage per second applied while overheating. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0"))
    float OverheatDamagePerSecond = 12.0f;

    /** 0 = no protection (full heat), 1 = fully insulated (no heat gain). Raised by future upgrades. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Survival", meta=(ClampMin="0.0", ClampMax="1.0"))
    float Insulation = 0.0f;

protected:
    virtual void BeginPlay() override;

private:
    void SetHeatExposure(float NewExposure);
    void ApplyOverheatDamage(float DeltaTime);

    UPROPERTY()
    float HeatExposure = 0.0f;

    UPROPERTY()
    bool bInHeatZone = false;

    UPROPERTY()
    bool bOverheating = false;
};
