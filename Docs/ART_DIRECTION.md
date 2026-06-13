# Art Direction

## Source Of Truth

The attached concept image is the primary visual target for the first map.

- Repository reference: `Content/ArtDirection/References/luminous_rift_core_reference.png`
- Working title in docs: `Core Luminous Rift Reference`
- Priority: highest. When another doc conflicts with this image, the image wins unless Vivek explicitly changes direction.

The map should be modeled, lit, and textured around this exact feeling: a colossal subterranean rift where black carved geology and ancient machine architecture frame a suspended blue-white energy sphere, gold beam networks, crystalline outcrops, and vertiginous platforms above an abyss.

## Visual Target

The Luminous Rift is not a normal cave, a generic alien jungle, or a simple crystal cavern. It is an impossible interior world where geology, buried megastructure, and luminous technology have fused together over ancient time.

The desired first impression:

- The player stands on a dark foreground ledge, visibly tiny against the scene.
- The cavern drops away into a deep vertical blue abyss.
- Huge rock arches, ribbed walls, and suspended structures frame the view from all sides.
- The central landmark is a bright, almost solar blue-white energy sphere held in place by a mechanical collector array.
- Warm gold beams connect the sphere to hexagonal collector petals and circular mechanical nodes.
- Blue crystals grow out of black rock and embedded architecture, acting as natural accent lights.
- The scene feels old, wet, cold, enormous, and sacred rather than clean sci-fi.

## Composition Rules

Every major shot in the map should preserve the reference's composition language.

### Foreground

- Use dark, high-contrast rock silhouettes to frame the scene.
- Include a human scale marker: player body, railings, beacon, survey crate, or small platform lights.
- Ledges should feel carved or eroded, not smooth ramps.
- Foreground crystals should be saturated cyan-blue and sharp enough to read against the dark rock.

### Midground

- Use bridges, suspended platforms, broken machine ribs, and vertical towers to lead the eye toward the energy sphere.
- Put the primary traversal path on a narrow ledge/bridge system, not a wide open floor.
- Midground shapes should overlap heavily; depth comes from layering silhouettes in fog.
- The central orb must be visible from multiple route points, partially occluded at first and fully revealed later.

### Background

- The abyss should continue far below the playable path, with mist and faint vertical blue light columns.
- Distant towers and hanging structures should fade into fog.
- The ceiling and side walls should show vertical striations, hanging slabs, and carved recesses.
- Avoid flat backdrop walls. Even distant shapes need readable vertical depth.

## Palette

The reference uses a disciplined three-part palette:

- Dominant: near-black rock and ancient dark metal.
- Cool light: cyan, blue, and blue-white emissive crystals, fog, and energy.
- Warm accent: gold/amber beams, small machine nodes, and limited work lights.

Do not let the scene become one-note blue. The gold beam network is essential; it provides contrast, focal hierarchy, and the sense that the central mechanism is active.

Suggested material color anchors:

- Wet basalt: almost black with blue-gray highlights, subtle green/brown mineral variation.
- Ancient metal/stone: gunmetal, graphite, dark bronze edges, worn bevels.
- Energy sphere: white core, cyan body, electric blue edge scatter.
- Crystal: deep blue base, cyan inner glow, white rim highlights.
- Beam/collector nodes: warm gold, not orange lava.
- Human equipment: muted off-white, dark gray, small cyan status LEDs.

## Lighting Rules

- The central energy sphere is the primary key light.
- Gold beams provide thin, directional warm highlights across platforms and collectors.
- Blue crystals act as localized rim/fill lights.
- The lower abyss glows with soft blue volumetric light but should remain unreadably deep.
- Human work lights must be weak by comparison; they are scale cues, not primary lighting.
- Use Lumen GI, volumetric fog, and high contrast exposure control. Keep emissive detail visible; do not over-bloom the orb into a blank white blob.

## Shape Language

### Natural

- Jagged basalt, eroded ledges, vertical cliff faces, stalactite-like slabs.
- Root/rib-like stone forms that curl around architecture.
- Crystals: faceted, angular, clustered, mostly vertical.

### Ancient Machine

- Circular doors, ring sockets, radial hubs, recessed glowing blue strips.
- Hexagonal collector plates arranged like honeycomb petals.
- Tall monolithic towers with vertical grooves.
- Suspended bridge slabs with carved panel seams and broken underside struts.

### Human

- Small, recent, practical, and slightly crude.
- Survey lamps, crates, cables, temporary railings, beacon devices.
- Human props should contrast with the ancient machinery: simple silhouettes, modern materials, smaller scale.

## What To Avoid

- Generic fantasy cave assets without machine integration.
- Oversized fungus as the main identity of this map. Biology can exist later, but this reference is dominated by crystal, abyss, and ancient machinery.
- Clean spaceship corridors. The machinery should feel buried, eroded, and fused with rock.
- A flat arena floor. The reference is about vertical drop, bridges, ledges, and suspended structures.
- Purple-only lighting, heavy magenta fog, or lava-dominant orange.
- Symmetry that feels sterile. The collector/orb can be symmetric; the cave and traversal path should be broken and organic.

## First-Map Asset Needs

Highest priority assets for the first playable beauty pass:

