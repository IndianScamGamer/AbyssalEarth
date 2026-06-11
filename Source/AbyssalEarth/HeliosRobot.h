#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AbyssalInteractable.h"
#include "HeliosRobot.generated.h"

class USkeletalMeshComponent;

UENUM(BlueprintType)
enum class EHeliosState : uint8
{
    Idle     UMETA(DisplayName = "Idle"),
    Working  UMETA(DisplayName = "Working"),
    Warning  UMETA(DisplayName = "Warning"),
    Disabled UMETA(DisplayName = "Disabled"),
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FHeliosStateChangedSignature, EHeliosState, NewState, EHeliosState, OldState);

/**
 * HELIOS construction-fleet robot NPC (roadmap D2). A humanoid autonomous unit that
 * built the shaft infrastructure; warns the player of the unresolved anomaly in the
 * prologue (PRO_005). Implements IAbyssalInteractable: each interaction plays the next
 * line in DialogueBeatIds through UNarrativeSubsystem (D1). A simple state machine
 * (Idle/Working/Warning/Disabled) drives animation/VFX via Blueprint hooks.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AHeliosRobot : public AActor, public IAbyssalInteractable
{
    GENERATED_BODY()

public:
    AHeliosRobot();

    // IAbyssalInteractable
    virtual bool CanInteract_Implementation(AActor* Interactor) override;
    virtual FText GetInteractionPrompt_Implementation() override;
    virtual void OnInteract_Implementation(AActor* Interactor) override;
    virtual void OnBeginFocus_Implementation(AActor* Interactor) override;
    virtual void OnEndFocus_Implementation(AActor* Interactor) override;

    UFUNCTION(BlueprintCallable, Category = "HELIOS")
    void SetHeliosState(EHeliosState NewState);

    UFUNCTION(BlueprintPure, Category = "HELIOS")
    EHeliosState GetHeliosState() const { return State; }

    /** Restart dialogue from the first line on the next interaction. */
    UFUNCTION(BlueprintCallable, Category = "HELIOS")
    void ResetDialogue() { DialogueIndex = 0; }

    /** Display name used in the interaction prompt ("Talk to {UnitName}"). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HELIOS")
    FText UnitName;

    /** Narrative beat ids spoken in order, one per interaction. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HELIOS")
    TArray<FName> DialogueBeatIds;

    /** If true, dialogue loops back to the first line after the last; else the last line repeats. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HELIOS")
    bool bLoopDialogue = false;

    UPROPERTY(BlueprintAssignable, Category = "HELIOS")
    FHeliosStateChangedSignature OnHeliosStateChanged;

protected:
    UFUNCTION(BlueprintImplementableEvent, Category = "HELIOS")
    void BP_OnStateChanged(EHeliosState NewState);

    UFUNCTION(BlueprintImplementableEvent, Category = "HELIOS")
    void BP_OnDialogueLine(FName BeatId, int32 LineIndex);

    UFUNCTION(BlueprintImplementableEvent, Category = "HELIOS")
    void BP_OnFocusBegin();

    UFUNCTION(BlueprintImplementableEvent, Category = "HELIOS")
    void BP_OnFocusEnd();

private:
    UPROPERTY(VisibleAnywhere)
    TObjectPtr<USkeletalMeshComponent> Mesh;

    UPROPERTY()
    EHeliosState State = EHeliosState::Working;

    UPROPERTY()
    int32 DialogueIndex = 0;
};
