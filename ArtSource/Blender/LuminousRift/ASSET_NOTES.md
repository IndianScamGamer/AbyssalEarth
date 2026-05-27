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
- Docs/AssetPrompts/LuminousRift/07_BackgroundDepthKit.md
- Docs/AssetPrompts/LuminousRift/08_HumanSurveyKit.md

Workers should use these prompts with Docs/CORE_REFERENCE_LUMINOUS_RIFT.md, Docs/BLENDER_ASSET_PIPELINE.md, and Docs/MATERIAL_SPECS.md. After creating any mesh, replace the relevant status below with source/export paths and production notes.

## Active Work Orders

Use work orders when starting an export batch. They turn the broader prompts into a concrete production sequence and handoff checklist.

- Docs/AssetWorkOrders/LuminousRift/01_CrystalExportBatch.md - create and export the nine blue crystal cluster variants first.
- Docs/AssetWorkOrders/LuminousRift/02_ForegroundRevealKit.md - create and export the first-overlook ledge, rock arches, and overhang variants next.

Use `Content/Design/LuminousRiftAssetImportChecklist.csv` as the export/import handoff tracker. When an asset is exported from Blender, update its checklist row with the current status and any pivot, collision, material-slot, or import issues found in Unreal.

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
- Active work order: Docs/AssetWorkOrders/LuminousRift/02_ForegroundRevealKit.md.

### SM_Rift_RockArch_A/B and SM_Rift_Overhang_A/B

- Status: needed.
- Intended use: first-overlook and second-sky vista framing so the scene reads like the core reference instead of an open arena.
- Approximate dimensions: rock arches 30-80 m span; overhangs 20-60 m apparent depth.
- Pivot/origin: document per mesh; use a placement-friendly base/anchor point rather than arbitrary scene center.
- Collision: none for decorative framing pieces unless reused near the player route; use Unreal blocking volumes for player-facing uses.
- Material slots: `mat_wet_basalt`, optional `mat_crystal_blue`, optional `mat_blue_emissive` if crystals are embedded.
- Nanite/LOD: Nanite recommended.
- Variant intent: A = strong primary reveal frame, B = broken/asymmetric alternate for repeated vista use.
- Active work order: Docs/AssetWorkOrders/LuminousRift/02_ForegroundRevealKit.md.

### SM_Rift_CrystalCluster_S_A/B/C, M_A/B/C, L_A/B, Hero_A

- Status: needed.
- Intended use: route language, local lighting accents, foreground silhouettes.
- Approximate dimensions: S 0.5-1.5 m, M 2-4 m, L 5-9 m, Hero 10-18 m.
- Pivot/origin: base center at floor contact.
- Collision: none for small/distant clusters; simple convex for clusters near player path.
- Material slots: `mat_crystal_blue`, `mat_blue_emissive`, optional `mat_wet_basalt` base.
- Nanite/LOD: Nanite acceptable for large/hero meshes; simple LODs acceptable for small clusters.
- Variant intent: A = clean route-readable silhouette, B = broken/asymmetric wall or ledge silhouette, C = low dense scatter/breadcrumb silhouette.
- Active work order: Docs/AssetWorkOrders/LuminousRift/01_CrystalExportBatch.md.

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

## Background Depth Targets

### SM_Rift_CavernWall_Large_A

- Status: needed.
- Intended use: large background/side cavern shell modules for First Overlook, Abyssal Approach, Ancient Gate, and Second Sky Overlook.
- Approximate dimensions: 40-100 m wide x 80-220 m tall x 8-30 m apparent depth.
- Pivot/origin: bottom center or lower rear corner; document exact choice when created.
- Collision: none for background placements; use Unreal blocking volumes if reused near the route.
- Material slots: `mat_wet_basalt`, optional `mat_crystal_blue`, optional `mat_blue_emissive`.
- Nanite/LOD: Nanite recommended.

### SM_Rift_TowerSegment_A/B/C

