# Luminous Rift Blockout Plan

## Goal

Build a 10-15 minute first playable cavern that immediately proves the visual promise: the player descends from a human-made elevator into an impossible glowing rift, crosses three distinct spaces, scans discoveries, and ends at a huge overlook.

## Scale

Unreal units are centimeters.

- Total playable route length: about 900 meters.
- Main cavern height: 180-260 meters.
- Main cavern width: 220-420 meters.
- Player path width: 3-12 meters depending on tension.
- Major landmarks should be visible from at least two previous route points.

## Route

### 1. Descent Elevator

Purpose: establish human scale and contrast.

- Small metal platform embedded in black basalt.
- Flickering work lights, cables, survey crates.
- First view is constrained until the player exits a short tunnel.
- First discovery: `D_Human_SurveyElevator`.

### 2. First Overlook

Purpose: deliver the first beauty moment.

- The tunnel opens onto a ledge above the Mirror Marsh.
- The Crystal Spine should be visible center-left.
- Ember Vents should glow warm in the far right distance.
- Ceiling crystals should create faint cyan light shafts.
- Player receives first objective: reach the far survey station.

### 3. Mirror Marsh

Purpose: slow movement, reflections, bioluminescent life.

- Shallow ankle-to-knee water plane.
- Clusters of translucent fungus used as route markers.
- Low fog over water.
- Discoveries:
  - `D_Bio_GlasscapFungus`
  - `D_Geo_MirrorSilt`
- Hazard: none in milestone 1; later add spore pockets.

### 4. Crystal Spine

Purpose: traversal and vertical composition.

- Rib-like mineral ridge rises 35-50 meters above marsh.
- Safe route winds through crystal shelves.
- Scanner highlights pulse veins that point toward climbable ledges.
- Discoveries:
  - `D_Geo_PulseQuartz`
  - `D_Anomaly_ResonantVein`

### 5. Ember Vents

Purpose: warm color contrast and environmental danger.

- Orange geothermal vents, drifting steam, wet black rocks.
- Timed safe paths between vent bursts in later milestones.
- For milestone 1, blockout uses visual-only vent columns.
- Discoveries:
  - `D_Geo_EmberVent`
  - `D_Bio_ThermalFilament`

### 6. Far Survey Station

Purpose: objective completion and next-cavern tease.

- Damaged human research outpost on a ledge.
- Scanner reveals impossible depth readings.
- End overlook frames a much larger cavern beyond.
- Final discovery: `D_Anomaly_SecondSkyCavern`.

## Room-by-Room Placement Checklist

Coordinates assume the map origin sits at the elevator platform center, +X is the forward route direction, +Z is up. Distances are approximate; readability of landmarks matters more than exact numbers. Light intensities use Unreal default unitless values for the blockout — replace with calibrated lumens during the M2 lighting pass.

### Zone 1 - Descent Elevator (approx X 0 to 3000)

Footprint: 30m tunnel + 12m platform, ceiling 8-10m, basalt enclosure on all sides.

- [ ] `PlayerStart` at (0, 0, 100) facing +X.
- [ ] `SM_Blockout_SurveyPlatform` at (0, 0, 0) for the elevator floor.
- [ ] 4x `SM_Blockout_BasaltWall_Large` forming the elevator shaft, scaled to 8m height.
- [ ] 2-3 placeholder crate static meshes along the platform edge (use engine cube primitives until art exists).
- [ ] `BP_DiscoveryActor_Base` configured as `D_Human_SurveyElevator` at the platform's far edge (2200, 0, 100), with `ScanFocusOffset = (0, 0, 80)` so the scan trace hits the platform mid-mast.
- [ ] 3-4 `PointLight` actors with white-amber tint (color 1.0, 0.85, 0.6), intensity 8, attenuation radius 600, slight flicker via lightmass random delay.
- [ ] `BP_ObjectiveTrigger` for `OBJ_DescentElevator` as a box volume 600x400x300 at (2700, 0, 150). Set `RequireCurrentObjective = true`, `TriggerOnce = true`, `OnlyPlayerControlledPawn = true`.
- [ ] Exit tunnel: `SM_Blockout_BasaltArch` at (3000, 0, 0), opens onto Zone 2.

