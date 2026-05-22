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