- Modular dark basalt cliffs, arches, ledges, and overhangs.
- Ancient machine platform kit: floor slabs, bridge spans, wall panels, circular sockets, vertical tower segments.
- Central orb apparatus: energy sphere mesh/VFX proxy, radial hub, beam emitters, hex collector panels.
- Hex collector panel kit: single hex tile, 7-tile flower cluster, broken cluster variants, brass/gold frame pieces.
- Blue crystal clusters in small, medium, large, and hero sizes.
- Abyss dressing: distant spires, suspended debris, hanging slabs, far blue light shafts.
- Human survey kit: player-scale platform, crates, lamps, cable coils, small console, temporary beacon.
- VFX placeholders: blue motes, gold beam splines, volumetric fog cards, slow falling dust/debris.

## Biome Naming Alignment

Earlier docs used `Mirror Marsh`, `Crystal Spine`, and `Ember Vents`. Going forward, the first map should be reframed around the concept art:

- `First Overlook`: the reference image composition from the player's first reveal ledge.
- `Abyssal Approach`: narrow ledges and bridges descending toward the ancient structure.
- `Crystal Galleries`: blue crystal clusters embedded in rock and machine ruins.
- `Collector Array`: central orb, gold beams, hex panels, and radial hub.
- `Ancient Gate`: the monumental right-side wall/gate structure from the reference.
- `Second Sky Overlook`: final view into the lower rift beyond the machine.

The old organic/geothermal ideas can become later biomes or side pockets, but they should not drive the core map anymore.

## Broader Map Art Direction

The world atlas images under `Content/ArtDirection/WorldMaps/` define the first set of future map identities. Each map must keep Abyssal Earth's grounded, high-fidelity inner-world tone while using a distinct color triad and silhouette language.

### Glassroot Forest

Reference: `Content/ArtDirection/WorldMaps/glassroot_forest_concept.png`

- Palette: pale green glass, pearl stone, red mineral sap.
- Silhouette: vertical translucent root-columns, soft terraces, shallow pools.
- Mood: biological cathedral, quiet field-science wonder.
- Avoid: surface jungle, leafy trees, generic fantasy forest.

### Inner Sea

Reference: `Content/ArtDirection/WorldMaps/inner_sea_concept.png`

- Palette: silver-black water, dark teal fog, gold plankton trails.
- Silhouette: low docks, drowned ruins, vast water plane, hanging mineral shelves.
- Mood: lonely ocean navigation inside Earth.
- Avoid: tropical beach, pirate imagery, surface sky.

### Fossil Sky

Reference: `Content/ArtDirection/WorldMaps/fossil_sky_concept.png`

- Palette: bone-white limestone, amber dust, cyan fossil veins.
- Silhouette: ceiling fossils, rib arches, suspended walkways, black chasms.
- Mood: scientific awe and deep-time mystery.
- Avoid: museum exhibit, horror skeleton cave, desert surface.

### Gravity Well

Reference: `Content/ArtDirection/WorldMaps/gravity_well_concept.png`

- Palette: dark basalt, blue-white anomaly light, amber stabilizer accents.
- Silhouette: spherical cavern, floating platforms, curved towers, suspended water ribbons.
- Mood: physically impossible but engineered and ancient.
- Avoid: outer space, stars, fantasy magic runes.

### Mantle Garden

Reference: `Content/ArtDirection/WorldMaps/mantle_garden_concept.png`

- Palette: black obsidian, white steam, orange heat, magenta mineral blooms.
- Silhouette: narrow ridges, steam columns, heat cracks, mineral flowers.
- Mood: beautiful environmental danger near extreme heat.
- Avoid: generic lava level, hell imagery, red-only palette.

---

## Geometry Quality Mandate

These rules apply to every Blender asset script in the library. They are enforced by
`Tools/validate_asset_scripts.py` (16 checks) and by visual review of render composites
attached to every PR.

### Ground truth is always the concept image

Documentation, scale tables, and design docs are guidance. The concept art is the target.
When they conflict, the concept art wins. Every script must carry a `Concept: IMAGE-ID`
docstring line that names the reference image (e.g. `Concept: AD-001, LR-006`).

### Silhouette first

A well-built asset must read correctly as a distinct silhouette at 100 m distance in the
Unreal viewport. If you cannot identify what the asset is from its outline alone, the geometry
needs more work regardless of polycount or material quality.

### No placeholder geometry

Scripts may not ship with:
- `bm.verts.new(...)` calls whose vertices are never connected to any face
- Chains of icospheres used as "bones" or "spines" (they do not auto-merge)
- Vertex positions set to `(0, 0, 0)` to simulate deletion (collapses geometry)
- Zero-thickness planes

### Scale must be documented in the script

Every script must define at least one module-level `UPPER_CASE` constant specifying a
key dimension. The scale must match the range in `Docs/ASSET_QUALITY_STANDARDS.md`. This
allows CI to flag scripts where geometry is built at the wrong order of magnitude.

### Visual acceptance protocol

1. CI runs `Tools/render_asset_preview.py` on every changed script and uploads a
   `*_vs_concept.png` composite to the PR as a GitHub Actions artifact.
2. The PR author reviews the composite before requesting merge.
3. The user (Vivek) gives explicit go/no-go per asset in the PR review.
4. Assets not yet approved loop back for geometry refinement. There is no fixed iteration
   limit; the loop continues until approval is given.

See `Docs/ASSET_QUALITY_STANDARDS.md` for the full per-biome checklist.
