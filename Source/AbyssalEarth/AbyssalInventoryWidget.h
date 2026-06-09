#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "AbyssalInventoryWidget.generated.h"

USTRUCT(BlueprintType)
struct FAbyssalInventorySlot
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly) FName ItemId;
    UPROPERTY(BlueprintReadOnly) int32 Count = 0;
    UPROPERTY(BlueprintReadOnly) FText DisplayName;
    UPROPERTY(BlueprintReadOnly) FText Description;
};

/**
 * HUD widget base for inventory grid display (roadmap J3).
 * Binds UInventorySubsystem::OnItemAdded/OnItemRemoved in NativeConstruct.
 * Blueprint subclass builds the actual grid from RefreshInventory.
 */
UCLASS(Abstract, Blueprintable)
class ABYSSALEARTH_API UAbyssalInventoryWidget : public UUserWidget
{
    GENERATED_BODY()

protected:
    virtual void NativeConstruct() override;
    virtual void NativeDestruct() override;

    /** Build/rebuild the full inventory grid from scratch. */
    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|HUD")
    void RefreshInventory(const TArray<FAbyssalInventorySlot>& Slots);

    /** Incremental update when an item stack changes. */
    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|HUD")
    void OnInventoryItemAdded(const FAbyssalInventorySlot& Slot);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|HUD")
    void OnInventoryItemRemoved(FName ItemId, int32 RemainingCount);

    /** Resolve display data for any item ID. Queries UAbyssalItemDatabase. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|HUD")
    FAbyssalInventorySlot ResolveSlot(FName ItemId, int32 Count) const;

private:
    UFUNCTION() void HandleItemAdded(FName ItemId, int32 NewCount);
    UFUNCTION() void HandleItemRemoved(FName ItemId, int32 RemainingCount);

    TArray<FAbyssalInventorySlot> BuildAllSlots() const;

    FDelegateHandle AddedHandle;
    FDelegateHandle RemovedHandle;
};
