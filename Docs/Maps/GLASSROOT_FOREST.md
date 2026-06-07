# Glassroot Forest Blockout Plan

Map 02 of the Abyssal Earth descent (`Docs/WORLD_ATLAS.md`). This is the first
**biological** map: after the ancient-machine awe of the Luminous Rift, the
underworld reveals that it is alive. Pacing should slow and the player should
feel like a field naturalist, not an intruder in a machine.

Concept references:

- `Content/ArtDirection/WorldMaps/glassroot_forest_concept.png` (hero target)
- `Content/ArtDirection/Concepts/Glassroot_Forest/` (GR-001 … GR-006 studies)

## Goal

Build a 10-14 minute calm-but-uneasy traversal through a cathedral-sized
subterranean forest of translucent root-columns, pearl mineral terraces, and
shallow reflective pools, with red mineral sap glowing like veins inside glasslike
biological structures. The map teaches the player that scanning can reveal living
infrastructure (safe bridges, dormant root gates) and introduces the first
biological hazards (spore clouds that distort scanner readouts).

The route should read as a chain of pearl terraces and pools winding between giant
roots, descending gently into mist, and ending on an overlook that hints at the
next layer (the Inner Sea).

## Scale

Unreal units are centimeters.

- Total playable route length: 600-900 meters.
- Primary cavern height: 120-220 meters (cathedral, calmer than the Rift).
- Root column trunk diameter: 3-12 meters; height 40-120 meters into mist.
- Pearl terrace width: 4-12 meters; height steps 1-4 meters.
- Shallow pool depth: 0.2-0.6 meters (readable reflections, not deep water).
- Player path width: 2-8 meters.
- Mist ceiling: roots fade into low cool mist by 80-120 meters up.
- Hero root cluster: a grove of 5-8 trunks framing the first overlook.

## Route Overview

### 1. Basalt Seam (transition in)

Purpose: connect from the Luminous Rift and reset the player's palette/mood.

- Tight, dark basalt crack with faint pale-green light leaking from ahead.
- No discoveries; this is a decompression corridor that hides the forest until
  the overlook.
- Sound shifts from machine hum to water drips and low root creaks.

### 2. First Overlook (Shaded Ledge)

Purpose: the postcard beauty moment matching the concept art.

- Player emerges from the seam onto a shadowed ledge.
- Below: a pale green-white root forest, dozens of translucent trunks rising into
  mist; red sap glows inside a few roots like veins.
- The playable route is legible below as a chain of pearl terraces and pools.
- Discovery: `D_Bio_GlassrootColumn` (the nearest hero trunk is scannable here).

### 3. Pearl Terraces

Purpose: introduce the core traversal — walking mineral terraces around root bases.

- Stepped pale terraces wind between trunk bases.
- Discovery: `D_Geo_PearlTerrace`.
- Teach: soft bioluminescent underside glows mark stable footing.

### 4. Reflective Pools

Purpose: shallow-water traversal and the first terrain hazard.

- Shallow reflective pools cross the route; mirror reflections of roots above.
- Hazard: some pools hide sinkholes — scanner pulse reveals safe vs. unsafe.
- Discovery: `D_Bio_SporeLantern` (small organisms that light safe paths).

### 5. Sap Veins

Purpose: close-up biological/material reveal that seeds later fabrication.

- A hollow where red mineral sap runs through glasslike root walls.
- Discovery: `D_Bio_RedMineralSap` — note it reads as **conductive**, foreshadowing
  its use as a fabrication/power material in later maps.
- Lighting: warm red sap glow contrasts the pale green forest.

### 6. Spore Hollows & Root Gates

Purpose: the signature mechanic zone.

- Spore-heavy pockets distort the scanner readout (reduced range / noisy results).
- Dormant **root gates** open in response to a scanner pulse, then close after a
  timed interval — a light traversal puzzle.
- Discovery: `D_Anomaly_RootSignalDelay` (roots answer scanner pulses after a delay).

### 7. Deep Grove Overlook (final reveal)

Purpose: route completion and a pointer to the next map.

- A hollow root tunnel climbs to a final ledge over a deeper grove.
- Distant mist parts to imply water far below — the first hint of the Inner Sea.
- Scanning the vista completes `CHK_GR_DeepGroveOverlook`.

## Room-by-Room Placement Checklist

Coordinates assume map origin at the basalt-seam entry, +X is the forward route
direction, +Z is up. These are blockout anchors, not final layout — the calm
forest composition and readable route matter more than exact numbers.

When this map enters production, mirror these rows into a
`Content/Design/GlassrootForestBlockoutChecklist.csv` (same column shape as
`LuminousRiftBlockoutChecklist.csv`) so editor work is status-tracked.

### Zone 1 - Basalt Seam (X 0 to 2500)

