# Blender Asset Pipeline For Claude MCP

## Purpose

This document is written for long-form agentic asset creation with Claude Code + Blender MCP. A Claude/Blender worker should be able to read this file plus `CORE_REFERENCE_LUMINOUS_RIFT.md` and produce useful Unreal-ready assets without needing constant clarification.

The immediate goal is not final shipped art. The goal is a coherent first art kit that makes `MAP_LuminousRift_Blockout` look like the core concept reference as quickly as possible.

## Required Inputs For Every Asset Worker

Before creating assets, read:

1. `Docs/CORE_REFERENCE_LUMINOUS_RIFT.md`
2. `Docs/ART_DIRECTION.md`
3. `Docs/MATERIAL_SPECS.md`
4. The specific asset brief in this file

Use the reference image at:

`Content/ArtDirection/References/luminous_rift_core_reference.png`

## Output Conventions

### Blender Files

Save source files under:

`ArtSource/Blender/LuminousRift/`

Naming:

- One source file per asset family.
- Use lowercase folders and Unreal-style object names.
- Example: `ArtSource/Blender/LuminousRift/SM_Rift_HexCollector_Cluster_A.blend`

### Unreal Export Files

Export static meshes to:

`Content/ArtSourceExports/LuminousRift/`

Naming:

- Static meshes: `SM_Rift_...`
- Materials placeholders: `M_Rift_...`
- Textures if generated: `T_Rift_...`

Preferred interchange:

- `.fbx` for static meshes unless the Unreal import path prefers `.glb`.
- Apply transforms before export.
- Use centimeters scale compatible with Unreal.
- Mesh origin should be intentional and documented in the asset notes.

### Asset Notes

For each created asset, add or update a short notes file:

`ArtSource/Blender/LuminousRift/ASSET_NOTES.md`

Each entry should include:

- Asset name.
- Intended use.
- Approximate dimensions in meters.
- Pivot/origin location.
- Collision recommendation.
- Material slots.
- LOD/Nanite recommendation.
- Any known issues.

### Import Checklist

After export, use the editor handoff checklist at:

`Content/Design/LuminousRiftAssetImportChecklist.csv`

For each exported mesh, update the matching row from `PromptReady` to `Exported`, then to `Imported` or `Placed` after Windows/Unreal verification. The checklist captures the expected export path, source prompt, material slots, pivot check, collision check, Nanite/LOD choice, placement zone, and first-pass acceptance test. Keep this file in sync with `Content/Design/LuminousRiftAssetManifest.csv` whenever asset names or prompt ownership change.

### Work Orders

Asset prompts define the target asset family. Work orders define the production batch sequence and export handoff for a specific session.

Current work orders:

- `Docs/AssetWorkOrders/LuminousRift/01_CrystalExportBatch.md` - first export batch for all blue crystal cluster variants.
- `Docs/AssetWorkOrders/LuminousRift/02_ForegroundRevealKit.md` - second export batch for the first-overlook ledge, rock arches, and overhang variants.

When a manifest row references a work order in its notes, keep that path valid and update the matching import-checklist row after export. Run `python3 Scripts/validate_design_data.py` before committing manifest, checklist, or work-order path changes.

## Scale And Units

Unreal units are centimeters. Blender should use metric units.

Default scale assumptions:

- Player height: 1.8 m.
- Player path width: 3-8 m.
- Small prop: 0.2-1.5 m.
- Crystal cluster small: 0.5-1.5 m tall.
- Crystal cluster medium: 2-4 m tall.
- Crystal cluster large: 5-9 m tall.
- Hero crystal: 10-18 m tall.
- Bridge span: 8-16 m wide, 20-80 m long.
- Gate/wall module: 20-50 m wide, 40-120 m tall.
- Central orb apparatus: 80-140 m wide.

If unsure, make assets large and modular. The reference depends on scale.

## Geometry Standards

### Static Mesh Readiness

- Apply transforms.
- Set clean origins.
- Remove hidden duplicate geometry.
- Keep normals consistent.
- Bevel important hard edges.
- Avoid razor-thin planes unless they are intended as VFX cards.
- Separate material slots by readable material families, not by every tiny detail.

### Nanite

Most rock and ancient machine meshes should be Nanite candidates.

