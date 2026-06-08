#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/EngineTypes.h"
#include "AbyssalTraversalComponent.generated.h"

UENUM(BlueprintType)
enum class EAbyssalTraversalState : uint8
{
    Grounded  UMETA(DisplayName = "Grounded"),
    Climbing  UMETA(DisplayName = "Climbing"),
    Swimming  UMETA(DisplayName = "Swimming"),
    Tethered  UMETA(DisplayName = "Tethered"),
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalTraversalStateChangedSignature, EAbyssalTraversalState, NewState, EAbyssalTraversalState, OldState);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalGravityReorientSignature, FVector, NewGravityDirection, float, LerpDuration);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalTetherChangedSignature, bool, bTethered);

class UCharacterMovementComponent;

/**
 * Traversal-modifier component (roadmap C3) for the explorer character.
 *
 * Owns a small movement-state machine — Grounded / Climbing / Swimming / Tethered —
 * and the systems the harder biomes need:
 *  - Climb: switches CharacterMovement to flying along a surface normal (Glassroot roots, Fossil Sky walls).
 *  - Swim: switches to swimming mode (Inner Sea).
 *  - Tether: stores an anchor point + max length; GetTetherCorrection() returns the
 *    pull-back vector when the owner drifts past TetherLength (Gravity Well low-g).
 *  - Gravity reorientation: AReorientationVolume calls RequestGravityReorientation();
 *    the component re-broadcasts it so the character/Blueprint applies the new
 *    gravity direction (kept out of C++ to stay engine-version-safe).
 *
 * Movement-mode switches use stock CharacterMovement modes; gravity direction is
 * delegated. Transient — not persisted.
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UAbyssalTraversalComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UAbyssalTraversalComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Traversal")
    EAbyssalTraversalState GetTraversalState() const { return State; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Traversal")
    bool IsTethered() const { return State == EAbyssalTraversalState::Tethered; }

    // --- Climb -------------------------------------------------------------

    /** Begin climbing along SurfaceNormal (points out of the climbable surface). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Traversal")
    void BeginClimb(FVector SurfaceNormal);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Traversal")
    void EndClimb();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Traversal")
    FVector GetClimbSurfaceNormal() const { return ClimbSurfaceNormal; }

    // --- Swim --------------------------------------------------------------

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Traversal")
    void SetSwimming(bool bInSwimming);

    // --- Tether ------------------------------------------------------------

    /** Anchor a tether at WorldAnchor; the owner is constrained within TetherLength of it. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Traversal")
    void FireTether(FVector WorldAnchor);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Traversal")
    void ReleaseTether();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Traversal")
    FVector GetTetherAnchor() const { return TetherAnchor; }

    /**
     * If tethered and the owner is beyond TetherLength from the anchor, returns the
     * correction vector that pulls it back onto the tether sphere (zero otherwise).
     * Movement/Blueprint code applies this; keeps the constraint engine-safe.
     */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Traversal")
    FVector GetTetherCorrection() const;

    // --- Gravity reorientation --------------------------------------------

    /** Called by AReorientationVolume. Re-broadcast on OnGravityReorientRequested. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Traversal")
    void RequestGravityReorientation(FVector NewGravityDirection, float LerpDuration);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Traversal")
    FVector GetCurrentGravityDirection() const { return CurrentGravityDirection; }

    // --- Delegates ---------------------------------------------------------

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Traversal")
    FAbyssalTraversalStateChangedSignature OnTraversalStateChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Traversal")
    FAbyssalGravityReorientSignature OnGravityReorientRequested;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Traversal")
    FAbyssalTetherChangedSignature OnTetherChanged;

    /** Max distance (cm) the owner may drift from a fired tether anchor. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Traversal", meta=(ClampMin="0.0"))
    float TetherLength = 800.0f;

protected:
    virtual void BeginPlay() override;

private:
    void SetState(EAbyssalTraversalState NewState);
    UCharacterMovementComponent* GetCharacterMovement() const;

    UPROPERTY()
    EAbyssalTraversalState State = EAbyssalTraversalState::Grounded;

    UPROPERTY()
    FVector ClimbSurfaceNormal = FVector::ZeroVector;

    UPROPERTY()
    FVector TetherAnchor = FVector::ZeroVector;

    UPROPERTY()
    FVector CurrentGravityDirection = FVector(0.0f, 0.0f, -1.0f);
};