### Zone 2 - First Overlook (approx X 3000 to 4200)

Footprint: 12m wide ledge, 80m drop to marsh below, framed by basalt arches on both sides. This is the postcard shot — composition matters more than complexity.

- [ ] Ledge floor: 2x `SM_Blockout_Ledge_Straight` end-to-end forming a 12x4m platform at z=100.
- [ ] Frame the view with `SM_Blockout_BasaltArch` on left (3300, -800, 0) and right (3300, 800, 0) so the player's eye is funneled toward the distance.
- [ ] Distant landmarks must be readable from this ledge:
  - Crystal Spine silhouette in center-left view (place Zone 4 hero crystals at z=2000+).
  - Ember Vent glow in far right (Zone 5 vent emissives visible past the marsh).
  - Far Survey Station as a tiny human silhouette barely visible center.
- [ ] `ExponentialHeightFog` actor with `FogDensity = 0.02`, `FogInscatteringColor` cyan-leaning (0.3, 0.55, 0.7), `StartDistance = 800`. Volumetric fog enabled.
- [ ] 1 `DirectionalLight` (or `SkyLight`) acting as ambient cavern bounce only — no sun. Intensity 0.2-0.4.
- [ ] `BP_ObjectiveTrigger` for `OBJ_FirstOverlook` as a box volume 800x1000x400 covering the ledge sweet spot at (3700, 0, 200).
- [ ] No discoveries in this zone — keep it pure as the beauty beat.
- [ ] Descent path: ramp or stepped ledges from (4200, 0, 100) down to (4400, 0, -7900) to enter the marsh. Use 4-5 `SM_Blockout_Ledge_Curve` pieces.

### Zone 3 - Mirror Marsh (approx X 4400 to 9000, Z -8000 marsh floor)

Footprint: 80m diameter shallow water basin, 1.5m water depth, fungus clusters as route markers across the surface.

- [ ] Marsh floor: 8x `SM_Blockout_BasaltWall_Large` rotated flat at z=-8050 (or `Landscape` if available).
- [ ] Water plane: a single scaled plane mesh with `M_ShallowMirrorWater` instance, sized 8000x8000, z=-7900 (10cm below player knee height for walking-through feel).
- [ ] 6-8 fungus clusters using mixed `SM_Blockout_FungusCap_S/M/L`, placed in a curving path that leads the eye from entry to exit. Cluster centers approximately at:
  - (5000, -300, -8000) - entry marker
  - (5800, 400, -8000)
  - (6400, -200, -8000)
  - (7100, 600, -8000) - hosts `D_Bio_GlasscapFungus` discovery
  - (7800, -500, -8000)
  - (8500, 100, -8000) - exit marker
- [ ] `BP_DiscoveryActor_Base` configured as `D_Bio_GlasscapFungus` at (7100, 600, -7920) with `ScanFocusOffset = (0, 0, 150)` to hit the cap.
- [ ] `BP_DiscoveryActor_Base` configured as `D_Geo_MirrorSilt` at (6700, -100, -7950), low to the water with `ScanFocusOffset = (0, 0, 30)`.
- [ ] 2-3 ceiling `SM_Blockout_CrystalCluster_L` at z=2000+ to cast cyan light shafts. Add child `PointLight` per cluster, color (0.3, 0.85, 1.0), intensity 6, radius 1500.
- [ ] Low fog layer: `ExponentialHeightFog` second-layer or a `LocalFogVolume`, `FogHeight = -7700`, density 0.06 for ankle-mist.
- [ ] `BP_ObjectiveTrigger` for `OBJ_MirrorMarsh` as a box volume 1200x1200x500 at (8500, 0, -7800), placed past both discoveries.
- [ ] Exit: climb path on +X side leading up to the Crystal Spine base.

### Zone 4 - Crystal Spine (approx X 9000 to 13000, Z -8000 to 2000 vertical traversal)

Footprint: a 35-50m vertical ridge rising out of the marsh. Player ascends via crystal shelves on alternating sides.

