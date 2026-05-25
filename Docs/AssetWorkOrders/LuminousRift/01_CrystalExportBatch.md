# Luminous Rift Work Order - Blue Crystal Export Batch

## Purpose

This is the first Blender/Claude production batch for Luminous Rift. The goal is to turn `Docs/AssetPrompts/LuminousRift/01_BlueCrystalClusters.md` into export-ready meshes that can be imported immediately into Unreal and placed along the first playable route.

Use this work order when the prompt is too broad and the asset worker needs a concrete sequence, acceptance bar, and handoff checklist.

## Required Inputs

Read these before starting:

- `Docs/CORE_REFERENCE_LUMINOUS_RIFT.md`
- `Docs/ART_DIRECTION.md`
- `Docs/BLENDER_ASSET_PIPELINE.md`
- `Docs/MATERIAL_SPECS.md`
- `Docs/AssetPrompts/LuminousRift/01_BlueCrystalClusters.md`
- `Content/Design/LuminousRiftAssetManifest.csv`
- `Content/Design/LuminousRiftAssetImportChecklist.csv`
- `ArtSource/Blender/LuminousRift/ASSET_NOTES.md`

Source reference:

- `Content/ArtDirection/References/luminous_rift_core_reference.png`

## Batch Assets

Produce these nine meshes as one coherent kit:

- `SM_Rift_CrystalCluster_S_A`
- `SM_Rift_CrystalCluster_S_B`
- `SM_Rift_CrystalCluster_S_C`
- `SM_Rift_CrystalCluster_M_A`
- `SM_Rift_CrystalCluster_M_B`
- `SM_Rift_CrystalCluster_M_C`
- `SM_Rift_CrystalCluster_L_A`
- `SM_Rift_CrystalCluster_L_B`
- `SM_Rift_CrystalCluster_Hero_A`

## Build Order

1. Create the shared crystal language first: dark-blue faceted body, selected cyan emissive cuts, black basalt base, chipped tips, and small satellite shards.
2. Build the small A/B/C set first because they establish repeatable route-breadcrumb forms.
3. Scale and elaborate the medium A/B/C set from the same language, but change silhouettes enough that they do not read as scaled duplicates.
4. Build `L_A` and `L_B` as focal pieces for Crystal Galleries and First Overlook. Keep their glow below the central orb's dominance.
5. Build `Hero_A` last as a background/landmark crystal, with enough profile complexity to read from overlook distances.

## Variant Intent

- A variants: clean, readable, repeatable route markers.
- B variants: broken or asymmetric shapes for wall seams, ledge edges, and damaged machine intersections.
- C variants: lower, denser scatter shapes for breadcrumbs and set dressing.
- `Hero_A`: a tall landmark cluster, not a walkable obstacle and not brighter than the orb.

## Required Material Slots

Use these exact slot names on every mesh:

- `mat_crystal_blue`
- `mat_blue_emissive`
- `mat_wet_basalt`

Assign `mat_blue_emissive` only to internal veins, selected facets, core cuts, or shard tips. The full mesh should not glow uniformly.

## Pivot And Collision

- Pivot: base center at the floor-contact point unless the asset is explicitly wall-anchored.
- Document any wall-anchor pivot exception in `ASSET_NOTES.md`.
- Small clusters: no collision by default.
- Medium clusters: simple convex collision only if player-adjacent.
- Large and hero clusters: simple blocking only when reachable; otherwise no collision and use level blocking volumes if needed.

## Export Targets

Export to:

- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_S_A.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_S_B.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_S_C.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_M_A.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_M_B.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_M_C.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_L_A.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_L_B.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_CrystalCluster_Hero_A.fbx`

Apply transforms before export and keep Blender units metric / Unreal-compatible centimeters.

## Handoff Updates

After exporting:

- Replace the placeholder crystal entries in `ArtSource/Blender/LuminousRift/ASSET_NOTES.md` with actual dimensions, source `.blend` path, export path, pivot notes, collision recommendation, material slots, Nanite/LOD recommendation, and known issues.
- Update each matching row in `Content/Design/LuminousRiftAssetImportChecklist.csv` from `PromptReady` to `Exported`.
- Leave `Content/Design/LuminousRiftAssetManifest.csv` at `PromptReady` until the whole batch is exported; then change the nine crystal rows to `Exported`.
- Run `python3 Scripts/validate_design_data.py` before committing.

## Unreal Acceptance Check

The batch is import-ready when:

- Each asset imports as a separate static mesh with the exact expected name.
- All three material slots exist and are ordered consistently enough for quick assignment.
- Scale matches the manifest: S 0.5-1.5 m, M 2-4 m, L 5-9 m, Hero 10-18 m.
- Silhouettes remain readable from first-person height and from the First Overlook vista.
- None of the assets look like ice props, fantasy gems, mushrooms, or generic spikes.
- Small and medium clusters can be repeated every 20-35 m without obvious tiling.
