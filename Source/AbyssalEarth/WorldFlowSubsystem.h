#pragma once

#include "CoreMinimal.h"
#include "AbyssalSaveSubsystem.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "WorldFlowSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalMapTravelSignature, FName, MapId, FName, EntryTag);

/**
 * Manages level transitions for Abyssal Earth.
 *
 * Call TravelToMap(MapId, EntryTag) to move between biomes.
 * The subsystem flushes the active save slot before the level opens, and
 * records LastMapId / LastEntryTag in UAbyssalProfileSaveGame::WorldFlow
 * so the destination level can restore the player at the correct APlayerStart.
 *
 * Map asset names must match the MapId FName exactly (e.g. "GlassrootForest").
 */
UCLASS()
class ABYSSALEARTH_API UWorldFlowSubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    /**
     * Flush the active save slot then open the named map.
     * EntryTag is written to WorldFlow.LastEntryTag before travel;
     * read it from the destination level's BeginPlay via GetLastEntryTag().
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|World Flow",
        meta = (WorldContext = "WorldContextObject"))
    void TravelToMap(UObject* WorldContextObject, FName MapId, FName EntryTag = NAME_None);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|World Flow")
    FName GetLastMapId() const { return LastMapId; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|World Flow")
    FName GetLastEntryTag() const { return LastEntryTag; }

    /** Fires just before the level open call, after the save flush. */
    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|World Flow")
    FAbyssalMapTravelSignature OnPreTravel;

private:
    FName LastMapId;
    FName LastEntryTag;
};
