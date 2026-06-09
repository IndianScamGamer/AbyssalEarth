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
| E13 | Map doc: MANTLE_GARDEN_DEEP | [x] done | roadmap-tick-20 |
| E14 | Map doc: RIFT_CHAMBER | [x] done | roadmap-tick-21 |

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
| J3 | `UAbyssalInventoryWidget` | [x] done | roadmap-tick-20 |

## Phase K — Power Routing

| ID | System | Status | Branch |
|----|--------|--------|--------|
| K1 | `AAbyssalPowerNode` (Source/Relay/Sink) | [x] done | roadmap-tick-19 |

## Phase L — Scanning

| ID | System | Status | Branch |
|----|--------|--------|--------|
| L1 | `IAbyssalScannable` + `UAbyssalScanComponent` | [x] done | roadmap-tick-20 |

## Phase M — Endgame

| ID | System | Status | Branch |
|----|--------|--------|--------|
| M1 | `AAbyssalRiftActor` | [x] done | roadmap-tick-21 |

## Phase N — Upgrades

| ID | System | Status | Branch |
|----|--------|--------|--------|
| N1 | `UAbyssalUpgradeSubsystem` | [x] done | roadmap-tick-21 |

---

## Status: Core Gameplay Loop Complete

All primary backend systems are authored. The full player journey from submarine to rift is now designed and coded:

**Prologue** (SUBMARINE_INTERIOR → ACCESS_PASSAGE → DESCENT_ELEVATOR → WRECKED_ELEVATOR)  
**Act 1** (LUMINOUS_RIFT → DEEP_CHANNEL)  
**Act 2** (FOSSIL_SKY_UPPER → FOSSIL_SKY)  
**Act 3** (GRAVITY_WELL → GRAVITY_WELL_LOWER)  
**Act 4** (MANTLE_GARDEN → MANTLE_GARDEN_DEEP)  
**Act 5** (RIFT_CHAMBER)  

## Up Next (tick-22)
- **O1** — `UAbyssalAudioSubsystem` — ambient layer manager (biome music + vital-state audio reactivity)
- **P1** — `AAbyssalPlayerCharacter` scaffold — base character class wiring all components together
- **Design** — Full `FabricationRecipes.csv` update with Rift Stabiliser recipe and tier-3 entries
