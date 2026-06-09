#include "AbyssalInventoryWidget.h"
#include "InventorySubsystem.h"
#include "AbyssalItemDatabase.h"
#include "AbyssalItemTableRow.h"

void UAbyssalInventoryWidget::NativeConstruct()
{
    Super::NativeConstruct();

    UGameInstance* GI = GetGameInstance();
    if (!GI)
    {
        return;
    }

    if (UInventorySubsystem* InvSub = GI->GetSubsystem<UInventorySubsystem>())
    {
        AddedHandle   = InvSub->OnItemAdded.AddUObject(this,   &UAbyssalInventoryWidget::HandleItemAdded);
        RemovedHandle = InvSub->OnItemRemoved.AddUObject(this, &UAbyssalInventoryWidget::HandleItemRemoved);
        RefreshInventory(BuildAllSlots());
    }
}

void UAbyssalInventoryWidget::NativeDestruct()
{
    if (UGameInstance* GI = GetGameInstance())
    {
        if (UInventorySubsystem* InvSub = GI->GetSubsystem<UInventorySubsystem>())
        {
            InvSub->OnItemAdded.Remove(AddedHandle);
            InvSub->OnItemRemoved.Remove(RemovedHandle);
        }
    }
    Super::NativeDestruct();
}

FAbyssalInventorySlot UAbyssalInventoryWidget::ResolveSlot(FName ItemId, int32 Count) const
{
    FAbyssalInventorySlot Slot;
    Slot.ItemId = ItemId;
    Slot.Count  = Count;

    UGameInstance* GI = GetGameInstance();
    if (!GI)
    {
        return Slot;
    }

    if (UAbyssalItemDatabase* DB = GI->GetSubsystem<UAbyssalItemDatabase>())
    {
        FAbyssalItemTableRow Row;
        if (DB->GetItemData(ItemId, Row))
        {
            Slot.DisplayName = Row.DisplayName;
            Slot.Description = Row.Description;
        }
    }
    return Slot;
}

void UAbyssalInventoryWidget::HandleItemAdded(FName ItemId, int32 NewCount)
{
    OnInventoryItemAdded(ResolveSlot(ItemId, NewCount));
}

void UAbyssalInventoryWidget::HandleItemRemoved(FName ItemId, int32 RemainingCount)
{
    OnInventoryItemRemoved(ItemId, RemainingCount);
}

TArray<FAbyssalInventorySlot> UAbyssalInventoryWidget::BuildAllSlots() const
{
    TArray<FAbyssalInventorySlot> Slots;
    UGameInstance* GI = GetGameInstance();
    if (!GI)
    {
        return Slots;
    }

    UInventorySubsystem* InvSub = GI->GetSubsystem<UInventorySubsystem>();
    if (!InvSub)
    {
        return Slots;
    }

    for (const FName& ItemId : InvSub->GetAllItemIds())
    {
        const int32 Count = InvSub->GetItemCount(ItemId);
        if (Count > 0)
        {
            Slots.Add(ResolveSlot(ItemId, Count));
        }
    }
    return Slots;
}