- [ ] Spine hero mesh: `SM_Blockout_CrystalSpine_A` at (10500, 0, -7000), scaled to 60m tall, slightly tilted (rotation pitch 5, roll -8) for natural composition.
- [ ] 5-7 climbable ledges using `SM_Blockout_Ledge_Straight` and `SM_Blockout_Ledge_Curve` arranged in a zig-zag from z=-7800 up to z=1800. Each ledge 4x3m, 80cm step height between them.
- [ ] 4-6 `SM_Blockout_CrystalCluster_M` and `_L` along the ridge as visual landmarks. Each gets a child `PointLight` (0.3, 0.85, 1.0), intensity 4, radius 800.
- [ ] `BP_DiscoveryActor_Base` configured as `D_Geo_PulseQuartz` on a mid-climb ledge at (10800, 400, -3500), `ScanFocusOffset = (0, 0, 60)`.
- [ ] `BP_DiscoveryActor_Base` configured as `D_Anomaly_ResonantVein` at (11400, -300, 800), placed on a vein running across the upper spine. `ScanFocusOffset = (0, 0, 40)`.
- [ ] `BP_ObjectiveTrigger` for `OBJ_CrystalSpine` as a box volume 1000x1000x600 at the ridge crest (11500, 0, 1900).
- [ ] Ensure Ember Vents are visible warm-glow in the distance from the crest — this is the second pre-reveal moment.
- [ ] Exit: descent path on the far side, leading down toward the Ember Vents at z=-2000.

### Zone 5 - Ember Vents (approx X 13000 to 16500, Z -2000)

Footprint: a wider chamber with 4-6 visible vent columns, drifting steam, black wet rock floor. Color palette flips from cyan to amber here.

- [ ] Floor: 4-6 `SM_Blockout_BasaltWall_Large` rotated flat at z=-2050, scattered slightly for organic edges.
- [ ] 5-6 `SM_Blockout_VentCone` placed in a loose arc:
  - (13500, -400, -2000)
  - (14000, 300, -2000) - hosts `D_Geo_EmberVent`
  - (14500, -100, -2000)
  - (15000, 500, -2000)
  - (15500, -300, -2000)
- [ ] Each vent gets a child `PointLight` with color (1.0, 0.45, 0.15), intensity 12, radius 700, plus a `NiagaraSystem` placeholder slot for steam (no particles needed in M1 blockout — use scaled emissive plane).
- [ ] `BP_DiscoveryActor_Base` configured as `D_Geo_EmberVent` at (14000, 300, -1900), `ScanFocusOffset = (0, 0, 120)` to hit the cone tip.
- [ ] `BP_DiscoveryActor_Base` configured as `D_Bio_ThermalFilament` clinging to a wet rock at (14700, -200, -1980), `ScanFocusOffset = (0, 0, 25)`.
- [ ] `ExponentialHeightFog` override volume in this zone with amber-leaning inscatter color (0.7, 0.4, 0.2), density 0.04.
- [ ] `BP_ObjectiveTrigger` for `OBJ_EmberVents` as a box volume 1000x1200x500 at (16000, 0, -1900), placed past all vents but before the survey station entrance.
- [ ] Exit: a basalt arch at (16500, 0, -2000) opens toward the human station.

### Zone 6 - Far Survey Station (approx X 16500 to 19000, Z -1500)

Footprint: small human-built outpost on a ledge, then a final overlook framing a vastly larger cavern beyond.

