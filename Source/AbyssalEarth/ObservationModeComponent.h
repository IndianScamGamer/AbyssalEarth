#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ObservationModeComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalObservationModeChangedSignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalScanCompleteSignature, FName, DiscoveryId);

/**
 * Observation / photo mode component (roadmap D4). Detaches the view from the
 * player pawn and gives a free-roaming camera capped within MaxRoamRadius.
 * While active the component drives a USpringArmComponent-backed camera actor
 * and exposes zoom (FOV), roll, and a scan action that feeds discoveries into
 * UDiscoverySubsystem. Input routing is handled by the owning PlayerController
 * (or Blueprint); this component tracks state and fires delegates.
 *
 * Attach to the player Character. One component per pawn.
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UObservationModeComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UObservationModeComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /** Enter observation mode. Spawns the free camera and disables pawn movement input. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Observation")
    void EnterObservationMode();

    /** Exit observation mode. Destroys the free camera and restores pawn input. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Observation")
    void ExitObservationMode();

    /** Toggle between observation mode and normal play. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Observation")
    void ToggleObservationMode();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Observation")
    bool IsObserving() const { return bIsObserving; }

    /**
     * Move the free camera in world space. Clamped to MaxRoamRadius from the
     * owner's location. Call every frame from the PlayerController while observing.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Observation")
    void MoveCamera(FVector WorldDelta);

    /** Adjust camera pitch and yaw (degrees per call, typically mapped to mouse). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Observation")
    void RotateCamera(float DeltaPitch, float DeltaYaw);

    /** Adjust camera roll in degrees. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Observation")
    void RollCamera(float DeltaRoll);

    /** Adjust field of view (zoom). Clamped to [MinFOV, MaxFOV]. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Observation")
    void AdjustZoom(float DeltaFOV);

    /**
     * Line-trace forward from the observation camera looking for discoverable
     * actors (any actor with a "DiscoveryId" tag or implementing a future
     * IAbyssalDiscoverable interface). Reports the hit to UDiscoverySubsystem.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Observation")
    void ScanForward();

    /** Current camera world location (valid only while observing). */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Observation")
    FVector GetCameraLocation() const;

    /** Current camera world rotation (valid only while observing). */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Observation")
    FRotator GetCameraRotation() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Observation")
    float GetCurrentFOV() const { return CurrentFOV; }

    // Delegates
    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Observation")
    FAbyssalObservationModeChangedSignature OnObservationModeEntered;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Observation")
    FAbyssalObservationModeChangedSignature OnObservationModeExited;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Observation")
    FAbyssalScanCompleteSignature OnScanComplete;

    // Configuration
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Observation", meta=(ClampMin="0.0"))
    float MaxRoamRadius = 1500.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Observation", meta=(ClampMin="10.0", ClampMax="170.0"))
    float MinFOV = 20.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Observation", meta=(ClampMin="10.0", ClampMax="170.0"))
    float MaxFOV = 90.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Observation")
    float DefaultFOV = 70.0f;

    /** Maximum pitch angle in degrees (clamped symmetrically). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Observation", meta=(ClampMin="1.0", ClampMax="89.0"))
    float MaxPitchAngle = 80.0f;

    /** Maximum roll angle in degrees (clamped symmetrically). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Observation", meta=(ClampMin="0.0", ClampMax="180.0"))
    float MaxRollAngle = 45.0f;

    /** Scan ray length in cm. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Observation", meta=(ClampMin="100.0"))
    float ScanDistance = 3000.0f;

protected:
    virtual void BeginPlay() override;
    virtual void EndPlay(EEndPlayReason::Type EndPlayReason) override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Observation")
    void BP_OnEnterObservationMode();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Observation")
    void BP_OnExitObservationMode();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Observation")
    void BP_OnScanHit(AActor* HitActor, FName DiscoveryId);

private:
    void SpawnObservationCamera();
    void DestroyObservationCamera();
    void ClampCameraToRadius();

    UPROPERTY()
    bool bIsObserving = false;

    UPROPERTY()
    float CurrentFOV = 70.0f;

    UPROPERTY()
    FVector CameraLocation = FVector::ZeroVector;

    UPROPERTY()
    FRotator CameraRotation = FRotator::ZeroRotator;

    UPROPERTY()
    TObjectPtr<class ACameraActor> ObservationCamera;

    UPROPERTY()
    FVector OwnerEnterLocation = FVector::ZeroVector;
};
