# Map 05 — Gravity Well

## Overview

**Biome theme:** Orbital disorientation, tether discipline, controlled falling.
**Narrative position:** Act 3 — "Make the Machine Answer" — third full biome.
The player must reach the Gravity Well core to activate the first ancient
machine relay, proving the alien technology can be operated at all.

**Primary traversal:** floating platforms arranged in a loose vortex around a
blue-white gravitational core. Gravity direction rotates per platform cluster —
standing on the "floor" of one island means the next island's floor is a wall
from your perspective. A tether tool (unlocked entering this map) anchors you
to launch points and arrests falls.

**Visual identity (concept-art key notes):**
- Central blue-white core: sphere of compressed gravity light, diameter ~20 m.
- Platforms orbit in slow ellipses — they move, but slowly enough to plan.
- Each platform is a shard of ancient black basalt rimmed with amber rune-light.
- Void between platforms is not empty: faint particle streams spiral inward.
- Colour triad: deep blue-black void, electric blue core, amber rune trim.
- Scale cue: the core silhouette is visible from every platform — constant
  orientation anchor. Humans look like dust motes at distance.

**Signature hazard:** `AGravityShearHazard` (derives from `AAbyssalHazardBase`,
DamageMode=None, ActiveDuration causes a gravity-flip event that launches the
player off their current "floor" if not tethered). Warning = amber rune-light
pulses faster + low rumble. Active = directional gravity shear for 1.5 s.

**Traversal dependency:** this map requires C3 `UGravityModifierComponent` and
the tether tool. It is the highest-risk traversal system in the game — plan for
a dedicated Windows/PIE tuning pass before shipping this map.

---

## Zone Breakdown

### Zone 0 — Approach Shaft (entry)

**Purpose:** Controlled introduction to reduced/variable gravity before the
full orbital experience.
**Size:** 60 m vertical shaft, 10 m diameter.
**Key beats:**
- Transition from Fossil Sky's upper fissure: the shaft opens upward, player
  climbs into it and gravity gradually reduces (0.8g → 0.4g over 30 m).
- MERIDIAN: "Gravity cohesion is unstable here. Do not let go."
- Tether tool tutorial: one anchor point, short gap, mandatory before proceeding.
- `CHK_GW_00` at shaft top (entry to orbital space).
- Discovery: `D_Anomaly_GravityGradient` (scan the transition zone where gravity
  noticeably shifts — the scanner readout spikes anomalously).

**Hazard:** none — controlled tutorial space.

---

### Zone 1 — Inner Ring

**Purpose:** First orbital experience; close platforms, forgiving gaps.
**Size:** Ring of 6 platforms, ~25 m orbit radius from core, 30 m drop gaps.
**Key beats:**
- All platforms share the same gravity orientation (toward core) — reassuringly
  like a floor, just curved.
- Two tether jumps required between platforms; gaps are 8–12 m.
- First amber rune puzzle: scan three rune-lit panels in sequence to unlock the
  path inward (early use of scanner outside discovery context).
- `CHK_GW_01` after completing the rune sequence.
- Discoveries: `D_AlienTech_RuneConduitPanel` (one of the three panels; scan
  gives first hint of machine language structure);
  `D_Geo_BasaltShard_Orbital` (geology note — these are fragments of a real
  seabed formation, now suspended).

---

### Zone 2 — The Reorientation Passage

**Purpose:** Introduce full gravity reorientation — the defining mechanic.
**Size:** 3 platform "rooms", each with a different gravity direction relative
to the player's path of travel.
**Key beats:**
- Room A: gravity down (normal). Room B: gravity rotates 90° as player crosses
  threshold — "floor" becomes "wall". Room C: gravity rotates another 90° —
  player walks on what was the ceiling.
- Transition zones use `AReorientationVolume` (C3); the rotation is smooth
  (0.5 s lerp) to avoid disorientation nausea.
- `AGravityShearHazard` first appearance: one instance in Room C, with long
  Warning duration (3.5 s) so the player can learn to tether before it fires.
- MERIDIAN: "The colonists built this. They moved through it as naturally as
  breathing. We are very far from their level."
- `CHK_GW_02` after Room C.
- Discovery: `D_AlienTech_ReorientationGlyph` (glyph at the Room B/C boundary
  that seems to *label* the gravity direction — alien wayfinding system).