Good Nanite candidates:

- Basalt cliffs.
- Eroded ledges.
- Gate walls.
- Tower segments.
- Bridge slabs.
- Collector frames.

Use lower-poly/non-Nanite for:

- Transparent collector panes.
- Beam meshes.
- VFX cards.
- Small interactive props that may need simple collision.

### Collision

For first pass, prefer simple collision:

- Player-walkable ledges and bridge spans: UCX boxes or simple convex hulls.
- Decorative cliffs: no collision unless close to the route.
- Crystals near the route: simple convex collision or no collision if tucked out of the path.
- Huge gate/wall: blocking volume in Unreal rather than complex per-poly collision.

## Material Slot Standards

Use stable slot names so Unreal material assignment is predictable.

Common slots:

- `mat_wet_basalt`
- `mat_ancient_machine_dark`
- `mat_ancient_machine_edge_wear`
- `mat_blue_emissive`
- `mat_gold_emissive`
- `mat_collector_glass`
- `mat_crystal_blue`
- `mat_human_equipment`

Do not bake final lighting into base color. Use emissive materials and Unreal lighting/VFX.

## Asset Family Briefs

## P0 - Foreground Reveal Ledge

Asset names:

- `SM_Rift_ForegroundLedge_A`
- `SM_Rift_ForegroundLedge_B_Broken`

Purpose:

The first ledge where the player sees the core vista. It must match the lower-left concept composition: dark, jagged, layered rock with embedded blue crystal pockets and enough flat playable surface for the player.

Dimensions:

- Playable top: 8-12 m wide, 10-18 m long.
- Full visual shelf: 25-40 m wide including overhangs.
- Thickness/drop silhouette: 5-12 m.

Modeling notes:

- Top surface should have an uneven but walkable central path.
- Outer edges should be jagged and non-rectangular.
- Add one or two hollow cavities with blue crystal clusters inside.
- Include layered striations that flow toward the abyss.
- Do not make it a flat rectangular platform.

Pivot:

- Center of walkable top surface at floor level.

Material slots:

- `mat_wet_basalt`
- `mat_crystal_blue`
- `mat_blue_emissive`

Unreal use:

- Place at the first overlook and final overlook.
- Nanite on.
- Add simple walkable collision over central path.

Acceptance:

- In silhouette, it reads as a natural dark rock shelf.
- From first-person height, it frames a dramatic drop.
- Blue crystals are visible but not so bright that they compete with the central orb.

## P0 - Bridge And Platform Kit

Asset names:

- `SM_Rift_BridgeSpan_A`
- `SM_Rift_BridgeSpan_B_Broken`
- `SM_Rift_PlatformNode_A`
- `SM_Rift_PlatformEdge_A`

Purpose:

Creates the traversal route across the abyss toward the Collector Array. Bridges should resemble ancient carved slabs fused with machine panels, not modern steel catwalks.

Dimensions:

- Bridge width: 6-10 m.
- Bridge module lengths: 12 m, 24 m, 48 m.
- Platform node: 14-24 m diameter or irregular equivalent.

Modeling notes:

- Use layered slab construction with visible underside depth.
- Add circular insets and recessed blue strips in moderation.
- Break some edges and expose missing chunks.
- Add grooves that align with the central orb direction.
- Include optional side lip/low curb, but no modern guardrail unless human kit is placed separately.

Pivot:

- Centerline at top walkable surface, origin at start edge for bridge spans if modular snapping is useful.

Material slots:

- `mat_ancient_machine_dark`
- `mat_ancient_machine_edge_wear`
- `mat_blue_emissive`
- `mat_wet_basalt` for fused rock patches.

Collision:

- Simple box/convex top collision; decorative underside can be no collision.

Acceptance:

- At a distance, bridge silhouettes look heavy and ancient.
- First-person view has enough detail: seams, bevels, worn edges, embedded blue light.
- The bridge does not look like a clean sci-fi hallway.

## P0 - Ancient Gate Wall

Asset names:

- `SM_Rift_AncientWall_Gate_A`
- `SM_Rift_AncientWall_Gate_DetailRing_A`
- `SM_Rift_AncientWall_Panel_A/B`

Purpose:

