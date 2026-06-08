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
DamageMode = None, ActiveDuration drives a floor-collapse animation).
Warning phase = hairline-crack VFX + audible creaking.

---

## Zone Breakdown

### Zone 0 — Ossuary Passage (entry)
**Purpose:** Landing and reorientation after tunnel from Glassroot. 30 × 10 m corridor.
- MERIDIAN: "If the strata age confirms what I suspect, the Rift has been inhabited for 4,000 years."
- `CHK_FS_00` on entry. Discovery: `D_Geo_StratumColumn`.

### Zone 1 — The Underpalate
**Purpose:** First vertical reveal; introduce brittle-floor mechanic. 60 × 40 m.
- Tutorial `ABrittleWalkwaySection` (4 m, falls 1 m — survivable).
- `CHK_FS_01`. Discovery: `D_Geo_BoarFossilMural` (ceiling scan, `bRequiresLook=true`).

### Zone 2 — Rib Corridor
**Purpose:** Signature setpiece; narrow ledge under fossil ribs. 80 m × 8 m.
- Three brittle bridges (4 m → 8 m → 14 m). 14 m instance: `WarningDuration=4.5f`.
- `CHK_FS_02`. Discoveries: `D_Geo_SpineFossilArch`, `D_Anomaly_DataTagOnBone`.

### Zone 3 — The Dating Chamber (story anchor)
**Purpose:** Scan plinth → age reveal. 40 × 40 m, 80 m cathedral ceiling.
- Scan (`IAbyssalInteractable`) → MERIDIAN: "4,327 years. The colonists didn't cause the Rift. *They were already inside.*"
- `CHK_FS_03`. Discoveries: `D_Geo_ExposedStratumSection`, `D_Anomaly_EmbeddedCarving` (AlienTech).

### Zone 4 — Collapse Gallery
**Purpose:** Escalation; 60 % brittle floor, island-hop over 30 m pit. 120 m long.
- `CHK_FS_04`. Discoveries: `D_Geo_FracturedStalactite`, `D_Structure_ExpeditionRope`.

### Zone 5 — Bone Orchard
**Purpose:** Dense fossil field + ceiling fragment hazard. 50 × 50 m.
- `ACeilingFragmentHazard` (DamageMode=Radial, radius=80 cm, DPS=40).
- `CHK_FS_05`. Discoveries: `D_Bio_CalcifiedSporeCluster`, `D_Geo_AbyssalSeamLayer`.

### Zone 6 — The Ascending Fissure (exit)
**Purpose:** Upward climb to Gravity Well. ~60 m elevation gain.
- MERIDIAN: "Gravity Well access is through the upper aperture."
- `CHK_FS_06` (autosave). Discovery: `D_Geo_FissureSkyline`.

---

## Discovery Catalog Rows

```
D_Geo_StratumColumn,        Geology,   FS_00, Layered limestone column bearing 4 million yr of abyssal sediment
D_Geo_BoarFossilMural,      Geology,   FS_01, Ceiling array of interlocked non-terrestrial skeletons 8 m across
D_Geo_SpineFossilArch,      Geology,   FS_02, Rib fossil forming a 12 m load-bearing arch over the ledge path
D_Anomaly_DataTagOnBone,    Anomaly,   FS_02, Modern MERIDIAN-format data tag embedded 3 m into 4000-yr stratum
D_Geo_ExposedStratumSection,Geology,   FS_03, Cross-section plinth revealing the colony-era sediment boundary
D_Anomaly_EmbeddedCarving,  AlienTech, FS_03, Glyph carved pre-colonisation — pre-dates any known Rift presence
D_Geo_FracturedStalactite,  Geology,   FS_04, Collapsed column repurposed as an informal crossing bridge
D_Structure_ExpeditionRope, HumanMade, FS_04, Frayed safety rope rigged by the previous expedition team
D_Bio_CalcifiedSporeCluster,Biology,   FS_05, Organic spore cluster mineralized within fossil stratum
D_Geo_AbyssalSeamLayer,     Geology,   FS_05, Thin phosphorescent mineral seam cutting across the bone field
D_Geo_FissureSkyline,       Geology,   FS_06, Reverse vista of the full Fossil Sky cavity from the upper fissure
```

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

## Objective Sequence

```
OBJ_FS_ENTER,        "Reach the Fossil Sky cavity",        FOSSIL_SKY, false
OBJ_FS_REACH_DATING, "Find the colony-era stratum plinth", FOSSIL_SKY, false
OBJ_FS_DateStrata,   "Scan the exposed stratum section",   FOSSIL_SKY, false
OBJ_FS_EXIT,         "Reach the Ascending Fissure exit",   FOSSIL_SKY, false
```

## Hazard Derivation Notes

### `ABrittleWalkwaySection : AAbyssalHazardBase`
```cpp
// DamageMode = None; WarningDuration = 2.0f (4.5f Zone 2 14 m instance)
// ActiveDuration = 0.8f; CooldownDuration = 8.0f (stays collapsed)
// OnHazardActive(): animate mesh out, enable blocking volume below.
```

### `ACeilingFragmentHazard : AAbyssalHazardBase`
```cpp
// DamageMode = Radial; DamageRadius = 80.0f; DPS = 40.0f
// IdleDuration randomized per instance; WarningDuration = 1.2f; ActiveDuration = 0.3f
// Warning: shadow decal drops. Active: Niagara debris burst.
```

## Asset Manifest (stub)

| Slot | Target Path |
|---|---|
| Brittle bone plate | `Content/Environment/FossilSky/SM_BonePlate_Tile` |
| Fossil rib arch | `Content/Environment/FossilSky/SM_RibArch_Large` |
| Limestone ledge | `Content/Environment/FossilSky/SM_Ledge_Module` |
| Ceiling fragment VFX | `Content/VFX/FossilSky/NS_CeilingFragment_Fall` |
