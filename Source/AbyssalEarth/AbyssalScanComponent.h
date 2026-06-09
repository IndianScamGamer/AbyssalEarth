#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "AbyssalScanComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalScanPulseSignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalScanHitSignature, AActor*, ScannedActor, FName, DiscoveryId);

/**
 * Player scanner component (roadmap L1). Emits a sphere-overlap pulse
 * looking for actors that implement IAbyssalScannable within ScanRadius.
 * Discovered IDs are registered with UDiscoverySubsystem. A cooldown
 * prevents pulse spam. Attach to AAbyssalPlayerCharacter.
 *
 * UObservationModeComponent provides a precision line-trace variant;
 * this component is the ambient area scanner for the main game loop.
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UAbyssalScanComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UAbyssalScanComponent();

    /**
     * Fire a scan pulse. Returns false if on cooldown.
     * Registers all IAbyssalScannable actors within ScanRadius with
     * UDiscoverySubsystem and fires OnScanHit for each new discovery.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Scan")
    bool ScanPulse();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scan")
    bool IsOnCooldown() const { return CooldownRemaining > 0.0f; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scan")
    float GetCooldownRemaining() const { return CooldownRemaining; }

    /** 0..1 fraction of cooldown elapsed (0 = fresh, 1 = ready). */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scan")
    float GetCooldownPercent() const;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Scan")
    FAbyssalScanPulseSignature OnScanPulseFired;

    /** Fires for each new (previously undiscovered) actor hit by the scan. */
    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Scan")
    FAbyssalScanHitSignature OnScanHit;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Scan")
    FAbyssalScanPulseSignature OnScanCooldownComplete;

    /** Sphere radius of the scan pulse in cm. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Scan", meta=(ClampMin="10.0"))
    float ScanRadius = 800.0f;

    /** Seconds between scan pulses. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Scan", meta=(ClampMin="0.5"))
    float CooldownDuration = 3.0f;

    /** If true, already-discovered actors still fire OnScanHit (for scan-mode feedback). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Scan")
    bool bRescanKnownActors = false;

protected:
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
    float CooldownRemaining = 0.0f;
};
