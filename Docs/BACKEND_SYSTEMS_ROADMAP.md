# AbyssalEarth Backend Systems Roadmap

Tracked here: every authored system, the branch it shipped on, and what’s queued next.

---

## Phase A — Save / Persistence

| ID | System | Status | Branch |
|----|--------|--------|--------|
| A1 | `UAbyssalSaveSubsystem` + `IAbyssalSaveProvider` | [x] done | roadmap-tick-1 |
| A2 | `UAbyssalProfileSaveGame` domain blobs (7 blobs) | [x] done | roadmap-tick-2 |

## Phase B — Survival Vitals

| ID | System | Status | Branch |
|----|--------|--------|--------|
| B1 | `UOxygenComponent` | [x] done | roadmap-tick-6 |
| B2 | `UStaminaComponent` | [x] done | roadmap-tick-7 |
| B3 | `UTemperatureComponent` | [x] done | roadmap-tick-9 |

## Phase C — Hazards

| ID | System | Status | Branch |
|----|--------|--------|--------|
| C1 | `AAbyssalHazardBase` phase state machine | [x] done | roadmap-tick-3 |
| C2 | Six biome hazard subclasses | [x] done | roadmap-tick-13 |

## Phase D — NPCs / Creatures

| ID | System | Status | Branch |
|----|--------|--------|--------|
| D1 | `UNarrativeSubsystem` + `UNarrativeTriggerComponent` + `UAbyssalCaptionWidget` | [x] done | roadmap-tick-10 |
| D2 | `AHeliosRobot` — HELIOS NPC interactable | [x] done | roadmap-tick-11 |
| D3 | `AAbyssalCreature` — perception/avoidance AI base | [x] done | roadmap-tick-12 |
| D4 | `UObservationModeComponent` (photo/scan mode) | [x] done | roadmap-tick-14 |
| D5 | Abyssal Interface terminal | [ ] queued | — |

## Phase E — World / Maps

| ID | System | Status | Branch |
|----|--------|--------|--------|
| E1 | `UWorldFlowSubsystem` map travel | [x] done | roadmap-tick-5 |
| E2 | Map doc: FOSSIL_SKY | [x] done | roadmap-tick-8 |
| E3 | Map doc: GRAVITY_WELL | [x] done | roadmap-tick-9 |
| E4 | Map doc: MANTLE_GARDEN | [x] done | roadmap-tick-10 |
| E5 | Map doc: WRECKED_ELEVATOR | [x] done | roadmap-tick-12 |
| E6 | Map doc: LUMINOUS_RIFT | [x] done | roadmap-tick-13 |
| E7 | Map doc: SUBMARINE_INTERIOR | [x] done | roadmap-tick-14 |
| E8 | Map doc: ACCESS_PASSAGE | [ ] queued | — |

## Phase F — Traversal

| ID | System | Status | Branch |
|----|--------|--------|--------|
| F1 | `UAbyssalTraversalComponent` (climb/swim/tether/gravity) | [x] done | roadmap-tick-8 |
| F2 | `AReorientationVolume` | [x] done | roadmap-tick-8 |

## Phase G — Objectives / Narrative

| ID | System | Status | Branch |
|----|--------|--------|--------|
| G1 | `UObjectiveSubsystem` + DataTable route | [x] done | roadmap-tick-4 |
| G2 | `DT_MainObjectiveArc.csv` | [x] done | roadmap-tick-6 |

## Phase H — Inventory / Crafting

| ID | System | Status | Branch |
|----|--------|--------|--------|
| H1 | `UInventorySubsystem` + `UAbyssalItemDefinition` | [x] done | roadmap-tick-5 |
| H2 | `UFabricationSubsystem` + `UAbyssalRecipeDefinition` + `AFabricatorStation` | [x] done | roadmap-tick-7 |
| H3 | `FabricationRecipes.csv` | [x] done | roadmap-tick-7 |

---

## Up Next (tick-15)
- **D5** — `AAbyssalInterfaceTerminal` (alien terminal — power routing + data readout)
- **E8** — Map doc: `ACCESS_PASSAGE.md` (HELIOS passage between sub dock and descent elevator)
- **B4** — `UPressureComponent` (depth pressure vital — complements oxygen in dive zones)
