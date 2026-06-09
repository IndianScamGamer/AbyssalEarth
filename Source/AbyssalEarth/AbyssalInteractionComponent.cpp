#include "AbyssalInteractionComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/PlayerController.h"
#include "Camera/CameraComponent.h"
#include "Engine/World.h"

UAbyssalInteractionComponent::UAbyssalInteractionComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UAbyssalInteractionComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UAbyssalInteractionComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (bTraceEveryTick)
    {
        RunTrace();
    }
    else
    {
        TimeSinceLastTrace += DeltaTime;
        if (TimeSinceLastTrace >= TraceInterval)
        {
            TimeSinceLastTrace = 0.0f;
            RunTrace();
        }
    }
}

bool UAbyssalInteractionComponent::TryInteract()
{
    AActor* Target = FocusedActor.Get();
    if (!Target)
    {
        return false;
    }

    IAbyssalInteractable* Interactable = Cast<IAbyssalInteractable>(Target);
    if (!Interactable)
    {
        return false;
    }

    if (!IAbyssalInteractable::Execute_CanInteract(Target, GetOwner()))
    {
        return false;
    }

    IAbyssalInteractable::Execute_OnInteract(Target, GetOwner());
    OnInteracted.Broadcast(GetOwner(), Target);
    return true;
}

FText UAbyssalInteractionComponent::GetInteractPrompt() const
{
    AActor* Target = FocusedActor.Get();
    if (!Target)
    {
        return FText::GetEmpty();
    }

    if (!Target->Implements<UAbyssalInteractable>())
    {
        return FText::GetEmpty();
    }

    if (!IAbyssalInteractable::Execute_CanInteract(Target, GetOwner()))
    {
        return FText::GetEmpty();
    }

    return IAbyssalInteractable::Execute_GetInteractPrompt(Target);
}

void UAbyssalInteractionComponent::RunTrace()
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    const FVector Start = GetTraceStart();
    const FVector End = GetTraceEnd();

    FHitResult Hit;
    FCollisionQueryParams Params;
    Params.AddIgnoredActor(GetOwner());

    AActor* NewFocus = nullptr;
    if (World->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
    {
        AActor* HitActor = Hit.GetActor();
        if (HitActor && HitActor->Implements<UAbyssalInteractable>())
        {
            NewFocus = HitActor;
        }
    }

    SetFocus(NewFocus);
}

void UAbyssalInteractionComponent::SetFocus(AActor* NewFocus)
{
    AActor* OldFocus = FocusedActor.Get();
    if (OldFocus == NewFocus)
    {
        return;
    }

    if (OldFocus && OldFocus->Implements<UAbyssalInteractable>())
    {
        IAbyssalInteractable::Execute_OnFocusEnd(OldFocus, GetOwner());
        OnFocusEnd.Broadcast(OldFocus);
    }

    FocusedActor = NewFocus;

    if (NewFocus && NewFocus->Implements<UAbyssalInteractable>())
    {
        IAbyssalInteractable::Execute_OnFocusBegin(NewFocus, GetOwner());
        OnFocusBegin.Broadcast(NewFocus);
    }
}

FVector UAbyssalInteractionComponent::GetTraceStart() const
{
    // Prefer camera location if owner has one, otherwise actor eye location
    if (ACharacter* Char = Cast<ACharacter>(GetOwner()))
    {
        if (UCameraComponent* Camera = Char->FindComponentByClass<UCameraComponent>())
        {
            return Camera->GetComponentLocation();
        }
    }
    FVector EyeLoc;
    FRotator EyeRot;
    GetOwner()->GetActorEyesViewPoint(EyeLoc, EyeRot);
    return EyeLoc;
}

FVector UAbyssalInteractionComponent::GetTraceEnd() const
{
    FVector EyeLoc;
    FRotator EyeRot;
    GetOwner()->GetActorEyesViewPoint(EyeLoc, EyeRot);
    return GetTraceStart() + EyeRot.Vector() * InteractDistance;
}
