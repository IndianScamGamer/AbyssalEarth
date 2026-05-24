# Luminous Rift Blockout Plan

## Goal

Build a 10-15 minute first playable cavern that matches the core concept reference: a player-scale descent into a massive vertical rift containing blue crystals, ancient machine architecture, suspended bridges, a central blue-white energy sphere, gold beam collector arrays, and a final overlook into an even deeper abyss.

The old marsh/fungus/vent route is deprecated for this first map. Those ideas may return later, but `MAP_LuminousRift_Blockout` should now be built around the ancient rift machine shown in:

`Content/ArtDirection/References/luminous_rift_core_reference.png`

## Scale

Unreal units are centimeters.

- Total playable route length: 700-1100 meters.
- Primary visible cavern height: 300-500 meters.
- Main vista width: 250-500 meters.
- Abyss visual drop: at least 300 meters below the route.
- Player path width: 3-10 meters.
- Central orb diameter: 18-28 meters.
- Collector array width: 80-140 meters.
- Gate wall height: 80-140 meters.
- Distant background towers can be much larger because they are scale silhouettes.

## Route Overview

### 1. Descent Elevator

Purpose: establish the player as a recent human intruder.

- Surface-built elevator forced into black basalt.
- Human lamps, survey crates, cable runs, and a temporary safety rail.
- Exit tunnel should hide the core vista until the first overlook.
- First discovery: `D_Human_SurveyElevator`.

### 2. First Overlook

Purpose: recreate the core reference composition as the first beauty moment.

- Player emerges onto a dark jagged ledge.
- The central orb is visible but partially occluded by rock and hanging slabs.
- Gold collector beams should be readable even from this distance.
- Blue crystals light the foreground and edges.
- Right-side ancient gate wall is visible across the void.
- Objective: reach the Collector Array.

### 3. Abyssal Approach

Purpose: traverse from natural rock into ancient machine structures.

- Narrow ledges and broken bridge spans descend along the left side of the abyss.
- Crystals act as route markers.
- Distant towers and hanging slabs deepen the vertical space.
- Discovery: `D_Geo_BlueRiftCrystal`.

### 4. Crystal Galleries

Purpose: close-up crystal and rock-machine fusion.

- A side gallery where blue crystals grow through carved wall panels.
- Player sees the orb through gaps between rock arches.
- Discovery: `D_Anomaly_CrystalResonance`.
- Optional hazard later: unstable crystal pulse or falling debris.

### 5. Collector Array

Purpose: central landmark interaction space.

- Player reaches a platform near the orb apparatus.
- Hex collector panels surround the orb in flower-like clusters.
- Gold beam emitter nodes connect hub to panels.
- Discovery: `D_Anomaly_RiftEnergyOrb`.
- Objective trigger should fire when the player reaches the safe platform near the apparatus.

### 6. Ancient Gate

Purpose: monumental right-side structure from the reference.

- A tall vertical wall/gate with circular blue-lit mechanisms.
- Path crosses a bridge or broken platform in front of it.
- Discovery: `D_Structure_AncientGate`.
- This zone should feel colder and more architectural than the approach.

### 7. Second Sky Overlook

Purpose: final reveal and route completion.

- The player reaches a ledge beyond the gate/collector array.
- The lower rift opens into an even larger blue-lit abyss.
- Final discovery: `D_Anomaly_SecondSkyCavern`.
- Scanning this vista completes `CHK_SecondSkyOverlook`.

## Room-by-Room Placement Checklist

Coordinates assume map origin at the elevator platform center, +X is the forward route direction, +Z is up. These are blockout anchors, not rigid final layout. Composition from the first overlook matters more than exact coordinates.

For editor tracking, the same work is also broken into status rows in:

`Content/Design/LuminousRiftBlockoutChecklist.csv`

### Zone 1 - Descent Elevator (X 0 to 3000)

Footprint: 30 m access tunnel plus 10-14 m elevator platform. Ceiling 8-12 m. Black basalt surrounds everything.

- [ ] `PlayerStart` at (0, 0, 100), facing +X.
- [ ] `SM_Human_SurveyPlatform_A` or blockout platform at (0, 0, 0), 10x10 m.
- [ ] Basalt shaft walls around platform, 10-15 m tall.
- [ ] 4-6 human props: crates, cable coils, portable lamps, temporary rail section.
- [ ] `BP_DiscoveryActor_Base`: `D_Human_SurveyElevator`, at (1800, 0, 120), `ScanFocusOffset = (0, 0, 80)`.
- [ ] Human lights: white/amber, low intensity, radius 400-600.
- [ ] `BP_ObjectiveTrigger`: `CHK_DescentElevator`, box 600x400x300 at (2700, 0, 150).
- [ ] Exit tunnel bends slightly so the first vista is hidden until Zone 2.

### Zone 2 - First Overlook (X 3000 to 4600)

This is the postcard shot. Use the concept image as direct reference.

