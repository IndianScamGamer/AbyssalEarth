# Inner Sea Blockout Plan

Map 03 of the Abyssal Earth descent (`Docs/WORLD_ATLAS.md`). After the verticality
of the Luminous Rift and the intimate biology of the Glassroot Forest, the Inner
Sea opens the world **horizontally**: a vast underground ocean that proves the
inner Earth has scale beyond walkable caverns. This map introduces water-edge
traversal, navigation uncertainty across similar-looking spaces, distant
landmarks, and larger route planning.

Concept references:

- `Content/ArtDirection/WorldMaps/inner_sea_concept.png` (hero target)
- `Content/ArtDirection/Concepts/Inner_Sea/` (IS-001 … IS-006 studies)
- Review notes: `Docs/CONCEPT_ART_REVIEW.md`

## Goal

Build a 12-16 minute traversal along the shores and ruins of an underground sea,
where the readable route is drawn by **scanner-reactive gold plankton trails** over
silver-black water. The player crosses wet basalt docks, broken ancient piers, and
half-submerged ruins, marking return routes with beacons, toward a far-shore
overlook that hints at the next layer (Fossil Sky).

## Scale

Unreal units are centimeters. This is the largest horizontal map so far.

- Total playable route length: 800-1200 meters (mostly horizontal).
- Open water span to far cave walls: 400-800 meters (scale silhouettes).
- Cavern ceiling height: 80-160 meters with hanging stalactites and mineral shelves.
- Dock/pier width: 3-7 meters; broken gaps 1.5-4 meters (step/jump or skiff).
- Water: shallow walkable edges 0.1-0.5 m; open water is non-walkable depth.
- Distant islands: 40-120 m wide silhouettes fading into teal haze.
- Plankton trail ribbons: 0.5-1.5 m wide glowing surface currents.

## Traversal Decision (flag for production)

`WORLD_ATLAS.md` leaves open whether water traversal is walking-only, skiff-based,
or staged for later. **P0 recommendation:** dock + stepping-stone-ruin walking only,
with a moored skiff as set dressing and a single scripted short skiff crossing near
the end. Full free skiff piloting and floating scanner buoys are staged as a later
upgrade (roadmap C3 traversal modifiers). Underwater diving stays out of P0.

## Route Overview

### 1. Shore Threshold (transition in)

Purpose: connect from the Glassroot Forest and withhold the sea reveal.

- Wet basalt cave mouth; growing sound of water slosh and distant cavern groans.
- No discoveries; a descending wet corridor that hides the sea until the overlook.

### 2. First Overlook (Wet Basalt Dock)

Purpose: the postcard beauty moment matching the concept art.

- Player steps onto a wet basalt dock above the underground sea.
- Water vanishes into blue-black distance; **gold plankton trails** draw route lines
  across the surface; broken ancient piers and half-submerged machine structures
  imply the sea drowned something older. Distant islands and blue-lit ruins read far off.
- Discovery: `D_Geo_AbyssalBrineSea`.

### 3. Pier Walk (Broken Piers)

Purpose: introduce edge traversal and gap crossing.

- Route follows wet docks and broken ancient piers with small gaps.
- A moored skiff sits at a pier (set dressing / future traversal).
- Discovery: `D_Structure_DrownedPier`.

### 4. Plankton Channels

Purpose: teach scanner-reactive route reading.

- Stepping-stone ruins cross a channel where gold plankton trails brighten and flow
  toward the safe path when pulsed by the scanner.
- Discovery: `D_Bio_GoldPlanktonTrail`.

### 5. Drowned Ruins

Purpose: the signature hazard zone.

- Half-submerged blue-lit machine ruins; periodic **electrical discharges** arc
  across submerged metal (timed hazard the player reads and avoids).
- Optional: deploy a floating scanner buoy to reveal the safe crossing.
- Discovery: `D_Anomaly_TideWithoutMoon` (tide patterns with no surface lunar cause).

### 6. Forward Dock (Human Camp)

Purpose: human-scale waypoint and staging.

- A temporary human staging dock with lamps, crates, and a tethered skiff.
- Discovery: `D_Human_ForwardDock`.
- Natural beacon/save waypoint before the final crossing.

### 7. Far Shore Overlook (final reveal)

Purpose: route completion and a pointer to the next map.

- A short scripted skiff crossing or a final pier reaches the far shore platform.
- The sea opens into even greater distance; high on the far cavern wall, pale
  bone-white shelves and a faint fossil silhouette hint at the Fossil Sky above.
- Scanning the vista completes `CHK_IS_FarShoreOverlook`.

## Room-by-Room Placement Checklist

Coordinates assume map origin at the shore-threshold entry, +X is the forward route
direction along the shore, +Y crosses toward open water, +Z is up. Anchors, not
final layout — the open-water scale and the readable plankton route matter most.

