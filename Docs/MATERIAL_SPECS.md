# Material Specs

These are editor-ready targets for the first beauty pass. Start with master materials and expose simple instance parameters. The material set should match `Content/ArtDirection/References/luminous_rift_core_reference.png`.

## Material Strategy

The Luminous Rift needs a small number of strong master materials:

- Dark wet basalt for the cavern shell and foreground silhouettes.
- Ancient stone-metal for buried machine architecture.
- Blue crystal for route accents and local light.
- Blue-white energy for the central orb and machine cores.
- Gold energy for beam lines and collector nodes.
- Frosted collector glass for hex-panel interiors.
- Human survey material for small scale props.

Avoid baking final lighting into albedo. Use emissive, Lumen, lights, Niagara, and fog to create the final mood.

## M_Rift_WetBasalt_Master

Purpose: cavern walls, ledges, arches, overhangs, crystal bases, and dark foreground silhouettes.

Visual target:

- Near-black charcoal/blue-gray base.
- Wet edge highlights, especially on ledges close to lights.
- Layered vertical striations and cracked planes.
- Subtle brown/green mineral variation only in roughness/base noise.

Parameters:

- `RockTint`
- `Wetness`
- `CrackContrast`
- `MacroScale`
- `StriationScale`
- `EdgeHighlightStrength`

Implementation notes:

- Use world-aligned texture projection to reduce UV seam pressure.
- Layer macro normal + detail normal.
- Vertex paint can drive wetness and mineral variation.
- Keep base color dark enough to frame emissive assets.

## M_Rift_AncientMachine_Master

Purpose: gate wall, bridge spans, platform nodes, tower segments, orb frame, circular sockets, and machine panels.

Visual target:

- Dark graphite/stone-metal hybrid.
- Worn bevels with subtle bronze/gold edge exposure.
- Recessed grooves and circular insets.
- Cracks, dust, mineral deposits, and slight wetness.

Parameters:

- `MachineTint`
- `EdgeWearTint`
- `EdgeWearStrength`
- `GrooveDarkness`
- `DustAmount`
- `Wetness`
- `PanelNoiseScale`

Implementation notes:

- Should work on modular architecture with trim-sheet style UVs if available.
- Add detail normals for carved grooves and worn bevels.
- Keep roughness varied: broad matte surfaces, slightly glossier worn edges.
- Blue/gold emissive strips should be separate material slots where possible.

## M_Rift_BlueCrystal_Master

Purpose: all blue crystal clusters and crystal veins.

Visual target:

- Deep blue body.
- Cyan internal glow.
- White/cyan edge rim.
- Faceted normals, not smooth glass.
- Some opacity/translucency feel, but opaque is acceptable for first pass stability.

Parameters:

- `CrystalTint`
- `CoreGlowStrength`
- `RimGlowStrength`
- `InternalNoiseScale`
- `PulseSpeed`
- `PulseContrast`
- `OpacityHint`

Implementation notes:

- Use Fresnel rim for edge glow.
- Add emissive noise concentrated toward the center/veins.
- Create dim/medium/bright material instances so not every cluster competes with the orb.
- For performance, nearby hero crystals can have actual point lights; distant clusters should be emissive-only.

## M_Rift_EnergyOrb_Master

Purpose: central blue-white energy sphere.

Visual target:

- White-hot core with cyan/blue body.
- Turbulent internal energy pattern.
- Strong but controlled bloom.
- Slow majestic pulse, not rapid flicker.
- Orb remains detailed; it must not become a flat white disc.

Parameters:

- `CoreColor`
- `OuterColor`
- `CoreGlowStrength`
- `ShellGlowStrength`
- `NoiseScaleA`
- `NoiseScaleB`
- `PulseSpeed`
- `FresnelStrength`
- `DistortionStrength`

Implementation notes:

- Use layered sphere meshes or a material with animated noise/panning coordinates.
- Consider a Blueprint actor that combines mesh, point lights, Niagara motes, and gold beam anchors.
- Keep exposure volumes tuned so detail remains visible.

## M_Rift_GoldEnergy_Master

Purpose: gold beam splines, beam emitter nodes, collector center nodes, and thin warm highlights.

