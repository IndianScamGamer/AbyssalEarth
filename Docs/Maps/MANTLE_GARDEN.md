# Mantle Garden — Map 06 Design Blockout

**Act:** 4 — Touch the Root  
**Entry:** from Gravity Well (Map 05) via Descent Corridor  
**Exit:** Root Conduit endgame chamber (Act 5 transition / credits)  
**Theme:** Primordial heat, extremophile bioluminescence, ancient colonist presence, Gate revelation  
**Gravity:** 1.0g (restored from Gravity Well variable gravity)

---

## Story Beat

The player descends from the activated Gravity Well relay into rising heat. The "Mantle Garden" is a 30,000-year-old bioluminescent ecosystem of sulfur-metabolizing extremophiles that flourishes at the mantle boundary — alien life that has never seen sunlight.

Midway through: abandoned colonist thermal suits and equipment logs confirm the colonists descended this deep deliberately. Their Day 14 log describes a "Gate" that responded to the third relay key.

Climax: the player activates the second relay in the Root Conduit. MERIDIAN delivers the central revelation.

> **MERIDIAN:** *"The colonists did not create the Rift. They found the Gate, already open, and tried to seal it. The relay is a lock. You are holding the key. And the Gate... the Gate is listening."*

---

## Zone Breakdown

### Z0 — Descent Corridor (Linear, ~120 m)

Entry from Gravity Well. Gravity ramps from 0.8g back to 1.0g over the first 30 m. Heat shimmer VFX, rising temperature audio. Steam vents line left and right walls alternately — stay center to avoid Overlap damage.

**Hazards:** `ASteamVentHazard` × 4 (alternating walls, staggered so left and right never fire simultaneously)  
- `DamageMode = Overlap`, `DPS = 20`  
- `IdleDuration = 2.0`, `WarningDuration = 1.0`, `ActiveDuration = 3.0`, `CooldownDuration = 5.0`  
- Right-wall vents: `bRandomizeInitialPhaseOffset = false`, `InitialPhaseOffset = 5.5` to stagger with left-wall cycle

**Checkpoint:** `CHK_MG_00`

---

### Z1 — Obsidian Shelf (Open Platforming, ~200 m²)

First view of the magma lake 80 m below — wide establishing shot. Three obsidian platform tiers step down toward the lake edge. Six fissures erupt as magma geysers on independent timers.

**Hazards:** `AMagmaGeyserHazard` × 6  
- `DamageMode = Radial`, `DamageRadius = 150`, `DPS = 80`  
- `IdleDuration = 4.0`, `WarningDuration = 1.5`, `ActiveDuration = 2.0`, `CooldownDuration = 6.0`  
- `bRandomizeInitialPhaseOffset = true` — geysers fire independently, not in sync  
- Visual: red ground-crack warning → magma column eruption, radiant heat distortion

**Discovery:** `DISC_MG_OBSIDIAN_FLOW` (Geology) — *"Obsidian flow predates the colonist occupation by 11,000 years. Whatever the Rift opened, this rock was here long before them."*

**Checkpoint:** `CHK_MG_01`

---

### Z2 — Thermal Garden (Exploration, ~400 m²)

Dense bloom field — bioluminescent organisms 2–5 m tall, emitting magenta and amber light. Heat-tolerance mechanic introduced: `UHeatMeterComponent` gauge fills as the player stands in open heat; standing within 4 m of a `AMantleBloomActor` slows the fill rate (passive aura via overlap primitive). Three routed segments force the player to path through bloom clusters.

**Hazards:** None discrete — heat meter buildup is the threat.

**Discoveries:**  
- `DISC_MG_BLOOM_ANALYSIS` (Flora) — *"Metabolism: sulfur oxidation. No chlorophyll. No surface dependency. An entire ecology that has never seen sunlight."*  
- `DISC_MG_BLOOM_AGE` (Flora) — *"Carbon signature consistent with 30,000+ years of continuous growth. Pre-human. Pre-Rift. Pre-everything we brought here."*  
- `DISC_MG_COLONIST_SAMPLE` (Artifact) — *"Colonist-manufactured sample container. Heat-rated to 2,400°C. Someone took a sample. They knew what was down here."*

**Checkpoint:** `CHK_MG_02`

---

### Z3 — Magma Crossing (Timed Platforming, 3 bridge segments)

Active lava river, 80 m wide. Three obsidian bridge segments cross it; 4 m gaps between segments. Magma pulse hazards sweep rolling walls of heat damage across each bridge on a 15 s cycle, staggered 5 s apart — each bridge pulses in sequence, giving the player a 10 s window per bridge to cross before the next pulse.

