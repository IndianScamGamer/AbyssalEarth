# Backend Systems Roadmap

## Purpose

This document is the gameplay-systems (C++ / backend) plan for taking Abyssal
Earth from its current **Luminous Rift vertical slice** to the **full designed
game**: a 9-beat prologue, a 5-act arc, and six biomes (`Docs/WORLD_ATLAS.md`).

### How the continuation loop should use this file

1. `git fetch --prune` and read this file plus `Docs/NEXT_TASKS.md`.
2. Pick the **lowest-numbered unstarted system whose dependencies are met**.
3. Implement following patterns of existing classes. Keep gameplay state in
   `UGameInstanceSubsystem`s and expose `BlueprintCallable`/`BlueprintAssignable`.
4. Update design data + `Scripts/validate_design_data.py` where relevant.
5. Append a dated entry to `Docs/HOURLY_LOG.md`, commit, and push.

> **Build note.** This (Linux) side authors C++, docs, and design data. Compile
> and PIE-test on the Windows/Unreal side.

---

## Current State (what already exists)

| Domain | Class(es) |
| --- | --- |
| Player / movement | `AAbyssalExplorerCharacter`, `AAbyssalEarthGameMode`, `UAbyssalTraversalComponent` |
| Scanning / discovery / journal | `UScannerComponent`, `ADiscoveryActor`, `UDiscoverySubsystem`, `UAbyssalScannerReadoutWidget`, `UAbyssalJournalWidget` |
| Objectives | `UObjectiveSubsystem` (data-driven + persisted), `AObjectiveTriggerActor` |
| Navigation beacons | `ABeaconActor`, `UBeaconSubsystem` |
| Health | `UAbyssalHealthComponent` |
| Audio | `UAbyssalAudioCueSubsystem` |
| Hazards | `AEmberVentHazard`, `AAbyssalHazardBase` |
| Save/load | `UAbyssalSaveSubsystem` + `UAbyssalProfileSaveGame`; providers: discovery, beacon, inventory, world-flow, objectives, fabrication |
| Interaction | `IAbyssalInteractable`, `UInteractionComponent` |
| Survival vitals | `UTemperatureComponent`, `AHeatZoneVolume`, `UOxygenComponent`, `UStaminaComponent` |
| Inventory | `UAbyssalItemDefinition` (DataAsset), `UInventorySubsystem`, `AHarvestableNode` |
| Fabrication | `UAbyssalRecipeDefinition` (DataAsset), `UFabricationSubsystem`, `AFabricatorStation` |
| Traversal | `UAbyssalTraversalComponent`, `AReorientationVolume` |
| World flow | `UWorldFlowSubsystem` |
| Utility | `UAbyssalGameplayLibrary` |

---

## Gap Analysis

| # | System | Status |
| --- | --- | --- |
| 1 | Save/persistence rework | **Done** (Windows compile pending) |
| 2 | Data-driven objectives + persistence | **Done** (Windows compile pending) |
| 3 | Interaction / use system | **In progress** (C++ authored; character wiring pending) |
| 4 | Inventory / resources | **Done** (Windows compile pending) |
| 5 | Fabrication / crafting | **Done** (Windows compile pending) |
| 6 | Survival vitals | **Done** (temperature + oxygen + stamina; Windows compile pending) |
| 7 | World flow / level transitions | **Done** (Windows compile pending) |
| 8 | Traversal modifiers | **Done** (Windows compile pending) |
| 9 | Hazard framework | **In progress** (base class done; biome derivations documented) |
| 10 | Narrative triggers + dialogue | Missing |
| 11 | HELIOS robot NPCs | Missing |
| 12 | Creatures / survival AI | Missing |
| 13 | Equipment / upgrades | Missing |
| 14 | Photo / observation mode | Missing |
| 15 | Abyssal Interface | Deferred |

---

## Dependency-ordered build plan

### Phase A — Foundations

**A1.** `UAbyssalSaveSubsystem` + `UAbyssalProfileSaveGame` + `IAbyssalSaveProvider`. Discovery + beacon providers migrated.

**A2.** `UObjectiveSubsystem` loads its route from a `FAbyssalObjectiveTableRow` `UDataTable` and persists progress via A1.

**A3.** `IAbyssalInteractable` + `UInteractionComponent` (authored). Wire into
`AAbyssalExplorerCharacter` + `IA_Interact` input asset (Windows-side).

### Phase B — Survival / fabrication

**B1.** `UAbyssalItemDefinition` (DataAsset) + `UInventorySubsystem` + `AHarvestableNode`. Done.

**B2.** `UFabricationSubsystem` + `UAbyssalRecipeDefinition` DataAssets + `AFabricatorStation`. Done.

**B3.** Survival vitals: `UTemperatureComponent` + `AHeatZoneVolume`, `UOxygenComponent`, `UStaminaComponent`. Done.

### Phase C — Maps and world

**C1.** `UWorldFlowSubsystem`: `TravelToMap` (save-on-exit, entry-tag persistence). Done.

**C2.** `AAbyssalHazardBase` (done). Biome derivations: `ABrittleWalkwaySection`,
`ACeilingFragmentHazard`, `AGravityShearHazard`, `ASteamVentHazard`, `AMagmaGeyserHazard`, `AMagmaPulseHazard`.

**C3.** `UAbyssalTraversalComponent` (climb/swim/tether state machine + tether constraint) + `AReorientationVolume` (gravity reorientation). Done. Windows-side: apply gravity-direction lerp + tether correction in character movement.

**C4.** Per-biome blockouts: all six complete.

### Phase D — Narrative, agents, meta

**D1.** `UNarrativeTriggerComponent` + caption widget for prologue beats.

**D2.** `AHeliosRobot` with A3 interaction + D1 dialogue.

**D3.** `AAbyssalCreature` + perception/avoidance.

**D4.** `UObservationModeComponent` (photo mode).

**D5.** Abyssal Interface (deferred).

---

## Status checklist

`[ ]` not started · `[~]` in progress · `[x]` done

- [x] A1 Save/persistence — subsystem + profile save + domain providers migrated; Windows compile pending
- [x] A2 Data-driven objectives — `BuildRouteFromTable` + progress persistence; Windows compile pending
- [~] A3 Interaction — authored; character wiring + Windows compile pending
- [x] B1 Inventory — `UAbyssalItemDefinition` + `UInventorySubsystem` + `AHarvestableNode`; Windows compile pending
- [x] B2 Fabrication — `UAbyssalRecipeDefinition` + `UFabricationSubsystem` + `AFabricatorStation`; Windows compile pending
- [x] B3 Survival vitals — temperature + oxygen + stamina components; Windows compile pending
- [x] C1 World flow — `UWorldFlowSubsystem::TravelToMap` + entry-tag save/restore; Windows-side `APlayerStart` wiring pending
- [~] C2 Hazard framework — base class done; biome derivations documented
- [x] C3 Traversal modifiers — `UAbyssalTraversalComponent` + `AReorientationVolume`; Windows-side movement integration pending
- [x] C4 Per-biome scaffolding — all 6 biome blockouts complete
- [ ] D1 Narrative triggers + prologue dialogue
- [ ] D2 HELIOS robot NPCs
- [ ] D3 Creatures / survival AI
- [ ] D4 Photo / observation mode
- [ ] D5 Abyssal Interface (deferred)
