# Claude/Blender Prompt - Ancient Bridge Span Kit

You are working on Abyssal Earth, an Unreal Engine 5 first-person exploration game. Create the first ancient bridge kit for the Luminous Rift route.

Read before modeling:

- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/LUMINOUS_RIFT_BLOCKOUT.md
- Docs/MATERIAL_SPECS.md

Use Content/ArtDirection/References/luminous_rift_core_reference.png as the source of truth. These bridges should look like ancient carved stone-metal slabs fused into basalt, not clean sci-fi catwalks or modern metal bridges.

## Assets To Create

- SM_Rift_BridgeSpan_A
- SM_Rift_BridgeSpan_B_Broken

Optional if time allows:

- SM_Rift_PlatformNode_A
- SM_Rift_PlatformEdge_A

## Scale Targets

- Bridge width: 6-10 m.
- Useful bridge lengths: 12 m, 24 m, and 48 m modules. If creating only one SM_Rift_BridgeSpan_A, make it 24-48 m long and easy to duplicate.
- Broken bridge variant: 12-32 m long with missing chunks and one clearly fractured end.
- Platform node: 14-24 m diameter or irregular equivalent.

## Visual Requirements

- Use heavy layered slab construction with visible underside depth.
- Add carved panel seams, radial grooves, circular insets, worn bevels, and limited blue emissive strips.
- Include dark basalt intrusion patches or broken rock fusing into the machine slab.
- Broken variant must have missing chunks, cracked underside, exposed layered structure, and a strong silhouette from below.
- Avoid thin railings, polished steel, clean hallway geometry, or spaceship-floor styling.
- Keep the walkable path readable for first-person traversal.

## Material Slots

Use these exact material slot names:

- mat_ancient_machine_dark
- mat_ancient_machine_edge_wear
- mat_blue_emissive
- mat_wet_basalt

## Pivot, Collision, And Export

- Preferred bridge pivot: centerline at top walkable surface with origin at start edge for modular snapping. If another pivot is chosen, document why.
- Apply transforms and keep Unreal-compatible metric scale.
- Collision: simple box or convex top collision only. Decorative underside can be no collision.
- Nanite recommended for decorative mesh; collision should remain simple.
- Save .blend source under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX or GLB under Content/ArtSourceExports/LuminousRift/.

## Acceptance Checklist

- From a distance, the bridges read as massive ancient slabs crossing the abyss.
- From first-person view, there are readable seams, bevels, cracks, and restrained blue machine lights.
- Broken bridge has a clear traversal/readability purpose and does not look accidentally clipped.
- Material slots are stable and named exactly as listed.
- ArtSource/Blender/LuminousRift/ASSET_NOTES.md is updated with dimensions, pivot, collision, material slots, Nanite/LOD recommendation, and known issues.