Recreate the right-side monumental vertical structure in the concept image: a dark wall/gate with circular mechanical rings, blue core lights, vertical grooves, and embedded crystals at the base.

Dimensions:

- Main module: 40-60 m wide, 80-140 m tall, 8-20 m deep.
- Circular ring detail: 10-18 m diameter.
- Vertical blue strip details: 0.3-1.0 m wide, 8-30 m tall.

Modeling notes:

- Build as modular wall/panel pieces if possible.
- Main silhouette should be vertical and imposing.
- Add one or two large circular sockets with blue emissive centers.
- Add nested rings and radial grooves around sockets.
- Add side bevels and cracks so it feels excavated.
- Embed rock intrusions and crystal clusters around the base/edges.

Pivot:

- Bottom center for easy placement against floor/ledge.

Material slots:

- `mat_ancient_machine_dark`
- `mat_ancient_machine_edge_wear`
- `mat_blue_emissive`
- `mat_crystal_blue`
- `mat_wet_basalt`

Acceptance:

- From the first overlook, it reads as a giant ancient mechanism.
- Blue circular cores are visible focal points but secondary to the central orb.
- It is visibly fused with the cave, not freestanding clean architecture.

## P0 - Central Orb Apparatus

Asset names:

- `SM_Rift_OrbFrame_A`
- `SM_Rift_OrbHub_A`
- `SM_Rift_BeamEmitterNode_A`
- `VFX_Rift_EnergyOrb_Proxy` or mesh proxy `SM_Rift_EnergyOrb_Proxy`

Purpose:

The central focal landmark. This is the most important asset family in the first map.

Dimensions:

- Orb diameter: 18-28 m.
- Hub/ring apparatus: 30-50 m diameter.
- Full apparatus including collector arc: 80-140 m wide.
- Beam emitter node: 2-5 m diameter.

Modeling notes:

- The orb itself can be a UV sphere or layered sphere mesh with animated material in Unreal.
- Frame should include a partial ring or radial hub, not a full clean perfect cage.
- Beam nodes should be small circular gold-lit devices.
- Use radial symmetry sparingly; damage, missing pieces, and offsets are important.
- Leave sockets or empties/markers where gold beam splines should attach.

Pivot:

- Orb apparatus origin at orb center.
- Beam emitter nodes origin at connection point.

Material slots:

- `mat_ancient_machine_dark`
- `mat_gold_emissive`
- `mat_blue_emissive`
- `mat_orb_energy`

Unreal notes:

- The energy orb is likely best as a Blueprint actor combining mesh, emissive material, lights, Niagara particles, and beam splines.
- Blender should provide the frame/hub mesh and a proxy orb.

Acceptance:

- In any wide shot, the orb is unmistakably the main focal point.
- Beam endpoints are obvious and easy to connect in Unreal.
- The frame feels ancient and heavy, not delicate.

## P0 - Hex Collector Panels

Asset names:

- `SM_Rift_HexCollector_Tile_A`
- `SM_Rift_HexCollector_Cluster_A`
- `SM_Rift_HexCollector_Cluster_B_Broken`
- `SM_Rift_HexCollector_Frame_A`

Purpose:

Recreate the honeycomb flower-like collector panels around the orb. These are essential to matching the reference.

Dimensions:

- Single hex tile: 4-7 m across.
- Cluster: 20-35 m wide.
- Frame thickness: 0.15-0.4 m.

Modeling notes:

- Build a single hex tile with gold/brass frame and frosted inner pane.
- Arrange 7-13 tiles into flower/petal clusters.
- Vary rotations and missing/broken panes.
- Include small node at each cluster center for beam attachment.
- Inner panes should support translucent or emissive material assignment in Unreal.

Pivot:

- Cluster center at beam attachment hub.
- Single tile origin at tile center.

Material slots:

- `mat_gold_emissive`
- `mat_collector_glass`
- `mat_ancient_machine_dark`

Acceptance:

- Clusters read clearly as hexagonal collectors from 100 m away.
- Warm gold frames contrast with blue pane interiors.
- Broken variants still preserve the flower silhouette.

## P0 - Blue Crystal Clusters

Asset names:

