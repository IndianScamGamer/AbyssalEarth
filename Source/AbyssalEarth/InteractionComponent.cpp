#include "InteractionComponent.h"
#include "AbyssalInteractable.h"
#include "CollisionQueryParams.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

UInteractionComponent::UInteractionComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UInteractionComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UInteractionComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    UpdateFocus();

    if (bInteracting && HoldRequired > 0.0f)
    {
        HoldElapsed += DeltaTime;
        if (HoldElapsed >= HoldRequired)
        {
            CompleteInteraction();
        }
    }
}

void UInteractionComponent::UpdateFocus()
{
    AActor* Candidate = FindFocusCandidate();
    if (Candidate == FocusedActor)
    {
        return;
    }

    AActor* Owner = GetOwner();

    if (FocusedActor && FocusedActor->Implements<UAbyssalInteractable>())
    {
        IAbyssalInteractable::Execute_OnEndFocus(FocusedActor, Owner);
    }

    // Changing focus cancels any hold in progress.
    if (bInteracting)
    {
        EndInteract();
    }

    FocusedActor = Candidate;

    if (FocusedActor && FocusedActor->Implements<UAbyssalInteractable>())
    {
        IAbyssalInteractable::Execute_OnBeginFocus(FocusedActor, Owner);
    }

    OnFocusChanged.Broadcast(FocusedActor);
}

AActor* UInteractionComponent::FindFocusCandidate() const
{
    AActor* Owner = GetOwner();
    UWorld* World = GetWorld();
    if (!Owner || !World)
    {
        return nullptr;
    }

    FVector ViewLocation;
    FRotator ViewRotation;
    Owner->GetActorEyesViewPoint(ViewLocation, ViewRotation);
    const FVector TraceEnd = ViewLocation + ViewRotation.Vector() * InteractionDistance;

    FCollisionQueryParams Params(SCENE_QUERY_STAT(AbyssalInteractionFocus), false);
    Params.AddIgnoredActor(Owner);

    FHitResult Hit;
    if (!World->LineTraceSingleByChannel(Hit, ViewLocation, TraceEnd, InteractionTraceChannel, Params))
    {
        return nullptr;
    }

    AActor* HitActor = Hit.GetActor();
    if (!HitActor || !HitActor->Implements<UAbyssalInteractable>())
    {
        return nullptr;
    }

    if (!IAbyssalInteractable::Execute_CanInteract(HitActor, Owner))
    {
        return nullptr;
    }

    return HitActor;
}

bool UInteractionComponent::BeginInteract()
{
    if (!FocusedActor || !FocusedActor->Implements<UAbyssalInteractable>())
    {
        return false;
    }

    AActor* Owner = GetOwner();
    if (!IAbyssalInteractable::Execute_CanInteract(FocusedActor, Owner))
    {
        return false;
    }

    HoldRequired = FMath::Max(0.0f, IAbyssalInteractable::Execute_GetInteractionHoldDuration(FocusedActor));
    HoldElapsed = 0.0f;
    bInteracting = true;

    OnInteractionStarted.Broadcast(FocusedActor, HoldRequired);

    if (HoldRequired <= 0.0f)
    {
        CompleteInteraction();
    }

    return true;
}

void UInteractionComponent::EndInteract()
{
    if (!bInteracting)
    {
        return;
    }

    const bool bWasHolding = HoldRequired > 0.0f && HoldElapsed < HoldRequired;
    bInteracting = false;
    HoldElapsed = 0.0f;
    HoldRequired = 0.0f;

    if (bWasHolding)
    {
        OnInteractionCanceled.Broadcast();
    }
}

void UInteractionComponent::CompleteInteraction()
{
    AActor* Owner = GetOwner();
    AActor* Target = FocusedActor;

    bInteracting = false;
    HoldElapsed = 0.0f;
    HoldRequired = 0.0f;

    if (Target && Target->Implements<UAbyssalInteractable>())
    {
        IAbyssalInteractable::Execute_OnInteract(Target, Owner);
        OnInteractionCompleted.Broadcast(Target);
    }
}

AActor* UInteractionComponent::GetFocusedActor() const
{
    return FocusedActor;
}

bool UInteractionComponent::HasFocus() const
{
    return FocusedActor != nullptr;
}

FText UInteractionComponent::GetFocusPrompt() const
{
    if (FocusedActor && FocusedActor->Implements<UAbyssalInteractable>())
    {
        return IAbyssalInteractable::Execute_GetInteractionPrompt(FocusedActor);
    }
    return FText::GetEmpty();
}

float UInteractionComponent::GetHoldProgress() const
{
    if (bInteracting && HoldRequired > 0.0f)
    {
        return FMath::Clamp(HoldElapsed / HoldRequired, 0.0f, 1.0f);
    }
    return 0.0f;
}
