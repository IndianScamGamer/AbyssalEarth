# Editor Guide: WBP_InventoryScreen

Widget Blueprint subclass of `UAbyssalInventoryWidget`. Full-screen inventory grid opened on pause/menu.

## 1. Create

1. `Content/UI/` → **Widget Blueprint**
2. Parent: **AbyssalInventoryWidget**
3. Name: `WBP_InventoryScreen`

## 2. Layout

Full-screen overlay (stretch-fill). Semi-transparent dark background (`0, 0, 0, 0.75`).

Main container: `UUniformGridPanel` or `UWrapBox` named `Grid_Inventory`, centered.

Create a child slot widget:

**WBP_InventorySlot** (separate Widget Blueprint, no parent requirement):
- `UBorder` with item icon background
- `UImage` named `IMG_Icon` (item thumbnail)
- `UTextBlock` named `TB_Count` (stack count, bottom-right corner)
- `UTextBlock` named `TB_Name` (item display name, below icon)
- Variables: `ItemId` (FName), `Count` (int32)
- Exposes a function `SetSlotData(FAbyssalInventorySlot Slot)` that populates the above fields

## 3. Implement BlueprintImplementableEvents

```
Event RefreshInventory (Slots)
  → Clear Children (Grid_Inventory)
  → For Each Slot in Slots:
       → Create Widget (WBP_InventorySlot)
       → Call SetSlotData(Slot)
       → Add Child to Grid_Inventory

Event OnInventoryItemAdded (InventorySlot)
  → Find existing WBP_InventorySlot where ItemId == InventorySlot.ItemId
  → If found: call SetSlotData(InventorySlot) + play pulse scale animation (1→1.2→1, 0.15s)
  → If not found: Create Widget (WBP_InventorySlot) → SetSlotData → Add to Grid

Event OnInventoryItemRemoved (ItemId, RemainingCount)
  → Find slot by ItemId
  → If RemainingCount > 0: call SetSlotData with updated count
  → If RemainingCount == 0: Remove from parent (destroy slot widget)
```

## 4. Open/Close Input

In `BP_AbyssalPlayerController` Event Graph:

```
[Add a new Input Action IA_Inventory (Tab or I key, Digital)]
Bind IA_Inventory ETriggerEvent::Started
  → If InventoryWidget is valid and visible:
       → Remove from Parent → Set InventoryWidget = null → Set Input Mode Game Only
  → Else:
       → Create Widget (WBP_InventoryScreen) → Add to Viewport (Z-Order = 10)
       → Store in variable → Set Input Mode Game And UI → Set Show Mouse Cursor = true
```

## 5. Verify

PIE → press I (or Tab) → inventory screen opens with all current items. Pick up an item in-world → screen updates with pulse animation. Drop/use an item → count decrements or slot disappears.
