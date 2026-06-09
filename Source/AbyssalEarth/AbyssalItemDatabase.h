#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Engine/DataTable.h"
#include "AbyssalItemTableRow.h"
#include "AbyssalItemDatabase.generated.h"

/**
 * DataTable-backed item registry (roadmap H4). Provides a game-instance
 * subsystem lookup so any system can resolve item metadata by FName without
 * a direct DataTable reference. Load the DataTable in Project Settings
 * (Subsystem config) or call SetItemTable at startup from the GameMode.
 *
 * Fallback used by UInventorySubsystem when AssetManager returns no
 * UAbyssalItemDefinition for a given ItemId.
 */
UCLASS()
class ABYSSALEARTH_API UAbyssalItemDatabase : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    /** Set the source DataTable (call once from GameMode or level blueprint). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Items")
    void SetItemTable(UDataTable* Table);

    /**
     * Look up item metadata by row name. Returns false if the ID is not found.
     * Out parameter Row is valid only when the function returns true.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Items")
    bool GetItemData(FName ItemId, FAbyssalItemTableRow& OutRow) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Items")
    bool HasItem(FName ItemId) const;

    /** All registered item IDs in table order. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Items")
    TArray<FName> GetAllItemIds() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Items")
    int32 GetItemCount() const;

private:
    UPROPERTY()
    TObjectPtr<UDataTable> ItemTable;

    static const FString ContextString;
};
