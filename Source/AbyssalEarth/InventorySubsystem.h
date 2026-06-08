#pragma once

#include "CoreMinimal.h"
#include "AbyssalSaveSubsystem.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "InventorySubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalItemChangedSignature, FName, ItemId, int32, NewCount);

UCLASS()
class ABYSSALEARTH_API UInventorySubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    /**
     * Add Count units of ItemId into the inventory.
     * Returns the number actually added (may be capped by MaxStackSize).
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Inventory")
    int32 AddItem(FName ItemId, int32 Count = 1);

    /**
     * Remove Count units of ItemId. Returns false if fewer than Count exist.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Inventory")
    bool RemoveItem(FName ItemId, int32 Count = 1);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Inventory")
    bool HasItem(FName ItemId, int32 Count = 1) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Inventory")
    int32 GetItemCount(FName ItemId) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Inventory")
    TArray<FName> GetAllItemIds() const;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Inventory")
    void ClearInventory();

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Inventory")
    FAbyssalItemChangedSignature OnItemAdded;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Inventory")
    FAbyssalItemChangedSignature OnItemRemoved;

    /** Fallback stack limit used when no UAbyssalItemDefinition is loaded for an item. */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Abyssal Earth|Inventory")
    int32 DefaultMaxStackSize = 99;

private:
    UPROPERTY()
    TMap<FName, int32> ItemStacks;

    int32 GetMaxStack(FName ItemId) const;
};
