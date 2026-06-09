#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AbyssalInteractable.h"
#include "CheckpointActor.generated.h"

UENUM(BlueprintType)
enum class ECheckpointState : uint8
{
    Inactive  UMETA(DisplayName = "Inactive"),
    Active    UMETA(DisplayName = "Active"),
};

/**
 * World-placed checkpoint actor (roadmap G3). Registers with UCheckpointSubsystem
 * on BeginPlay. The player activates it via UAbyssalInteractionComponent —
 * once activated the state changes to Active and OnCheckpointActivated fires.
 * Blueprint subclass controls visuals (mesh swap, particle, sound).
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API ACheckpointActor : public AActor, public IAbyssalInteractable
{
    GENERATED_BODY()

public:
    ACheckpointActor();

    virtual void BeginPlay() override;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Checkpoint")
    ECheckpointState GetCheckpointState() const { return CurrentState; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Checkpoint")
    bool IsActive() const { return CurrentState == ECheckpointState::Active; }

    // IAbyssalInteractable
    virtual bool CanInteract_Implementation(AActor* Interactor) const override;
    virtual void OnInteract_Implementation(AActor* Interactor) override;
    virtual FText GetInteractPrompt_Implementation() const override;
    virtual void OnFocusBegin_Implementation(AActor* Interactor) override;
    virtual void OnFocusEnd_Implementation(AActor* Interactor) override;

    /** Unique ID used to identify this checkpoint in UCheckpointSubsystem. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Checkpoint")
    FName CheckpointId;

    /** Map ID this checkpoint belongs to (must match UWorldFlowSubsystem map IDs). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Checkpoint")
    FName MapId;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Checkpoint")
    FAbyssalCheckpointActivatedSignature OnCheckpointActivated;

protected:
    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Checkpoint")
    void BP_OnActivated();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Checkpoint")
    void BP_OnFocusBegin();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Checkpoint")
    void BP_OnFocusEnd();

private:
    ECheckpointState CurrentState = ECheckpointState::Inactive;
};
