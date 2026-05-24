# Claude/Blender Prompt - Blue Crystal Clusters

You are working on Abyssal Earth, an Unreal Engine 5 first-person exploration game. Create the first blue crystal cluster kit for the Luminous Rift map.

Read before modeling:

- Docs/CORE_REFERENCE_LUMINOUS_RIFT.md
- Docs/ART_DIRECTION.md
- Docs/BLENDER_ASSET_PIPELINE.md
- Docs/MATERIAL_SPECS.md
- Content/Design/LuminousRiftAssetManifest.csv

Use Content/ArtDirection/References/luminous_rift_core_reference.png as the source of truth. The crystals should match the saturated blue/cyan crystalline growths in the concept: angular, faceted, embedded in black basalt, and useful as route-lighting accents.

## Assets To Create

- SM_Rift_CrystalCluster_S_A
- SM_Rift_CrystalCluster_S_B
- SM_Rift_CrystalCluster_M_A
- SM_Rift_CrystalCluster_M_B
- SM_Rift_CrystalCluster_L_A
- SM_Rift_CrystalCluster_Hero_A

## Scale Targets

- Small clusters: 0.5-1.5 m tall.
- Medium clusters: 2-4 m tall.
- Large cluster: 5-9 m tall.
- Hero cluster: 10-18 m tall.
- Each cluster should include a small basalt base so it sits naturally on ledges, walls, and machine seams.

## Visual Requirements

- Build angular faceted prisms, not smooth gemstones or rounded organic forms.
- Vary height, rotation, density, and breakage so repeated placement does not look tiled.
- Include at least three silhouette types across the kit:
  - vertical spear cluster
  - fan cluster leaning out of a surface
  - low broken shard cluster
- Crystals should have readable dark-blue body geometry plus separate emissive areas. Do not make the entire mesh uniformly glowing.
- Add chipped tips, smaller satellite shards, and embedded basalt/mineral buildup at the base.
- Keep the forms sharp enough to read from first-person distance and from a wide vista.

## Material Slots

Use these exact material slot names:

- mat_crystal_blue
- mat_blue_emissive
- mat_wet_basalt

Assign emissive slots only to inner faces, core veins, or selected shard tips. The basalt base should use mat_wet_basalt.

## Pivot, Collision, And Export

- Pivot/origin: base center at the floor-contact point for each asset.
- Apply transforms and use metric scale compatible with Unreal centimeters.
- Small/distant clusters can ship with no collision.
- Medium/large/hero clusters near player paths should have simple convex collision recommendations in notes, not complex per-poly collision.
- Save source files under ArtSource/Blender/LuminousRift/.
- Export Unreal-ready FBX or GLB files under Content/ArtSourceExports/LuminousRift/.

## Acceptance Checklist

- From silhouette alone, every cluster reads as blue crystal rather than ice, glass, fungus, or generic spikes.
- Small and medium variants can act as route breadcrumbs every 20-35 m.
- Large and hero variants can frame the Crystal Galleries and First Overlook without competing with the central orb.
- Material slots are stable and named exactly as listed.
- ArtSource/Blender/LuminousRift/ASSET_NOTES.md is updated with dimensions, pivot, collision, material slots, Nanite/LOD recommendation, and known issues for every exported asset.

