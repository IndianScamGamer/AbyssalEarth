#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "ScannerComponent.h"
#include "AbyssalScannerReadoutWidget.generated.h"

class ADiscoveryActor;
class UScannerComponent;

UCLASS()
class ABYSSALEARTH_API UAbyssalScannerReadoutWidget : public UUserWidget
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Scanner")
    void SetScannerComponent(UScannerComponent* InScannerComponent);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scanner")
    UScannerComponent* GetBoundScannerComponent() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scanner")
    FAbyssalScanResult GetCurrentScanResult() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scanner")
    FText GetCurrentReadoutText() const;

protected:
    virtual void NativeConstruct() override;
    virtual void NativeDestruct() override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner", meta = (DisplayName = "Scanner Result Changed"))
    void BP_OnScannerResultChanged(const FAbyssalScanResult& ScanResult);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner", meta = (DisplayName = "Scanner Pulse Started"))
    void BP_OnScannerPulseStarted(FVector ScanOrigin, float EffectiveRadius);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner", meta = (DisplayName = "Scanner Discovery Found"))
    void BP_OnScannerDiscoveryFound(ADiscoveryActor* Discovery, bool bNewDiscovery);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner", meta = (DisplayName = "Scanner Missed"))
    void BP_OnScannerMissed();

private:
    UFUNCTION()
    void HandleScannerResultChanged(const FAbyssalScanResult& ScanResult);

    UFUNCTION()
    void HandleScannerPulseStarted(FVector ScanOrigin, float EffectiveRadius);

    UFUNCTION()
    void HandleScannerDiscoveryFound(ADiscoveryActor* Discovery, bool bNewDiscovery);

    UFUNCTION()
    void HandleScannerMissed();

    void BindToScanner(UScannerComponent* InScannerComponent);
    void UnbindFromScanner();

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<UScannerComponent> BoundScannerComponent;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner", meta = (AllowPrivateAccess = "true"))
    FAbyssalScanResult CurrentScanResult;
};
