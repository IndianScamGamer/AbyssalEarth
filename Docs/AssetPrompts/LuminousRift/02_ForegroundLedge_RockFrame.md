# Claude/Blender Prompt - Foreground Ledge And Rock Frame Kit

You are working on Abyssal Earth, an Unreal Engine 5 first-person exploration game. Create the foreground reveal ledge and first rock-frame pieces for the Luminous Rift map.

Read before modeling:

- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/LUMINOUS_RIFT_BLOCKOUT.md
- Docs/MATERIAL_SPECS.md

Use Content/ArtDirection/References/luminous_rift_core_reference.png as the source of truth. These assets must support the first postcard shot: the tiny player stands on a dark jagged ledge while a huge orb, gold beams, hex collectors, blue crystals, and an ancient gate fill the abyss.

## Assets To Create

- SM_Rift_ForegroundLedge_A
- SM_Rift_RockArch_A
- SM_Rift_RockArch_B
- SM_Rift_Overhang_A
- SM_Rift_Overhang_B

## Scale Targets

SM_Rift_ForegroundLedge_A:

- Playable top: 8-12 m wide, 10-18 m long.
- Full visual shelf: 25-40 m wide including overhangs and broken side mass.
- Thickness/drop silhouette: 5-12 m.

SM_Rift_RockArch_A:

- Span: 30-80 m.
- Must frame the orb from First Overlook and Crystal Galleries views.

SM_Rift_RockArch_B:

- Span: 30-80 m.
- Broken/asymmetric alternate silhouette for the Second Sky Overlook or side-frame variation.

SM_Rift_Overhang_A:

- Depth: 20-60 m.
- Must frame the top edge of the first vista without becoming a smooth tunnel.

SM_Rift_Overhang_B:

- Depth: 20-60 m.
- More jagged alternate top-frame piece for screenshot composition tuning.

## Visual Requirements

- Use near-black basalt forms with blue-gray edge highlights and vertical erosion/striation.
- The ledge must have an uneven but walkable central surface. Avoid flat rectangles.
- Outer edges should be jagged, broken, and non-symmetrical.
- Add one or two cavities or cracks containing blue crystal pockets.
- Rock arch and overhang pieces should create strong dark silhouettes around a luminous center view.
- Include sockets, cracks, or embedded crystal pockets so the assets can blend with crystal clusters.
- The ledge should visibly suggest a sheer drop into the abyss from first-person height.

## Material Slots

Use these exact material slot names:

- mat_wet_basalt
- mat_crystal_blue
- mat_blue_emissive

## Pivot, Collision, And Export

- SM_Rift_ForegroundLedge_A pivot: center of walkable top surface at floor level.
- SM_Rift_RockArch_A/B pivot: bottom center or one anchor foot, whichever is more useful; document the choice.
- SM_Rift_Overhang_A/B pivot: ceiling/anchor side or center; document the choice.
- Apply transforms and keep Unreal-compatible metric scale.
- Ledge collision: simple walkable collision over the central top surface; decorative overhangs can be no collision.
- Rock arch/overhang collision: decorative unless reachable by the player.
- Save .blend files under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX or GLB files under Content/ArtSourceExports/LuminousRift/.

## Acceptance Checklist

- The ledge reads as the lower-left human-scale reveal platform from the core reference.
- The top surface supports safe first-person traversal while the outer silhouette stays wild and natural.
- Rock frame pieces create top/side dark framing shapes for the first overlook composition.
- B variants clearly differ from A variants and can dress the second overlook without obvious repetition.
- Blue crystal pockets are visible but subordinate to the central orb.
- ArtSource/Blender/LuminousRift/ASSET_NOTES.md is updated for all exported meshes.
