# Map 05 — Gravity Well

## Overview

**Biome theme:** Orbital disorientation, tether discipline, controlled falling.
**Narrative position:** Act 3 — "Make the Machine Answer" — third full biome.
The player reaches the Gravity Well core to activate the first ancient machine relay.

**Primary traversal:** floating platforms in a vortex around a blue-white core.
Gravity direction rotates per platform cluster. A tether tool arrests falls and
enables zip-launches.

**Visual identity:**
- Central blue-white core sphere, ~20 m diameter.
- Platforms: ancient black basalt shards rimmed with amber rune-light.
- Faint particle streams spiral inward through the void.
- Colour triad: deep blue-black void, electric blue core, amber rune trim.

**Signature hazard:** `AGravityShearHazard` (derives from `AAbyssalHazardBase`,
DamageMode=None, launches un-tethered pawns off their current floor).

**C3 dependency:** `AReorientationVolume` + tether tool required. Highest-risk
traversal system — plan a dedicated Windows/PIE tuning pass.

---

## Zone Breakdown

### Zone 0a — Parkour Approach Corridor (pre-entry)
**Purpose:** Introduce the gravity pull threat through active parkour before the player reaches the shaft. A 120 m winding descent corridor where gravity subtly increases and ceiling debris pulls upward.
- Crumbling stone ledges at various angles requiring precision jumps and mantling.
- 6 tethered floating rocks (SM_GW_TetherRock_A): basalt shards 2-5m across, chained to cave walls by iron cables. They drift and sway on their tethers. Player can fire tether at them to swing across gaps or arrest a fall.
- No platform mechanics yet — this is pure parkour and spatial reading.
- The gravity shear starts mild (0.95g) and reaches 0.7g at the corridor's end, causing jumps to arc strangely.
- MERIDIAN: "Your suit's gravity sensors are reading an anomaly below. Proceed carefully."
- `CHK_GW_00a` (pre-shaft). Discovery: `D_Human_AbandonedParkourRig` — frayed personal tether harness and chalk marks left by a previous expedition member; evidence of the same route.

### Zone 0 — Approach Shaft (entry)
**Purpose:** Introduce reduced gravity + tether tutorial. 60 m shaft, 10 m diameter.
- Gravity: 0.8g → 0.4g over 30 m. Mandatory tether tutorial before proceeding.
- MERIDIAN: "Gravity cohesion is unstable here. Do not let go."
- `CHK_GW_00`. Discovery: `D_Anomaly_GravityGradient`.

### Zone 1 — Inner Ring
**Purpose:** First orbital space; 6 platforms, same gravity orientation.
- Two tether jumps. Amber rune panel puzzle (3 panels in sequence).
- `CHK_GW_01`. Discoveries: `D_AlienTech_RuneConduitPanel`, `D_Geo_BasaltShard_Orbital`.

### Zone 2 — The Reorientation Passage
**Purpose:** Introduce gravity reorientation. 3 rooms, each rotated 90°.
- `AReorientationVolume` at thresholds (0.5 s lerp). First `AGravityShearHazard` (WarningDuration=3.5f).
- MERIDIAN: "The colonists built this. We are very far from their level."
- `CHK_GW_02`. Discovery: `D_AlienTech_ReorientationGlyph`.

### Zone 3 — Mid-Ring Debris Field
**Purpose:** Timing + moving hazards. 12 drifting platforms + 4 anchored.
- 4 staggered `AGravityShearHazard` instances. MERIDIAN audio log: core breathes on 47-min cycle.
- `CHK_GW_03`. Discoveries: `D_Anomaly_OrbitalDebrisPattern`, `D_AlienTech_AnchorRune`.

### Zone 4 — The Core Antechamber
**Purpose:** Full core reveal. Single 40 × 30 m platform facing core at 15 m.
- Scattered expedition gear. MERIDIAN: "I can only tell you the frequency."
- `CHK_GW_04`. Discoveries: `D_Structure_AbandonedHarness`, `D_AlienTech_CorePulsePattern`.

### Zone 5 — Core Entry & Relay Activation (story anchor)
**Purpose:** Act 3 climax. 30 m sphere interior, centrifugal-shell gravity.
- 6 relay nodes (each `IAbyssalInteractable`, hold 1.5 s). All six → MERIDIAN: "It responded. It is listening."
- `CHK_GW_05`. Discovery: `D_AlienTech_RelayNode_Primary`.

### Zone 6 — Descent Corridor (exit)
**Purpose:** Exit; foreshadow Mantle Garden heat. 40 m shaft, gravity restores to 1g.
- Scanner detects heat bloom. MERIDIAN: "The next relay is deeper. I can already feel the heat."
- `CHK_GW_06` (autosave). Discovery: `D_Geo_ThermalConvectionSeam`.

---

## Tethered Floating Object Mechanic

**SM_GW_TetherRock_A/B** are floating basalt shards physically chained to cave anchor points by heavy iron cables (1.5-3m chain length). They drift in slow arcs on their tethers — not random, but following the gravity field's orbital influence. Visual behavior:
- The chain hangs slack when the object is close to its anchor rest position.
- The chain pulls taut when the object drifts to chain limit.
- Amber rune marks on the anchor bolts (alien installation — the colonists used these for traversal too).

