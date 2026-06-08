#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "DiscoveryActor.generated.h"

UENUM(BlueprintType)
enum class EDiscoveryCategory : uint8
{
    Geology,
    Biology,
    Anomaly,
    HumanMade,
    // Appended after HumanMade so existing serialized values keep their indices.
    Structure,
    AlienTech
};

UCLASS()
class ABYSSALEARTH_API ADiscoveryActor : public AActor
{
    GENERATED_BODY()

public:
    ADiscoveryActor();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    bool RegisterScan();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    FVector GetScanFocusLocation() const;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Discovery")
    void OnScanned(bool bWasAlreadyDiscovered);

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Discovery")
    FName DiscoveryId;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Discovery")
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Discovery", meta=(MultiLine=true))
    FText JournalText;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Discovery")
    EDiscoveryCategory Category = EDiscoveryCategory::Geology;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Discovery")
    FVector ScanFocusOffset = FVector::ZeroVector;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    FName ObjectiveIdToCompleteOnScan;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    bool bCompleteObjectiveOnlyOnNewDiscovery = true;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Discovery")
    bool bDiscovered = false;
};