**Hazards:** `AMagmaPulseHazard` × 3 (one per bridge)  
- `DamageMode = Overlap` (full bridge volume), `DPS = 120`  
- `IdleDuration = 11.0`, `WarningDuration = 3.0`, `ActiveDuration = 0.5`, `CooldownDuration = 0.5` — total cycle: 15 s  
- `bRandomizeInitialPhaseOffset = false`  
- Bridge 1: `InitialPhaseOffset = 0.0` · Bridge 2: `InitialPhaseOffset = 5.0` · Bridge 3: `InitialPhaseOffset = 10.0`  
- Visual: orange heat-shimmer warning 3 s prior; magma wave sweeps full bridge length

**Discovery:** `DISC_MG_LAVA_COMPOSITION` (Geology) — *"Iron-rich. Anomalous isotope ratios. This magma is not native to this stratum. Something is producing heat from below."*

**Checkpoint:** `CHK_MG_03`

---

### Z4 — Root Vestibule (Narrative Chamber, ~150 m²)

Colonist-cut stone chambers, not natural. Abandoned thermal equipment: suits on racks, sealed containers, instrument panels. MERIDIAN reads equipment logs aloud as the player approaches each station.

**Hazards:** None.

**Discoveries:**  
- `DISC_MG_THERMAL_SUIT` (Artifact) — *"Mark IV Thermal Suit. Serial RFT-4481. Rated 90 minutes at core-adjacent temperature. Fifty-one suits found. Fifty-one descended. None returned."*  
- `DISC_MG_EQUIPMENT_LOG` (Artifact) — MERIDIAN reads: *"Day 14. The Gate responded to the third key. Full resonance in 48 hours. The seal must hold. The seal must hold."*  
- `DISC_MG_COLONIST_SEAL_DIAGRAM` (Artifact) — *"Schematic: six-point resonance seal. The node arrangement matches the relay configuration of the Gravity Well core exactly."*

**Objective:** `OBJ_MG_FIND_EQUIPMENT` — Read the colonist logs

**Checkpoint:** `CHK_MG_04`

---

### Z5 — Garden Core (Dense Traversal, ~300 m²)

The thickest bloom cluster — pillars of bioluminescent life 30 m tall. Heat is extreme in open spaces; the player routes between bloom safe-zones. Geological pressure from above causes periodic ceiling fragment drops in the open lanes.

**Hazards:** `ACeilingFragmentHazard` × 5  
- `DamageMode = Radial`, `DamageRadius = 80`, `DPS = 40`  
- `WarningDuration = 1.2`, `ActiveDuration = 0.3`, `CooldownDuration = 12.0`  
- `bRandomizeInitialPhaseOffset = true`

**Discoveries:**  
- `DISC_MG_GARDEN_CENTER` (Flora) — *"The central bloom cluster is a single organism. Thirty thousand years of continuous growth. Four hundred square meters. Older than the Rift."*  
- `DISC_MG_GATE_SIGNAL` (Enigma) — *"MERIDIAN: The blooms are resonating at the same frequency as the relay nodes. They have been for 30,000 years. The Garden is not just surviving near the Gate. It is responding to it."*

**Checkpoint:** `CHK_MG_05`

---

### Z6 — Root Conduit (Climax Chamber, ~250 m²)

The deepest point in the game. A vast spherical chamber. The Gate: an ancient seal-ring 40 m across, embedded in the mantle wall, matching the colonist schematic exactly. Six relay nodes at the seal vertices. The player activates the second relay — nodes light in sequence, seal-ring resonates. MERIDIAN's climactic revelation plays over the activation.

> **MERIDIAN:** *"The colonists did not create the Rift. They found the Gate, already open, and tried to seal it. The relay is a lock. You are holding the key. And the Gate... the Gate is listening."*

**Hazards:** None discrete — heat meter continues (ambient tension).

**Discovery:** `DISC_MG_THE_GATE` (Enigma) — *"The Gate. Older than the planet. Older than the Rift. The Rift is not a wound in the world. It is a door. And something on the other side has been waiting."*

**Objective:** `OBJ_MG_ACTIVATE_RELAY` — Activate the relay

**Checkpoint:** `CHK_MG_06` (final checkpoint — triggers Act 5 transition or credits roll)

---

## Discovery Catalog (11 entries)

