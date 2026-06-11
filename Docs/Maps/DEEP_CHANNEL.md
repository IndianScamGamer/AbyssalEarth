# Map 02 — Deep Channel (Act 1 Transition)

## Overview
A narrow flooded passage connecting the open LUMINOUS_RIFT cavern to the upper approach of FOSSIL_SKY. The player’s first extended water segment — `UOxygenComponent` matters here. Short enough that base oxygen capacity handles it without upgrades, but tight enough to feel tense. The bioluminescence dims; the alien architecture grows denser and more structured.

## Dimensions
Linear + one branch — approximately 80 m long, 4–6 m diameter passage. Fully flooded main path; an air pocket alcove mid-route provides a breathing stop.

---

## Zones

### Z1 — Channel Mouth
Transition from LUMINOUS_RIFT. Stone arch covered in slow-pulsing organisms. Dry footing, then a 1 m ledge drop into the water. A wall-scan here gives `DIS_CHANNEL_CARVING` — geometric patterns etched into stone that’ll recur in FOSSIL_SKY and later maps.

**Checkpoint**: `CHK_DEEP_CHANNEL_ENTRY` placed before the water line. Activating it triggers an auto-save so the player doesn’t re-run LUMINOUS_RIFT on death.

### Z2 — Flooded Passage (Main)
Fully submerged. `UOxygenComponent::SetSubmerged(true)` fires here. Bioluminescent fish-analog creatures (passive Lantern Fin species) drift through. Swim corridor is 4 m wide — open enough to not feel like a tube but still directional.

**Hazard**: One `ASteamVentHazard` embedded in the passage wall (inactive at rest, cycles every 30 s) — teaches the player to watch for the Warning state particle glow before proceeding.

### Z3 — Air Pocket Alcove
A ceiling dome above water level, accessed by swimming up a short shaft. Air sphere restores oxygen. Props: ancient carved stone seat, a cracked alien vessel (scan: `DIS_ALIEN_VESSEL_FRAGMENT`), and a HELIOS maintenance drone in low-power mode (scavenge: 1× `ITEM_MINERAL_ABYSSAL_CORE`).

**Narrative beat**: `CHAN_AIR_01` (auto on surface): player character gasps and then notices the carvings.

### Z4 — Deeper Run
Second flooded stretch. Narrower, 2.5 m. A Depth Lurker egg cluster is visible (scan: `DIS_LURKER_EGG_CLUSTER`) but the creatures haven’t hatched — no combat. Mild thermal glow from below hints at the magma fields in MANTLE_GARDEN far beneath.

**Hazard**: `ACeilingFragmentHazard` — vibration from the thermal glow causes a ceiling chunk to fall as the player passes beneath. First one-shot physics hazard encounter.

### Z5 — Channel Exit
Emergence onto a wet stone shelf. Player surfaces; `UOxygenComponent::SetSubmerged(false)`. Another carved archway, this one intact, frames the ascending path to FOSSIL_SKY. Level stream trigger here.

---

## Creatures
| Species | State Default | Count | Zone |
|---------|--------------|-------|------|
| Lantern Fin | Passive | 6–8 | Z2, Z4 |
| (Depth Lurker eggs — non-hostile) | — | 1 cluster | Z4 |

## Discoveries
| ID | Type | Zone |
|----|------|------|
| DIS_CHANNEL_CARVING | Scan | Z1 |
| DIS_ALIEN_VESSEL_FRAGMENT | Scan | Z3 |
| DIS_LURKER_EGG_CLUSTER | Scan | Z4 |

## Hazards
| Type | Zone | Notes |
|------|------|-------|
| `ASteamVentHazard` | Z2 | Cyclic; first hazard the player encounters underwater |
| `ACeilingFragmentHazard` | Z4 | One-shot physics drop; respawn disabled |

## Checkpoints
| ID | Zone | Notes |
|----|------|-------|
| `CHK_DEEP_CHANNEL_ENTRY` | Z1 | Before water; blocks LUMINOUS_RIFT re-run |

## Notes
- Oxygen bar should visibly deplete during Z2 and Z4 — design the passage length so the player reaches Z3 with ~40% oxygen remaining. This creates tension without death.
- Lantern Fin creatures should slowly scatter when the player swims through them — not flee aggressively, just drift apart. `AAbyssalCreature::bIsAggressive = false`, low `CuriousSpeed`.
- The carvings in Z1 and Z5 are the same geometric pattern as the monolith array in LUMINOUS_RIFT Z4 — first hint of a designed, intentional architecture.
