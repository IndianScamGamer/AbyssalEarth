# Editor Guides — Build Order

Step-by-step in-editor instructions for standing up the playable
Prologue→Act 1 slice. Work through them in this order; each guide assumes
the ones above it are done.

| # | Guide | What it produces | Blocks |
|---|---|---|---|
| 1 | [BP_AbyssalGameMode.md](BP_AbyssalGameMode.md) | Game mode wired to the new pawn/controller | Everything |
| 2 | [BP_PlayerCharacter.md](BP_PlayerCharacter.md) | Playable pawn (camera, mesh, death wiring) | 3–8 |
| 3 | [BP_AbyssalPlayerController.md](BP_AbyssalPlayerController.md) | Input mapping context + action assets | 4–8 |
| 4 | [WBP_VitalsHUD.md](WBP_VitalsHUD.md) | Health/oxygen/stamina/temp/pressure HUD | — |
| 5 | [WBP_ObjectiveTracker.md](WBP_ObjectiveTracker.md) | Objective display + completion animations | — |
| 6 | [WBP_InventoryScreen.md](WBP_InventoryScreen.md) | Inventory grid overlay | — |
| 7 | [WBP_SecondaryWidgets.md](WBP_SecondaryWidgets.md) | Journal + narrative captions (optional for slice) | — |
| 8 | [PrologueLevel_Blockout.md](PrologueLevel_Blockout.md) | PRO_001 submarine interior level | 9 |
| 9 | [Act1Level_Blockout.md](Act1Level_Blockout.md) | A1_001 thermal vent field level | — |

## Debug commands

Available in PIE via the `~` console (exec functions on
`AAbyssalPlayerController`):

| Command | Effect |
|---|---|
| `AbyssalCompleteObjective` | Complete the current objective |
| `AbyssalGiveItem <ItemId> [Count]` | Add items (IDs in `Content/Design/DT_ItemDatabase.csv`) |
| `AbyssalKill` | Kill the pawn — exercises death → checkpoint respawn |
| `AbyssalSave` / `AbyssalLoad` | Flush / reload the active profile slot |

## Verifying the slice end-to-end

After guide 9, run the PIE checklist at the end of each blockout guide, then:
1. `AbyssalKill` → confirm respawn at the last checkpoint with refilled vitals
2. `AbyssalGiveItem ITEM_MINERAL_ABYSSAL_CORE 5` → craft at the fabricator
3. Quit PIE, re-enter → confirm checkpoint, inventory, and objective restore
   (profile auto-loads in `AAbyssalGameMode::BeginPlay`)
