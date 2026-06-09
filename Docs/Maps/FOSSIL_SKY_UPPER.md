# Map 03A — Fossil Sky Upper (Act 2 Approach)

## Overview
The transition zone between the DEEP_CHANNEL exit and the full FOSSIL_SKY map. A wide but low-ceilinged shelf covered in fossilized megafauna bones that jut from the walls and floor like an ancient graveyard. The “sky” is the underside of a vast fossil shelf — which the player misreads as a ceiling until they reach the edge and look down into the true depth of FOSSIL_SKY. The scale reveal here is the map’s purpose.

## Dimensions
Open shelf — approximately 200 m × 80 m, 15–25 m ceiling clearance. Gently sloping toward the main FOSSIL_SKY drop. No water. First map without bioluminescent ambience — lit by mineral phosphorescence in the bone structures.

---

## Zones

### Z1 — Channel Exit Shelf
Immediate emergence from DEEP_CHANNEL. Dry stone, scattered bone fragments. First breath of non-flooded air in the transition sequence. Checkpoint: `CHK_FOSSIL_SKY_UPPER_ENTRY`.

**Narrative beat**: `FSK_UPPER_01` (auto): player character says *"What the hell are those?"* — referring to the bones.

**Discovery**: `DIS_MEGAFAUNA_RIB` (scan the exposed rib arch in Z1 entrance).

### Z2 — Bone Forest
Dense cluster of fossilized columns — vertebrae stacked 8–12 m high, ribs arching overhead. Navigation requires threading between them. `AAbyssalCreature` species: Bone Crawler (curious/fleeing, skitters along fossil surfaces). First time the creature’s `CuriousSpeed` matters — it will follow the player between columns before fleeing.

**Hazard**: `ACeilingFragmentHazard` — loose fossil shard lodged in a rib arch, triggered by proximity.

**Discovery**: `DIS_FOSSIL_VERTEBRAE_COLUMN` (scan in Z2 centre).

### Z3 — Ancient Kill Site
A clearing where a massive skeleton lies partially buried. The bones of two distinct species — predator and prey — interlocked. A harvestable node (`ITEM_FOSSIL_SHARD` ×2, respawn 120 s). Scan yields `DIS_ANCIENT_KILL_SITE`.

**Objective nudge**: First time the HUD shows `OBJ_DISCOVER_PLACE` with a scan-progress counter. Encourages players to scan everything.

### Z4 — Shelf Edge
The ground ends abruptly. The player walks to the edge and sees FOSSIL_SKY proper for the first time — a cathedral-scale chasm 500 m across with fossil structures suspended in midair by the same unknown force as the Gravity Well. Cinematic beat: camera pulls back to reveal the full scale.

**Narrative beat**: `FSK_EDGE_01` (auto, edge proximity): *"I need to stop saying ‘impossible’."*

**Discovery**: `DIS_FOSSIL_SKY_FIRST_VIEW` (auto-granted on edge approach — no scan needed).

**Exit**: Jump/climb down a HELIOS-bolted ladder onto the first FOSSIL_SKY platform. Level stream to `FOSSIL_SKY` map.

---

## Creatures
| Species | State Default | Count | Zone |
|---------|--------------|-------|------|
| Bone Crawler | Curious | 3–4 | Z2 |
| (Megafauna skeleton — non-hostile remains) | — | 1 | Z3 |

## Discoveries
| ID | Type | Zone |
|----|------|------|
| DIS_MEGAFAUNA_RIB | Scan | Z1 |
| DIS_FOSSIL_VERTEBRAE_COLUMN | Scan | Z2 |
| DIS_ANCIENT_KILL_SITE | Scan | Z3 |
| DIS_FOSSIL_SKY_FIRST_VIEW | Auto | Z4 edge |

## Hazards
| Type | Zone | Notes |
|------|------|-------|
| `ACeilingFragmentHazard` | Z2 | Loose fossil shard; one-shot |

## Checkpoints
| ID | Zone |
|----|------|
| `CHK_FOSSIL_SKY_UPPER_ENTRY` | Z1 |

## Notes
- Bone Crawler creature design: small (dog-sized), six-legged, white-translucent. `bIsAggressive = false`. It should feel curious, not threatening — the player’s first friendly-ish creature interaction.
- The phosphorescent bone lighting should make the zone feel eerily beautiful, not frightening. Fear comes from scale, not darkness.
- `FSK_EDGE_01` beat timing: fire when the player is within 3 m of the shelf edge and has been there for 1.5 s (let them take the view in first).
- HELIOS ladder at Z4 exit: functional geometry, no special component needed — player climbs via `UAbyssalTraversalComponent::BeginClimb`.
