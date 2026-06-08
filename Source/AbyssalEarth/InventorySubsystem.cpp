#include "InventorySubsystem.h"
#include "AbyssalItemDefinition.h"
#include "AbyssalProfileSaveGame.h"
#include "Engine/AssetManager.h"

void UInventorySubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    Collection.InitializeDependency(UAbyssalSaveSubsystem::StaticClass());
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->RegisterSaveProvider(this);
    }
}

void UInventorySubsystem::Deinitialize()
{
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->UnregisterSaveProvider(this);
    }
    Super::Deinitialize();
}

void UInventorySubsystem::OnSaveRequested(UAbyssalProfileSaveGame* SaveGame)
{
    SaveGame->Inventory.ItemStacks = ItemStacks;
}

void UInventorySubsystem::OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame)
{
    ItemStacks.Reset();
    for (const TPair<FName, int32>& Pair : SaveGame->Inventory.ItemStacks)
    {
        if (!Pair.Key.IsNone() && Pair.Value > 0)
        {
            ItemStacks.Add(Pair.Key, Pair.Value);
        }
    }
}

int32 UInventorySubsystem::AddItem(FName ItemId, int32 Count)
{
    if (ItemId.IsNone() || Count <= 0)
    {
        return 0;
    }

    const int32 MaxStack = GetMaxStack(ItemId);
    const int32 Current = ItemStacks.FindRef(ItemId);
    const int32 Available = FMath::Max(0, MaxStack - Current);
    const int32 ToAdd = FMath::Min(Count, Available);

    if (ToAdd <= 0)
    {
        return 0;
    }

    ItemStacks.FindOrAdd(ItemId) += ToAdd;
    OnItemAdded.Broadcast(ItemId, ItemStacks[ItemId]);
    return ToAdd;
}

bool UInventorySubsystem::RemoveItem(FName ItemId, int32 Count)
{
    if (ItemId.IsNone() || Count <= 0)
    {
        return false;
    }

    const int32 Current = ItemStacks.FindRef(ItemId);
    if (Current < Count)
    {
        return false;
    }

    const int32 Remaining = Current - Count;
    if (Remaining == 0)
    {
        ItemStacks.Remove(ItemId);
    }
    else
    {
        ItemStacks[ItemId] = Remaining;
    }

    OnItemRemoved.Broadcast(ItemId, Remaining);
    return true;
}

bool UInventorySubsystem::HasItem(FName ItemId, int32 Count) const
{
    return GetItemCount(ItemId) >= Count;
}

int32 UInventorySubsystem::GetItemCount(FName ItemId) const
{
    return ItemStacks.FindRef(ItemId);
}

TArray<FName> UInventorySubsystem::GetAllItemIds() const
{
    TArray<FName> Keys;
    ItemStacks.GetKeys(Keys);
    return Keys;
}

void UInventorySubsystem::ClearInventory()
{
    ItemStacks.Reset();
}

int32 UInventorySubsystem::GetMaxStack(FName ItemId) const
{
    // Synchronous lookup: works for definitions loaded by a hard reference in the current level.
    if (UAssetManager* AM = UAssetManager::GetIfInitialized())
    {
        const FPrimaryAssetId AssetId(TEXT("AbyssalItem"), ItemId);
        if (UAbyssalItemDefinition* Def = Cast<UAbyssalItemDefinition>(AM->GetPrimaryAssetObject(AssetId)))
        {
            return FMath::Max(1, Def->MaxStackSize);
        }
    }
    return DefaultMaxStackSize;
}
