# AbyssalEarth Hourly Dev Log

Each entry = one autonomous tick. Branch → push → squash-merge to main.

---

## Tick 01 — Save Subsystem Foundation
**Branch**: roadmap-tick-1  
**Merged**: PR #2  
`UAbyssalSaveSubsystem`, `IAbyssalSaveProvider`, slot management, `UAbyssalProfileSaveGame` scaffold.

---

## Tick 02 — Save Blobs + Discovery/Beacon Migration
**Branch**: roadmap-tick-3  
**Merged**: PR #3  
7-blob `UAbyssalProfileSaveGame`; `UDiscoverySubsystem` + `UBeaconSubsystem` migrated to `IAbyssalSaveProvider`.

---

## Tick 03 — Hazard Base + Objective Subsystem
**Branch**: roadmap-tick-4  
**Merged**: PR #4  
`AAbyssalHazardBase` phase state machine; `UObjectiveSubsystem` with DataTable route.

---

## Tick 04 — World Flow + Inventory
**Branch**: roadmap-tick-5  
**Merged**: PR #5  
`UWorldFlowSubsystem`; `UInventorySubsystem` + `UAbyssalItemDefinition`.

---

## Tick 05 — Objectives DataTable + Oxygen Vital
**Branch**: roadmap-tick-6  
**Merged**: PR #6  
`DT_MainObjectiveArc.csv`; `UOxygenComponent`.

---

## Tick 06 — Stamina + Fabrication
**Branch**: roadmap-tick-7  
**Merged**: PR #7  
`UStaminaComponent`; `UFabricationSubsystem` + `AFabricatorStation`; `FabricationRecipes.csv`.

---

## Tick 07 — Traversal + Fossil Sky Map
**Branch**: roadmap-tick-8  
**Merged**: PR #8  
`UAbyssalTraversalComponent`; `AReorientationVolume`; `FOSSIL_SKY.md`.

---

## Tick 08 — Temperature Vital + Gravity Well Map
**Branch**: roadmap-tick-9  
**Merged**: PR #9  
`UTemperatureComponent`; `GRAVITY_WELL.md`.

---

## Tick 09 — Narrative System + Mantle Garden Map
**Branch**: roadmap-tick-10  
**Merged**: PR #10  
`UNarrativeSubsystem`; `UNarrativeTriggerComponent`; `UAbyssalCaptionWidget`; `PrologueNarrativeBeats.csv`; `MANTLE_GARDEN.md`.

---

## Tick 10 — HELIOS Robot NPC
**Branch**: roadmap-tick-11  
**Merged**: PR #11  
`AHeliosRobot` state machine + sequential dialogue; `HeliosDialogueBeats.csv`.

---

## Tick 11 — Creature AI Base + Wrecked Elevator Map
**Branch**: roadmap-tick-12  
**Merged**: PR #12  
`AAbyssalCreature` sight perception, five-state machine, RVO avoidance; `WRECKED_ELEVATOR.md`.

---

## Tick 12 — Six Biome Hazard Subclasses + Luminous Rift Map
**Branch**: roadmap-tick-13  
**Merged**: PR #13  
`ASteamVentHazard`, `AMagmaGeyserHazard`, `AMagmaPulseHazard`, `ABrittleWalkwaySection`, `ACeilingFragmentHazard`, `AGravityShearHazard`; `LUMINOUS_RIFT.md`.

---

## Tick 13 — Observation Mode + Submarine Interior Map
**Branch**: roadmap-tick-14  
**Merged**: PR #14 (pending)  
`UObservationModeComponent` free-camera with roam radius, zoom, roll, scan-to-discover line trace; `SUBMARINE_INTERIOR.md` prologue start layout; `SubmarineNarrativeBeats.csv` (4 beats).

---