- Status: needed.
- Intended use: distant ancient machine silhouettes and vertical depth markers behind bridges, collectors, and gate wall.
- Approximate dimensions: 12-30 m wide x 40-120 m tall.
- Pivot/origin: bottom center.
- Collision: none for distant placements; simple blocking volume only if player-adjacent.
- Material slots: `mat_ancient_machine_dark`, `mat_ancient_machine_edge_wear`, `mat_blue_emissive`, optional `mat_wet_basalt`.
- Nanite/LOD: Nanite recommended.
- Variant intent: A = narrow eroded tower, B = wider stacked/stepped tower, C = broken-topped silhouette.

### SM_Rift_HangingSlab_A/B/C

- Status: needed.
- Intended use: dark top/side vista frames and suspended abyss silhouettes.
- Approximate dimensions: 8-40 m wide x 20-100 m long/deep x 6-30 m thick.
- Pivot/origin: ceiling/anchor side if meant to hang, otherwise center; document exact choice when created.
- Collision: none for background placements.
- Material slots: `mat_wet_basalt`, optional `mat_ancient_machine_dark`, optional `mat_blue_emissive`.
- Nanite/LOD: Nanite recommended.
- Variant intent: A = broad framing slab, B = long blade-like slab, C = chunkier broken slab with fused machine fragments.

### SM_Rift_DistantSpire_A/B

- Status: needed.
- Intended use: lower-abyss geology/machine silhouettes fading into blue fog.
- Approximate dimensions: 10-40 m wide x 60-200 m tall.
- Pivot/origin: base center.
- Collision: none.
- Material slots: `mat_wet_basalt`, optional `mat_ancient_machine_dark`, optional `mat_blue_emissive`.
- Nanite/LOD: Nanite recommended for hero-distance pieces; simple LODs acceptable for very distant copies.

## Human Survey Kit Targets

Use Docs/AssetPrompts/LuminousRift/08_HumanSurveyKit.md for this first human-scale prop pass.

### SM_Human_SurveyCrate_A

- Status: needed.
- Intended use: recent field-expedition crate for Descent Elevator, First Overlook, and temporary camp dressing.
- Approximate dimensions: 0.8-1.2 m wide x 0.5-0.9 m tall.
- Pivot/origin: base center at floor contact.
- Collision: simple box collision or none if decorative.
- Material slots: `mat_human_equipment`, optional `mat_blue_emissive` for tiny status LEDs.
- Nanite/LOD: standard static mesh LODs; Nanite not required.

### SM_Human_PortableLamp_A

- Status: needed.
- Intended use: small human work light for route readability, first-overlook scale, and descent elevator dressing.
- Approximate dimensions: 0.6-1.4 m tall.
- Pivot/origin: base center at floor contact.
- Collision: simple convex or none if tucked out of player path.
- Material slots: `mat_human_equipment`, `mat_blue_emissive`.
- Nanite/LOD: standard static mesh LODs; pair with a small Unreal light only for nearby placed instances.

### SM_Human_CableCoil_A

- Status: needed.
- Intended use: temporary survey dressing near elevator, lamps, consoles, bridge nodes, and small camps.
- Approximate dimensions: 0.8-1.5 m diameter.
- Pivot/origin: base center at floor contact; document if modeled vertical instead of flat.
- Collision: no collision or simple low convex collision.
- Material slots: `mat_human_equipment`, optional `mat_blue_emissive` for connector status light.
- Nanite/LOD: standard static mesh LODs.

### SM_Human_FieldConsole_A

- Status: needed.
- Intended use: small rugged expedition readout/terminal prop for the elevator area and optional overlook camp.
- Approximate dimensions: 1.2-2.0 m wide, waist-high.
- Pivot/origin: base center at floor contact.
- Collision: simple box collision if placed near player path.
- Material slots: `mat_human_equipment`, `mat_blue_emissive`.
- Nanite/LOD: standard static mesh LODs; keep screen/status glow small.
