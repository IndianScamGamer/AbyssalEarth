#pragma once

#include "CoreMinimal.h"
#include "DiscoverySaveGame.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "BeaconSubsystem.generated.h"

class ABeaconActor;

UCLASS()
class ABYSSALEARTH_API UBeaconSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    void RegisterBeacon(ABeaconActor* Beacon);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon", meta=(WorldContext="WorldContextObject"))
    int32 RestoreSavedBeacons(UObject* WorldContextObject, TSubclassOf<ABeaconActor> BeaconClass);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Beacon")
    TArray<FAbyssalBeaconSaveData> GetSavedBeacons() const;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    void SaveBeacons();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    void LoadBeacons();

private:
    UPROPERTY()
    TArray<FAbyssalBeaconSaveData> SavedBeacons;

    UPROPERTY()
    TSet<FGuid> RestoredBeaconIds;

    UPROPERTY()
    FString SaveSlotName = TEXT("AbyssalEarth_Discoveries");

    UPROPERTY()
    int32 SaveUserIndex = 0;

    int32 FindBeaconIndex(FGuid BeaconId) const;
};
