# Concept Art Review

Grounded notes from actually viewing the concept images (not just filenames), so
blockouts, materials, and per-map backend stay faithful to the canonical art.
Each entry records: canonical (must-have) elements, optional flavour, the colour
triad, the human-scale cue, traversal/backend implications, and any consistency
notes vs. `Docs/WORLD_ATLAS.md` and the map blockout docs.

> These are AI-generated concepts. In-game compositions must exclude any baked-in
> title text, watermark, or sparkle/UI icon (present on the Luminous Rift plate).

## Review status

- [x] Luminous Rift core reference
- [x] Glassroot Forest (Map 02)
- [x] Inner Sea (Map 03)
- [x] Fossil Sky (Map 04)
- [x] Gravity Well (Map 05)
- [x] Mantle Garden (Map 06)
- [ ] Detailed concept studies under `Content/ArtDirection/Concepts/` (≈120 images, by folder)

---

## Luminous Rift — `Content/ArtDirection/References/luminous_rift_core_reference.png`

Map 01. Cross-ref: `Docs/CORE_REFERENCE_LUMINOUS_RIFT.md`, `Docs/LUMINOUS_RIFT_BLOCKOUT.md`.

**Canonical elements (must read in-engine):**
- Central blue-white **energy orb** as the focal light source.
- Warm **gold beams** radiating in a radial spoke pattern from the orb to a ring of
  **hexagonal collector panels** arranged like flower petals.
- **Blue crystals** glowing in black basalt across foreground ledges and edges.
- A **bridge/causeway** crossing the mid-ground.
- Right-side **ancient machine wall** with circular blue-lit mechanisms (the gate).
- Background towers/structures fading into blue haze; strong **abyssal depth**.
- A tiny **human diver silhouette** on the foreground-left ledge for scale.

**Colour triad:** black/navy rock · cyan-blue crystal & orb glow · warm gold beams.

**Traversal/backend implications:** matches the existing blockout 1:1. The orb is a
landmark/scan target (no collision), beams are emissive splines, gate is a distant
landmark.

**Consistency note:** the plate shows **reflective water with a small boat** at the
base of the rift. The current `LUMINOUS_RIFT_BLOCKOUT.md` does not call out water in
the Rift. Either (a) add a shallow mirror-water pool at the lowest visible level for
the reflection beauty (it also foreshadows the Inner Sea), or (b) treat the water as
concept-only flavour. Recommend (a) as an optional low pool, not a traversal surface.

---

## Glassroot Forest — `Content/ArtDirection/WorldMaps/glassroot_forest_concept.png`

Map 02. Cross-ref: `Docs/Maps/GLASSROOT_FOREST.md`, `WORLD_ATLAS.md` Map 02.

**Canonical elements:**
- Tall, pale **translucent root-columns** rising from the floor into a misty ceiling.
- **Red sap/veins** glowing inside several trunks (vertical red internal glow).
- **Shallow reflective pools** (teal-green) with pale banks/terraces between them.
- Low cool **mist** throughout; small scattered floor **glints** (spore-lanterns).
- Foreground-left **dark rock ledge** with a tiny diver looking out — the overlook.

**Colour triad:** pale green-white roots · teal reflective pools · red sap accents
(against dark rock frame).

**Traversal/backend implications:** confirms the blockout's First-Overlook framing,
hero root grove, red sap (conductive material seed), pearl terraces, pools, and
spore-lanterns. Spore scanner-distortion and timed root gates remain the map's
signature backend (roadmap C2/C3).

**Consistency note:** in the concept the inter-pool banks read as **pale muddy
terraces**, not the crisp **pearl-white mineral stone** the World Atlas/blockout
specify. Decide which is canonical: either push the pearl-white mineral material in
production, or soften the "pearl" language to match the concept's subtler banks. The
blockout currently says pearl-white; flagging for an art call.

---

## Inner Sea — `Content/ArtDirection/WorldMaps/inner_sea_concept.png`

Map 03. Cross-ref: `WORLD_ATLAS.md` Map 03. (Blockout doc not yet written — this
review should inform it.)

**Canonical elements:**
- A vast dark **underground ocean** receding into haze; **stalactites** overhead.
- **Gold plankton trails** glowing as route-like ribbons across the water surface.
- **Docks and broken piers** along the shores with **moored boats/skiffs** and warm
  lamp lights.
- **Blue-lit half-submerged ruins** at the left and distant islands/structures.
- Foreground **wet dock/platform** with a tiny diver holding a lamp — the overlook.

