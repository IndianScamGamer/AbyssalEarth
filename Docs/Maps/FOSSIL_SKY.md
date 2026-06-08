# Map 04 — Fossil Sky

## Overview

**Biome theme:** Petrified ceiling, deep-time geology, silent weight.
**Narrative position:** Act 2 — "Read the Bones" — second full biome after
Glassroot Forest. MERIDIAN sends you here to date a bone-strata formation that
could establish the true age of the Rift colonization event.

**Primary traversal:** narrow ledge-walks beneath a vast fossil ceiling, with
bridge sections made of layered bone-plate — brittle and collapse-prone.
The danger is falling, not burning; silence and patience replace the urgency
of the Mantle Garden approach. Gravity here is normal but the floor is not.

**Visual identity (concept-art key notes):**
- Ceiling-dominant composition: massive fossil arches hang 40–80 m above floor.
- Amber-to-ochre palette for stone; pale-bone ivory for fossil inclusions.
- Tight directional shafts of light from micro-fissures — pools of amber in dark.
- No bioluminescence; light is geological (fissures, reflected amber).
- Scale cue: single human silhouette dwarfed by one rib arch, 12+ m diameter.

**Signature hazard:** `ABrittleWalkwaySection` (derives from `AAbyssalHazardBase`,
DamageMode = None, ActiveDuration drives a floor-collapse animation; player must
sprint across or fall). Warning phase = hairline-crack VFX + audible creaking.

---

## Zone Breakdown

### Zone 0 — Ossuary Passage (entry)

**Purpose:** Landing and reorientation after tunnel from Glassroot.
**Size:** 30 × 10 m corridor.
**Key beats:**
- MERIDIAN briefing hologram: "If the strata age confirms what I suspect, the
  Rift has been inhabited for 4,000 years."
- First fossil arch visible through the exit aperture — establishes scale.
- `CHK_FS_00` checkpoint on entry.
- One `D_Geo_StratumColumn` discovery actor (roadmap C4 data row, see below).

**Hazard:** none — safe landing buffer.

---

### Zone 1 — The Underpalate

**Purpose:** First vertical reveal; introduce the brittle-floor mechanic.
**Size:** 60 × 40 m floor with 20 m ceiling clearance.
**Key beats:**
- Floor is a mosaic of solid limestone patches and grey bone-plate sections
  (visually identical until weight is applied — first-time ambush of expectation).
- Tutorial: first `ABrittleWalkwaySection` (short, 4 m, falls 1 m — survivable,
  teaches the pattern without killing). Warning = 1 s creak; Active = collapse.
- Large fossil mural in ceiling: array of interlocked creatures, clearly
  non-terrestrial anatomy.
- `CHK_FS_01` after crossing first brittle section.
- Discovery: `D_Geo_BoarFossilMural` (ceiling scan; spawns with `bRequiresLook=true`,
  so player must look up — reinforces ceiling-dominant framing).

---

### Zone 2 — Rib Corridor

**Purpose:** Signature visual setpiece; narrow navigation under fossil ribs.
**Size:** 80 m long × 8 m wide ledge path; ribs span overhead every 15 m.
**Key beats:**
- Path: left-hugging ledge above a 20 m drop to a dry fossil riverbed.
- Three `ABrittleWalkwaySection` bridges break the ledge path — each longer
  than the last (4 m → 8 m → 14 m) escalating stakes.
- Mid-corridor alcove: MERIDIAN audio log — expedition team dated this formation
  "inconsistently" before going dark.
- `CHK_FS_02` at alcove.
- Discoveries: `D_Geo_SpineFossilArch` (left rib cluster);
  `D_Anomaly_DataTagOnBone` (modern data tag embedded 3 m into ancient stratum —
  anomaly, raises the question "who was here?").
- **Designer note:** the 14 m final bridge must give the player 4–5 s in Warning
  before collapse — tune `WarningDuration=4.5f` on this specific instance.

---

### Zone 3 — The Dating Chamber (story anchor)

**Purpose:** Core narrative beat — scan the formation, receive the age reveal.
**Size:** 40 × 40 m chamber, cathedral ceiling 80 m up.
**Key beats:**
- Central plinth: a bone stratum exposed like a geologist's cross-section, lit
  by a single fissure beam directly from above.
- Scan interaction (`IAbyssalInteractable` → triggers `UObjectiveSubsystem::
  CompleteObjective("OBJ_FS_DateStrata")`).
- On scan complete: MERIDIAN voice — "4,327 years. Before the Rift was sealed.
  The colonists didn't cause the Rift. *They were already inside.*"
- Camera briefly looks upward (Blueprint cinematic impulse — player retains
  control but look-input is overridden for 2 s).