---

### Zone 3 — Mid-Ring Debris Field

**Purpose:** Chaotic traversal; pressure from moving hazards.
**Size:** 60 m span, 12 loose debris platforms plus 4 anchored ones.
**Key beats:**
- Loose debris platforms orbit slowly and occasionally drift — tether-launch
  between them requires timing.
- `AGravityShearHazard` instances × 4 (staggered via `bRandomizeInitialPhaseOffset`)
  — player must time crossings around the shear pulses.
- One debris shard has a MERIDIAN data burst on it (audio log): expedition
  leader describes the core as "breathing" on a 47-minute cycle.
- `CHK_GW_03` at the last anchored platform.
- Discoveries: `D_Anomaly_OrbitalDebrisPattern` (the debris orbit is not random —
  it matches a mathematical sequence; anomaly category);
  `D_AlienTech_AnchorRune` (rune on an anchored platform — same script as the
  conduit panels, different glyph class).

---

### Zone 4 — The Core Antechamber

**Purpose:** Pre-boss decompression; reinforce the scale of the core.
**Size:** Single large platform 40 × 30 m, directly facing the core at 15 m.
**Key beats:**
- The core is visible in full here — massive, humming, pulsing blue-white.
- MERIDIAN: "The relay activation point is in the core structure itself. I
  cannot tell you how to enter. I can only tell you the frequency."
- Environmental storytelling: scattered expedition gear (frayed harness, a cracked
  helmet) — the previous team made it here.
- `CHK_GW_04` on arrival.
- Discoveries: `D_Structure_AbandonedHarness` (`EDiscoveryCategory::HumanMade` —
  confirms prior expedition reached this point);
  `D_AlienTech_CorePulsePattern` (scan the core from here — the pulse pattern
  encodes the relay frequency MERIDIAN needs).

---

### Zone 5 — Core Entry & Relay Activation (story anchor)

**Purpose:** Act 3 climax beat — operate the first ancient machine.
**Size:** Core interior, 30 m diameter, gravity points toward inner surface
(centrifugal shell — player walks the inside of a sphere).
**Key beats:**
- Entry: tether from Antechamber to the core aperture; gravity transitions to
  centrifugal shell on crossing the threshold.
- Six relay nodes arranged around the inner equator — player must scan-activate
  all six in sequence (each `IAbyssalInteractable`, hold-duration 1.5 s).
- On final activation: machine sound, amber light floods the core interior,
  MERIDIAN: "It responded. It is listening."
- Brief gravity surge shakes all platforms — visual only, no damage.
- `CHK_GW_05` on activation complete.
- Discovery: `D_AlienTech_RelayNode_Primary` (the central relay node; scan after
  activation reveals power-routing data pointing toward the Mantle Garden).

---

### Zone 6 — Descent Corridor (exit)

**Purpose:** Exit from the core; foreshadow Mantle Garden heat.
**Size:** 40 m descent shaft, gravity normalises as player descends.
**Key beats:**
- Gravity restores to 1g over 20 m (opposite of the entry shaft).
- Temperature noticeably rises — scanner detects heat bloom from below.
- MERIDIAN: "The next relay is deeper. I can already feel the heat from here."
- `CHK_GW_06` at bottom — map complete; autosave.
- Discovery: `D_Geo_ThermalConvectionSeam` (geological seam in the shaft wall
  carrying heat up from the Mantle Garden — bridges the two biomes).

---

## Discovery Catalog Rows

> Add to `Content/Design/DiscoveryCatalog.csv`.

