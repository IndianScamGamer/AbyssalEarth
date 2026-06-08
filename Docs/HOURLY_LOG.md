# Hourly Work Log

## 2026-06-08 (tick 7)

- **B3 — Oxygen + stamina vitals** (`Source/AbyssalEarth/OxygenComponent.h/.cpp`, `StaminaComponent.h/.cpp`):
  - `UOxygenComponent`: oxygen (0..1) drains while `bSubmerged`, refills while breathing; suffocation damage at zero via engine damage path (`UGameplayStatics::ApplyDamage` → `UAbyssalHealthComponent`), mirroring `UTemperatureComponent`. `SetSubmerged`, `RefillOxygen`, `OnOxygenChanged`/`OnSuffocationBegan`/`OnSuffocationEnded`. `AirCapacityBonus` foreshadows rebreather upgrades (halves drain at 1.0). Map use: Inner Sea.
  - `UStaminaComponent`: stamina (0..1) drains while `bExerting`, regenerates after `RegenDelay` once exertion stops. Exhaustion gate: `CanExert()` false until stamina climbs past `ExhaustionRecoveryThreshold`. `TryConsumeStamina(Cost)` for discrete actions (dodge/climb-jump). `OnStaminaChanged`/`OnExhausted`/`OnRecovered`. No damage path — gates traversal only.
  - Both transient (reset on load), like health — not persisted.
- **Verification:** `python3 Scripts/validate_design_data.py` passes. Windows compile/PIE pending (drive `SetSubmerged` from water volumes, `SetExerting` from sprint input; wire HUD gauges).
- Roadmap checklist updated: B3 `[x]`. **All of Phases A and B (except A3 character wiring) now complete.**
- Next priority: **C3** (traversal modifiers: `AReorientationVolume`, climb/swim states, tether tool — unblocks Gravity Well) or **D1** (narrative triggers).

## 2026-06-08 (tick 6)

- **B2 — Fabrication system** (`AbyssalRecipeDefinition.h`, `FabricationSubsystem.h/.cpp`, `FabricatorStation.h/.cpp`, `AbyssalProfileSaveGame.h`, `Content/Design/FabricationRecipes.csv`):
  - `UAbyssalRecipeDefinition` (PrimaryDataAsset): inputs/output, `bRequiresUnlock`, `RequiredStationTier`.
  - `UFabricationSubsystem` (`IAbyssalSaveProvider`): `RegisterRecipe`/`UnlockRecipe`/`CanCraft`/`Craft` (`EAbyssalCraftResult`); consumes/produces via `UInventorySubsystem`; unlocked recipes persisted via new `Fabrication` blob.
  - `AFabricatorStation` (`IAbyssalInteractable`): tiered station, registers recipes on interact, BP hooks.
- Roadmap checklist updated: B2 `[x]`.

## 2026-06-08 (tick 5)

- **A2 — Data-driven objectives + persistence**: `FAbyssalObjectiveTableRow` + `BuildRouteFromTable`; `UObjectiveSubsystem` implements `IAbyssalSaveProvider` (persists index + completed IDs). Hardcoded default retained as fallback.
- Roadmap checklist updated: A2 `[x]`.

## 2026-06-08 (tick 4)

- **B1 — Inventory system**: `UAbyssalItemDefinition`, `UInventorySubsystem` (`IAbyssalSaveProvider`), `AHarvestableNode` (`IAbyssalInteractable`).
- **C1 — World flow**: `UWorldFlowSubsystem` (`IAbyssalSaveProvider`, `TravelToMap`).
- Roadmap checklist updated: B1 `[x]`, C1 `[x]`.

## 2026-06-08 (tick 3)

- **A1 — Provider migration**: `UDiscoverySubsystem` + `UBeaconSubsystem` implement `IAbyssalSaveProvider`.
- **C4 — Mantle Garden blockout**: final map (Map 06, Act 4). 7 zones, 11 discoveries.
- Roadmap: A1 `[x]`, C4 `[x]`.

## 2026-06-08 (tick 2)

- **C4 — Gravity Well blockout**: Map 05 (Act 3). 7 zones, 10 discoveries.
- **A1 — `UAbyssalSaveSubsystem` + `UAbyssalProfileSaveGame`**: interface + slot management + domain blobs.
- Roadmap: A1 `[~]`, C4 `[~]`.

## 2026-06-08 (tick 1 / session resumed)

- PR #1 merged to main (squash `383ce0c`).
- **C2 — `AAbyssalHazardBase`**: phase machine + damage modes, BP hooks.
- **C4 — Fossil Sky blockout**: Map 04 (Act 2). 11 discoveries.

## 2026-06-07 14:34 EDT

- Added `AHeatZoneVolume` — box trigger calling `SetInHeatZone` on `UTemperatureComponent`.

## 2026-06-07 14:07 EDT

- Added `UTemperatureComponent`: heat-exposure vital, overheat damage.

## 2026-06-07 13:40 EDT

- Completed world-map concept review: all six world plates reviewed.

## 2026-06-07 13:12 EDT

- Wrote `Docs/Maps/INNER_SEA.md` (Map 03 blockout).

## 2026-06-07 12:45 EDT

- Concept art review: 3 canonical plates.

## 2026-06-07 12:18 EDT

- Added `IAbyssalInteractable` UINTERFACE + `UInteractionComponent` (A3).

## 2026-06-07 11:52 EDT

- Wrote `Docs/Maps/GLASSROOT_FOREST.md` (Map 02 blockout).

## 2026-06-07 11:18 EDT

- Scope expanded. Full backend gap analysis. Added `Docs/BACKEND_SYSTEMS_ROADMAP.md`.

## 2026-06-07 10:31 EDT

- Fixed `EDiscoveryCategory` drift: added `Structure` + `AlienTech`.

## Earlier entries (2026-05-18 — 2026-05-27)

See git log for full history of initial project setup, Luminous Rift slice, asset pipeline, save/health/audio systems, and design data validation.
