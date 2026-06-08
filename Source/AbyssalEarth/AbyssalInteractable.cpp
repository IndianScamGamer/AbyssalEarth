#include "AbyssalInteractable.h"

// Default C++ implementations for the BlueprintNativeEvent interface methods.
// Blueprint children may override any of these.

bool IAbyssalInteractable::CanInteract_Implementation(AActor* Interactor)
{
    return true;
}

FText IAbyssalInteractable::GetInteractionPrompt_Implementation()
{
    return NSLOCTEXT("AbyssalEarthInteraction", "DefaultPrompt", "Interact");
}

float IAbyssalInteractable::GetInteractionHoldDuration_Implementation()
{
    return 0.0f;
}

void IAbyssalInteractable::OnInteract_Implementation(AActor* Interactor)
{
}

void IAbyssalInteractable::OnBeginFocus_Implementation(AActor* Interactor)
{
}

void IAbyssalInteractable::OnEndFocus_Implementation(AActor* Interactor)
{
}