| ID | Zone | Category | Short Description |
|---|---|---|---|
| `DISC_MG_OBSIDIAN_FLOW` | Z1 | Geology | Obsidian predates colonists by 11,000 years |
| `DISC_MG_BLOOM_ANALYSIS` | Z2 | Flora | Sulfur-metabolizing extremophile ecosystem |
| `DISC_MG_BLOOM_AGE` | Z2 | Flora | 30,000+ years old; pre-human, pre-Rift |
| `DISC_MG_COLONIST_SAMPLE` | Z2 | Artifact | Heat-rated sample container; someone sampled the blooms |
| `DISC_MG_LAVA_COMPOSITION` | Z3 | Geology | Anomalous isotopes; non-native heat source below |
| `DISC_MG_THERMAL_SUIT` | Z4 | Artifact | 51 suits; none returned |
| `DISC_MG_EQUIPMENT_LOG` | Z4 | Artifact | Day 14 log — Gate responded, seal must hold |
| `DISC_MG_COLONIST_SEAL_DIAGRAM` | Z4 | Artifact | Six-point resonance seal schematic |
| `DISC_MG_GARDEN_CENTER` | Z5 | Flora | Single organism, 400 m², 30,000 years old |
| `DISC_MG_GATE_SIGNAL` | Z5 | Enigma | Blooms resonating at relay frequency for 30,000 years |
| `DISC_MG_THE_GATE` | Z6 | Enigma | The Gate: ancient seal — not a wound, a door |

---

## Objective Sequence

| ID | Zone | Description |
|---|---|---|
| `OBJ_MG_ENTER` | Z0 | Descend into the Mantle Garden |
| `OBJ_MG_CROSS` | Z3 | Cross the Magma River |
| `OBJ_MG_FIND_EQUIPMENT` | Z4 | Read the colonist logs |
| `OBJ_MG_REACH_CONDUIT` | Z5 | Reach the Root Conduit |
| `OBJ_MG_ACTIVATE_RELAY` | Z6 | Activate the relay |

---

## Checkpoint Map

| ID | Zone | Notes |
|---|---|---|
| `CHK_MG_00` | Z0 | End of descent corridor; gravity fully restored to 1.0g |
| `CHK_MG_01` | Z1 | After clearing obsidian shelf |
| `CHK_MG_02` | Z2 | After completing thermal garden route |
| `CHK_MG_03` | Z3 | After magma crossing |
| `CHK_MG_04` | Z4 | After reading colonist logs |
| `CHK_MG_05` | Z5 | Before root conduit entrance |
| `CHK_MG_06` | Z6 | After relay activation (final; triggers Act 5 or credits) |

---

## C3 Risk Flags

| Component | Risk | Note |
|---|---|---|
| `UHeatMeterComponent` | Medium | New vital UI component; needs HUD wire-up and drain/recover curve design |
| `AMantleBloomActor` | Low | Passive overlap buff zone; use `AAbyssalHazardBase` proximity base with DamageMode=None + inverse logic |
| Steam vent stagger | Low | `InitialPhaseOffset` on right-wall `ASteamVentHazard` pairs; verify via PIE timer log |
| Magma pulse timing | Medium | 15 s cycle, 3 bridges 5 s apart; player needs ≤10 s per bridge — requires playtesting for pacing |

---

## Implementation Notes

All discrete hazards are `AAbyssalHazardBase` derivations:

| Hazard Class | DamageMode | Radius | DPS | Idle | Warning | Active | Cooldown |
|---|---|---|---|---|---|---|---|
| `ASteamVentHazard` | Overlap | — | 20 | 2.0 | 1.0 | 3.0 | 5.0 |
| `AMagmaGeyserHazard` | Radial | 150 | 80 | 4.0 | 1.5 | 2.0 | 6.0 |
| `AMagmaPulseHazard` | Overlap | — | 120 | 11.0 | 3.0 | 0.5 | 0.5 |
| `ACeilingFragmentHazard` | Radial | 80 | 40 | — | 1.2 | 0.3 | 12.0 |

`AMagmaGeyserHazard`: `bRandomizeInitialPhaseOffset = true`.  
`AMagmaPulseHazard`: `bRandomizeInitialPhaseOffset = false`; explicit `InitialPhaseOffset` per bridge (0 / 5.0 / 10.0 s).  
`ACeilingFragmentHazard`: reused from Fossil Sky unchanged.  
`ASteamVentHazard`: new; Overlap damage, alternating-wall stagger via `InitialPhaseOffset`.