- [ ] Station platform: `SM_Blockout_SurveyPlatform` at (17000, 0, -1500), scaled to 8x6m.
- [ ] 4-6 placeholder crates / equipment props (engine primitives are fine for M1).
- [ ] 3-4 `PointLight` actors with cold white work-light color (0.85, 0.9, 1.0), intensity 5, radius 400 — these should look weak and human against the cavern scale.
- [ ] `BP_ObjectiveTrigger` for `OBJ_FarSurveyStation` as a box volume 600x600x400 at (17200, 0, -1400), at the station entrance.
- [ ] Final overlook ledge extends past the station to (18500, 0, -1500). Use 2x `SM_Blockout_Ledge_Straight`.
- [ ] `BP_DiscoveryActor_Base` configured as `D_Anomaly_SecondSkyCavern` at (18500, 0, -1400). **Set `ObjectiveIdToCompleteOnScan = OBJ_SecondSkyOverlook` and `bCompleteObjectiveOnlyOnNewDiscovery = true`.** No trigger volume needed — scanning the vista completes the route.
- [ ] Beyond the ledge: a vast distant chamber readable as "second sky". Place a single huge curved basalt back-wall mesh at (24000, 0, -3000) scaled to enormous (200x200x200) to suggest depth. Add a faint warm-cyan light far below (z=-8000) to imply more world.

## Beacon Placement Guidance

Beacons are player-placed, but the level should have 3-4 natural "ah, I'd put one here" spots. Make sure the geometry near these points has a clear ledge or wall surface within a 900-unit `MaxBeaconPlacementDistance` line trace from the typical player path:

- First Overlook ledge near the descent ramp (handy as a "back to start" marker).
- Mirror Marsh exit, before the climb begins.
- Crystal Spine crest, looking back over the route taken.
- Ember Vents entrance, in case the player wants to retreat from the warmer zone.

## Landmark Layout

Top-down rough arrangement:

```
                Second Sky Overlook
                        |
              Far Survey Station
                        |
        Ember Vents ----+---- Crystal Spine
              \              /
               \            /
                Mirror Marsh
                    |
              First Overlook
                    |
             Descent Elevator
```

## Lighting Notes

- First Overlook: low exposure adaptation into vast cyan/amber reveal.
- Mirror Marsh: cyan fungus bounce with strong water reflections.
- Crystal Spine: blue-white emissive veins and sharp silhouettes.
- Ember Vents: orange volumetric fog with black rock shapes.
- Far Station: human white work lights look weak against the cavern.

## Blockout Mesh List

- `SM_Blockout_BasaltWall_Large`
- `SM_Blockout_BasaltArch`
- `SM_Blockout_Ledge_Straight`
- `SM_Blockout_Ledge_Curve`
- `SM_Blockout_CrystalSpine_A`
- `SM_Blockout_CrystalCluster_S/M/L`
- `SM_Blockout_FungusCap_S/M/L`
- `SM_Blockout_VentCone`
- `SM_Blockout_SurveyPlatform`

## Objective Trigger Checklist

Use Blueprint children of `AObjectiveTriggerActor` with visible editor-only labels so the first playable route can be tested before final art. Keep trigger volumes wide enough to catch normal exploration, but place them at clear spatial commitments rather than every few meters.

- `OBJ_DescentElevator`: just beyond the elevator platform exit, after the player steps into the basalt access tunnel.
- `OBJ_FirstOverlook`: at the reveal ledge where the Mirror Marsh, Crystal Spine, and Ember Vents are all readable.
- `OBJ_MirrorMarsh`: on the far side of the marsh path, after at least one fungus cluster and the mirror silt discovery placement.
- `OBJ_CrystalSpine`: at the ridge crest, where pulse quartz and the next warm vent landmark are visible.
- `OBJ_EmberVents`: after the final vent column cluster, before the path bends toward human survey lights.
- `OBJ_FarSurveyStation`: at the station entrance platform, before the final scan/readout beat.
- `OBJ_SecondSkyOverlook`: complete this from `D_Anomaly_SecondSkyCavern.ObjectiveIdToCompleteOnScan` after the player scans the final vista. Use a trigger volume only as a fallback for early blockout testing.

Suggested Blueprint behavior:

- Bind HUD text to `UObjectiveSubsystem::OnObjectiveChanged`.
- Use `GetObjectiveHudText` for the compact objective line and `GetObjectiveProgress` for step counters/progress bars.
- Play a restrained chime or scanner ping from `OnObjectiveTriggerActivated(true)`.
- Set `ObjectiveIdToCompleteOnScan` on the final Second Sky discovery so `OnRouteCompleted` fires after the actual scan.
