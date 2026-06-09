#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "AbyssalHUDSubsystem.generated.h"

USTRUCT(BlueprintType)
struct FAbyssalVitalReadout
{
    GENERATED_BODY()

    /** 0..1 fraction. */
    UPROPERTY(BlueprintReadOnly) float HealthPercent = 1.0f;
    UPROPERTY(BlueprintReadOnly) float OxygenPercent = 1.0f;
    UPROPERTY(BlueprintReadOnly) float StaminaPercent = 1.0f;
    /** 0..100 from UTemperatureComponent::GetHeatPercent(). */
    UPROPERTY(BlueprintReadOnly) float HeatPercent = 0.0f;
    /** 0..100 from UPressureComponent::GetPressurePercent(). */
    UPROPERTY(BlueprintReadOnly) float PressurePercent = 0.0f;

    UPROPERTY(BlueprintReadOnly) bool bSubmerged = false;
    UPROPERTY(BlueprintReadOnly) bool bOverheating = false;
    UPROPERTY(BlueprintReadOnly) bool bAbovePressureRating = false;
    UPROPERTY(BlueprintReadOnly) bool bExhausted = false;
    UPROPERTY(BlueprintReadOnly) bool bDead = false;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalVitalsUpdatedSignature, const FAbyssalVitalReadout&, Readout);

/**
 * HUD data aggregator (roadmap J1). UMG widgets poll this subsystem via
 * GetVitalReadout() instead of finding individual components themselves.
 * The subsystem caches weak pointers to the local player pawn’s vital
 * components and refreshes them when the pawn changes. OnVitalsUpdated
 * fires whenever any vital delegate fires — widgets can bind once and
 * receive a consolidated snapshot on each change.
 *
 * Only valid for the local player; AI pawns do not register here.
 */
UCLASS()
class ABYSSALEARTH_API UAbyssalHUDSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    /**
     * Bind to the local player pawn. Call from AAbyssalPlayerCharacter::BeginPlay
     * (and after respawn). Clears previous bindings automatically.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|HUD")
    void RegisterPlayerPawn(APawn* PlayerPawn);

    /** Returns a snapshot of all current vital values. Safe to call every frame. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|HUD")
    FAbyssalVitalReadout GetVitalReadout() const;

    /**
     * Fires each time any registered vital changes. Carries the full snapshot
     * so widgets don’t need to call GetVitalReadout separately.
     */
    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|HUD")
    FAbyssalVitalsUpdatedSignature OnVitalsUpdated;

private:
    void BindVitalDelegates();
    void UnbindVitalDelegates();
    void BroadcastReadout();

    // Vital component weak refs (refreshed on RegisterPlayerPawn)
    UPROPERTY() TWeakObjectPtr<class UAbyssalHealthComponent> HealthComp;
    UPROPERTY() TWeakObjectPtr<class UOxygenComponent>        OxygenComp;
    UPROPERTY() TWeakObjectPtr<class UStaminaComponent>       StaminaComp;
    UPROPERTY() TWeakObjectPtr<class UTemperatureComponent>   TempComp;
    UPROPERTY() TWeakObjectPtr<class UPressureComponent>      PressComp;

    // Delegate handles for cleanup
    FDelegateHandle HealthHandle;
    FDelegateHandle OxygenHandle;
    FDelegateHandle StaminaHandle;
    FDelegateHandle TempHandle;
    FDelegateHandle PressHandle;
};
