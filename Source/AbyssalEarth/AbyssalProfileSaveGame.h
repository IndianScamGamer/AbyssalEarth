#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "DiscoverySaveGame.h"
#include "AbyssalProfileSaveGame.generated.h"

USTRUCT()
struct FAbyssalDiscoverySaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    TMap<FName, FAbyssalDiscoveryEntry> DiscoveredEntries;

    UPROPERTY()
    TArray<FName> DiscoveredIds_Legacy;
};

USTRUCT()
struct FAbyssalBeaconSaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    TArray<FAbyssalBeaconSaveData> SavedBeacons;
};

USTRUCT()
struct FAbyssalObjectiveSaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    int32 CurrentObjectiveIndex = 0;

    UPROPERTY()
    TArray<FName> CompletedObjectiveIds;
};

USTRUCT()
struct FAbyssalWorldFlowSaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    FName LastMapId;

    UPROPERTY()
    FName LastEntryTag;

    UPROPERTY()
    FName ActiveCheckpointId;
};

USTRUCT()
struct FAbyssalInventorySaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    TMap<FName, int32> ItemStacks;

    UPROPERTY()
    TArray<FName> InstalledUpgradeIds;
};

USTRUCT()
struct FAbyssalFabricationSaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    TArray<FName> UnlockedRecipeIds;
};

USTRUCT()
struct FAbyssalNarrativeSaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    TArray<FName> PlayedBeatIds;
};

/**
 * Root save-game object owned by UAbyssalSaveSubsystem.
 * Each gameplay domain owns a nested blob struct; domain subsystems access
 * their blob via IAbyssalSaveProvider callbacks.
 * Slot name: "AbyssalProfile_<N>", UserIndex 0.
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

    UPROPERTY()
    FAbyssalFabricationSaveBlob Fabrication;

    UPROPERTY()
    FAbyssalNarrativeSaveBlob Narrative;

    UPROPERTY()
    int32 SaveVersion = 1;
};