When this map enters production, mirror these rows into a
`Content/Design/InnerSeaBlockoutChecklist.csv` (same shape as
`LuminousRiftBlockoutChecklist.csv`).

### Zone 1 - Shore Threshold (X 0 to 2500)

- [ ] `PlayerStart` at (0, 0, 100), facing +X.
- [ ] Wet basalt corridor, 4-6 m wide, one bend hiding the sea.
- [ ] Rising water-slosh ambience near the exit.
- [ ] `BP_ObjectiveTrigger`: `CHK_IS_ShoreThreshold`, box 500x500x300 at (2300, 0, 120).

### Zone 2 - First Overlook (X 2500 to 4500)

The postcard shot. Use the concept image as direct reference.

- [ ] Wet basalt dock at (3000, 0, 0), 6-8 m wide, reflective surface material.
- [ ] Open water plane from Y 800 outward to the far walls.
- [ ] 4-8 `BP_InnerSea_PlanktonTrailSpline` ribbons across the water, drawing the route.
- [ ] 3-5 `SM_InnerSea_BrokenPier_A/B` mid-water; 2-3 `SM_InnerSea_DistantIsland_A/B` on the horizon.
- [ ] `SM_InnerSea_MineralShelf_Ceiling_A` shelves + stalactites overhead.
- [ ] Blue-lit `SM_InnerSea_SubmergedRuin_A` cluster visible to the left.
- [ ] One player-scale cue near the dock edge (lamp, beacon, survey marker).
- [ ] `BP_DiscoveryActor_Base`: `D_Geo_AbyssalBrineSea` at (3200, 600, -40), `ScanFocusOffset = (0, 200, 60)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_IS_FirstOverlook`, box 1000x1400x400 at (3300, 0, 150).

Lighting: warm gold plankton & lamp accents over cool silver-black water; teal
volumetric haze for depth; blue-lit ruins as secondary accents.

### Zone 3 - Pier Walk (X 4500 to 7500)

- [ ] 3-5 `SM_InnerSea_BasaltDock_A/B` + `SM_InnerSea_BrokenPier_A/B` with 1.5-4 m gaps.
- [ ] A moored skiff (set dressing) at one pier.
- [ ] `BP_DiscoveryActor_Base`: `D_Structure_DrownedPier` at (6000, 400, -20), `ScanFocusOffset = (0, 0, 120)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_IS_PierWalk`, box 900x900x400 at (7300, 0, 60).

Safety: collision blockers on open-water edges for early prototype; hide with pier
posts and rope lines.

### Zone 4 - Plankton Channels (X 7500 to 10000)

- [ ] Stepping-stone ruin blocks across a channel; gaps require deliberate steps.
- [ ] Dense `BP_InnerSea_PlanktonTrailSpline` ribbons that brighten/flow on scan pulse.
- [ ] `BP_DiscoveryActor_Base`: `D_Bio_GoldPlanktonTrail` at (8700, 300, 10), `ScanFocusOffset = (0, 0, 50)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_IS_PlanktonChannels`, box 900x1000x400 at (9800, 0, 40).

### Zone 5 - Drowned Ruins (X 10000 to 13000)

Signature hazard zone.

- [ ] `SM_InnerSea_SubmergedRuin_A/B/C` cluster, half-submerged, blue-lit.
- [ ] Timed electrical-discharge hazard arcing across submerged metal (roadmap C2).
- [ ] Optional `SM_InnerSea_Buoy_A` deploy point that reveals the safe crossing.
- [ ] `BP_DiscoveryActor_Base`: `D_Anomaly_TideWithoutMoon` at (11500, 500, 20), `ScanFocusOffset = (0, 0, 150)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_IS_DrownedRuins`, box 1100x1100x500 at (12800, 0, 40).

### Zone 6 - Forward Dock (X 13000 to 15000)

- [ ] Human staging dock: lamps, `SM_Human_SurveyCrate_A`, cable coils, a tethered skiff.
- [ ] `BP_DiscoveryActor_Base`: `D_Human_ForwardDock` at (14000, 0, 60), `ScanFocusOffset = (0, 0, 80)`.
- [ ] `BP_ObjectiveTrigger`: `CHK_IS_ForwardDock`, box 900x900x400 at (14800, 0, 60).

### Zone 7 - Far Shore Overlook (X 15000 to 18000)

Final reveal and end beat.

- [ ] Short scripted skiff crossing or final pier to the far shore platform at (17500, 0, 40).
- [ ] Open sea recedes into teal distance; far wall shows pale bone-white shelves and
      a faint fossil silhouette (Fossil Sky hint, next map).
- [ ] `BP_DiscoveryActor_Base`: vista discovery with `ObjectiveIdToCompleteOnScan = CHK_IS_FarShoreOverlook`, `bCompleteObjectiveOnlyOnNewDiscovery = true`.

