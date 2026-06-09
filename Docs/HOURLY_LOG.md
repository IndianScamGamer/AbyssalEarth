# AbyssalEarth Hourly Dev Log

Each entry = one autonomous tick. Branch → push → squash-merge to main.

---

## Tick 01 — Save Subsystem Foundation
**Branch**: roadmap-tick-1  
**Merged**: PR #2  
`UAbyssalSaveSubsystem`, `IAbyssalSaveProvider`, slot management (3 slots), `UAbyssalProfileSaveGame` scaffold.

---

## Tick 02 — Save Blobs + Discovery/Beacon Migration
**Branch**: roadmap-tick-3 (clean re-branch after PR #2 conflict)  
**Merged**: PR #3  
7-blob `UAbyssalProfileSaveGame`; `UDiscoverySubsystem` + `UBeaconSubsystem` migrated to `IAbyssalSaveProvider`.

---

## Tick 03 — Hazard Base + Objective Subsystem
**Branch**: roadmap-tick-4  
**Merged**: PR #4  
`AAbyssalHazardBase` phase state machine (Idle/Warning/Active/Cooldown); `UObjectiveSubsystem` with DataTable route support.

---

## Tick 04 — World Flow + Inventory
**Branch**: roadmap-tick-5  
**Merged**: PR #5  
`UWorldFlowSubsystem` map travel; `UInventorySubsystem` + `UAbyssalItemDefinition` PrimaryDataAsset.

---

## Tick 05 — Objectives DataTable + Oxygen Vital
**Branch**: roadmap-tick-6  
**Merged**: PR #6  
`DT_MainObjectiveArc.csv`; `UOxygenComponent` drain/refill/suffocation.

---

## Tick 06 — Stamina + Fabrication
**Branch**: roadmap-tick-7  
**Merged**: PR #7  
`UStaminaComponent` exhaustion gate; `UFabricationSubsystem` + `UAbyssalRecipeDefinition` + `AFabricatorStation`; `FabricationRecipes.csv`.

---

## Tick 07 — Traversal + Fossil Sky Map
**Branch**: roadmap-tick-8  
**Merged**: PR #8  
`UAbyssalTraversalComponent` (climb/swim/tether/gravity reorientation); `AReorientationVolume`; `FOSSIL_SKY.md`.

---

## Tick 08 — Temperature Vital + Gravity Well Map
**Branch**: roadmap-tick-9  
**Merged**: PR #9  
`UTemperatureComponent` heat/insulation/overheat damage; `GRAVITY_WELL.md`.

---

## Tick 09 — Narrative System + Mantle Garden Map
**Branch**: roadmap-tick-10  
**Merged**: PR #10  
`UNarrativeSubsystem` queued beats + `IAbyssalSaveProvider`; `UNarrativeTriggerComponent`; `UAbyssalCaptionWidget`; `PrologueNarrativeBeats.csv`; `MANTLE_GARDEN.md`.

---

## Tick 10 — HELIOS Robot NPC
**Branch**: roadmap-tick-11  
**Merged**: PR #11  
`AHeliosRobot` actor with `EHeliosState` state machine; `IAbyssalInteractable` sequential dialogue via `UNarrativeSubsystem`; `HeliosDialogueBeats.csv`.

---

## Tick 11 — Creature AI Base + Wrecked Elevator Map
**Branch**: roadmap-tick-12  
**Merged**: PR #12  
`AAbyssalCreature` with `UAIPerceptionComponent` sight sense, five-state machine, RVO avoidance, health/damage handling; `WRECKED_ELEVATOR.md`.

---

## Tick 12 — Six Biome Hazard Subclasses + Luminous Rift Map
**Branch**: roadmap-tick-13  
**Merged**: PR #13 (pending)  
`ASteamVentHazard` (column + launch impulse); `AMagmaGeyserHazard` (apex radial + knockback); `AMagmaPulseHazard` (instant radial burst); `ABrittleWalkwaySection` (integrity countdown + collapse); `ACeilingFragmentHazard` (physics fall + impact damage); `AGravityShearHazard` (traversal reorientation zone); `LUMINOUS_RIFT.md` Act 1 start area layout.

---