- [ ] Foreground ledge: `SM_Rift_ForegroundLedge_A` at (3600, 0, 0), playable area 8-12 m wide.
- [ ] Dark rock overhangs frame the top and left side of the view.
- [ ] Blue crystals in foreground left/right: 3-5 clusters, small to medium.
- [ ] Add one visible player-scale human prop near the ledge edge: beacon, lamp, or survey tripod.
- [ ] Central orb proxy at approximately (11500, 0, -2000), diameter 2200 cm.
- [ ] Hex collector clusters arranged around orb, spanning roughly 100 m wide.
- [ ] Right-side gate wall at approximately (11800, 6500, -2500), 100 m tall.
- [ ] Lower abyss: visible blue fog column from Z -20000 downward.
- [ ] Distant tower silhouettes behind orb and under bridge path.
- [ ] `BP_ObjectiveTrigger`: `CHK_FirstOverlook`, box 900x1200x400 at (3800, 0, 200).
- [ ] No mandatory discovery in this zone; let the view breathe.

Lighting:

- Orb visible as cool key light.
- Gold beam splines visible but thin.
- Foreground crystals provide small cyan edge lights.
- Use volumetric fog. Distant shapes fade blue.

### Zone 3 - Abyssal Approach (X 4600 to 8200)

The player descends from natural ledges into machine bridge slabs.

- [ ] 3-5 staggered rock ledges, each 6-10 m wide, descending from Z 0 to Z -3500.
- [ ] 2 broken bridge spans: `SM_Rift_BridgeSpan_A/B_Broken`, linking ledges across small gaps.
- [ ] Route must keep the orb visible at least twice through rock windows.
- [ ] Crystal breadcrumb clusters every 20-35 m, mostly medium size.
- [ ] Distant hanging slabs below and above path to sell vertical space.
- [ ] `BP_DiscoveryActor_Base`: `D_Geo_BlueRiftCrystal` at (6500, -500, -1800), `ScanFocusOffset = (0, 0, 140)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_AbyssalApproach`, box 1000x1000x500 at (8100, 0, -3300).

Safety:

- Use collision blockers at abyss edges for early prototype if falling is not implemented.
- Hide blockers with low rock lips or ancient platform curbs.

### Zone 4 - Crystal Galleries (X 8200 to 10800)

A close-up space where natural crystal growth pierces ancient wall structures.

- [ ] Carved wall panel modules on one side, basalt on the other.
- [ ] 8-12 crystal clusters of mixed sizes, including at least one large 7-9 m cluster.
- [ ] Rock arch/window framing the central orb in the distance.
- [ ] Small platform node with circular blue-lit inset.
- [ ] `BP_DiscoveryActor_Base`: `D_Anomaly_CrystalResonance` at (9300, 600, -3000), `ScanFocusOffset = (0, 0, 120)`.
- [ ] Optional later hazard placeholder: pulsing crystal field marked by emissive floor cracks.
- [ ] `BP_ObjectiveTrigger`: `CHK_CrystalGalleries`, box 900x900x500 at (10600, 0, -2800).

Lighting:

- Stronger blue crystal glow than Zone 3.
- Keep orb light partially occluded for contrast.
- Add small dust/mote VFX in shafts.

### Zone 5 - Collector Array (X 10800 to 13500)

Central landmark. This must read like the concept art's orb + hex panel apparatus.

- [ ] Orb actor/proxy centered around (11800, 0, -1800), diameter 1800-2800 cm.
- [ ] `SM_Rift_OrbFrame_A` or blockout ring around/behind orb.
- [ ] 5-8 `SM_Rift_HexCollector_Cluster_A/B` around orb, offset in depth and height.
- [ ] Gold beam splines from hub/beam nodes to collector cluster centers.
- [ ] Platform node near orb at (11200, -1200, -2200), not directly inside the energy.
- [ ] Bridge span from Crystal Galleries to the platform.
- [ ] 3-5 beam emitter nodes placed along platform and ring.
- [ ] `BP_DiscoveryActor_Base`: `D_Anomaly_RiftEnergyOrb` at platform edge, `ScanFocusOffset = (0, 0, 300)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_CollectorArray`, box 1200x1200x600 at (11200, -1200, -2100).

Lighting:

- Orb: primary cool light, high intensity, bloom controlled.
- Beams: warm gold, visible in fog, endpoints glow.
- Panels: faint blue-white translucent interior.

Gameplay:

- Keep collision away from orb; it is a landmark and scan target, not a walk-through object yet.
- The platform should have at least two safe beacon placement surfaces.

### Zone 6 - Ancient Gate (X 13500 to 16500)

The player crosses in front of or through the right-side monumental gate structure.

- [ ] `SM_Rift_AncientWall_Gate_A` placed as dominant right-side wall, 80-140 m tall.
- [ ] At least one large circular blue core at player-visible height.
- [ ] Vertical grooves and blue strips visible from 50+ m.
- [ ] Embedded crystals at base and broken panel edges.
- [ ] Bridge/platform route runs along the wall, 6-8 m wide.
- [ ] `BP_DiscoveryActor_Base`: `D_Structure_AncientGate` at (14800, 1200, -2000), `ScanFocusOffset = (0, 0, 400)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_AncientGate`, box 1000x1200x600 at (15800, 800, -2000).