## Landmark Layout

Top-down rough arrangement (route hugs the shore, sea opens to +Y):

```
  Shore        Pier      Plankton    Drowned    Forward     Far Shore
  Threshold -> Walk  ->  Channels -> Ruins  ->  Dock    ->  Overlook
     |          |           |          |          |            | (Fossil Sky hint)
  ===============================  open sea (+Y)  ===============================
   gold plankton trails . . . distant islands . . . blue-lit submerged ruins
```

Wide-shot composition from First Overlook:

```
  stalactite ceiling + hanging mineral shelves
  ------------------------------------------------
  foreground wet dock     gold plankton trails    distant islands
  player + lamp           broken piers / skiff     blue-lit ruins
  silver-black water       teal haze depth         far cavern wall
```

## Beacon Placement Guidance

Beacons matter more here than any prior map — water spaces look alike. Invite them at:

- First Overlook before leaving the dock.
- End of the Pier Walk.
- Mid Plankton Channels.
- Before the Drowned Ruins hazard crossing.
- Forward Dock (primary waypoint).

## Blockout Mesh List

P0:

- `SM_InnerSea_BasaltDock_A/B`
- `SM_InnerSea_BrokenPier_A/B`
- `SM_InnerSea_SubmergedRuin_A/B/C`
- `SM_InnerSea_MineralShelf_Ceiling_A`
- `SM_InnerSea_DistantIsland_A/B`
- `BP_InnerSea_PlanktonTrailSpline`

P1:

- `SM_InnerSea_Buoy_A`
- `M_InnerSea_SilverBlackWater_Master`
- `M_InnerSea_GoldPlankton_Master`
- (reuse) `SM_Human_SurveyCrate_A`, `SM_Human_PortableLamp_A`, `SM_Human_CableCoil_A`

## Proposed Discovery Catalog Rows

For a future `Content/Design/DiscoveryCatalog_World.csv`. Columns match
`DiscoveryCatalog.csv`. All categories below are valid `EDiscoveryCategory` members.

| DiscoveryId | DisplayName | Category | Zone |
| --- | --- | --- | --- |
| `D_Geo_AbyssalBrineSea` | Abyssal Brine Sea | Geology | First Overlook |
| `D_Structure_DrownedPier` | Drowned Pier | Structure | Pier Walk |
| `D_Bio_GoldPlanktonTrail` | Gold Plankton Trail | Biology | Plankton Channels |
| `D_Anomaly_TideWithoutMoon` | Tide Without a Moon | Anomaly | Drowned Ruins |
| `D_Human_ForwardDock` | Forward Dock | HumanMade | Forward Dock |

## Hazards

- Flooding route changes (timed water-level shifts altering the safe path).
- Low-visibility water pockets / fog banks.
- Electrical discharges in submerged machine ruins (timed).
- Moving platforms or floating debris.

## Ambience Direction

Deep water slosh, distant cavern groans, echoing droplets, faint whale-like low
tones, plankton shimmer, creaking docks. For a future `DT_InnerSeaAmbience.csv`.

## Objective Trigger Checklist

The `CHK_IS_*` ids are spatial checkpoints, not the player-facing main objective arc
(`OBJ_VERIFY_HELIOS` … `OBJ_OPEN_RIFT` in `UObjectiveSubsystem`). Within this map the
player is in the `OBJ_DISCOVER_PLACE` / `OBJ_BUILD_WAY_OUT` band.

- `CHK_IS_ShoreThreshold`: enter from the Glassroot connector.
- `CHK_IS_FirstOverlook`: first full view of the sea.
- `CHK_IS_PierWalk`: crossed the broken piers.
- `CHK_IS_PlanktonChannels`: crossed the plankton channel.
- `CHK_IS_DrownedRuins`: cleared the electrical-hazard ruins.
- `CHK_IS_ForwardDock`: reached the human staging dock.
- `CHK_IS_FarShoreOverlook`: completed by scanning the far-shore vista discovery.

## Screenshot Review Checklist

Take screenshots from:

- Shore threshold exit before the reveal.
- First Overlook, matching the concept art.
- Pier Walk, with broken piers and a moored skiff.
- Plankton Channels, trails glowing along the route.
- Drowned Ruins, blue-lit and half-submerged.
- Forward Dock, warm human camp against the dark sea.
- Far Shore Overlook, with the Fossil Sky hint on the far wall.

For the First Overlook screenshot to pass:

- Gold plankton trails read as the route across the water.
- Silver-black water reflects the scene.
- Broken piers and at least one distant island are visible.
- Blue-lit submerged ruins read as drowned machinery.
- Hanging mineral shelves/stalactites frame the top.
- A human scale cue is present.
- The space reads as a vast ocean, never a small pool.
