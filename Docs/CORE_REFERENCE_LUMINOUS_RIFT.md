# Core Reference - Luminous Rift

## File

`Content/ArtDirection/References/luminous_rift_core_reference.png`

This image is the core target for the Luminous Rift map. Treat it as a production reference, not mood art. Asset generation, level blockout, lighting, material work, and screenshot review should all compare against this image.

## One-Sentence Target

A lone explorer stands on a dark rock ledge before a gigantic underground abyss where ancient carved machinery, blue crystal growth, suspended platforms, and a radiant blue-white energy sphere are tied together by warm gold beam arrays.

## Image Breakdown

### Camera And Composition

- Wide cinematic view from a high foreground ledge.
- Player silhouette in the lower-left foreground establishes human scale.
- The center of the image is dominated by a bright suspended orb.
- Gold beam lines radiate from mechanical nodes into hexagonal collector panels.
- The right third contains a monumental vertical gate/wall with circular blue-lit mechanisms.
- The left and upper edges are framed by dark cave overhangs and rough stone.
- The lower center falls into a deep blue rift, creating strong vertical depth.
- Distant towers and cavern walls fade into blue atmospheric perspective.

### Scale

Use these scale relationships when modeling:

- Player: about 180 cm.
- Foreground ledge width: 6-10 m playable surface, but visually part of a 25-40 m rock shelf.
- Central orb diameter: 18-28 m.
- Hex collector flower clusters: 20-35 m wide each.
- Collector support ring/arc: 80-140 m wide.
- Main bridge/platform spans: 8-16 m wide, 50-120 m long.
- Right-side ancient gate: 80-140 m tall in the first playable slice.
- Cavern height visible from overlook: 250-500 m.
- Abyss drop below route: visually 300 m or more, even if collision blocks the player earlier.

### Geometry Families

#### Dark Cavern Shell

- Irregular basalt walls, ceiling shelves, and overhangs.
- Vertical grooves and erosion channels.
- Sharp silhouette edges, especially around the top and sides of the shot.
- Rock should wrap around and partially swallow architecture.

#### Ancient Architecture

- Large, dark, carved, monolithic structures.
- Recessed blue light channels.
- Circular sockets and radial rings.
- Tall towers with vertical striping and panel seams.
- Bridge slabs with layered undersides, cracks, and missing chunks.
- Surfaces should be readable as stone-metal hybrid rather than polished steel.

#### Energy Apparatus

- Central blue-white orb with turbulent internal texture.
- Mechanical radial hub beside or partly behind the orb.
- Thin gold beam lines connecting orb/hub to collector panels.
- Hexagonal panels arranged into flower-like clusters.
- Each panel has a thin gold frame and translucent blue-white interior.
- Some panels should be broken, tilted, or missing to avoid sterile symmetry.

#### Crystals

- Saturated blue/cyan clusters embedded in ledges, walls, and machine bases.
- Forms should be faceted and angular, not soft organic growth.
- Sizes range from 0.5 m shards to 8 m hero crystals.
- Crystals work as accent lights and visual breadcrumbs along the route.

#### Human Survey Presence

- One small explorer silhouette is enough for the key vista.
- Add practical props only near player path: lamps, crates, cables, beacon, small console.
- Human items must look temporary and recent, not part of the ancient structure.

## Lighting Breakdown

### Primary Light

The orb is the brightest object. It should cast cool blue-white light on nearby panels, bridges, and mist.

Implementation target:

- Use an emissive orb material plus one or more hidden point/rect lights.
- Keep the emissive texture detailed. Bloom is allowed, but the orb must not become a flat white circle.
- Add slow animated noise to imply energy movement.

### Secondary Warm Light

Gold beams and collector nodes supply the warm contrast.

Implementation target:

- Use spline meshes or Niagara beam emitters for gold lines.
- Attach small warm point lights to beam endpoints.
- Beam color should be gold/amber, not red/orange lava.

### Accent Blue Light

Crystals and machine seams provide localized cyan glows.

Implementation target:

- Use emissive crystal material instances.
- Add small point lights only to clusters close to the player or important silhouettes.
- Keep distant crystals emissive-only for performance.

### Atmosphere

- Dense but readable volumetric fog.
- Blue atmospheric perspective in the abyss.
- Floating dust/motes visible in beam paths.
- Vertical light shafts from above and below.

## Material Breakdown

### Rock

- Near-black wet basalt.
- Blue-gray edge highlights.
- Layered striation normals.
- Occasional glossy wet patches.
- Cracked and broken where machine structure pierces the stone.

### Ancient Stone-Metal

- Dark graphite/bronze base.
- Worn bevels with subtle gold/brown edge exposure.
- Recessed grooves with blue emissive strips.
- Panel seams and circular insets.
- Dust, mineral deposits, and cracks to show age.

### Collector Panels

- Thin gold/brass metal frame.
- Translucent frosted blue-white pane.
- Inner hex pattern or subtle circuit-like linework.
- Some panels chipped, missing, rotated, or dark.

### Orb

- Layered translucent-looking energy shell.
- White/cyan core.
- Electric tendrils/noise inside.
- Fresnel rim glow.
- Slow pulse, not frantic flicker.

### Crystals

- Deep blue body, cyan internal glow, white rim.
- Rough/faceted normal.
- Different material instances for dim, medium, and high-glow clusters.

## Required First-Pass Assets

Create these before polishing minor props.

| Priority | Asset | Purpose |
|---|---|---|
| P0 | `SM_Rift_ForegroundLedge_A` | Player reveal ledge matching the lower-left reference silhouette. |
| P0 | `SM_Rift_BridgeSpan_A` | Main traversal bridge/platform toward the central apparatus. |
| P0 | `SM_Rift_AncientWall_Gate_A` | Right-side monumental gate/wall with circular blue-lit mechanisms. |
| P0 | `SM_Rift_OrbFrame_A` | Central hub/ring support around the energy sphere. |
| P0 | `SM_Rift_HexCollector_Cluster_A` | Flower-like hex collector panel cluster. |
| P0 | `SM_Rift_CrystalCluster_S/M/L/Hero` | Blue crystals for route language and lighting accents. |
| P0 | `M_Rift_EnergyOrb_Master` | Orb material target. |
| P0 | `M_Rift_AncientMachine_Master` | Ancient architecture material target. |
| P1 | `SM_Rift_TowerSegment_A/B` | Vertical distant towers and structural supports. |
| P1 | `SM_Rift_HangingSlab_A/B` | Ceiling and abyss silhouettes. |
| P1 | `SM_Rift_RockArch_A/B` | Natural frame around the vista. |
| P1 | `SM_Rift_BeamEmitterNode_A` | Gold beam endpoint device. |
| P1 | `SM_Human_SurveyKit_A` | Small props for scale near player path. |

## Screenshot Acceptance Criteria

A generated map screenshot is on-target only if these are true:

- A tiny player or human prop is visible against a huge environment.
- The central orb is the dominant focal point.
- Gold beam lines are visible and connect to hex-panel collectors.
- Dark rock frames the top/left/right edges of the view.
- Blue crystals appear in foreground and midground.
- The right-side monumental gate/wall reads as ancient machinery.
- The lower center reads as a deep vertical abyss, not a flat floor.
- The scene has strong cyan/blue light but still contains warm gold contrast.

## Negative Checks

Reject or revise outputs that look like:

- A plain cave with random crystals.
- A mushroom forest.
- A lava cavern.
- A clean spaceship interior.
- A flat platform arena.
- A blue/purple fog scene without gold beam structure.
- A symmetrical sci-fi device with no erosion, rock, or age.
