#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "DiscoverySaveGame.generated.h"

USTRUCT(BlueprintType)
struct FAbyssalBeaconSaveData
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category = "Abyssal Earth|Save")
    FGuid BeaconId;

    UPROPERTY(BlueprintReadWrite, Category = "Abyssal Earth|Save")
    FTransform Transform = FTransform::Identity;

    UPROPERTY(BlueprintReadWrite, Category = "Abyssal Earth|Save")
    FLinearColor LightColor = FLinearColor(0.2f, 0.85f, 1.0f);
};

UCLASS()
class ABYSSALEARTH_API UDiscoverySaveGame : public USaveGame
{
    GENERATED_BODY()

public:
    UPROPERTY(BlueprintReadWrite, Category = "Abyssal Earth|Save")
    TArray<FName> DiscoveredIds;

    UPROPERTY(BlueprintReadWrite, Category = "Abyssal Earth|Save")
    TArray<FAbyssalBeaconSaveData> SavedBeacons;
};
