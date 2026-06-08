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
| Player / movement | `AAbyssalExplorerCharacter`, `AAbyssalEarthGameMode` |
| Scanning / discovery / journal | `UScannerComponent`, `ADiscoveryActor`, `UDiscoverySubsystem`, `UAbyssalScannerReadoutWidget`, `UAbyssalJournalWidget` |
| Objectives | `UObjectiveSubsystem`, `AObjectiveTriggerActor` |
| Navigation beacons | `ABeaconActor`, `UBeaconSubsystem` |
| Health | `UAbyssalHealthComponent` |
| Audio | `UAbyssalAudioCueSubsystem` |
| Hazards | `AEmberVentHazard`, `AAbyssalHazardBase` (new) |
| Save/load | `UDiscoverySaveGame` (legacy), `UAbyssalSaveSubsystem` + `UAbyssalProfileSaveGame`; `UDiscoverySubsystem` + `UBeaconSubsystem` on `IAbyssalSaveProvider` |
| Interaction | `IAbyssalInteractable`, `UInteractionComponent` |
| Survival vitals | `UTemperatureComponent`, `AHeatZoneVolume` |
| Inventory | `UAbyssalItemDefinition` (DataAsset), `UInventorySubsystem` (new) |
| World flow | `UWorldFlowSubsystem` (new) |
| Harvestables | `AHarvestableNode` (new) |
| Utility | `UAbyssalGameplayLibrary` |

---

## Gap Analysis

| # | System | Status |
| --- | --- | --- |
| 1 | Save/persistence rework | **Done** (Windows compile pending) |
| 2 | Data-driven objectives + persistence | Partial (hardcoded; not yet persisted) |
| 3 | Interaction / use system | **In progress** (C++ authored; character wiring pending) |
| 4 | Inventory / resources | **Done** (Windows compile pending) |
| 5 | Fabrication / crafting | Missing |
| 6 | Survival vitals | **In progress** (temperature done; oxygen/stamina pending) |
| 7 | World flow / level transitions | **Done** (Windows compile pending) |
| 8 | Traversal modifiers | Missing |
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

**A1.** `UAbyssalSaveSubsystem` + `UAbyssalProfileSaveGame` + `IAbyssalSaveProvider`. `UDiscoverySubsystem` and `UBeaconSubsystem` migrated; direct `UGameplayStatics::SaveGameToSlot` calls removed.

**A2.** Load objective route from `UDataTable`; persist `CurrentObjectiveIndex` via A1.

**A3.** `IAbyssalInteractable` + `UInteractionComponent` (authored). Wire into
`AAbyssalExplorerCharacter` + `IA_Interact` input asset (Windows-side).

### Phase B — Survival / fabrication

**B1.** `UAbyssalItemDefinition` (DataAsset) + `UInventorySubsystem` + `AHarvestableNode`. Done.

**B2.** `UFabricationSubsystem` + recipe DataAssets + fabricator interactable.

**B3.** `UTemperatureComponent` + `AHeatZoneVolume` (done). Oxygen/pressure + stamina pending.

### Phase C — Maps and world

**C1.** `UWorldFlowSubsystem`: `TravelToMap` (save-on-exit, entry-tag persistence). Done. Windows-side: wire `APlayerStart` tag selection from `GetLastEntryTag()`.

**C2.** `AAbyssalHazardBase` (done). Biome derivations: `ABrittleWalkwaySection`,
`ACeilingFragmentHazard`, `AGravityShearHazard`, `ASteamVentHazard`, `AMagmaGeyserHazard`, `AMagmaPulseHazard`.

**C3.** `AReorientationVolume`, climb/swim states, tether tool.

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

- [x] A1 Save/persistence — subsystem + profile save + both domain providers migrated; Windows compile pending
- [~] A2 Data-driven objectives (CSV mirror exists; not yet data-driven or persisted)
- [~] A3 Interaction — authored; character wiring + Windows compile pending
- [x] B1 Inventory — `UAbyssalItemDefinition` + `UInventorySubsystem` + `AHarvestableNode`; Windows compile pending
- [ ] B2 Fabrication / recipe unlocks
- [~] B3 Survival vitals — temperature done; oxygen/stamina pending
- [x] C1 World flow — `UWorldFlowSubsystem::TravelToMap` + entry-tag save/restore; Windows-side `APlayerStart` wiring pending
- [~] C2 Hazard framework — base class done; biome derivations documented
- [ ] C3 Traversal modifiers
- [x] C4 Per-biome scaffolding — all 6 biome blockouts complete
- [ ] D1 Narrative triggers + prologue dialogue
- [ ] D2 HELIOS robot NPCs
- [ ] D3 Creatures / survival AI
- [ ] D4 Photo / observation mode
- [ ] D5 Abyssal Interface (deferred)
