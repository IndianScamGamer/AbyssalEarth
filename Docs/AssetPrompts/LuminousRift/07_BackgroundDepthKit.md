# Claude/Blender Prompt - Background Depth Kit

You are working on Abyssal Earth, an Unreal Engine 5 first-person exploration game. Create the distant tower, hanging slab, cavern wall, and lower spire kit that makes the Luminous Rift feel like a vast vertical abyss instead of a flat arena.

Read before modeling:

- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/LUMINOUS_RIFT_BLOCKOUT.md
- Docs/MATERIAL_SPECS.md
- Content/Design/LuminousRiftAssetManifest.csv

Use Content/ArtDirection/References/luminous_rift_core_reference.png as the source of truth. These assets should support the background and silhouette language of the reference: distant ancient towers, black hanging rock slabs, vertical cavern walls, and spires fading into blue fog below the playable path.

## Assets To Create

- SM_Rift_CavernWall_Large_A
- SM_Rift_TowerSegment_A
- SM_Rift_TowerSegment_B
- SM_Rift_TowerSegment_C
- SM_Rift_HangingSlab_A
- SM_Rift_HangingSlab_B
- SM_Rift_HangingSlab_C
- SM_Rift_DistantSpire_A
- SM_Rift_DistantSpire_B

Optional if time allows:

- SM_Rift_CavernWall_Large_B
- SM_Rift_TowerSegment_C_Broken, if a separate broken version is useful after the C silhouette exists.
- SM_Rift_HangingSlab_C_Broken, if a separate broken version is useful after the C silhouette exists.

## Scale Targets

SM_Rift_CavernWall_Large_A:

- 40-100 m wide.
- 80-220 m tall.
- 8-30 m apparent depth, with strong relief and ledge silhouettes.

SM_Rift_TowerSegment_A/B:

- 12-30 m wide.
- 40-120 m tall.
- Should stack or overlap visually with other machine pieces.

SM_Rift_HangingSlab_A/B:

- 8-40 m wide.
- 20-100 m long/deep.
- 6-30 m thick, irregular and broken.

SM_Rift_DistantSpire_A/B:

- 10-40 m wide.
- 60-200 m tall.
- Designed mainly as lower-abyss silhouettes, not player-contact meshes.

## Visual Requirements

- Prioritize big readable silhouettes over small detail. These assets must read from the First Overlook and Second Sky Overlook.
- Cavern wall pieces need vertical basalt striations, wet dark planes, carved recesses, and broken ledges.
- Tower segments should feel like ancient stone-metal machinery buried in rock: vertical grooves, inset panels, circular sockets, occasional blue strips, and eroded/broken tops.
- Hanging slabs should frame the top and sides of vistas with jagged black negative space. Some should include machine panel fragments fused into basalt.
- Distant spires should be tall, narrow, and partly ambiguous between geology and machinery.
- Add sparse blue emissive seams or crystal pockets only where they help depth readability. Do not make background pieces compete with the central orb, hex collectors, or foreground crystals.
- Keep all assets asymmetrical, aged, cracked, and partly swallowed by geology.

## Material Slots

Use only the relevant exact material slot names from this list:

- mat_wet_basalt
- mat_ancient_machine_dark
- mat_ancient_machine_edge_wear
- mat_blue_emissive
- mat_crystal_blue

Recommended slot usage:

- Cavern walls and hanging slabs: mat_wet_basalt, optional mat_crystal_blue, optional mat_blue_emissive.
- Tower segments: mat_ancient_machine_dark, mat_ancient_machine_edge_wear, mat_blue_emissive, optional mat_wet_basalt.
- Distant spires: mat_wet_basalt, optional mat_ancient_machine_dark, optional mat_blue_emissive.

## Pivot, Collision, And Export

- Cavern wall pivot: bottom center or lower rear corner; document the choice.
- Tower pivot: bottom center so it can sit on platforms, ledges, or distant floor planes.
- Hanging slab pivot: top/anchor side if it hangs from a ceiling, otherwise center; document the choice.
- Distant spire pivot: base center.
- Collision: none for distant/background-only instances. If a piece is reused near the route, use separate simple blocking volumes in Unreal.
- Nanite recommended for rock and machine geometry.
- Apply transforms and keep Unreal-compatible metric scale.
- Save .blend source files under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX or GLB under Content/ArtSourceExports/LuminousRift/.

## Placement Intent

- First Overlook: use hanging slabs and far spires to frame the orb and deepen the lower drop.
- Abyssal Approach: use tower segments and cavern walls behind bridge spans so the path feels suspended above a huge system.
- Collector Array: use distant spires below and behind hex collector clusters so the gold beam network floats over depth.
- Ancient Gate: use tower segments and cavern wall modules to extend the gate wall beyond the player path.
- Second Sky Overlook: use spires, slabs, and wall silhouettes to show an even deeper cavern continuing beyond the first map.

## Acceptance Checklist

- A wide screenshot with these pieces placed no longer reads as a flat backdrop or empty fog volume.
- The lower center of the scene reads as a deep vertical abyss with silhouettes fading into blue atmosphere.
- Distant machine towers feel ancient and eroded, not clean sci-fi skyscrapers.
- Hanging slabs create strong dark framing shapes without blocking the central orb.
- Blue accents are sparse and subordinate to the orb, crystals, and gate cores.
- Material slots are stable and named exactly as listed.
- ArtSource/Blender/LuminousRift/ASSET_NOTES.md is updated with dimensions, pivot, collision, material slots, Nanite/LOD recommendation, and known issues for every exported asset.
