# Luminous Rift Work Order - Foreground Reveal Kit

## Purpose

This is the second Blender/Claude production batch for Luminous Rift. The goal is to turn `Docs/AssetPrompts/LuminousRift/02_ForegroundLedge_RockFrame.md` into the first-overlook reveal kit: a playable jagged ledge plus dark rock-frame silhouettes that make the map immediately match the core reference.

Use this work order after or alongside the crystal export batch when the asset worker needs a concrete sequence, acceptance bar, and handoff checklist.

## Required Inputs

Read these before starting:

- `Docs/CORE_REFERENCE_LUMINOUS_RIFT.md`
- `Docs/ART_DIRECTION.md`
- `Docs/BLENDER_ASSET_PIPELINE.md`
- `Docs/LUMINOUS_RIFT_BLOCKOUT.md`
- `Docs/MATERIAL_SPECS.md`
- `Docs/AssetPrompts/LuminousRift/02_ForegroundLedge_RockFrame.md`
- `Content/Design/LuminousRiftAssetManifest.csv`
- `Content/Design/LuminousRiftAssetImportChecklist.csv`
- `ArtSource/Blender/LuminousRift/ASSET_NOTES.md`

Source reference:

- `Content/ArtDirection/References/luminous_rift_core_reference.png`

## Batch Assets

Produce these five meshes as one coherent kit:

- `SM_Rift_ForegroundLedge_A`
- `SM_Rift_RockArch_A`
- `SM_Rift_RockArch_B`
- `SM_Rift_Overhang_A`
- `SM_Rift_Overhang_B`

## Build Order

1. Block the First Overlook composition first using simple masses: player ledge low/near, central negative space for the orb, top/side frame silhouettes, and visible abyss drop.
2. Build `SM_Rift_ForegroundLedge_A` as the playable anchor. Keep the walkable center reliable while letting the side and underside silhouette stay broken and dramatic.
3. Build `SM_Rift_RockArch_A` as the primary reveal frame. It should give a strong side/top silhouette without turning the view into a smooth tunnel.
4. Build `SM_Rift_Overhang_A` as the top-frame piece for the first reveal shot. It should darken the upper edge of the composition and leave the orb/collector array unobstructed.
5. Build `SM_Rift_RockArch_B` and `SM_Rift_Overhang_B` as alternate broken/asymmetric silhouettes for the Second Sky Overlook and composition tuning.
6. Add embedded crystal sockets and small crystal pockets only after the large silhouettes work. The crystals are supporting accents; the central orb remains the dominant light source.

## Variant Intent

- `ForegroundLedge_A`: human-scale playable reveal platform with a jagged abyss-facing edge.
- `RockArch_A`: strong primary first-overlook side frame, broad enough to sell cavern scale.
- `RockArch_B`: broken/asymmetric alternate that avoids repeating the same arch outline.
- `Overhang_A`: dark top-frame slab for the first reveal.
- `Overhang_B`: more jagged top-frame alternate for screenshot composition and second-overlook use.

## Required Material Slots

Use these exact slot names where listed in the manifest/checklist:

- `SM_Rift_ForegroundLedge_A`: `mat_wet_basalt`, `mat_crystal_blue`, `mat_blue_emissive`
- `SM_Rift_RockArch_A`: `mat_wet_basalt`, `mat_crystal_blue`
- `SM_Rift_RockArch_B`: `mat_wet_basalt`, `mat_crystal_blue`
- `SM_Rift_Overhang_A`: `mat_wet_basalt`, `mat_crystal_blue`
- `SM_Rift_Overhang_B`: `mat_wet_basalt`, `mat_crystal_blue`

Use `mat_blue_emissive` on the ledge only for small crystal seams or cracks. The arch and overhang meshes should usually rely on separate placed crystal clusters or non-emissive crystal pockets so they do not compete with the orb.

## Pivot And Collision

- `SM_Rift_ForegroundLedge_A` pivot: center of the walkable top surface at floor level.
- `SM_Rift_RockArch_A/B` pivot: bottom center or a clear anchor foot. Choose the point that makes Unreal placement easiest and document it in `ASSET_NOTES.md`.
- `SM_Rift_Overhang_A/B` pivot: ceiling/anchor side if it hangs from the cavern roof, otherwise lower rear center. Document the exact choice.
- Ledge collision: simple walkable collision over the central top surface only. Decorative side mass, underside, and crystal pockets can be no collision.
- Rock arch/overhang collision: no collision by default unless a copy is intentionally reused near the player route. Use Unreal blocking volumes for player-facing boundaries.

## Export Targets

Export to:

- `Content/ArtSourceExports/LuminousRift/SM_Rift_ForegroundLedge_A.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_RockArch_A.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_RockArch_B.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_Overhang_A.fbx`
- `Content/ArtSourceExports/LuminousRift/SM_Rift_Overhang_B.fbx`

Apply transforms before export and keep Blender units metric / Unreal-compatible centimeters.

## Handoff Updates

After exporting:

- Replace the placeholder foreground-frame entries in `ArtSource/Blender/LuminousRift/ASSET_NOTES.md` with actual dimensions, source `.blend` path, export path, pivot notes, collision recommendation, material slots, Nanite/LOD recommendation, and known issues.
- Update each matching row in `Content/Design/LuminousRiftAssetImportChecklist.csv` from `PromptReady` to `Exported`.
- Leave `Content/Design/LuminousRiftAssetManifest.csv` at `PromptReady` until the whole batch is exported; then change these five rows to `Exported`.
- Run `python3 Scripts/validate_design_data.py` before committing.

## Unreal Acceptance Check

The batch is import-ready when:

- `SM_Rift_ForegroundLedge_A` is safely walkable in first person without reading as a rectangular platform.
- From the intended first-overlook camera, the ledge, arch, and overhang create a dark frame around the orb/collector vista.
- The arch and overhang variants can be offset/rotated/scaled without obvious repetition.
- The visible scale makes the player feel tiny against the cavern, not merely standing in a normal cave room.
- Blue crystal pockets remain secondary accents and do not flatten the lighting hierarchy.
- None of the meshes look like generic fantasy cave arches, smooth tunnels, or modern concrete platforms.