- `SM_Rift_CrystalCluster_S_A/B/C`
- `SM_Rift_CrystalCluster_M_A/B/C`
- `SM_Rift_CrystalCluster_L_A/B`
- `SM_Rift_CrystalCluster_Hero_A`

Purpose:

Route language, lighting accents, foreground interest, and visual continuity between natural cave and ancient machine.

Dimensions:

- Small: 0.5-1.5 m.
- Medium: 2-4 m.
- Large: 5-9 m.
- Hero: 10-18 m.

Modeling notes:

- Use angular faceted prisms, not smooth gems.
- Clusters should have varied heights and rotations.
- Bases should include small rock/mineral buildup so they sit naturally on ledges.
- Make several silhouettes: vertical spear cluster, fan cluster, low broken cluster.

Pivot:

- Base center at floor contact.

Material slots:

- `mat_crystal_blue`
- `mat_blue_emissive`
- `mat_wet_basalt` for base.

Acceptance:

- Crystals look good as silhouettes even without final material.
- Emissive areas are visible but not uniformly glowing everywhere.
- Variants prevent obvious repetition.

## P1 - Distant Towers And Hanging Slabs

Asset names:

- `SM_Rift_TowerSegment_A/B/C`
- `SM_Rift_HangingSlab_A/B/C`
- `SM_Rift_DistantSpire_A/B`

Purpose:

Create the dense background layering visible in the reference. These assets sell scale more than gameplay.

Dimensions:

- Tower segment: 12-30 m wide, 40-120 m tall.
- Hanging slab: 8-40 m wide, 20-100 m long.
- Distant spire: 10-40 m wide, 60-200 m tall.

Modeling notes:

- Prioritize silhouette over close detail.
- Add vertical grooves and occasional blue emissive strips.
- Create broken bottoms and uneven tops.
- Use fog to soften repetition in Unreal.

Pivot:

- Bottom center for towers/spires.
- Top anchor point for hanging slabs if suspended from ceiling.

Acceptance:

- Background no longer feels empty.
- Objects fade well in blue fog.
- Silhouettes reinforce vertical abyss depth.

## P1 - Rock Arch And Cavern Frame Kit

Asset names:

- `SM_Rift_RockArch_A/B`
- `SM_Rift_CavernWall_Large_A/B`
- `SM_Rift_Overhang_A/B`

Purpose:

Frame the camera like the reference: dark cave edges around a luminous central view.

Dimensions:

- Rock arch: 30-80 m span.
- Cavern wall module: 40-100 m wide.
- Overhang: 20-60 m deep.

Modeling notes:

- Strong silhouette is more important than microdetail.
- Add vertical erosion lines and wet highlights.
- Include sockets where crystals can be embedded.
- Avoid smooth rounded tunnel shapes.

Pivot:

- Bottom center for wall pieces.
- Anchor side or center depending on placement needs; document it.

Acceptance:

- The first overlook can be framed top/left/right using these pieces.
- The edge shapes are irregular and natural.
- Works with Nanite and world-aligned rock material.

## P1 - Human Survey Kit

Asset names:

- `SM_Human_SurveyCrate_A`
- `SM_Human_PortableLamp_A`
- `SM_Human_CableCoil_A`
- `SM_Human_FieldConsole_A`
- `SM_Human_TemporaryRailing_A`

Purpose:

Scale cues and gameplay readability. Human kit should never dominate the shot.

Dimensions:

- Crate: 0.8-1.2 m.
- Lamp: 0.6-1.4 m.
- Console: 1.2-2.0 m wide.
- Railing segment: 2-4 m long.

Modeling notes:

- Practical, modern, slightly worn.
- Simple readable shapes.
- Small cyan status lights.
- Avoid high-tech glossy sci-fi styling.

Acceptance:

- Makes the environment feel huge.
- Looks recently placed by explorers.
- Does not look like part of the ancient machine civilization.

## Suggested Work Order For Claude Agents

1. Create `SM_Rift_CrystalCluster_S/M/L` variants first. They are fast and immediately improve the map.
2. Create `SM_Rift_ForegroundLedge_A` and `SM_Rift_RockArch_A` to establish the first vista frame.
3. Create bridge/platform kit so the map route can be dressed.
4. Create the hex collector tile and cluster system.
5. Create the central orb frame/hub and beam emitter nodes.
6. Create the right-side ancient gate wall.
7. Create distant towers/hanging slabs for depth.
8. Create small human survey kit for scale.

