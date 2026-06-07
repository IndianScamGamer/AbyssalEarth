#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "AbyssalInteractable.generated.h"

UINTERFACE(MinimalAPI, BlueprintType)
class UAbyssalInteractable : public UInterface
{
    GENERATED_BODY()
};

/**
 * Implement on any actor the player can focus and "use" through UInteractionComponent.
 *
 * This is the foundational interaction contract for, e.g.:
 *  - prying open the crushed elevator doors (prologue beat 08),
 *  - operating ancient systems / routing power (Act 3, "Make the Machine Answer"),
 *  - terminals, harvest nodes, fabricators, and level-transition actors.
 *
 * All methods are BlueprintNativeEvent so Blueprint children can override behaviour
 * while C++ provides sensible defaults (see AbyssalInteractable.cpp).
 */
class ABYSSALEARTH_API IAbyssalInteractable
{
    GENERATED_BODY()

public:
    /** Whether this actor can currently be interacted with by Interactor. Default: true. */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Interaction")
    bool CanInteract(AActor* Interactor);

    /** Short verb-phrase prompt shown while focused, e.g. "Pry open". Default: "Interact". */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Interaction")
    FText GetInteractionPrompt();

    /** Seconds the interact input must be held before completing; 0 means instant. Default: 0. */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Interaction")
    float GetInteractionHoldDuration();

    /** Called when the interaction is performed (after any required hold completes). */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Interaction")
    void OnInteract(AActor* Interactor);

    /** Called when this actor becomes the focused interactable. */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Interaction")
    void OnBeginFocus(AActor* Interactor);

    /** Called when this actor stops being the focused interactable. */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Interaction")
    void OnEndFocus(AActor* Interactor);
};
