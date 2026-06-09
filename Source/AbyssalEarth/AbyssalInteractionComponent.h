#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "AbyssalInteractable.h"
#include "AbyssalInteractionComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalInteractionFocusSignature, AActor*, FocusedActor);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalInteractSignature, AActor*, Interactor, AActor*, Target);

/**
 * Player-side interaction manager (roadmap F3). Runs a per-tick forward line
 * trace from the owning camera (or actor forward vector as fallback) to find
 * the nearest IAbyssalInteractable within InteractDistance. Manages focus
 * (calling OnFocusBegin/End on candidates) and exposes TryInteract() which
 * calls OnInteract on the current target.
 *
 * Attach to the player Character. Driven by PlayerController input.
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UAbyssalInteractionComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UAbyssalInteractionComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /**
     * Attempt to interact with the currently focused actor.
     * Returns false if nothing is focused or CanInteract returns false.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Interaction")
    bool TryInteract();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Interaction")
    AActor* GetFocusedActor() const { return FocusedActor.Get(); }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Interaction")
    bool HasFocus() const { return FocusedActor.IsValid(); }

    /** Returns the interact prompt from the focused actor, or empty text if none. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Interaction")
    FText GetInteractPrompt() const;

    /** Maximum distance for interaction line trace (cm). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Interaction", meta=(ClampMin="10.0"))
    float InteractDistance = 250.0f;

    /** If true the trace fires every tick; if false it fires on a timer at TraceInterval. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Interaction")
    bool bTraceEveryTick = true;

    /** Seconds between traces when bTraceEveryTick is false. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Interaction", meta=(ClampMin="0.05"))
    float TraceInterval = 0.1f;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Interaction")
    FAbyssalInteractionFocusSignature OnFocusBegin;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Interaction")
    FAbyssalInteractionFocusSignature OnFocusEnd;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Interaction")
    FAbyssalInteractSignature OnInteracted;

protected:
    virtual void BeginPlay() override;

private:
    void RunTrace();
    void SetFocus(AActor* NewFocus);

    FVector GetTraceStart() const;
    FVector GetTraceEnd() const;

    UPROPERTY()
    TWeakObjectPtr<AActor> FocusedActor;

    float TimeSinceLastTrace = 0.0f;
};