Footprint: 25 m winding crack, 3-5 m wide, ceiling 6-10 m.

- [ ] `PlayerStart` at (0, 0, 100), facing +X.
- [ ] Basalt seam walls; one bend so the forest is hidden until Zone 2.
- [ ] Pale-green light leak and rising mist near the exit.
- [ ] `BP_ObjectiveTrigger`: `CHK_GR_BasaltSeam`, box 500x400x300 at (2300, 0, 150).

### Zone 2 - First Overlook (X 2500 to 4200)

The postcard shot. Use the concept image as direct reference.

- [ ] Foreground ledge at (3000, 0, 0), playable area 6-10 m wide.
- [ ] Hero root grove: 5-8 `SM_Glassroot_RootColumn_L/Hero` at (6000-9000, +/-3000, -1500), rising into mist.
- [ ] 2-3 roots carry visible red sap veins (`SM_Glassroot_SapVein_A`).
- [ ] Low cool mist band from Z +6000 upward; trunks fade blue-green.
- [ ] Pearl terraces and pools legible below as the onward route.
- [ ] One player-scale cue near the ledge edge (beacon, lamp, or survey marker).
- [ ] `BP_DiscoveryActor_Base`: `D_Bio_GlassrootColumn` at (5200, 0, -800), `ScanFocusOffset = (0, 0, 300)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_GR_FirstOverlook`, box 900x1200x400 at (3200, 0, 200).

Lighting: pale green translucent roots as soft key fill; red sap as warm accent;
volumetric mist for depth.

### Zone 3 - Pearl Terraces (X 4200 to 7000)

- [ ] 4-6 stepped `SM_Glassroot_Terrace_PearlStone_A/B`, descending Z 0 to -2000.
- [ ] Trunk bases (`SM_Glassroot_RootColumn_M`) interrupt the route as soft gates.
- [ ] Soft underside glow strips mark stable footing.
- [ ] `BP_DiscoveryActor_Base`: `D_Geo_PearlTerrace` at (5600, 600, -900), `ScanFocusOffset = (0, 0, 60)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_GR_PearlTerraces`, box 900x900x500 at (6800, 0, -1800).

### Zone 4 - Reflective Pools (X 7000 to 10000)

- [ ] 3-5 shallow pools using `SM_Glassroot_PoolEdge_A`; mirror-flat material.
- [ ] At least 2 sinkhole pools: visually similar, revealed unsafe by scanner.
- [ ] `BP_DiscoveryActor_Base`: `D_Bio_SporeLantern` at (8200, -700, -2100), `ScanFocusOffset = (0, 0, 90)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_GR_ReflectivePools`, box 1000x1000x400 at (9800, 0, -2200).

Safety: use collision blockers under sinkhole pools for early prototype if fall
damage is not yet implemented; reveal them only on scan.

### Zone 5 - Sap Veins (X 10000 to 12000)

- [ ] Hollow framed by glasslike root walls with internal red sap channels.
- [ ] 1 large `SM_Glassroot_SapVein_A` hero channel as the scan focus.
- [ ] `BP_DiscoveryActor_Base`: `D_Bio_RedMineralSap` at (11000, 500, -2400), `ScanFocusOffset = (0, 0, 120)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_GR_SapVeins`, box 800x800x500 at (11900, 0, -2400).

### Zone 6 - Spore Hollows & Root Gates (X 12000 to 15000)

Signature mechanic zone.

- [ ] 2-3 spore pockets (`SM_Glassroot_SporePod_A/B` + `VFX_Glassroot_SporeMist`).
- [ ] 2 dormant root gates (`SM_Glassroot_RootBridge_A` variants) that open on
      scanner pulse and reclose after a timed interval.
- [ ] `BP_DiscoveryActor_Base`: `D_Anomaly_RootSignalDelay` at (13200, -600, -2600), `ScanFocusOffset = (0, 0, 150)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_GR_SporeHollows`, box 1000x1000x500 at (14800, 0, -2700).

Note: spore scanner-distortion, timed root gates, and sinkhole reveals are the
map-specific backend for this biome — see roadmap items C2 (hazard framework) and
C3 (traversal) in `Docs/BACKEND_SYSTEMS_ROADMAP.md`.

### Zone 7 - Deep Grove Overlook (X 15000 to 17500)

Final reveal and end beat.

- [ ] Hollow root tunnel (`SM_Glassroot_HollowRootTunnel_A`) climbs to the ledge.
- [ ] Final ledge at (17000, 0, -2200); deeper grove and parting mist ahead.
- [ ] Distant water shimmer / low tone implies the Inner Sea below (next map).
- [ ] `BP_DiscoveryActor_Base`: `D_Anomaly_RootSignalDelay` is NOT reused here;
      place the vista discovery and set its `ObjectiveIdToCompleteOnScan = CHK_GR_DeepGroveOverlook`.
