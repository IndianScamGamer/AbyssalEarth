# Claude/Blender Prompt - Ancient Gate Wall

You are working on Abyssal Earth, an Unreal Engine 5 first-person exploration game. Create the monumental Ancient Gate wall mesh for the Luminous Rift route.

Read before modeling:

- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/LUMINOUS_RIFT_BLOCKOUT.md
- Docs/MATERIAL_SPECS.md

Use Content/ArtDirection/References/luminous_rift_core_reference.png as the source of truth. This asset should recreate the right-side vertical gate/wall: dark carved ancient machinery with circular blue-lit mechanisms, vertical grooves, basalt intrusion, and embedded crystals.

## Assets To Create

- SM_Rift_AncientWall_Gate_A

Optional if modular decomposition is faster or cleaner:

- SM_Rift_AncientWall_Gate_DetailRing_A
- SM_Rift_AncientWall_Panel_A
- SM_Rift_AncientWall_Panel_B

## Scale Targets

- Main gate module: 40-60 m wide, 80-140 m tall, 8-20 m deep.
- Circular ring detail: 10-18 m diameter.
- Vertical blue strip details: 0.3-1.0 m wide, 8-30 m tall.

## Visual Requirements

- Main silhouette must be vertical, imposing, and readable from the First Overlook across the abyss.
- Add one or two large circular sockets with blue emissive centers at player-visible heights.
- Use nested rings, radial grooves, vertical channeling, panel seams, worn bevels, and cracked stone-metal surfaces.
- Embed basalt intrusions and blue crystal clusters at the base and broken edges so the wall feels excavated from the cave.
- Include broken panels, missing corners, age cracks, dust/mineral deposits, and uneven silhouette.
- Avoid clean spaceship walls, modern doors, polished steel, or a flat rectangular slab.

## Material Slots

Use these exact material slot names:

- mat_ancient_machine_dark
- mat_ancient_machine_edge_wear
- mat_blue_emissive
- mat_crystal_blue
- mat_wet_basalt

## Pivot, Collision, And Export

- Pivot/origin: bottom center for placement against floor/ledge.
- Collision: recommend a blocking volume in Unreal; mesh collision can be decorative or simple.
- Nanite recommended.
- Apply transforms and keep Unreal-compatible metric scale.
- Save .blend source under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX or GLB under Content/ArtSourceExports/LuminousRift/.

## Acceptance Checklist

- From the first overlook, it reads as a giant ancient mechanism on the right side of the vista.
- Blue circular cores are visible focal points but remain secondary to the central orb.
- The wall is visibly fused with cave rock and crystal growth.
- The asset supports Zone 6 traversal framing from Docs/LUMINOUS_RIFT_BLOCKOUT.md.
- ArtSource/Blender/LuminousRift/ASSET_NOTES.md is updated with dimensions, pivot, collision, material slots, Nanite/LOD recommendation, and known issues.

