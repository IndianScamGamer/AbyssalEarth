#pragma once

#include "CoreMinimal.h"
#include "AbyssalSaveSubsystem.h"
#include "DiscoverySaveGame.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "BeaconSubsystem.generated.h"

class ABeaconActor;

UCLASS()
class ABYSSALEARTH_API UBeaconSubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    void RegisterBeacon(ABeaconActor* Beacon);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    bool RemoveBeacon(ABeaconActor* Beacon);

    /**
     * Update the saved color of an already-registered beacon. Unlike
     * RegisterBeacon this never adds a new entry, so cosmetic color changes
     * on unplaced/preview beacons don't get persisted.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    bool UpdateBeaconColor(ABeaconActor* Beacon);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon", meta=(WorldContext="WorldContextObject"))
    bool RemoveBeaconById(UObject* WorldContextObject, FGuid BeaconId);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon", meta=(WorldContext="WorldContextObject"))
    int32 RestoreSavedBeacons(UObject* WorldContextObject, TSubclassOf<ABeaconActor> BeaconClass);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Beacon")
    TArray<FAbyssalBeaconSaveData> GetSavedBeacons() const;

    /** Routes through UAbyssalSaveSubsystem::SaveActiveSlot. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    void SaveBeacons();

    /** No-op: load is driven by UAbyssalSaveSubsystem::LoadSlot. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    void LoadBeacons();

private:
    UPROPERTY()
    TArray<FAbyssalBeaconSaveData> SavedBeacons;

    UPROPERTY()
    TSet<FGuid> RestoredBeaconIds;

    int32 FindBeaconIndex(FGuid BeaconId) const;
};
