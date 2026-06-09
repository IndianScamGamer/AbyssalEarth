# AbyssalEarth Backend Systems Roadmap

Tracked here: every authored system, the branch it shipped on, and what’s queued next.

---

## Phase A — Save / Persistence — COMPLETE
| ID | System | Branch |
|----|--------|--------|
| A1 | `UAbyssalSaveSubsystem` + `IAbyssalSaveProvider` | roadmap-tick-1 |
| A2 | `UAbyssalProfileSaveGame` (7 blobs) | roadmap-tick-2 |
| A3 | `UCheckpointSubsystem` | roadmap-tick-16 |

## Phase B — Survival Vitals — COMPLETE
| ID | System | Branch |
|----|--------|--------|
| B1 | `UOxygenComponent` | roadmap-tick-6 |
| B2 | `UStaminaComponent` | roadmap-tick-7 |
| B3 | `UTemperatureComponent` | roadmap-tick-9 |
| B4 | `UPressureComponent` | roadmap-tick-15 |

## Phase C — Hazards — COMPLETE
| ID | System | Branch |
|----|--------|--------|
| C1 | `AAbyssalHazardBase` | roadmap-tick-3 |
| C2 | Six biome hazard subclasses | roadmap-tick-13 |

## Phase D — NPCs / Creatures — COMPLETE
| ID | System | Branch |
|----|--------|--------|
| D1 | Narrative system (subsystem + trigger + caption widget) | roadmap-tick-10 |
| D2 | `AHeliosRobot` | roadmap-tick-11 |
| D3 | `AAbyssalCreature` | roadmap-tick-12 |
| D4 | `UObservationModeComponent` | roadmap-tick-14 |
| D5 | `AAbyssalInterfaceTerminal` | roadmap-tick-15 |

## Phase E — World / Maps — COMPLETE (14 map docs)
| ID | Map | Branch |
|----|-----|--------|
| E1 | `UWorldFlowSubsystem` | roadmap-tick-5 |
| E2–E14 | FOSSIL_SKY, GRAVITY_WELL, MANTLE_GARDEN, WRECKED_ELEVATOR, LUMINOUS_RIFT, SUBMARINE_INTERIOR, ACCESS_PASSAGE, DESCENT_ELEVATOR, DEEP_CHANNEL, FOSSIL_SKY_UPPER, GRAVITY_WELL_LOWER, MANTLE_GARDEN_DEEP, RIFT_CHAMBER | ticks 8–21 |

## Phase F — Traversal / Interaction — COMPLETE
| ID | System | Branch |
|----|--------|--------|
| F1 | `UAbyssalTraversalComponent` | roadmap-tick-8 |
| F2 | `AReorientationVolume` | roadmap-tick-8 |
| F3 | `UAbyssalInteractionComponent` | roadmap-tick-16 |

## Phase G — Objectives / Narrative — COMPLETE
| ID | System | Branch |
|----|--------|--------|
| G1 | `UObjectiveSubsystem` | roadmap-tick-4 |
| G2 | `DT_MainObjectiveArc.csv` | roadmap-tick-6 |
| G3 | `ACheckpointActor` | roadmap-tick-17 |

## Phase H — Inventory / Crafting — COMPLETE
| ID | System | Branch |
|----|--------|--------|
| H1 | `UInventorySubsystem` + `UAbyssalItemDefinition` | roadmap-tick-5 |
| H2 | `UFabricationSubsystem` + `AFabricatorStation` | roadmap-tick-7 |
| H3 | `FabricationRecipes.csv` (8 recipes incl. Rift Stabiliser) | tick-7, updated tick-22 |
| H4 | `UAbyssalItemDatabase` + `DT_ItemDatabase.csv` | roadmap-tick-18 |

## Phase I — Health / Death — COMPLETE
| I1 | `UAbyssalHealthComponent` | roadmap-tick-17 |

## Phase J — HUD / UI — COMPLETE
| ID | System | Branch |
|----|--------|--------|
| J1 | `UAbyssalHUDSubsystem` | roadmap-tick-18 |
| J2 | `UAbyssalObjectiveWidget` | roadmap-tick-19 |
| J3 | `UAbyssalInventoryWidget` | roadmap-tick-20 |

## Phase K — Power Routing — COMPLETE
| K1 | `AAbyssalPowerNode` | roadmap-tick-19 |

## Phase L — Scanning — COMPLETE
| L1 | `IAbyssalScannable` + `UAbyssalScanComponent` | roadmap-tick-20 |

## Phase M — Endgame — COMPLETE
| M1 | `AAbyssalRiftActor` | roadmap-tick-21 |

## Phase N — Upgrades — COMPLETE
| N1 | `UAbyssalUpgradeSubsystem` | roadmap-tick-21 |

## Phase O — Audio — COMPLETE
| O1 | `UAbyssalAudioSubsystem` (4-layer mix state manager) | roadmap-tick-22 |

## Phase P — Player — COMPLETE
| P1 | `AAbyssalPlayerCharacter` (full component wiring) | roadmap-tick-22 |

---

# BACKEND STATUS: ALL PHASES COMPLETE ✅

Every planned C++ system is authored. Remaining work is editor-side:
Blueprint subclasses, UMG widget layouts, level blockouts, audio assets,
art, and animation — none of which can be authored in code.

## Final tick (tick-23): Story finish line
- Full narrative script: Act 1–5 beat CSVs (player monologue arc)
- `STORY_BIBLE.md` — complete story reference (world truth, the Confluence, HELIOS anomaly explanation, the Observer ending)
- `EPILOGUE.md` — ending sequence design + post-credits hook
