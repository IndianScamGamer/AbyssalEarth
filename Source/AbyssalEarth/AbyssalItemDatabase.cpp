#include "AbyssalItemDatabase.h"

const FString UAbyssalItemDatabase::ContextString(TEXT("UAbyssalItemDatabase"));

void UAbyssalItemDatabase::SetItemTable(UDataTable* Table)
{
    if (!Table || Table->GetRowStruct() != FAbyssalItemTableRow::StaticStruct())
    {
        UE_LOG(LogTemp, Warning, TEXT("UAbyssalItemDatabase: Rejected table — wrong row struct or null."));
        return;
    }
    ItemTable = Table;
}

bool UAbyssalItemDatabase::GetItemData(FName ItemId, FAbyssalItemTableRow& OutRow) const
{
    if (!ItemTable || ItemId.IsNone())
    {
        return false;
    }
    const FAbyssalItemTableRow* Row = ItemTable->FindRow<FAbyssalItemTableRow>(ItemId, ContextString, false);
    if (!Row)
    {
        return false;
    }
    OutRow = *Row;
    return true;
}

bool UAbyssalItemDatabase::HasItem(FName ItemId) const
{
    if (!ItemTable || ItemId.IsNone())
    {
        return false;
    }
    return ItemTable->FindRow<FAbyssalItemTableRow>(ItemId, ContextString, false) != nullptr;
}

TArray<FName> UAbyssalItemDatabase::GetAllItemIds() const
{
    return ItemTable ? ItemTable->GetRowNames() : TArray<FName>();
}

int32 UAbyssalItemDatabase::GetItemCount() const
{
    return ItemTable ? ItemTable->GetRowNames().Num() : 0;
}