## Prompt Template For Claude/Blender Worker

Use this shape when assigning a single asset task:

```text
You are working on Abyssal Earth, an Unreal Engine 5 exploration game. Read:
- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/MATERIAL_SPECS.md

Create [ASSET NAME/FAMILY] in Blender for the Luminous Rift map. The asset must match Content/ArtDirection/References/luminous_rift_core_reference.png.

Requirements:
- Save the .blend under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX/GLB under Content/ArtSourceExports/LuminousRift/.
- Use metric scale and Unreal-compatible transforms.
- Apply transforms, clean normals, and assign material slots named per BLENDER_ASSET_PIPELINE.md.
- Add/update ArtSource/Blender/LuminousRift/ASSET_NOTES.md with dimensions, pivot, collision recommendation, material slots, and known issues.
- Do not create unrelated assets.
```

## Review Checklist

Before accepting an asset:

- Does it serve the core reference image?
- Does it have correct scale?
- Does the silhouette read from far away?
- Does it have material slots with stable names?
- Is the pivot useful?
- Is it exportable to Unreal without cleanup?
- Does it avoid clean generic sci-fi or generic cave styling?
- Did the worker update `ASSET_NOTES.md`?

---

## Visual Validation

Starting with PR #2 of the asset overhaul, every PR that changes an `sm_*.py` script
triggers an automated visual validation pipeline before merge is allowed:

### How it works

1. **Render harness** (`Tools/render_asset_preview.py`) patches `shared.utils` to stub
   operators, runs `build()`, extracts vertex/face data, and produces a three-view matplotlib
   wireframe PNG (front / side / 3-quarter) for every changed script.

2. **Comparison compositer** (`Tools/compare_concept.py`) reads the `Concept: IMAGE-ID` line
   in each script's docstring, finds the matching concept art PNG in
   `Content/ArtDirection/Concepts/`, and produces a side-by-side composite
   (`*_vs_concept.png`).

3. **CI uploads** both sets of PNGs as GitHub Actions artifacts attached to the PR.
   Artifact name: `concept-vs-render-<sha>`.

4. **Human review**: Before requesting merge, the PR author downloads the artifacts and
   confirms that wireframe geometry clearly matches the concept art silhouette.

5. **User approval** (Vivek): Explicit go/no-go per asset. Failed assets trigger a
   refinement round with a new commit; the CI re-runs automatically.

### Running locally

```bash
# Single script
pip install matplotlib numpy bpy Pillow
python3 Tools/render_asset_preview.py \
    --script ArtSource/Blender/Scripts/luminous_rift_machines/sm_orb_hub.py \
    --out /tmp/renders/

# All scripts changed since main
python3 Tools/render_asset_preview.py --changed-since origin/main --out /tmp/renders/

# Build comparison composites
python3 Tools/compare_concept.py \
    --renders-dir /tmp/renders/ \
    --scripts-dir ArtSource/Blender/Scripts/ \
    --concepts-dir Content/ArtDirection/Concepts/ \
    --out /tmp/comparisons/
```

### Adding a Concept: reference to a script

Every `sm_*.py` must include a `Concept:` line in its module docstring:

```python
"""
SM_Rift_OrbHub_A — AbyssalEarth procedural mesh.
Concept: AD-001, LR-006, LR-007
Run standalone:  blender --background --python <this_file>.py
"""
```

CI check 13 warns when this line is absent. The render harness uses it to auto-locate
the reference concept image for the comparison composite.

### Acceptance criteria (visual)

A script's geometry is approved when the wireframe composite shows:
- **Correct scale relationship** — the asset occupies the right proportion of the frame
  relative to the concept's implied scale (human figure comparison where applicable)
- **Correct mass distribution** — dominant shapes are in the right positions and proportions
- **Recognisable silhouette** — an observer who has seen both images can identify the
  correspondence without labels
- **No obvious anti-patterns** — no point clouds, icosphere blob chains, or flat slabs
  where three-dimensional structure should be

Visual acceptance overrides all other checks. An asset can pass all 16 CI checks and still
fail visual review; it does not ship until the geometry matches the concept art.
