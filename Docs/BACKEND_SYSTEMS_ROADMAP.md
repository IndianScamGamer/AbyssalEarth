# AbyssalEarth Backend Systems Roadmap

Tracked here: every authored system, the branch it shipped on, and what’s queued next.

---

## Phase A — Save / Persistence

| ID | System | Status | Branch |
|----|--------|--------|--------|
| A1 | `UAbyssalSaveSubsystem` + `IAbyssalSaveProvider` | [x] done | roadmap-tick-1 |
| A2 | `UAbyssalProfileSaveGame` domain blobs (7 blobs) | [x] done | roadmap-tick-2 |
| A3 | `UCheckpointSubsystem` | [x] done | roadmap-tick-16 |

## Phase B — Survival Vitals

| ID | System | Status | Branch |
|----|--------|--------|--------|
| B1 | `UOxygenComponent` | [x] done | roadmap-tick-6 |
| B2 | `UStaminaComponent` | [x] done | roadmap-tick-7 |
| B3 | `UTemperatureComponent` | [x] done | roadmap-tick-9 |
| B4 | `UPressureComponent` | [x] done | roadmap-tick-15 |

## Phase C — Hazards

| ID | System | Status | Branch |
|----|--------|--------|--------|
| C1 | `AAbyssalHazardBase` phase state machine | [x] done | roadmap-tick-3 |
| C2 | Six biome hazard subclasses | [x] done | roadmap-tick-13 |

## Phase D — NPCs / Creatures

| ID | System | Status | Branch |
|----|--------|--------|--------|
| D1 | `UNarrativeSubsystem` + `UNarrativeTriggerComponent` + `UAbyssalCaptionWidget` | [x] done | roadmap-tick-10 |
| D2 | `AHeliosRobot` | [x] done | roadmap-tick-11 |
| D3 | `AAbyssalCreature` | [x] done | roadmap-tick-12 |
| D4 | `UObservationModeComponent` | [x] done | roadmap-tick-14 |
| D5 | `AAbyssalInterfaceTerminal` | [x] done | roadmap-tick-15 |

## Phase E — World / Maps

| ID | System | Status | Branch |
|----|--------|--------|--------|
| E1 | `UWorldFlowSubsystem` | [x] done | roadmap-tick-5 |
| E2 | Map doc: FOSSIL_SKY | [x] done | roadmap-tick-8 |
| E3 | Map doc: GRAVITY_WELL | [x] done | roadmap-tick-9 |
| E4 | Map doc: MANTLE_GARDEN | [x] done | roadmap-tick-10 |
| E5 | Map doc: WRECKED_ELEVATOR | [x] done | roadmap-tick-12 |
| E6 | Map doc: LUMINOUS_RIFT | [x] done | roadmap-tick-13 |
| E7 | Map doc: SUBMARINE_INTERIOR | [x] done | roadmap-tick-14 |
| E8 | Map doc: ACCESS_PASSAGE | [x] done | roadmap-tick-15 |
| E9 | Map doc: DESCENT_ELEVATOR | [x] done | roadmap-tick-16 |
| E10 | Map doc: DEEP_CHANNEL | [x] done | roadmap-tick-17 |
| E11 | Map doc: FOSSIL_SKY_UPPER | [x] done | roadmap-tick-18 |
| E12 | Map doc: GRAVITY_WELL_LOWER | [x] done | roadmap-tick-19 |

## Phase F — Traversal / Interaction

| ID | System | Status | Branch |
|----|--------|--------|--------|
| F1 | `UAbyssalTraversalComponent` | [x] done | roadmap-tick-8 |
| F2 | `AReorientationVolume` | [x] done | roadmap-tick-8 |
| F3 | `UAbyssalInteractionComponent` | [x] done | roadmap-tick-16 |

## Phase G — Objectives / Narrative

| ID | System | Status | Branch |
|----|--------|--------|--------|
| G1 | `UObjectiveSubsystem` + DataTable route | [x] done | roadmap-tick-4 |
| G2 | `DT_MainObjectiveArc.csv` | [x] done | roadmap-tick-6 |
| G3 | `ACheckpointActor` | [x] done | roadmap-tick-17 |

## Phase H — Inventory / Crafting

| ID | System | Status | Branch |
|----|--------|--------|--------|
| H1 | `UInventorySubsystem` + `UAbyssalItemDefinition` | [x] done | roadmap-tick-5 |
| H2 | `UFabricationSubsystem` + `UAbyssalRecipeDefinition` + `AFabricatorStation` | [x] done | roadmap-tick-7 |
| H3 | `FabricationRecipes.csv` | [x] done | roadmap-tick-7 |
| H4 | `FAbyssalItemTableRow` + `UAbyssalItemDatabase` + `DT_ItemDatabase.csv` | [x] done | roadmap-tick-18 |

## Phase I — Health / Death

| ID | System | Status | Branch |
|----|--------|--------|--------|
| I1 | `UAbyssalHealthComponent` | [x] done | roadmap-tick-17 |

## Phase J — HUD / UI

| ID | System | Status | Branch |
|----|--------|--------|--------|
| J1 | `UAbyssalHUDSubsystem` + `FAbyssalVitalReadout` | [x] done | roadmap-tick-18 |
| J2 | `UAbyssalObjectiveWidget` | [x] done | roadmap-tick-19 |

## Phase K — Power Routing

| ID | System | Status | Branch |
|----|--------|--------|--------|
| K1 | `AAbyssalPowerNode` (Source/Relay/Sink) + propagation graph | [x] done | roadmap-tick-19 |

---

## Up Next (tick-20)
- **L1** — `UAbyssalScanComponent` — player-held scanner tool component; emits scan pulses, detects `IAbyssalScannable`, feeds `UDiscoverySubsystem`
- **E13** — Map doc: `MANTLE_GARDEN_DEEP.md` (Act 4 fabrication zone)
- **J3** — `UAbyssalInventoryWidget` — UUserWidget base for inventory grid display
