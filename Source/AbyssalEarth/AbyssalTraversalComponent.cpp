#include "AbyssalTraversalComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/Pawn.h"

UAbyssalTraversalComponent::UAbyssalTraversalComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UAbyssalTraversalComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UAbyssalTraversalComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
}

UCharacterMovementComponent* UAbyssalTraversalComponent::GetCharacterMovement() const
{
    if (const ACharacter* Character = Cast<ACharacter>(GetOwner()))
    {
        return Character->GetCharacterMovement();
    }
    return nullptr;
}

void UAbyssalTraversalComponent::SetState(EAbyssalTraversalState NewState)
{
    if (State == NewState)
    {
        return;
    }

    const EAbyssalTraversalState OldState = State;
    State = NewState;
    OnTraversalStateChanged.Broadcast(State, OldState);
}

void UAbyssalTraversalComponent::BeginClimb(FVector SurfaceNormal)
{
    ClimbSurfaceNormal = SurfaceNormal.GetSafeNormal();

    if (UCharacterMovementComponent* Movement = GetCharacterMovement())
    {
        // Flying mode lets the character move freely along the surface; the
        // climb input direction is projected onto the surface plane in BP/movement code.
        Movement->SetMovementMode(MOVE_Flying);
    }

    SetState(EAbyssalTraversalState::Climbing);
}

void UAbyssalTraversalComponent::EndClimb()
{
    if (State != EAbyssalTraversalState::Climbing)
    {
        return;
    }

    ClimbSurfaceNormal = FVector::ZeroVector;

    if (UCharacterMovementComponent* Movement = GetCharacterMovement())
    {
        Movement->SetMovementMode(MOVE_Falling);
    }

    SetState(EAbyssalTraversalState::Grounded);
}

void UAbyssalTraversalComponent::SetSwimming(bool bInSwimming)
{
    if (bInSwimming)
    {
        if (UCharacterMovementComponent* Movement = GetCharacterMovement())
        {
            Movement->SetMovementMode(MOVE_Swimming);
        }
        SetState(EAbyssalTraversalState::Swimming);
    }
    else if (State == EAbyssalTraversalState::Swimming)
    {
        if (UCharacterMovementComponent* Movement = GetCharacterMovement())
        {
            Movement->SetMovementMode(MOVE_Falling);
        }
        SetState(EAbyssalTraversalState::Grounded);
    }
}

void UAbyssalTraversalComponent::FireTether(FVector WorldAnchor)
{
    TetherAnchor = WorldAnchor;
    SetState(EAbyssalTraversalState::Tethered);
    OnTetherChanged.Broadcast(true);
}

void UAbyssalTraversalComponent::ReleaseTether()
{
    if (State != EAbyssalTraversalState::Tethered)
    {
        return;
    }

    TetherAnchor = FVector::ZeroVector;
    SetState(EAbyssalTraversalState::Grounded);
    OnTetherChanged.Broadcast(false);
}

FVector UAbyssalTraversalComponent::GetTetherCorrection() const
{
    if (State != EAbyssalTraversalState::Tethered)
    {
        return FVector::ZeroVector;
    }

    const AActor* Owner = GetOwner();
    if (!Owner)
    {
        return FVector::ZeroVector;
    }

    const FVector ToOwner = Owner->GetActorLocation() - TetherAnchor;
    const float Distance = ToOwner.Size();
    if (Distance <= TetherLength || Distance <= KINDA_SMALL_NUMBER)
    {
        return FVector::ZeroVector;
    }

    // Vector from the current position back onto the tether sphere surface.
    const FVector Direction = ToOwner / Distance;
    const float Overshoot = Distance - TetherLength;
    return -Direction * Overshoot;
}

void UAbyssalTraversalComponent::RequestGravityReorientation(FVector NewGravityDirection, float LerpDuration)
{
    const FVector Normalized = NewGravityDirection.GetSafeNormal();
    if (Normalized.IsNearlyZero())
    {
        return;
    }

    CurrentGravityDirection = Normalized;
    OnGravityReorientRequested.Broadcast(Normalized, FMath::Max(0.0f, LerpDuration));
}
