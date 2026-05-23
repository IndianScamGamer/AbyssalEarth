# Claude/Blender Prompt - Central Orb Apparatus

You are working on Abyssal Earth, an Unreal Engine 5 first-person exploration game. Create the static mesh pieces for the Luminous Rift central orb apparatus.

Read before modeling:

- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/MATERIAL_SPECS.md

Use Content/ArtDirection/References/luminous_rift_core_reference.png as the source of truth. The central blue-white orb is the dominant focal point. Blender should provide the heavy ancient frame, radial hub, beam endpoint devices, and a proxy sphere; Unreal can later replace the orb proxy with a Blueprint combining material animation, lights, Niagara, and spline beams.

## Assets To Create

- SM_Rift_OrbFrame_A
- SM_Rift_OrbHub_A
- SM_Rift_BeamEmitterNode_A
- SM_Rift_EnergyOrb_Proxy

## Scale Targets

- Orb proxy diameter: 18-28 m.
- Hub/ring apparatus: 30-50 m diameter.
- Full collector apparatus context: should visually support an 80-140 m wide array.
- Beam emitter node: 2-5 m diameter.

## Visual Requirements

- Orb frame should be a heavy partial ring or broken radial support, not a perfect clean cage.
- Hub should include radial mechanical details, sockets, carved dark panels, and visible beam anchor points.
- Beam emitter nodes should be circular gold-lit devices that can sit on platforms, rings, or panel cluster centers.
- Include asymmetrical damage, missing pieces, offsets, and rock/mineral intrusion so the apparatus feels ancient.
- Leave obvious attachment markers, sockets, empties, or named small mesh features where gold beam splines should connect in Unreal.
- Orb proxy can be a UV sphere or layered sphere mesh with clean UVs for animated material testing.

## Material Slots

Use these exact material slot names:

- mat_ancient_machine_dark
- mat_gold_emissive
- mat_blue_emissive
- mat_orb_energy

## Pivot, Collision, And Export

- SM_Rift_OrbFrame_A, SM_Rift_OrbHub_A, and SM_Rift_EnergyOrb_Proxy origin: orb center.
- SM_Rift_BeamEmitterNode_A origin: beam connection point.
- Collision: none for first pass; the apparatus is a landmark and scan target, not a walkable object.
- Nanite recommended for frame/hub; orb proxy and beam/VFX pieces can be non-Nanite.
- Apply transforms and keep Unreal-compatible metric scale.
- Save .blend source under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX or GLB under Content/ArtSourceExports/LuminousRift/.

## Acceptance Checklist

- In a wide shot, this kit immediately reads as the central focal machine around the energy orb.
- Beam endpoints are easy for an Unreal worker to identify and connect.
- The frame feels ancient, heavy, and damaged rather than delicate or sterile.
- Orb proxy remains detailed enough for material tests and does not imply a flat white disc.
- ArtSource/Blender/LuminousRift/ASSET_NOTES.md is updated with dimensions, pivot, collision, material slots, Nanite/LOD recommendation, and known issues.

