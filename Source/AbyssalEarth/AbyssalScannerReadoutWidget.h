#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "AbyssalScannerReadoutWidget.generated.h"

class UAbyssalScanComponent;

/** Snapshot of the most recent scan pulse result for HUD display. */
USTRUCT(BlueprintType)
struct FAbyssalScanReadout
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    bool bHasSignal = false;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    FName DiscoveryId;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    FText DisplayName;

    /** Distance from the scanning pawn to the hit actor, in cm. */
    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    float Distance = 0.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    FVector FocusLocation = FVector::ZeroVector;
};

/**
 * UMG base for WBP_ScannerReadout. Auto-binds to the owning pawn's
 * UAbyssalScanComponent on construct and forwards pulse/hit/miss events
 * to Blueprint, caching the last hit for GetCurrentReadoutText.
 */
UCLASS()
class ABYSSALEARTH_API UAbyssalScannerReadoutWidget : public UUserWidget
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Scanner")
    void SetScanComponent(UAbyssalScanComponent* InScanComponent);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scanner")
    UAbyssalScanComponent* GetBoundScanComponent() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scanner")
    FAbyssalScanReadout GetCurrentScanReadout() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scanner")
    FText GetCurrentReadoutText() const;

protected:
    virtual void NativeConstruct() override;
    virtual void NativeDestruct() override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner", meta = (DisplayName = "Scanner Readout Changed"))
    void BP_OnScannerReadoutChanged(const FAbyssalScanReadout& Readout);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner", meta = (DisplayName = "Scanner Pulse Started"))
    void BP_OnScannerPulseStarted();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner", meta = (DisplayName = "Scanner Hit"))
    void BP_OnScannerHit(AActor* ScannedActor, FName DiscoveryId);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner", meta = (DisplayName = "Scanner Missed"))
    void BP_OnScannerMissed();

private:
    UFUNCTION()
    void HandleScanPulseFired();

    UFUNCTION()
    void HandleScanHit(AActor* ScannedActor, FName DiscoveryId);

    UFUNCTION()
    void HandleScanMissed();

    void BindToScanner(UAbyssalScanComponent* InScanComponent);
    void UnbindFromScanner();

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<UAbyssalScanComponent> BoundScanComponent;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner", meta = (AllowPrivateAccess = "true"))
    FAbyssalScanReadout CurrentReadout;
};