**Colour triad:** dark blue-black water · warm gold plankton & lamp accents · teal-blue
atmospheric haze (with blue-lit ruin accents).

**Traversal/backend implications (feed the future blockout + roadmap C3):**
- The gold plankton trails are literally the readable route — implement
  `BP_InnerSea_PlanktonTrailSpline` as scanner-reactive route guidance.
- Moored skiffs imply a possible **skiff/boat traversal** mode (or staged for later);
  at minimum, dock-to-dock stepping across piers.
- Half-submerged ruins → electrical-discharge hazard; flooding route changes.
- Beacons matter more here (similar-looking water spaces) — emphasise beacon prompts.

**Composition note:** the first-overlook framing (foreground dock + lamp-lit diver
looking across the water toward gold trails) should be the postcard shot for the
eventual `Docs/Maps/INNER_SEA.md`.

---

## Fossil Sky — `Content/ArtDirection/WorldMaps/fossil_sky_concept.png`

Map 04. Cross-ref: `WORLD_ATLAS.md` Map 04. (Blockout doc not yet written.)

**Canonical elements:**
- A **ceiling-dominant** composition: a colossal fossil **skeleton** (vertebrae +
  rib arches) embedded across the ceiling like a second firmament. The player looks
  **up**, not down.
- **Bone-white / amber limestone** cavern with **amber dust shafts** of light.
- Suspended ancient **observation walkways/bridges** crossing the space, with a tiny
  diver on a walkway for scale.
- **Black chasms** below the walkways; small **cyan fossil-vein** scanner-reactive
  accents.

**Colour triad:** bone-white/amber limestone · warm amber dust light · cyan
fossil-vein accents (against black chasms).

**Traversal/backend implications:** narrow brittle observation walkways over chasms
(brittle-walkway hazard, roadmap C2); scanner reconstructs fossil outlines / hidden
route clues (a scan-reveal mechanic). Composition rule: stage the first overlook so
the player looks up at the ceiling leviathan.

## Gravity Well — `Content/ArtDirection/WorldMaps/gravity_well_concept.png`

Map 05. Cross-ref: `WORLD_ATLAS.md` Map 05. (Blockout doc not yet written.)

**Canonical elements:**
- A **spherical/vortex** cavern: rock platforms, debris, and arcs spiral **around a
  central blue-white anomaly**, with the path visibly continuing sideways and upward
  around the void.
- **Floating basalt platforms** and curved **stabilizer** arcs with **amber machine
  accents**; suspended **water ribbons**; bent light / lensing toward the core.
- Foreground diver on a ledge with a **tether/line** for scale (matches
  `D_Human_TetherAnchor` and the tether traversal idea).

**Colour triad:** blue-white anomaly core · dark blue-grey floating basalt · amber
stabilizer accents.

**Traversal/backend implications:** the headline system — **gravity reorientation
volumes** and floating-platform traversal with tether safety (roadmap C3). This is
the highest-risk traversal map; the World Atlas itself calls for a technical risk
note before implementation. Keep route orientation readable by beacon colour and
scanner vectors.

## Mantle Garden — `Content/ArtDirection/WorldMaps/mantle_garden_concept.png`

Map 06. Cross-ref: `WORLD_ATLAS.md` Map 06. (Blockout doc not yet written.)

**Canonical elements:**
- **Black obsidian** terraces/ridges forming a thin walkable path through the danger.
- **Orange molten** glow in cracks and below; tall **white steam columns** rising from
  vents in the background.
- **Magenta mineral flowers** clustered along the (cooler, safe) foreground ridges.
- A tiny diver on the obsidian ridge for scale; a large heat-resistant **machinery**
  structure reads upper-left.

**Colour triad:** black obsidian · orange heat bloom · magenta mineral flowers (with
white steam).

**Traversal/backend implications:** read heat cycles and move during safe windows;
the magenta blooms literally mark cool/safe ridges (a readability affordance). Needs
the **temperature/heat-exposure vital** (roadmap B3) and a generalized cyclic
**pressure/steam vent hazard** derived from `AEmberVentHazard` (roadmap C2). The route
is "a thin black path through lethal heat" — keep safe footing visually distinct.

## Next review pass

World-map plates are all reviewed. Next, sample the per-area study folders under
`Content/ArtDirection/Concepts/` (Characters, Items, Intro, Narrative_Beats, and the
per-biome study sets) to derive exact palettes and confirm asset silhouettes before
each map's blockout and asset manifest. Do this in small batches to manage context.