- [ ] `bCompleteObjectiveOnlyOnNewDiscovery = true`.

## Landmark Layout

Top-down rough arrangement:

```
            Deep Grove Overlook  (hint of Inner Sea)
                     |
          Spore Hollows & Root Gates
                     |
               Sap Veins
                     |
     Reflective Pools --+-- (sinkhole pools)
                     |
             Pearl Terraces
                     |
            First Overlook (hero root grove)
                     |
              Basalt Seam (from Luminous Rift)
```

Wide-shot composition from First Overlook:

```
  low mist ceiling, trunks fading blue-green
  ------------------------------------------------
  hero root grove        pearl terraces      red sap veins
  foreground ledge       reflective pools    soft underglow
  player silhouette      winding route       deep grove mist
```

## Beacon Placement Guidance

The level should invite player beacons at:

- First Overlook before descending into the forest.
- Pearl Terraces midpoint.
- Reflective Pools (mark the safe crossing once scanned).
- Sap Veins hollow.
- Before the timed root gates in the Spore Hollows.

Each needs a clear surface within the character's `MaxBeaconPlacementDistance`.

## Blockout Mesh List

P0:

- `SM_Glassroot_RootColumn_S/M/L/Hero`
- `SM_Glassroot_Terrace_PearlStone_A/B`
- `SM_Glassroot_PoolEdge_A`
- `SM_Glassroot_SapVein_A`
- `SM_Glassroot_RootBridge_A`
- `SM_Glassroot_SporePod_A/B`
- `SM_Glassroot_HollowRootTunnel_A`

P1:

- `VFX_Glassroot_SporeMist`
- `M_Glassroot_TranslucentRoot_Master`
- `M_Glassroot_RedSap_Master`
- `M_Glassroot_PearlStone_Master`

## Proposed Discovery Catalog Rows

For a future `Content/Design/DiscoveryCatalog_World.csv` (or a Glassroot section
of the world catalog). Columns match `DiscoveryCatalog.csv`
(`DiscoveryId,DisplayName,Category,Zone,JournalText`). All categories below are
valid `EDiscoveryCategory` members.

| DiscoveryId | DisplayName | Category | Zone |
| --- | --- | --- | --- |
| `D_Bio_GlassrootColumn` | Glassroot Column | Biology | First Overlook |
| `D_Geo_PearlTerrace` | Pearl Terrace | Geology | Pearl Terraces |
| `D_Bio_SporeLantern` | Spore Lantern | Biology | Reflective Pools |
| `D_Bio_RedMineralSap` | Red Mineral Sap | Biology | Sap Veins |
| `D_Anomaly_RootSignalDelay` | Root Signal Delay | Anomaly | Spore Hollows |

## Hazards

- Spore clouds that distort/shrink scanner readouts.
- Fragile terrace edges.
- Root gates that close after a timed interval.
- Pools that hide sinkholes (revealed by scan).

## Ambience Direction

Soft water drips, low resonant root creaks, distant glass chimes, faint biological
pulses, muffled footfalls. For a future `DT_GlassrootAmbience.csv` (same shape as
`DT_LuminousRiftAmbience.csv`).

## Objective Trigger Checklist

The `CHK_GR_*` ids are spatial checkpoints, not the player-facing main objective
arc (the shared `OBJ_VERIFY_HELIOS` … `OBJ_OPEN_RIFT` chain in
`UObjectiveSubsystem`). Within this map the player is in the `OBJ_DISCOVER_PLACE`
/ `OBJ_MAKE_MACHINE_ANSWER` band.

- `CHK_GR_BasaltSeam`: enter from the Luminous Rift connector.
- `CHK_GR_FirstOverlook`: first full view of the root forest.
- `CHK_GR_PearlTerraces`: descended onto the terraces.
- `CHK_GR_ReflectivePools`: crossed the pools.
- `CHK_GR_SapVeins`: reached the sap hollow.
- `CHK_GR_SporeHollows`: cleared the spore/root-gate zone.
- `CHK_GR_DeepGroveOverlook`: completed by scanning the final vista discovery.

## Screenshot Review Checklist

Take screenshots from:

- Basalt seam exit before the reveal.
- First Overlook, matching the concept art.
- Pearl Terraces, with trunks and underglow.
- Reflective Pools, with mirror reflections.
- Sap Veins hollow, warm red against pale green.
- Spore Hollows with a root gate mid-open.
- Deep Grove Overlook, mist parting toward the Inner Sea hint.

For the First Overlook screenshot to pass:

- A hero root grove is the focal point.
- Pale green translucent roots read clearly.
- At least one red sap vein is visible.
- Pearl terraces/pools show the onward route.
- Low cool mist creates depth.
- A human scale cue is present.
- The image reads as biological, never as a generic cave.
