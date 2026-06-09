# Map 06B — Mantle Garden Deep (Act 4 — OBJ_BUILD_WAY_OUT)

## Overview
The deepest accessible biome: a series of magma-lit chambers beneath the main Mantle Garden. Extreme thermal conditions force the player to manage `UTemperatureComponent` carefully, and pressure from depth adds `UPressureComponent` into play simultaneously. The reward for surviving here is access to tier-3 fabrication stations and the raw materials for the Rift Stabiliser.

## Dimensions
Multi-chamber layout — 4 chambers connected by narrow choke points, each approximately 60 m × 40 m. Total length: ~280 m linear. Ceiling 8–15 m (low — oppressive).

---

## Zones

### Z1 — Heat Front
Entry from MANTLE_GARDEN main. Immediate temperature spike: `UTemperatureComponent::HeatGainRate` effectively doubles here (via `AEmberVentHazard` placed in entry corridor). `ITEM_TOOL_HEAT_SHIELD` consumables are critical. Checkpoint: `CHK_MANTLE_DEEP_ENTRY`.

**Hazard**: `AMagmaPulseHazard` ×2 (flanking the narrow entry; 3.5 s cooldown).

**Creature**: Magma Crawler — `AAbyssalCreature` subclass; `bIsAggressive = true`; aggressive at 100% health; patrols Z1 perimeter.

### Z2 — Crystal Seam
A chamber with exposed Gravity Crystal deposits in the walls (harvestable: 1–3× `ITEM_MINERAL_GRAVITY_CRYSTAL`, respawn 180 s). The crystals distort local gravity slightly — use `AReorientationVolume` with a 10° tilt to communicate this without breaking navigation. A secondary `AMagmaGeyserHazard` erupts at the room’s centre every 10 s (long cooldown gives traversal windows).

**Discovery**: `DIS_GRAVITY_CRYSTAL_SEAM`.

### Z3 — Forge Chamber
The main fabrication hub. Two `AFabricatorStation` actors: tier-2 (mid-room) and tier-3 (rear alcove, gated behind a `ABrittleWalkwaySection` that collapses and respawns on a 60 s timer). The tier-3 station is the only place the player can craft `ITEM_KEY_RIFT_STABILISER`.

**Required materials for Rift Stabiliser** (from `FabricationRecipes.csv` / pending addition):
- 2× `ITEM_MINERAL_ABYSSAL_CORE`
- 1× `ITEM_MINERAL_GRAVITY_CRYSTAL`
- 1× `ITEM_MINERAL_MAGMA_RESIDUE`

**Narrative beat**: `MGD_FORGE_01` (auto on tier-3 station approach): *"Okay. I know what this needs to be."*

### Z4 — Magma Vent Core
A dead-end chamber at the bottom. No fabrication; pure hazard challenge. `ASteamVentHazard` ×3 arranged in an overlapping pattern requiring the player to time their passage. A unique harvestable deposit of `ITEM_MINERAL_MAGMA_RESIDUE` ×3 (no respawn) justifies the risk.

**Discovery**: `DIS_MAGMA_VENT_CORE_RESIDUE`.

---

## Creatures
| Species | State Default | Count | Zone |
|---------|--------------|-------|------|
| Magma Crawler | Aggressive | 2 | Z1 |
| Cinder Floater | Passive | 3 | Z2–Z3 |

## Discoveries
| ID | Type | Zone |
|----|------|------|
| DIS_GRAVITY_CRYSTAL_SEAM | Scan | Z2 |
| DIS_MAGMA_VENT_CORE_RESIDUE | Scan | Z4 |

## Hazards
| Type | Zone | Notes |
|------|------|-------|
| `AMagmaPulseHazard` (x2) | Z1 | Entry flanking |
| `AMagmaGeyserHazard` | Z2 | 10 s cycle; 2 s Active |
| `ABrittleWalkwaySection` | Z3 | 60 s respawn; gates tier-3 station |
| `ASteamVentHazard` (x3) | Z4 | Overlapping timing puzzle |

## Checkpoints
| ID | Zone |
|----|------|
| `CHK_MANTLE_DEEP_ENTRY` | Z1 |

## Notes
- Temperature here sits at 0.6–0.8 range passively — player needs either `ITEM_TOOL_HEAT_SHIELD` active or the `ITEM_UPGRADE_THERMAL_WEAVE` installed to survive extended stays.
- Both survival stats (temperature + pressure) are simultaneously relevant here for the first time — the HUD should show both bars prominently.
- Tier-3 station gating via `ABrittleWalkwaySection` respawn: the walkway resets every 60 s, meaning a failed crossing attempt has a short forced-wait punishment rather than permanently blocking progress.
- The `MGD_FORGE_01` beat should feel like a character beat, not exposition — the player has solved the puzzle and knows what to do.