- `CHK_FS_03` after scan.
- Discoveries: `D_Geo_ExposedStratumSection` (scan target; central);
  `D_Anomaly_EmbeddedCarving` (glyph carved by someone long before MERIDIAN's
  knowledge — `EDiscoveryCategory::AlienTech` override).

---

### Zone 4 — Collapse Gallery

**Purpose:** Environmental escalation; answer "what fell."
**Size:** 120 m long; wide open, ~25 m floor width, but floor is 60 % brittle.
**Key beats:**
- Large-scale collapse has already happened — half the floor is open grid of
  fallen bone over a 30 m pit; player must path-find across safe limestone
  islands.
- Two `ABrittleWalkwaySection` sections embedded in the island-hopping route,
  each fully spanning a gap — fail = drop into the pit (damage but survivable
  at ~40 % health cost from `UAbyssalHealthComponent`).
- Audio: distant settling creak throughout — environmental pressure.
- `CHK_FS_04` before the widest gap.
- Discovery: `D_Geo_FracturedStalagtite` (one fallen column used as an informal
  bridge — scan it for geology data);
  `D_Structure_ExpeditionRope` (`EDiscoveryCategory::HumanMade` — a safety rope
  someone rigged before us, now frayed but still usable for one of the crossings).

---

### Zone 5 — Bone Orchard

**Purpose:** Dense fossil field; secondary hazard (falling ceiling fragments).
**Size:** 50 × 50 m; vertical density 40 m.
**Key beats:**
- Vertical fossil stalactites cluster like petrified trees; navigation requires
  weaving between them.
- Overhead impact hazard: periodic `ACeilingFragmentHazard` (derives from
  `AAbyssalHazardBase`, DamageMode=Radial, radius=80 cm, DPS=40 — punishing
  but targeted) — small shadow appears (Warning), fragment drops (Active).
- The fragment hazard telegraphs the Gravity Well approach (falling things from
  above — same instinct, different cause).
- `CHK_FS_05` at far edge.
- Discoveries: `D_Bio_CalcifiedSporeCluster` (organic material calcified inside
  fossil — biology reading in a geology zone, surprising);
  `D_Geo_AbyssalSeamLayer` (thin phosphorescent mineral seam — first colour
  other than amber in the zone, gentle surprise).

---

### Zone 6 — The Ascending Fissure (exit)

**Purpose:** Exit beat; upward traversal to reach Gravity Well.
**Size:** Vertical climb, 3 platforms with bridging, ~60 m elevation gain.
**Key beats:**
- Narrow fissure cut by ancient seismic event — exit to the next biome above.
- Platforms are bone ledges; two final `ABrittleWalkwaySection` spans (short,
  but stakes higher because a fall is longer).
- MERIDIAN: "Gravity Well access is through the upper aperture. I am
  recalibrating. Stay close."
- `CHK_FS_06` at crest — map complete; autosave.
- Discovery: `D_Geo_FissureSkyline` (look back down through the fissure — full
  Fossil Sky panorama visible; triggers an awe-framing journal entry).

---

## Discovery Catalog Rows

> Add these rows to `Content/Design/DiscoveryCatalog.csv`.
> Format: `ID, Category, ZoneHint, ShortDescription`

```
D_Geo_StratumColumn,       Geology,   FS_00, Layered limestone column bearing 4 million yr of abyssal sediment
D_Geo_BoarFossilMural,     Geology,   FS_01, Ceiling array of interlocked non-terrestrial skeletons 8 m across
D_Geo_SpineFossilArch,     Geology,   FS_02, Rib fossil forming a 12 m load-bearing arch over the ledge path
D_Anomaly_DataTagOnBone,   Anomaly,   FS_02, Modern MERIDIAN-format data tag embedded 3 m into 4000-yr stratum
D_Geo_ExposedStratumSection,Geology,  FS_03, Cross-section plinth revealing the colony-era sediment boundary
D_Anomaly_EmbeddedCarving, AlienTech, FS_03, Glyph carved pre-colonisation — pre-dates any known Rift presence
D_Geo_FracturedStalactite, Geology,   FS_04, Collapsed column repurposed as an informal crossing bridge
D_Structure_ExpeditionRope,HumanMade, FS_04, Frayed safety rope rigged by the previous expedition team
D_Bio_CalcifiedSporeCluster,Biology,  FS_05, Organic spore cluster mineralized within fossil stratum
D_Geo_AbyssalSeamLayer,    Geology,   FS_05, Thin phosphorescent mineral seam cutting across the bone field
D_Geo_FissureSkyline,      Geology,   FS_06, Reverse vista of the full Fossil Sky cavity from the upper fissure
```

---

## Checkpoint List

