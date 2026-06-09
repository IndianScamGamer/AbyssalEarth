# Map 05B — Gravity Well Lower (Act 3 — OBJ_MAKE_MACHINE_ANSWER)

## Overview
The deepest accessible section of the Gravity Well system — below the main GRAVITY_WELL map where gravity is merely inverted. Here gravity is *fractured*: multiple competing gravity directions exist simultaneously, creating floating rock platforms, inverted pools, and passages where a wrong step sends the player toward a wall rather than the floor. Three `AAbyssalInterfaceTerminal` actors are here, requiring the player to activate a power-routing puzzle to read them.

## Dimensions
Multi-axis open volume — approximately 150 m × 150 m × 80 m. No single “floor.” Navigation relies heavily on `UAbyssalTraversalComponent` and `AReorientationVolume` volumes placed throughout.

---

## Zones

### Z1 — Entry Rift
Fall/climb from GRAVITY_WELL main map through a narrow rift. Gravity normalises briefly — the last moment of predictable footing. Checkpoint: `CHK_GRAVITY_WELL_LOWER_ENTRY`.

**Discovery**: `DIS_GRAVITY_FRACTURE_SEAM` (scan the rift wall — visible shear line where two gravity fields meet).

### Z2 — Floating Platform Grid
Six rock platforms hovering at different heights and orientations, each governed by a separate `AReorientationVolume`. Stepping from one to the next reorients the player. The player must traverse all six to reach the power sources.

**Hazard**: `AGravityShearHazard` — two active zones between platforms that fire when the player transitions; brief disorientation.

**Creature**: Gravity Mote — small floating spherical creature that orbits platform edges (`bIsAggressive = false`; `PassiveSpeed = 50`). Cannot attack but blocks narrow ledges.

### Z3 — Power Source Chamber
Three `AAbyssalPowerNode` (Source type) nodes distributed across separate platforms, each requiring the player to navigate a reorientation sequence to reach. Activating all three powers the relay network.

**Power network**: Source A → Relay 1 → Terminal Alpha; Source B → Relay 2 → Terminal Beta; Source A+B → Relay 3 → Terminal Gamma (requires both sources active).

### Z4 — Terminal Cluster
Three `AAbyssalInterfaceTerminal` actors (Alpha, Beta, Gamma), each oriented to a different gravity plane. Alpha and Beta unlock with single sources; Gamma requires both and delivers the key lore beat.

**Narrative beats** (from `TerminalDataBeats.csv` pool + new GWL beats):
- Terminal Alpha: boot sequence + partial record
- Terminal Beta: origin designation + purpose
- Terminal Gamma: the Confluence acknowledgment — player registered as Observer, rift protocol becomes available

**Objective trigger**: After Gamma reads out, `OBJ_MAKE_MACHINE_ANSWER` completes → `OBJ_BUILD_WAY_OUT` activates.

### Z5 — Observer Ledge
A platform that only becomes reachable after Gamma activates — a new `AReorientationVolume` fires, pulling the player upward to a previously inaccessible ledge. Contains: a fabrication schematic pickup (unlocks `ITEM_KEY_RIFT_STABILISER` recipe), and `DIS_CONFLUENCE_MARK` (scan an alien glyph that matches the monolith array in LUMINOUS_RIFT).

---

## Creatures
| Species | State Default | Count | Zone |
|---------|--------------|-------|------|
| Gravity Mote | Passive | 5–7 | Z2 platforms |
| Void Drifter | Curious | 2 | Z3 (slow, patrol power nodes) |

## Discoveries
| ID | Type | Zone |
|----|------|------|
| DIS_GRAVITY_FRACTURE_SEAM | Scan | Z1 |
| DIS_CONFLUENCE_MARK | Scan | Z5 |

## Hazards
| Type | Zone | Notes |
|------|------|-------|
| `AGravityShearHazard` (x2) | Z2 | Between platform transitions |

## Power Network
```
Source A (Z3) ───────> Relay 1 ─> Terminal Alpha
                   └────> Relay 3 ─> Terminal Gamma (requires A+B)
Source B (Z3) ───────> Relay 2 ─> Terminal Beta
                   └────> Relay 3 ┈
```
Relay 3 only passes power when both Source A and Source B are active (designer configures via `ConnectedNodes` in-editor; Relay 3 checks power level > 0.5).

## Notes
- The “both sources required” mechanic for Gamma is achieved by setting Relay 3’s `ActivationThreshold` (via AAbyssalInterfaceTerminal) to 0.75 — a single source (1.0) passes through but halved through Relay 3’s 0.5 RelayLoss only reaches 0.5; two sources both routing through Relay 3 sum to 1.0.
- Gravity Mote creature: `AAbyssalCreature` subclass; all speeds slow (Passive 50, Curious 80, Flee 150); `bIsAggressive = false`; spherical mesh.
- Checkpoint in Z1 is mandatory — dying during the power puzzle should not reset the player to the surface.
