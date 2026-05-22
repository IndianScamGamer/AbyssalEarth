# Material Specs

These are editor-ready targets for the first beauty pass. Start with master materials and expose simple instance parameters.

## M_WetBasalt_Master

Purpose: main cavern walls, ledges, arches, and foreground silhouettes.

- Base color: near-black charcoal with subtle brown/green mineral variation.
- Roughness: 0.38-0.72, vertex-painted wetter areas lower roughness.
- Normal: layered rock striation normal plus macro crack normal.
- Detail: world-aligned texture projection to reduce visible UV seams.
- Parameters:
  - `RockTint`
  - `Wetness`
  - `CrackContrast`
  - `MacroScale`

## M_LuminousCrystal_Master

Purpose: crystal veins, clusters, and major Crystal Spine structures.

- Base: translucent-looking milky quartz, but use opaque/masked first for stability.
- Emissive: cyan-blue core glow with pulsing scalar.
- Fresnel rim to catch edges.
- Parameters:
  - `CrystalTint`
  - `CoreGlowStrength`
  - `PulseSpeed`
  - `PulseContrast`
  - `InternalNoiseScale`

## M_BioFungus_Master

Purpose: glowing fungus caps, stalks, and glassy bioluminescent vegetation.

- Cap gradient: cyan underside, pale green edge, dark translucent top.
- Emissive concentrated under cap and along vein lines.
- Wind sway through World Position Offset for larger caps.
- Parameters:
  - `CapTint`
  - `UndersideGlow`
  - `VeinGlow`
  - `SwayAmount`
  - `SwaySpeed`

## M_ShallowMirrorWater_Master

Purpose: Mirror Marsh water.

- Shallow reflective plane with gentle normal ripples.
- Darker around edges with depth fade.
- Receives strong cyan/amber reflections.
- Parameters:
  - `WaterTint`
  - `RippleStrength`
  - `RippleScale`
  - `Opacity`
  - `EdgeDarkness`

## M_EmberVent_Master

Purpose: geothermal vent interiors and heated mineral deposits.

- Black crust with orange cracks.
- Emissive crack mask driven by noise.
- Heat shimmer should be VFX, not only material.
- Parameters:
  - `LavaTint`
  - `GlowStrength`
  - `CrustDarkness`
  - `NoiseScale`

## M_Beacon_Master

Purpose: player navigation beacons.

- Clean human-made material so it contrasts with organic cave visuals.
- Small cyan status light and colored channel ring.
- Parameters:
  - `BeaconColor`
  - `LightBandStrength`
  - `BodyRoughness`
