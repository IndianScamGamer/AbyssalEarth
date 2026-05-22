#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "DiscoveryActor.h"
#include "Engine/EngineTypes.h"
#include "ScannerComponent.generated.h"

USTRUCT(BlueprintType)
struct FAbyssalScanResult
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    bool bHasDiscovery = false;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    bool bNewDiscovery = false;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    TObjectPtr<ADiscoveryActor> Discovery = nullptr;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    FName DiscoveryId;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    FText DisplayName;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    EDiscoveryCategory Category = EDiscoveryCategory::Geology;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    float Distance = 0.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    FVector FocusLocation = FVector::ZeroVector;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalScanPulseStartedSignature, FVector, ScanOrigin, float, EffectiveRadius);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalScanDiscoveryFoundSignature, ADiscoveryActor*, Discovery, bool, bNewDiscovery);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalScanMissedSignature);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalScanResultChangedSignature, const FAbyssalScanResult&, ScanResult);

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UScannerComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UScannerComponent();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Scanner")
    void Scan();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scanner")
    FAbyssalScanResult GetLastScanResult() const;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner")
    void OnScanPulseStarted(FVector ScanOrigin, float EffectiveRadius);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner")
    void OnScanDiscoveryFound(ADiscoveryActor* Discovery, bool bNewDiscovery);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Scanner")
    void OnScanMissed();

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Scanner")
    FAbyssalScanPulseStartedSignature OnScanPulseStartedEvent;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Scanner")
    FAbyssalScanDiscoveryFoundSignature OnScanDiscoveryFoundEvent;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Scanner")
    FAbyssalScanMissedSignature OnScanMissedEvent;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Scanner")
    FAbyssalScanResultChangedSignature OnScanResultChanged;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Scanner")
    float ScanRadius = 1800.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Scanner")
    float ForwardBonusDistance = 900.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Scanner")
    bool bRequireLineOfSight = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Scanner")
    TEnumAsByte<ECollisionChannel> LineOfSightTraceChannel = ECC_Visibility;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    TObjectPtr<ADiscoveryActor> LastDiscovery;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Scanner")
    FAbyssalScanResult LastScanResult;

private:
    bool HasLineOfSightToDiscovery(const AActor* Owner, const FVector& ScanOrigin, const ADiscoveryActor* Discovery) const;
};
