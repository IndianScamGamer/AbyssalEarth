# Claude/Blender Prompt - Human Survey Kit

You are working on Abyssal Earth, an Unreal Engine 5 first-person exploration game. Create the small human expedition props that sell scale, recent arrival, and route readability in the Luminous Rift without stealing focus from the ancient cavern.

Read before modeling:

- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/LUMINOUS_RIFT_BLOCKOUT.md
- Docs/MATERIAL_SPECS.md
- Content/Design/LuminousRiftAssetManifest.csv

Use Content/ArtDirection/References/luminous_rift_core_reference.png as the source of truth for scale and mood. Human equipment should look temporary, practical, and recently placed by a field expedition. It should contrast with ancient machinery but remain visually small and subdued.

## Assets To Create

- SM_Human_SurveyCrate_A
- SM_Human_PortableLamp_A
- SM_Human_CableCoil_A
- SM_Human_FieldConsole_A

Optional if time allows:

- SM_Human_TemporaryRailing_A
- SM_Human_SurveyBeacon_Prop_A

## Scale Targets

SM_Human_SurveyCrate_A:

- 0.8-1.2 m wide.
- 0.5-0.9 m tall.
- Stackable field case silhouette with beveled reinforced edges.

SM_Human_PortableLamp_A:

- 0.6-1.4 m tall.
- Tripod, clamp, or compact standing work light.
- Light head should have a clear emissive/status-light surface for Unreal material assignment.

SM_Human_CableCoil_A:

- 0.8-1.5 m diameter.
- 0.15-0.4 m thick cable loops.
- Include loose cable tail or connector plug for readable silhouette.

SM_Human_FieldConsole_A:

- 1.2-2.0 m wide.
- Waist-high rugged scanner/readout console or fold-out expedition terminal.
- Include one or two small display/status-light surfaces, not a giant glowing screen.

## Visual Requirements

- Props must look human-made, recent, and temporary: dark gray/off-white field gear, rubberized edges, handles, clamps, cases, cable ports, and small cyan status LEDs.
- Keep forms grounded and utilitarian. Do not use clean spaceship styling, glossy luxury materials, or oversized sci-fi panels.
- The kit should be readable at first-person distance and as a tiny scale cue from vista shots.
- Add dust, scratches, and slight damage from the crash/descent environment, but avoid ancient corrosion. These are new human items, not buried artifacts.
- Make the props easy to scatter near PlayerStart, the first overlook ledge, bridge nodes, and the Second Sky Overlook.
- Keep emissive areas small. Human lights should support navigation and scale, not compete with blue crystals, the central orb, or gold beam networks.

## Material Slots

Use these exact material slot names:

- mat_human_equipment
- mat_blue_emissive

Optional, only if a prop includes dirt/rock contact buildup:

- mat_wet_basalt

Recommended slot usage:

- Crates and cable coil: mostly mat_human_equipment, optional tiny mat_blue_emissive status LEDs.
- Portable lamp: mat_human_equipment for body/tripod, mat_blue_emissive for the lamp face and status LEDs.
- Field console: mat_human_equipment for casing, mat_blue_emissive for screen/status strips.

## Pivot, Collision, And Export

- Survey crate pivot: base center at floor contact.
- Portable lamp pivot: base center at floor contact.
- Cable coil pivot: center of coil at floor contact if lying flat; document orientation if vertical.
- Field console pivot: base center at floor contact.
- Apply transforms and use metric scale compatible with Unreal centimeters.
- Collision: simple box/convex collision recommendations only. These props should be easy to block or ignore in Unreal.
- Nanite is not required for small human props; use normal static mesh LODs if needed.
- Save .blend source files under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX or GLB under Content/ArtSourceExports/LuminousRift/.

## Placement Intent

- Descent Elevator: crates, cable coils, lamp, and field console establish the human expedition before the first cavern reveal.
- First Overlook: one crate, lamp, or beacon near the player gives human scale without blocking the vista.
- Abyssal Approach: a cable coil or lamp can mark a safe bridge node.
- Collector Array: keep human gear sparse so ancient machinery dominates.
- Second Sky Overlook: a small temporary camp behind or beside the player can imply the expedition is trying to understand the deeper cavern.

## Acceptance Checklist

- In a wide shot, the props read as tiny human-scale equipment against the cavern.
- In first person, silhouettes are recognizable as crate, lamp, cable coil, and console without relying on final materials.
- Materials use the exact slot names listed above.
- Cyan emissive details are small and subordinate to crystals, machine cores, and the central orb.
- Props feel recently deployed by a field team, not ancient or alien.
- ArtSource/Blender/LuminousRift/ASSET_NOTES.md is updated with dimensions, pivot, collision, material slots, LOD recommendation, and known issues for every exported asset.
