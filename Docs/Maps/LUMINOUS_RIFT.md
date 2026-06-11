# Map 01 — Luminous Rift (Act 1 Start)

## Overview
The first full biome after the crash. A vast fractured cavern ceiling lets alien bioluminescence cascade down in curtain-like streams. The space feels beautiful and deeply wrong: the scale is impossible, the light-sources are alive, and something large is moving in the mid-distance. The player’s primary goal is **SURVIVE** — find shelter, identify threats, and locate a stable path deeper in.

## Dimensions
Large open-plan — roughly 300 m × 180 m floor, 60–90 m ceiling. Vertical play via rocky shelves and collapse debris. Navigation is on foot; no climbing gear yet.

---

## Zones

### Z1 — Crash Scatter
Immediate area after the shaft exit. Elevator debris, HELIOS robot wreckage, cracked floor tiles. Low creature density (passive gliders only). Tutorial-density interaction nodes: one harvestable crystal, one HELIOS log fragment.

**Key beats**: NAR_PRO_REVEAL already fired in WRECKED_ELEVATOR. No new narration here — let the visuals breathe.

### Z2 — The Veil
Curtains of bioluminescent organisms hang from the ceiling in slow pulses. Walking through them triggers a low-vibration audio cue. First encounter with `AAbyssalCreature` (passive Veil Drifter species). Scanning the organisms populates discovery `DIS_VEIL_ORGANISM`.

**Hazard**: None in base pass. Optional `ASteamVentHazard` in one corner for environmental variety.

### Z3 — Shard Shelf
Elevated rock shelf reachable by climbing a debris pile (no `UAbyssalTraversalComponent` needed — static stair geometry). Contains the first chest-equivalent: sealed HELIOS supply crate with 2× `ITEM_MINERAL_ABYSSAL_CORE`.

**Discovery**: `DIS_HELIOS_SUPPLY_CACHE` (scan the crate before opening).

### Z4 — Rift Heart
Central clearing dominated by a dormant alien structure: a ring of upright monoliths surrounding a cracked floor vent that glows amber. Not yet interactable (unlocks in OBJ_MAKE_MACHINE_ANSWER). Creatures gather here at night-cycle intervals — a territorial Depth Lurker patrols.

**Hazard**: `AMagmaPulseHazard` placed inside the rift vent (inaccessible, but visible through cracks — signals future utility).

**Discovery**: `DIS_MONOLITH_ARRAY`, `DIS_RIFT_VENT_AMBER`.

### Z5 — Collapse Bridge
Narrow land-bridge over a chasm. Uses `ABrittleWalkwaySection` (2 integrity steps) as a one-time gate: the player can slow-walk across, or run and have it crumble — dropping them to Z6 below instead of Z7 ahead. Teaches the structural hazard class.

### Z6 — Chasm Floor (alternate)
Rocky floor under the Z5 bridge. Slightly longer route to Z7. Contains a unique creature-only discovery: `DIS_DEPTH_LURKER_NEST` (scan a shed carapace).

### Z7 — Act 1 Waypoint
Cave mouth leading toward `FOSSIL_SKY` map. A HELIOS beacon (non-functional) provides the first save-compatible map marker. Objective `OBJ_SURVIVE` completes here, transitioning to `OBJ_DISCOVER_PLACE`.

---

## Creatures
| Species | State Default | Count | Zone |
|---------|--------------|-------|------|
| Veil Drifter | Passive | 4–6 | Z2 |
| Depth Lurker | Aggressive | 1 | Z4 |
| Shelf Crawler | Curious | 2 | Z3 edges |

## Discoveries
| ID | Type | Zone |
|----|------|------|
| DIS_VEIL_ORGANISM | Scan | Z2 |
| DIS_HELIOS_SUPPLY_CACHE | Object | Z3 |
| DIS_MONOLITH_ARRAY | Scan | Z4 |
| DIS_RIFT_VENT_AMBER | Scan | Z4 |
| DIS_DEPTH_LURKER_NEST | Scan | Z6 |

## Hazards
| Type | Zone | Notes |
|------|------|-------|
| `ASteamVentHazard` | Z2 corner | Optional, low pressure |
| `AMagmaPulseHazard` | Z4 vent | Visual only (inaccessible) |
| `ABrittleWalkwaySection` | Z5 | 2-integrity gate; alt route Z6 |

## Notes
- Day/night cycle here is cosmetic: bioluminescence brightens on a 90-second pulse. No gameplay change yet.
- Depth Lurker in Z4 should be `bIsAggressive = true`; all others `false` until harmed.
- Music: ambient bioluminescent drone (no percussion) until Depth Lurker is triggered; then low-percussion tension layer.
