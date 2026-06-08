#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "AbyssalProfileSaveGame.generated.h"

// ---------------------------------------------------------------------------
// Discovery domain blob (migrated from UDiscoverySaveGame)
// ---------------------------------------------------------------------------

USTRUCT()
struct FAbyssalDiscoveryEntry;  // forward; defined in DiscoverySubsystem.h

USTRUCT()
struct FAbyssalDiscoverySaveBlob
{
    GENERATED_BODY()

    /** All scanned entries, keyed by discovery id. */
    UPROPERTY()
    TMap<FName, FAbyssalDiscoveryEntry> DiscoveredEntries;

    /** Legacy flat id list for back-compat with saves from UDiscoverySaveGame. */
    UPROPERTY()
    TArray<FName> DiscoveredIds_Legacy;
};

// ---------------------------------------------------------------------------
// Beacon domain blob (migrated from UDiscoverySaveGame / UBeaconSubsystem)
// ---------------------------------------------------------------------------

USTRUCT()
struct FAbyssalBeaconSaveData;  // forward; defined in BeaconActor.h

USTRUCT()
struct FAbyssalBeaconSaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    TArray<FAbyssalBeaconSaveData> SavedBeacons;
};

// ---------------------------------------------------------------------------
// Objective domain blob
// ---------------------------------------------------------------------------

USTRUCT()
struct FAbyssalObjectiveSaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    int32 CurrentObjectiveIndex = 0;

    UPROPERTY()
    TArray<FName> CompletedObjectiveIds;
};

// ---------------------------------------------------------------------------
// World-flow domain blob (which map, which entry tag)
// ---------------------------------------------------------------------------

USTRUCT()
struct FAbyssalWorldFlowSaveBlob
{
    GENERATED_BODY()

    /** The map asset name last successfully entered (empty = Luminous Rift default). */
    UPROPERTY()
    FName LastMapId;

    /** Player entry tag within that map (empty = default entry). */
    UPROPERTY()
    FName LastEntryTag;
};

// ---------------------------------------------------------------------------
// Inventory domain blob (stub — populated when B1 is authored)
// ---------------------------------------------------------------------------

USTRUCT()
struct FAbyssalInventorySaveBlob
{
    GENERATED_BODY()

    /** Item id → stack count. */
    UPROPERTY()
    TMap<FName, int32> ItemStacks;
};

// ---------------------------------------------------------------------------
// Root save game object
// ---------------------------------------------------------------------------

/**
 * The single save-game object owned by UAbyssalSaveSubsystem.
 *
 * Each gameplay domain owns a nested blob struct.  Domain subsystems access
 * their blob via IAbyssalSaveProvider::OnSaveRequested / OnLoadCompleted.
 * Adding a new domain means adding a new blob here and implementing the
 * IAbyssalSaveProvider interface on the domain subsystem.
 *
 * Slot name format: "AbyssalProfile_<SlotIndex>" (see UAbyssalSaveSubsystem).
 * UserIndex is always 0 (single-player, local save).
 */
UCLASS()
class ABYSSALEARTH_API UAbyssalProfileSaveGame : public USaveGame
{
    GENERATED_BODY()

public:
    UPROPERTY()
    FAbyssalDiscoverySaveBlob Discoveries;

    UPROPERTY()
    FAbyssalBeaconSaveBlob Beacons;

    UPROPERTY()
    FAbyssalObjectiveSaveBlob Objectives;

    UPROPERTY()
    FAbyssalWorldFlowSaveBlob WorldFlow;

    UPROPERTY()
    FAbyssalInventorySaveBlob Inventory;

    /** Profile schema version — bump when structs change incompatibly. */
    UPROPERTY()
    int32 SaveVersion = 1;
};
