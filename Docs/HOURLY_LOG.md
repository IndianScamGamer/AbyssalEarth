# Hourly Work Log

## 2026-06-08 (tick 6)

- **B2 — Fabrication system** (`Source/AbyssalEarth/AbyssalRecipeDefinition.h`, `FabricationSubsystem.h/.cpp`, `FabricatorStation.h/.cpp`, `AbyssalProfileSaveGame.h`, `Content/Design/FabricationRecipes.csv`):
  - `UAbyssalRecipeDefinition`: `UPrimaryDataAsset` with `RecipeId`, `Inputs` (`TArray<FAbyssalRecipeIngredient>`), `OutputItemId`/`OutputCount`, `bRequiresUnlock`, `RequiredStationTier`. Primary asset type `AbyssalRecipe`.
  - `UFabricationSubsystem`: `IAbyssalSaveProvider`. `RegisterRecipe` (auto-unlocks non-gated recipes), `UnlockRecipe`, `IsRecipeUnlocked`, `CanCraft` (returns `EAbyssalCraftResult`: Success / MissingIngredients / Locked / StationTierTooLow / InvalidRecipe), `Craft` (consumes inputs + adds output via `UInventorySubsystem`). Unlocked recipe IDs persist through new `Fabrication` save blob.
  - `AFabricatorStation`: `IAbyssalInteractable` actor; `AvailableRecipes` + `StationTier`; on interact registers recipes with the subsystem and fires `BP_OnFabricatorActivated`; `CraftAtStation` convenience.
  - `AbyssalProfileSaveGame.h`: added `FAbyssalFabricationSaveBlob` (`UnlockedRecipeIds`).
  - `FabricationRecipes.csv`: 5 design recipes (patch kit, lumen cell, thermal wrap, grav tether tool, relay key) spanning station tiers 1–3 and unlock gating.
- **Verification:** `python3 Scripts/validate_design_data.py` passes. Windows compile/PIE pending.
- Roadmap checklist updated: B2 `[x]`.
- Next priority: **B3** (oxygen/stamina vitals) or **C3** (traversal modifiers: `AReorientationVolume`, tether tool) or **D1** (narrative triggers).

## 2026-06-08 (tick 5)

- **A2 — Data-driven objectives + persistence** (`Source/AbyssalEarth/ObjectiveSubsystem.h/.cpp`, `Content/Design/DT_MainObjectiveArc.csv`):
  - `FAbyssalObjectiveTableRow : FTableRowBase`; `BuildRouteFromTable(UDataTable*)` loads steps in table order.
  - `UObjectiveSubsystem` implements `IAbyssalSaveProvider`: persists `CurrentObjectiveIndex` + `CompletedObjectiveIds`, clamps stale index on route change.
  - Hardcoded `BuildDefaultRoute` retained as fallback.
- Roadmap checklist updated: A2 `[x]`.

## 2026-06-08 (tick 4)

- **B1 — Inventory system**: `UAbyssalItemDefinition` (PrimaryDataAsset), `UInventorySubsystem` (`IAbyssalSaveProvider`, stack-capped), `AHarvestableNode` (`IAbyssalInteractable`).
- **C1 — World flow**: `UWorldFlowSubsystem` (`IAbyssalSaveProvider`, `TravelToMap` save+entry-tag).
- Roadmap checklist updated: B1 `[x]`, C1 `[x]`.

## 2026-06-08 (tick 3)

- **A1 — Provider migration**: `UDiscoverySubsystem` + `UBeaconSubsystem` implement `IAbyssalSaveProvider`; direct `UGameplayStatics::SaveGameToSlot` calls removed.
- **C4 — Mantle Garden blockout** (`Docs/Maps/MANTLE_GARDEN.md`): final map (Map 06, Act 4). 7 zones, 11 discoveries, 5 objectives, 7 checkpoints.
- Roadmap: A1 `[x]`, C4 `[x]`.

## 2026-06-08 (tick 2)

- **C4 — Gravity Well blockout** (`Docs/Maps/GRAVITY_WELL.md`): Map 05 (Act 3). 7 zones, 10 discoveries, 5 objectives, 7 checkpoints.
- **A1 — `UAbyssalSaveSubsystem` + `UAbyssalProfileSaveGame`**: interface + slot management + 5 domain blobs.
- Roadmap: A1 `[~]`, C4 `[~]`.

## 2026-06-08 (tick 1 / session resumed)

- PR #1 merged to main (squash `383ce0c`).
- **C2 — `AAbyssalHazardBase`**: phase machine + Radial/Overlap/None damage modes, BP hooks, overlap tracking.
- **C4 — Fossil Sky blockout** (`Docs/Maps/FOSSIL_SKY.md`): Map 04 (Act 2). Brittle walkways, Dating Chamber, 11 discoveries.

## 2026-06-07 14:34 EDT

- Added `AHeatZoneVolume` — box trigger calling `SetInHeatZone` on `UTemperatureComponent`.

## 2026-06-07 14:07 EDT

- Added `UTemperatureComponent`: heat-exposure vital, `Insulation` scaling, overheat damage.

## 2026-06-07 13:40 EDT

- Completed world-map concept review: all six world plates reviewed.

## 2026-06-07 13:12 EDT

- Wrote `Docs/Maps/INNER_SEA.md` (Map 03 blockout).

## 2026-06-07 12:45 EDT

- Concept art review: 3 canonical plates. Notes in `Docs/CONCEPT_ART_REVIEW.md`.

## 2026-06-07 12:18 EDT

- Added `IAbyssalInteractable` UINTERFACE + `UInteractionComponent` (A3).

## 2026-06-07 11:52 EDT

- Wrote `Docs/Maps/GLASSROOT_FOREST.md` (Map 02 blockout).

## 2026-06-07 11:18 EDT

- Scope expanded. Full backend gap analysis. Added `Docs/BACKEND_SYSTEMS_ROADMAP.md`.

## 2026-06-07 10:31 EDT

- Fixed `EDiscoveryCategory` drift: added `Structure` + `AlienTech`. Added `validate_discovery_categories` guard.

## Earlier entries (2026-05-18 — 2026-05-27)

See git log for full history of initial project setup, Luminous Rift slice, asset pipeline, save/health/audio systems, and design data validation.