Visual target:

- Warm gold/amber.
- Thin and precise beam lines.
- Slight haze in fog.
- No lava-red shift.

Parameters:

- `GoldColor`
- `BeamIntensity`
- `CoreWidth`
- `EdgeSoftness`
- `PulseSpeed`
- `EndpointGlowStrength`

Implementation notes:

- Use spline meshes or Niagara beams for beam paths.
- Endpoints should have small warm point lights.
- Beam intensity should support cinematic readability without washing the scene.

## M_Rift_CollectorGlass_Master

Purpose: translucent/frosted inner panes of the hex collector panels.

Visual target:

- Pale blue-white frosted pane.
- Subtle inner linework or cellular texture.
- Thin warm gold frame handled by separate material slot.
- Some panes broken/dark for variation.

Parameters:

- `PaneTint`
- `PaneOpacity`
- `InnerGlowStrength`
- `PatternContrast`
- `FrostNoiseScale`
- `DamageDarkening`

Implementation notes:

- Use translucent if acceptable; otherwise masked/opaque with emissive for first pass.
- Make a dark/damaged material instance for broken panels.
- Keep panes readable from a distance.

## M_Rift_BlueMachineLight_Master

Purpose: blue circular cores, recessed strips, gate sockets, tower lights, and platform insets.

Visual target:

- Saturated cyan-blue.
- Cleaner than crystal glow but still ancient and slightly uneven.
- Used sparingly to guide the eye.

Parameters:

- `LightColor`
- `GlowStrength`
- `PulseSpeed`
- `PulseAmount`
- `GrimeMaskStrength`

Implementation notes:

- Use on separate emissive slots inside machine meshes.
- Pair important cores with point lights.
- Do not let every panel glow; reserve glow for focal hierarchy.

## M_Rift_HumanSurvey_Master

Purpose: crates, lamps, cables, temporary railings, consoles, and beacon body materials.

Visual target:

- Practical, recent human gear.
- Dark gray/off-white materials.
- Small cyan status LEDs.
- Slight dust/wear from field use.

Parameters:

- `BodyTint`
- `Roughness`
- `DustAmount`
- `StatusLightColor`
- `StatusLightStrength`

Implementation notes:

- Human props must stay visually small and subdued.
- Use these assets for scale, not spectacle.

## Legacy Material Mapping

Earlier docs named materials around marsh/fungus/vents. For the concept-art-driven first map, map them as follows:

- `M_WetBasalt_Master` -> `M_Rift_WetBasalt_Master`
- `M_LuminousCrystal_Master` -> `M_Rift_BlueCrystal_Master`
- `M_ShallowMirrorWater_Master` -> defer; not required for the core reference map.
- `M_BioFungus_Master` -> defer to later biome.
- `M_EmberVent_Master` -> defer to later biome or side hazard pocket.
- `M_Beacon_Master` -> `M_Rift_HumanSurvey_Master` plus beacon-specific material instance.

## First Material Instances

Create these instances for the first beauty pass:

- `MI_Rift_Basalt_DarkWet`
- `MI_Rift_Basalt_DrySilhouette`
- `MI_Rift_Machine_DarkGraphite`
- `MI_Rift_Machine_WornBronzeEdge`
- `MI_Rift_Crystal_Dim`
- `MI_Rift_Crystal_RouteGlow`
- `MI_Rift_Crystal_HeroGlow`
- `MI_Rift_EnergyOrb_Primary`
- `MI_Rift_GoldBeam_Primary`
- `MI_Rift_CollectorGlass_Lit`
- `MI_Rift_CollectorGlass_DamagedDark`
- `MI_Rift_BlueMachineCore`
- `MI_Rift_HumanSurvey_DarkGray`

## Lighting Pairing

Materials should be authored with the intended light behavior:

- Orb material pairs with cool point/rect lights and Niagara motes.
- Gold beam material pairs with small endpoint point lights and volumetric fog.
- Crystal material pairs with local cyan point lights only for near/hero clusters.
- Ancient machine material should remain mostly dark unless hit by orb/gold/crystal light.
- Human survey material should be readable under weak local lamps, not under full scene brightness.