Lighting:

- Blue gate cores are secondary focal points.
- Gold beam spill from Collector Array should graze the wall surface.
- Use darker exposure here to make the gate feel massive and cold.

### Zone 7 - Second Sky Overlook (X 16500 to 19000)

Final reveal and end beat.

- [ ] Final ledge extends to (18500, 0, -1600), using foreground ledge or bridge edge kit.
- [ ] The lower rift opens directly ahead with no flat floor visible.
- [ ] Distant spires, hanging slabs, and blue fog create a second-horizon effect.
- [ ] Human survey station or tiny temporary camp can sit behind the player, not in the main view.
- [ ] `BP_DiscoveryActor_Base`: `D_Anomaly_SecondSkyCavern` at (18500, 0, -1450).
- [ ] Set `D_Anomaly_SecondSkyCavern.ObjectiveIdToCompleteOnScan = CHK_SecondSkyOverlook`.
- [ ] `bCompleteObjectiveOnlyOnNewDiscovery = true`.
- [ ] Use trigger volume only as fallback during early testing.

## Landmark Layout

Top-down rough arrangement:

```
                  Second Sky Overlook
                           |
                    Ancient Gate
                           |
       Crystal Galleries --+-- Collector Array / Orb
              \                 /
               \               /
             Abyssal Approach
                    |
              First Overlook
                    |
             Descent Elevator
```

Wide-shot composition from First Overlook:

```
  dark ceiling/rock frame
  ------------------------------------------------
  left rock/towers       orb + hex array       ancient gate wall
  foreground ledge       gold beams            blue circular cores
  player silhouette      deep blue abyss       crystals/platforms
```

## Beacon Placement Guidance

The level should naturally invite player beacons at:

- First Overlook before leaving the safe human route.
- Abyssal Approach halfway down the ledge descent.
- Crystal Galleries entrance.
- Collector Array platform.
- Ancient Gate crossing before the final overlook.

Each location needs a clear surface within the character's `MaxBeaconPlacementDistance`.

## Blockout Mesh List

P0:

- `SM_Rift_ForegroundLedge_A`
- `SM_Rift_BridgeSpan_A`
- `SM_Rift_BridgeSpan_B_Broken`
- `SM_Rift_PlatformNode_A`
- `SM_Rift_AncientWall_Gate_A`
- `SM_Rift_OrbFrame_A`
- `SM_Rift_OrbHub_A`
- `SM_Rift_BeamEmitterNode_A`
- `SM_Rift_HexCollector_Tile_A`
- `SM_Rift_HexCollector_Cluster_A`
- `SM_Rift_CrystalCluster_S/M/L/Hero`

P1:

- `SM_Rift_RockArch_A/B`
- `SM_Rift_CavernWall_Large_A/B`
- `SM_Rift_Overhang_A/B`
- `SM_Rift_TowerSegment_A/B/C`
- `SM_Rift_HangingSlab_A/B/C`
- `SM_Rift_DistantSpire_A/B`
- `SM_Human_SurveyCrate_A`
- `SM_Human_PortableLamp_A`
- `SM_Human_CableCoil_A`
- `SM_Human_FieldConsole_A`

## Objective Trigger Checklist

The `CHK_*` ids below are spatial checkpoints, not the player-facing main objective arc. The current player-facing arc is `OBJ_VERIFY_HELIOS` -> `OBJ_SURVIVE` -> `OBJ_DISCOVER_PLACE` -> `OBJ_MAKE_MACHINE_ANSWER` -> `OBJ_BUILD_WAY_OUT` -> `OBJ_OPEN_RIFT`.

- `CHK_DescentElevator`: exit from elevator/tunnel.
- `CHK_FirstOverlook`: first full view of the core vista.
- `CHK_AbyssalApproach`: after descending onto machine bridge structures.
- `CHK_CrystalGalleries`: after scanning/entering the crystal-machine fusion zone.
- `CHK_CollectorArray`: safe platform near orb apparatus.
- `CHK_AncientGate`: crossing the monumental gate structure.
- `CHK_SecondSkyOverlook`: completed by scanning `D_Anomaly_SecondSkyCavern`.

## Screenshot Review Checklist

Take screenshots from:

- Elevator exit before reveal.
- First Overlook, matching the concept art.
- Mid-Abyssal Approach, with orb partially occluded.
- Crystal Galleries, with close crystals and distant orb.
- Collector Array platform, looking at orb/hex panels.
- Ancient Gate crossing, looking up at circular blue cores.
- Second Sky Overlook, looking into lower rift.

For the First Overlook screenshot to pass:

- The orb is the focal point.
- Hex collector clusters and gold beams are visible.
- Dark rock frames the shot.
- Blue crystals appear in foreground.
- A human scale cue is present.
- The lower abyss reads as very deep.
- The right-side gate wall reads clearly as ancient machinery.
