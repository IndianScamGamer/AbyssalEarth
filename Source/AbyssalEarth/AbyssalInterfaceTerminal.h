#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AbyssalInteractable.h"
#include "AbyssalInterfaceTerminal.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalTerminalActivatedSignature, class AAbyssalInterfaceTerminal*, Terminal);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalTerminalDataReadoutSignature, class AAbyssalInterfaceTerminal*, Terminal, FName, DataBeatId);

UENUM(BlueprintType)
enum class EAbyssalTerminalState : uint8
{
    Dormant     UMETA(DisplayName = "Dormant"),
    Powering    UMETA(DisplayName = "Powering"),
    Active      UMETA(DisplayName = "Active"),
    Locked      UMETA(DisplayName = "Locked"),
};

/**
 * Alien interface terminal (roadmap D5). Central to Act 3 objective
 * OBJ_MAKE_MACHINE_ANSWER. Must be powered to a threshold before the player
 * can interact. Each interaction plays the next beat in DataBeatIds via
 * UNarrativeSubsystem; when all beats are exhausted a terminal-complete
 * delegate fires. Power is supplied externally by the power-routing puzzle
 * (future C3 system); this actor just tracks its own state.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AAbyssalInterfaceTerminal : public AActor, public IAbyssalInteractable
{
    GENERATED_BODY()

public:
    AAbyssalInterfaceTerminal();

    /** Supply or drain power (0..1 normalised). Above ActivationThreshold → Powering → Active. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Terminal")
    void SetPowerLevel(float NewPower);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Terminal")
    float GetPowerLevel() const { return CurrentPower; }

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Terminal")
    void SetTerminalState(EAbyssalTerminalState NewState);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Terminal")
    EAbyssalTerminalState GetTerminalState() const { return CurrentState; }

    /** Lock the terminal (e.g. alien defence system triggered). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Terminal")
    void LockTerminal();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Terminal")
    void UnlockTerminal();

    /** True when all data beats have been played. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Terminal")
    bool IsDataExhausted() const;

    // IAbyssalInteractable
    virtual bool CanInteract_Implementation(AActor* Interactor) const override;
    virtual void OnInteract_Implementation(AActor* Interactor) override;
    virtual FText GetInteractPrompt_Implementation() const override;
    virtual void OnFocusBegin_Implementation(AActor* Interactor) override;
    virtual void OnFocusEnd_Implementation(AActor* Interactor) override;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Terminal")
    FAbyssalTerminalActivatedSignature OnTerminalActivated;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Terminal")
    FAbyssalTerminalDataReadoutSignature OnDataReadout;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Terminal")
    FAbyssalTerminalActivatedSignature OnDataExhausted;

    /** Ordered narrative beat IDs played sequentially on each interaction. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Terminal")
    TArray<FName> DataBeatIds;

    /** Normalised power level (0..1) required to transition Dormant → Powering. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Terminal", meta=(ClampMin="0.0", ClampMax="1.0"))
    float ActivationThreshold = 0.6f;

    /** Seconds for the Powering state before becoming Active. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Terminal", meta=(ClampMin="0.0"))
    float PowerUpDuration = 3.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Terminal")
    FText TerminalLabel = NSLOCTEXT("AbyssalEarth", "TerminalDefaultLabel", "Interface Terminal");

protected:
    virtual void BeginPlay() override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Terminal")
    void BP_OnStateChanged(EAbyssalTerminalState NewState);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Terminal")
    void BP_OnDataReadout(FName BeatId);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Terminal")
    void BP_OnDataExhausted();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Terminal")
    void BP_OnFocusBegin();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Terminal")
    void BP_OnFocusEnd();

private:
    UFUNCTION()
    void OnPowerUpComplete();

    UPROPERTY()
    EAbyssalTerminalState CurrentState = EAbyssalTerminalState::Dormant;

    UPROPERTY()
    float CurrentPower = 0.0f;

    UPROPERTY()
    int32 DataBeatIndex = 0;

    FTimerHandle PowerUpTimer;
};