```
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

---

## Checkpoint List

| ID | Location | Trigger |
|---|---|---|
| `CHK_GW_00` | Zone 0 shaft top | `AObjectiveTriggerActor` |
| `CHK_GW_01` | Zone 1 rune sequence complete | Objective complete callback |
| `CHK_GW_02` | Zone 2 after Room C | `AObjectiveTriggerActor` |
| `CHK_GW_03` | Zone 3 last anchored platform | `AObjectiveTriggerActor` |
| `CHK_GW_04` | Zone 4 antechamber arrival | `AObjectiveTriggerActor` |
| `CHK_GW_05` | Zone 5 relay activation | Objective complete callback |
| `CHK_GW_06` | Zone 6 descent bottom / map exit | `AObjectiveTriggerActor` (autosave) |

---

## Objective Sequence

> Add to `Content/Design/MainObjectiveArc.csv`.

```
OBJ_GW_ENTER,       "Reach the Gravity Well orbital space",   GRAVITY_WELL, false
OBJ_GW_INNER_RING,  "Cross the inner orbital ring",           GRAVITY_WELL, false
OBJ_GW_ANTECHAMBER, "Reach the core antechamber",             GRAVITY_WELL, false
OBJ_GW_ACTIVATE,    "Activate the six relay nodes",           GRAVITY_WELL, false
OBJ_GW_EXIT,        "Descend to the Mantle Garden approach",  GRAVITY_WELL, false
```

---

## Hazard Derivation Notes

### `AGravityShearHazard : AAbyssalHazardBase`

```cpp
// DamageMode = EHazardDamageMode::None
// IdleDuration = 8.0f (bRandomizeInitialPhaseOffset=true staggers instances)
// WarningDuration = 2.0f (3.5f for Zone 2 tutorial instance)
// ActiveDuration = 1.5f (shear window — tethered players are safe)
// CooldownDuration = 3.0f
//
// Active phase: Blueprint applies a temporary force impulse to un-tethered pawns
// via LaunchCharacter() pointing away from local "floor" normal.
// OnHazardWarning: rune-light on nearby platforms pulses faster (material param).
// OnHazardActive: directional wind VFX + rumble camera shake.
// Detection: overlap sphere on hazard actor tracks tethered vs un-tethered pawns
// (query the tether tool's bIsTethered bool via IAbyssalInteractable query or
// a dedicated ITetherTarget interface — design TBD in C3).
```

---

## Traversal System Notes (C3 dependency)

### `AReorientationVolume` (C3)

Volumes placed at platform thresholds that smoothly lerp the pawn's gravity
direction over 0.5 s. Blueprint must fade-rotate the camera's roll and update
the character movement component's `GravityScale` direction vector.

### Tether Tool (C3)

A holdable/equippable actor that fires a projectile anchoring to tagged surfaces.
When tethered, the player is immune to gravity shear and can zip-launch to the
anchor point. Blueprint-implementable; C++ provides `bIsTethered` state and the
physics constraint setup.

### Designer Notes

- **Platform drift:** implement as slow, looping spline movement on platform actors
  (no physics — deterministic, predictable for the player).
- **Core interior gravity:** use a gravity field component that overrides
  `UCharacterMovementComponent::GravityDirection` based on the vector from the
  pawn to the core surface normal.
- **Fall safety:** a `ADeathVolume` / damage volume at the outermost void boundary;
  the fall distance from an unanchored platform is lethal to keep stakes real.

---

## Asset Manifest (stub)

| Slot | Target Path | Notes |
|---|---|---|
| Basalt platform shard | `Content/Environment/GravityWell/SM_GW_Platform_Shard_*` | A/B/C variants, 3 sizes |
| Core sphere (dynamic) | `Content/Environment/GravityWell/BP_GW_CoreSphere` | Pulsing material + light |
| Amber rune panel | `Content/Environment/GravityWell/SM_GW_RunePanel` | Emissive rune channels |
| Tether anchor point | `Content/Environment/GravityWell/SM_GW_AnchorRing` | |
| Orbital particle stream | `Content/VFX/GravityWell/NS_GW_OrbitalStream` | Niagara spiral |
| Gravity shear VFX | `Content/VFX/GravityWell/NS_GW_GravityShear` | Directional distortion |

---

## Backend Hooks Required

| Feature | Depends on | Status |
|---|---|---|
| Gravity shear hazard | C2 `AAbyssalHazardBase` | C2 authored |
| Reorientation volumes | C3 `AReorientationVolume` | C3 not yet authored |
| Tether tool | C3 traversal system | C3 not yet authored |
| Relay node interaction | A3 `IAbyssalInteractable` | A3 authored |
| Rune panel sequence | A3 `IAbyssalInteractable` | A3 authored |
| Discovery actors | `ADiscoveryActor` + `UDiscoverySubsystem` | Exists |
| Autosave on exit | A1 `UAbyssalSaveSubsystem` | A1 in progress this tick |
