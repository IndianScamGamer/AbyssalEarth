#pragma once

#include "CoreMinimal.h"
#include "DiscoverySaveGame.h"
#include "ObjectiveSubsystem.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "AbyssalAudioCueSubsystem.generated.h"

class ADiscoveryActor;
class UScannerComponent;

UENUM(BlueprintType)
enum class EAbyssalAudioCueType : uint8
{
    Ambience,
    Scanner,
    Discovery,
    Objective,
    RouteComplete
};

USTRUCT(BlueprintType)
struct FAbyssalAudioCueEvent
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Audio")
    EAbyssalAudioCueType CueType = EAbyssalAudioCueType::Ambience;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Audio")
    FName CueId;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Audio")
    FName RelatedId;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Audio")
    TObjectPtr<UObject> SourceObject = nullptr;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Audio")
    FVector WorldLocation = FVector::ZeroVector;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Audio")
    float Intensity = 1.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Audio")
    FText DisplayText;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalAudioCueRequestedSignature, const FAbyssalAudioCueEvent&, CueEvent);

UCLASS()
class ABYSSALEARTH_API UAbyssalAudioCueSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Audio")
    void RegisterScannerComponent(UScannerComponent* ScannerComponent);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Audio")
    void UnregisterScannerComponent(UScannerComponent* ScannerComponent);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Audio")
    void RequestAmbienceCue(FName CueId, FVector WorldLocation, float Intensity = 1.0f);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Audio")
    void RequestAudioCue(const FAbyssalAudioCueEvent& CueEvent);

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Audio")
    FAbyssalAudioCueRequestedSignature OnAudioCueRequested;

private:
    UFUNCTION()
    void HandleDiscoveryAdded(const FAbyssalDiscoveryEntry& Entry);

    UFUNCTION()
    void HandleObjectiveChanged(const FAbyssalObjectiveStep& Objective);

    UFUNCTION()
    void HandleObjectiveCompleted(FName ObjectiveId);

    UFUNCTION()
    void HandleRouteCompleted();

    UFUNCTION()
    void HandleScannerPulseStarted(FVector ScanOrigin, float EffectiveRadius);

    UFUNCTION()
    void HandleScannerDiscoveryFound(ADiscoveryActor* Discovery, bool bNewDiscovery);

    UFUNCTION()
    void HandleScannerMissed();

    void BindCoreSubsystems(FSubsystemCollectionBase& Collection);
    void UnbindCoreSubsystems();
    void CleanRegisteredScanners();

    UPROPERTY()
    TArray<TObjectPtr<UScannerComponent>> RegisteredScanners;
};
