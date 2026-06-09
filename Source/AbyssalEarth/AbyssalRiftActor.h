#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AbyssalInteractable.h"
#include "AbyssalRiftActor.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalRiftStateChangedSignature, EAbyssalRiftState, NewState);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalRiftOpenedSignature);

UENUM(BlueprintType)
enum class EAbyssalRiftState : uint8
{
    Dormant   UMETA(DisplayName = "Dormant"),
    Charging  UMETA(DisplayName = "Charging"),
    Open      UMETA(DisplayName = "Open"),
    Stable    UMETA(DisplayName = "Stable"),
};

/**
 * Endgame rift portal actor (roadmap M1 — Act 5 OBJ_OPEN_RIFT).
 * Requires:
 *   1. Sufficient power (via SetPowerLevel, same interface as terminals)
 *   2. ITEM_KEY_RIFT_STABILISER in the player's UInventorySubsystem
 * When both conditions are met the player can interact to begin the
 * Charging phase. After ChargeDuration seconds the rift transitions
 * to Open, OnRiftOpened fires, and OBJ_OPEN_RIFT completes.
 * Blueprint subclass handles all VFX and audio for each state.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AAbyssalRiftActor : public AActor, public IAbyssalInteractable
{
    GENERATED_BODY()

public:
    AAbyssalRiftActor();

    /** Called by AAbyssalPowerNode or directly to supply power (0..1). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Rift")
    void SetPowerLevel(float NewPower);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Rift")
    float GetPowerLevel() const { return CurrentPower; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Rift")
    EAbyssalRiftState GetRiftState() const { return CurrentState; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Rift")
    bool IsOpen() const { return CurrentState == EAbyssalRiftState::Open || CurrentState == EAbyssalRiftState::Stable; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Rift")
    float GetChargePercent() const;

    // IAbyssalInteractable
    virtual bool CanInteract_Implementation(AActor* Interactor) const override;
    virtual void OnInteract_Implementation(AActor* Interactor) override;
    virtual FText GetInteractPrompt_Implementation() const override;
    virtual void OnFocusBegin_Implementation(AActor* Interactor) override;
    virtual void OnFocusEnd_Implementation(AActor* Interactor) override;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Rift")
    FAbyssalRiftStateChangedSignature OnRiftStateChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Rift")
    FAbyssalRiftOpenedSignature OnRiftOpened;

    /** Power threshold (0..1) required before the rift can be activated. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Rift", meta=(ClampMin="0.0", ClampMax="1.0"))
    float PowerThreshold = 0.8f;

    /** Seconds for the Charging state before transitioning to Open. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Rift", meta=(ClampMin="1.0"))
    float ChargeDuration = 8.0f;

    /** Item ID consumed from inventory on activation. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Rift")
    FName RequiredItemId = FName(TEXT("ITEM_KEY_RIFT_STABILISER"));

protected:
    virtual void BeginPlay() override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Rift")
    void BP_OnStateChanged(EAbyssalRiftState NewState);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Rift")
    void BP_OnRiftOpened();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Rift")
    void BP_OnFocusBegin();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Rift")
    void BP_OnFocusEnd();

private:
    void SetRiftState(EAbyssalRiftState NewState);
    bool CheckActivationRequirements(AActor* Interactor) const;

    UFUNCTION()
    void OnChargeComplete();

    UPROPERTY()
    EAbyssalRiftState CurrentState = EAbyssalRiftState::Dormant;

    UPROPERTY()
    float CurrentPower = 0.0f;

    float ChargeElapsed = 0.0f;
    FTimerHandle ChargeTimer;
};