| ID | Location | Trigger |
|---|---|---|
| `CHK_FS_00` | Zone 0 entry | Auto on map load |
| `CHK_FS_01` | Zone 1 after first bridge | `AObjectiveTriggerActor` |
| `CHK_FS_02` | Zone 2 alcove | `AObjectiveTriggerActor` |
| `CHK_FS_03` | Zone 3 after strata scan | Objective complete callback |
| `CHK_FS_04` | Zone 4 before widest gap | `AObjectiveTriggerActor` |
| `CHK_FS_05` | Zone 5 far edge | `AObjectiveTriggerActor` |
| `CHK_FS_06` | Zone 6 crest / map exit | `AObjectiveTriggerActor` (autosave) |

---

## Objective Sequence

> Add to `Content/Design/MainObjectiveArc.csv` under the Fossil Sky section.
> Format: `ID, DisplayText, MapHint, AutoAdvance`

```
OBJ_FS_ENTER,          "Reach the Fossil Sky cavity",     FOSSIL_SKY, false
OBJ_FS_REACH_DATING,   "Find the colony-era stratum plinth", FOSSIL_SKY, false
OBJ_FS_DateStrata,     "Scan the exposed stratum section", FOSSIL_SKY, false
OBJ_FS_EXIT,           "Reach the Ascending Fissure exit", FOSSIL_SKY, false
```

---

## Hazard Derivation Notes

### `ABrittleWalkwaySection : AAbyssalHazardBase`

```cpp
// Derives from AAbyssalHazardBase with these tuning overrides:
// DamageMode = EHazardDamageMode::None (hazard is the fall, not a damage aura)
// WarningDuration = 2.0f (default; 4.5f on the 14 m Zone 2 instance)
// ActiveDuration  = 0.8f (collapse animation window)
// CooldownDuration = 8.0f (walkway stays collapsed; effectively permanent in v1)
//
// Collapse is a Blueprint visual/physics event triggered from OnHazardActive();
// no C++ physics needed — animate the mesh out, enable a blocking volume below,
// update nav mesh at runtime.
//
// Trigger: weight sensor — a sphere overlap on the walkway mesh detects the
// player pawn (RegisterDamagePrimitive on the sphere to drive overlap tracking;
// phase advance called manually from HandleOverlapBegin override).
```

### `ACeilingFragmentHazard : AAbyssalHazardBase`

```cpp
// DamageMode = EHazardDamageMode::Radial
// DamageRadius = 80.0f, DamagePerSecond = 40.0f, DamageTickInterval = 0.25f
// IdleDuration = FRandRange(6.0f, 12.0f) per instance (stagger via bRandomizeInitialPhaseOffset)
// WarningDuration = 1.2f (shadow drops)
// ActiveDuration  = 0.3f (impact + damage burst)
// CooldownDuration = 1.5f (dust settles)
//
// Warning phase: Blueprint spawns a shadow decal at ground position.
// Active phase : Blueprint drops the fragment mesh (Niagara debris burst).
// Cooldown     : remove decal, reset mesh.
```

---

## Asset Manifest (stub)

> Populate as Blender / UE5 assets are created. Paths are targets, not existing.

| Slot | Target Path | Notes |
|---|---|---|
| Brittle bone plate tile | `Content/Environment/FossilSky/SM_BonePlate_Tile` | 1×1 m, destructible |
| Fossil rib arch | `Content/Environment/FossilSky/SM_RibArch_Large` | 12 m span |
| Limestone ledge modular | `Content/Environment/FossilSky/SM_Ledge_Module` | 2 m × 4 m snapping |
| Ceiling stalactite (fossil) | `Content/Environment/FossilSky/SM_FossilStalactite_*` | 3 LODs |
| Amber fissure light | `Content/Environment/FossilSky/BP_FissureLight` | Rect light + haze |
| Stratum plinth (scan target) | `Content/Environment/FossilSky/SM_StratumPlinth` | |
| Ceiling fragment VFX | `Content/VFX/FossilSky/NS_CeilingFragment_Fall` | Niagara |

---

## Backend Hooks Required

| Feature | Depends on | Status |
|---|---|---|
| Brittle walkway section | C2 `AAbyssalHazardBase` | C2 authored (Windows compile pending) |
| Ceiling fragment hazard | C2 `AAbyssalHazardBase` | C2 authored |
| Strata scan objective | A3 `IAbyssalInteractable`, A2 data-driven objectives | A3 authored |
| Discovery actors | `ADiscoveryActor` + `UDiscoverySubsystem` | Exists |
| Checkpoints | `AObjectiveTriggerActor` | Exists |
| Autosave on exit | A1 `UAbyssalSaveSubsystem` | A1 not yet authored |
