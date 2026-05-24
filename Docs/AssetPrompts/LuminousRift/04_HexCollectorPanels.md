# Claude/Blender Prompt - Hex Collector Panels

You are working on Abyssal Earth, an Unreal Engine 5 first-person exploration game. Create the hexagonal collector panel kit for the Luminous Rift central apparatus.

Read before modeling:

- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/MATERIAL_SPECS.md

Use Content/ArtDirection/References/luminous_rift_core_reference.png as the source of truth. The gold beam network and honeycomb collector panels are essential to making the scene match the concept.

## Assets To Create

- SM_Rift_HexCollector_Tile_A
- SM_Rift_HexCollector_Cluster_A
- SM_Rift_HexCollector_Cluster_B_Broken

Optional if useful:

- SM_Rift_HexCollector_Frame_A

## Scale Targets

- Single hex tile: 4-7 m across.
- Cluster: 20-35 m wide.
- Frame thickness: 0.15-0.4 m.
- Cluster should hold 7-13 hex tiles in a flower-like arrangement.

## Visual Requirements

- Tile shape must read as a clear hexagon from 100 m away.
- Each tile should have a warm gold/brass outer frame and a frosted blue-white interior pane.
- Clusters should form petal/flower groupings around a central beam attachment node.
- Broken cluster must preserve the flower silhouette while including missing panes, rotated tiles, cracked glass, or dark inactive panes.
- Add small dark machine brackets or arms so panels feel like ancient machinery rather than floating UI.
- Use asymmetry, damage, and slight depth offsets to avoid sterile radial perfection.

## Material Slots

Use these exact material slot names:

- mat_gold_emissive
- mat_collector_glass
- mat_ancient_machine_dark

## Pivot, Collision, And Export

- Single tile pivot: tile center.
- Cluster pivot: central beam attachment hub.
- Collision: none for first pass unless a panel is reachable.
- Transparent panes may be non-Nanite; frames can be Nanite.
- Apply transforms and keep Unreal-compatible metric scale.
- Save .blend source under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX or GLB under Content/ArtSourceExports/LuminousRift/.

## Acceptance Checklist

- Tile and cluster silhouettes are readable from First Overlook distance.
- Gold frames provide warm contrast against blue panes.
- Broken cluster looks intentionally damaged and ancient, not like an import error.
- The central attachment node is obvious enough for Unreal gold beam spline placement.
- ArtSource/Blender/LuminousRift/ASSET_NOTES.md is updated for every exported mesh.

