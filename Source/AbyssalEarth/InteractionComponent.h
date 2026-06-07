#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/EngineTypes.h"
#include "InteractionComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalFocusChangedSignature, AActor*, FocusedActor);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalInteractionStartedSignature, AActor*, InteractedActor, float, HoldDuration);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalInteractionCompletedSignature, AActor*, InteractedActor);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalInteractionCanceledSignature);

/**
 * Player-owned component that line-traces from the owner's eye viewpoint each tick,
 * tracks the focused IAbyssalInteractable, and drives instant or hold interactions.
 *
 * Input/UI layers bind to the delegates: OnFocusChanged updates the interaction
 * prompt, OnInteractionStarted/Completed/Canceled drive hold UI and feedback.
 */
UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UInteractionComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UInteractionComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /**
     * Begin interacting with the focused actor. Instant interactables complete
     * immediately; hold interactables start the hold timer. Returns true if an
     * interaction began.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Interaction")
    bool BeginInteract();

    /** Release the interact input, cancelling an in-progress hold that has not completed. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Interaction")
    void EndInteract();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Interaction")
    AActor* GetFocusedActor() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Interaction")
    bool HasFocus() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Interaction")
    FText GetFocusPrompt() const;

    /** 0..1 progress of an in-progress hold interaction (0 when not holding). */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Interaction")
    float GetHoldProgress() const;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Interaction")
    FAbyssalFocusChangedSignature OnFocusChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Interaction")
    FAbyssalInteractionStartedSignature OnInteractionStarted;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Interaction")
    FAbyssalInteractionCompletedSignature OnInteractionCompleted;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Interaction")
    FAbyssalInteractionCanceledSignature OnInteractionCanceled;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Interaction")
    float InteractionDistance = 350.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Interaction")
    TEnumAsByte<ECollisionChannel> InteractionTraceChannel = ECC_Visibility;

protected:
    virtual void BeginPlay() override;

private:
    void UpdateFocus();
    AActor* FindFocusCandidate() const;
    void CompleteInteraction();

    UPROPERTY()
    TObjectPtr<AActor> FocusedActor = nullptr;

    bool bInteracting = false;
    float HoldElapsed = 0.0f;
    float HoldRequired = 0.0f;
};
