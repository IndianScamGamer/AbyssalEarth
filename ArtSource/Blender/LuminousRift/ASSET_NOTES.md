# Luminous Rift Asset Notes

This file tracks Blender-created source assets for the Luminous Rift kit. Claude/Blender workers should update it whenever they create or revise an asset.

## Prompt Package

Detailed Claude/Blender prompts for the first Luminous Rift asset pass live under:

- Docs/AssetPrompts/LuminousRift/01_BlueCrystalClusters.md
- Docs/AssetPrompts/LuminousRift/02_ForegroundLedge_RockFrame.md
- Docs/AssetPrompts/LuminousRift/03_BridgeSpanKit.md
- Docs/AssetPrompts/LuminousRift/04_HexCollectorPanels.md
- Docs/AssetPrompts/LuminousRift/05_OrbApparatus.md
- Docs/AssetPrompts/LuminousRift/06_AncientGateWall.md

Workers should use these prompts with Docs/CORE_REFERENCE_LUMINOUS_RIFT.md, Docs/BLENDER_ASSET_PIPELINE.md, and Docs/MATERIAL_SPECS.md. After creating any mesh, replace the relevant status below with source/export paths and production notes.

## Required Note Format

Each asset entry should include:

- Asset name
- Source `.blend` path
- Export path
- Intended use
- Approximate dimensions in meters
- Pivot/origin
- Collision recommendation
- Material slots
- Nanite/LOD recommendation
- Known issues

## Initial P0 Targets

### SM_Rift_ForegroundLedge_A

- Status: needed.
- Intended use: first concept-art reveal ledge and possible final overlook ledge.
- Approximate dimensions: playable 8-12 m wide x 10-18 m long; visual shelf 25-40 m wide.
- Pivot/origin: center of walkable top at floor level.
- Collision: simple walkable collision on central top surface; decorative overhangs can be no collision.
- Material slots: `mat_wet_basalt`, `mat_crystal_blue`, `mat_blue_emissive`.
- Nanite/LOD: Nanite recommended.

### SM_Rift_CrystalCluster_S/M/L/Hero

- Status: needed.
- Intended use: route language, local lighting accents, foreground silhouettes.
- Approximate dimensions: S 0.5-1.5 m, M 2-4 m, L 5-9 m, Hero 10-18 m.
- Pivot/origin: base center at floor contact.
- Collision: none for small/distant clusters; simple convex for clusters near player path.
- Material slots: `mat_crystal_blue`, `mat_blue_emissive`, optional `mat_wet_basalt` base.
- Nanite/LOD: Nanite acceptable for large/hero meshes; simple LODs acceptable for small clusters.

### SM_Rift_BridgeSpan_A / SM_Rift_BridgeSpan_B_Broken

- Status: needed.
- Intended use: traversable ancient bridge kit across the abyss.
- Approximate dimensions: 6-10 m wide, 12-48 m long.
- Pivot/origin: centerline at top walkable surface or start-edge snap point; document exact choice when created.
- Collision: simple box/convex collision for walkable top.
- Material slots: `mat_ancient_machine_dark`, `mat_ancient_machine_edge_wear`, `mat_blue_emissive`, `mat_wet_basalt`.
- Nanite/LOD: Nanite recommended for decorative mesh; collision kept simple.

### SM_Rift_HexCollector_Tile_A / SM_Rift_HexCollector_Cluster_A/B

- Status: needed.
- Intended use: honeycomb collector panels around central energy sphere.
- Approximate dimensions: tile 4-7 m across; cluster 20-35 m wide.
- Pivot/origin: tile center for tiles; beam attachment center for clusters.
- Collision: none unless reachable; decorative only in first pass.
- Material slots: `mat_gold_emissive`, `mat_collector_glass`, `mat_ancient_machine_dark`.
- Nanite/LOD: non-Nanite may be better for translucent pane variants; frames can be Nanite.

### SM_Rift_OrbFrame_A / SM_Rift_OrbHub_A / SM_Rift_BeamEmitterNode_A

- Status: needed.
- Intended use: central orb apparatus and gold beam endpoints.
- Approximate dimensions: frame 30-50 m diameter, hub 8-18 m diameter, emitter node 2-5 m diameter.
- Pivot/origin: orb/frame/hub at orb center; emitter node at beam connection point.
- Collision: none for orb apparatus in first pass.
- Material slots: `mat_ancient_machine_dark`, `mat_gold_emissive`, `mat_blue_emissive`, optional `mat_orb_energy` for proxy sphere.
- Nanite/LOD: Nanite recommended for frame/hub; beam effects handled in Unreal.

### SM_Rift_AncientWall_Gate_A

- Status: needed.
- Intended use: monumental right-side gate/wall matching the concept reference.
- Approximate dimensions: 40-60 m wide, 80-140 m tall, 8-20 m deep.
- Pivot/origin: bottom center.
- Collision: blocking volume in Unreal; mesh can be decorative.
- Material slots: `mat_ancient_machine_dark`, `mat_ancient_machine_edge_wear`, `mat_blue_emissive`, `mat_crystal_blue`, `mat_wet_basalt`.
- Nanite/LOD: Nanite recommended.
