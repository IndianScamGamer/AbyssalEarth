#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "AbyssalProfileSaveGame.generated.h"

USTRUCT()
struct FAbyssalDiscoveryEntry;  // forward; defined in DiscoverySubsystem.h

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
struct FAbyssalBeaconSaveData;  // forward; defined in BeaconActor.h

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
};

USTRUCT()
struct FAbyssalInventorySaveBlob
{
    GENERATED_BODY()

    UPROPERTY()
    TMap<FName, int32> ItemStacks;
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
    int32 SaveVersion = 1;
};