**Player interaction:**
- Fire tether at the rock → tether attaches to the iron ring mount on the rock's face.
- While tethered to a drifting rock: the rock's momentum carries the player (swing across gap, descend controlled, use as moving platform).
- Release tether: the rock continues its drift, player releases.
- Stack mechanic: tether to Rock A → swing to Rock B → tether to Rock B → chain-swing.
- Risk: if a Rock swings into a shear hazard zone, it carries the player with it.

**Blueprint actor:** `BP_GW_TetherRock` (derives from `AAbyssalInteractable`). Uses a PhysicsConstraint with angular limit for the chain swing arc. Chain length configurable per instance (150-300 cm).

---

## Discovery Catalog Rows

```
D_Human_AbandonedParkourRig,    HumanMade, GW_00a, Personal tether harness and chalk route marks — a previous expedition member cleared this approach
D_Anomaly_GravityGradient,      Anomaly,   GW_00, Measurable gravity reduction over 30 m — no natural geological cause
D_AlienTech_RuneConduitPanel,   AlienTech, GW_01, Amber rune panel; activating three in sequence unlocks the inner ring
D_Geo_BasaltShard_Orbital,      Geology,   GW_01, Seabed basalt fragment now suspended in orbital path around the core
D_AlienTech_ReorientationGlyph, AlienTech, GW_02, Alien wayfinding glyph labelling the gravity-direction transition point
D_Anomaly_OrbitalDebrisPattern, Anomaly,   GW_03, Debris orbit follows a non-random mathematical sequence
D_AlienTech_AnchorRune,         AlienTech, GW_03, Rune on an anchored platform; different glyph class from conduit panels
D_Structure_AbandonedHarness,   HumanMade, GW_04, Frayed expedition tether harness — the previous team reached this point
D_AlienTech_CorePulsePattern,   AlienTech, GW_04, Core pulse encodes the relay activation frequency MERIDIAN needs
D_AlienTech_RelayNode_Primary,  AlienTech, GW_05, Central relay node; post-activation scan reveals Mantle Garden routing
D_Geo_ThermalConvectionSeam,    Geology,   GW_06, Heat-carrying geological seam rising from the Mantle Garden below
```

## Checkpoint List

| ID | Location | Trigger |
|---|---|---|
| `CHK_GW_00a` | Zone 0a corridor end | `AObjectiveTriggerActor` |
| `CHK_GW_00` | Zone 0 shaft top | `AObjectiveTriggerActor` |
| `CHK_GW_01` | Zone 1 rune sequence | Objective complete callback |
| `CHK_GW_02` | Zone 2 after Room C | `AObjectiveTriggerActor` |
| `CHK_GW_03` | Zone 3 last platform | `AObjectiveTriggerActor` |
| `CHK_GW_04` | Zone 4 antechamber | `AObjectiveTriggerActor` |
| `CHK_GW_05` | Zone 5 relay activation | Objective complete callback |
| `CHK_GW_06` | Zone 6 bottom / map exit | `AObjectiveTriggerActor` (autosave) |

## Objective Sequence

```
OBJ_GW_ENTER,       "Reach the Gravity Well orbital space",  GRAVITY_WELL, false
OBJ_GW_INNER_RING,  "Cross the inner orbital ring",          GRAVITY_WELL, false
OBJ_GW_ANTECHAMBER, "Reach the core antechamber",            GRAVITY_WELL, false
OBJ_GW_ACTIVATE,    "Activate the six relay nodes",          GRAVITY_WELL, false
OBJ_GW_EXIT,        "Descend to the Mantle Garden approach", GRAVITY_WELL, false
```

## Hazard Derivation Notes

### `AGravityShearHazard : AAbyssalHazardBase`
```cpp
// DamageMode = None; IdleDuration = 8.0f (randomized); WarningDuration = 2.0f (3.5f tutorial)
// ActiveDuration = 1.5f; CooldownDuration = 3.0f
// Active: Blueprint LaunchCharacter() on un-tethered pawns away from floor normal.
// Warning: rune-light material param pulses faster.
```

## Asset Manifest (stub)

| Slot | Target Path |
|---|---|
| Basalt platform shard | `Content/Environment/GravityWell/SM_GW_Platform_Shard_*` |
| Core sphere | `Content/Environment/GravityWell/BP_GW_CoreSphere` |
| Amber rune panel | `Content/Environment/GravityWell/SM_GW_RunePanel` |
| Orbital particle stream | `Content/VFX/GravityWell/NS_GW_OrbitalStream` |
| Gravity shear VFX | `Content/VFX/GravityWell/NS_GW_GravityShear` |
| Tether rock shard A | `Content/Environment/GravityWell/SM_GW_TetherRock_A` |
| Tether rock shard B | `Content/Environment/GravityWell/SM_GW_TetherRock_B` |
| Parkour approach ledge | `Content/Environment/GravityWell/SM_GW_ParkourLedge_A` |
| Tether anchor post | `Content/Environment/GravityWell/SM_GW_TetherAnchorPost_A` |
