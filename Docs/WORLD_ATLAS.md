# Abyssal Earth World Atlas

## Purpose

This document defines the long-term map vision for Abyssal Earth. It gives future agents, Claude/Blender workers, Unreal Editor sessions, and design passes a shared picture of what the game should become beyond the first Luminous Rift vertical slice.

The maps below should feel like connected layers of one impossible inner-Earth world, not disconnected fantasy levels. Each map needs:

- A distinct visual identity.
- A strong first-overlook composition.
- A traversal fantasy.
- A scanner/discovery theme.
- Clear asset families for Blender/Unreal production.
- A reason to exist in the player's descent.

## Visual Progression

The game should descend from ancient machine mystery into increasingly strange natural and physical systems:

1. **Luminous Rift**: ancient machine + crystal abyss. First proof that Earth contains impossible structures.
2. **Glassroot Forest**: living mineral ecosystem. The underworld is biologically active.
3. **Inner Sea**: underground ocean and drowned ruins. The world has scale beyond walkable caverns.
4. **Fossil Sky**: deep-time archive. Earth remembers impossible eras.
5. **Gravity Well**: physics anomaly. The planet's interior laws are unstable or engineered.
6. **Mantle Garden**: geothermal edge. Beauty survives near violent heat and pressure.

This order can change during production, but the contrast between neighboring maps should remain.

## Map 01 - Luminous Rift

![Luminous Rift](../Content/ArtDirection/References/luminous_rift_core_reference.png)

### Core Fantasy

A colossal vertical rift where black basalt, blue crystals, and ancient machine architecture frame a suspended blue-white energy sphere connected to hexagonal collectors by warm gold beams.

### Role In Game

Opening vertical slice and proof of concept. Teaches movement, scanning, beacons, route objectives, environmental scale, and ancient-machine mystery.

### Player Route

- Descent Elevator
- First Overlook
- Abyssal Approach
- Crystal Galleries
- Collector Array
- Ancient Gate
- Second Sky Overlook

### Visual Pillars

- Dark rock frame.
- Central energy orb.
- Gold beam network.
- Hex collector arrays.
- Blue crystals.
- Suspended bridges and ledges.
- Monumental gate wall.
- Tiny human scale.

### Primary Asset Families

- `SM_Rift_ForegroundLedge_A`
- `SM_Rift_BridgeSpan_A/B_Broken`
- `SM_Rift_HexCollector_Tile_A`
- `SM_Rift_HexCollector_Cluster_A/B`
- `SM_Rift_OrbFrame_A`
- `SM_Rift_OrbHub_A`
- `SM_Rift_BeamEmitterNode_A`
- `SM_Rift_AncientWall_Gate_A`
- `SM_Rift_CrystalCluster_S/M/L/Hero`

### Discovery Themes

- Ancient containment/collector machine.
- Scanner-reactive crystals.
- Blue energy transmission.
- Human intrusion into something much older.

## Map 02 - Glassroot Forest

![Glassroot Forest](../Content/ArtDirection/WorldMaps/glassroot_forest_concept.png)

### Core Fantasy

A cathedral-sized subterranean forest made of translucent root-columns, pearl mineral terraces, shallow reflective pools, and red mineral sap glowing inside glasslike biological structures.

### Role In Game

First strong biological map. It proves the inner Earth is not only mechanical and geologic, but alive. This map should slow the pacing after the Luminous Rift and make the player feel like a field naturalist.

### First Overlook

The player exits a tight basalt seam onto a shadowed ledge. Below is a pale green-white root forest, with dozens of translucent trunks rising into mist. Red sap glows inside a few roots like veins. The playable route is visible as a chain of pearl terraces and shallow pools.

### Traversal Fantasy

- Walk across mineral terraces around root bases.
- Cross shallow reflective pools.
- Use scanner pulses to reveal safe living bridges or dormant root gates.
- Move quietly through spore-heavy pockets.
- Climb inside hollow root tubes in later versions.

### Visual Pillars

- Pale green translucent roots.
- Pearl-white mineral stone.
- Red mineral sap accents.
- Shallow reflective pools.
- Low cool mist.
- Soft bioluminescent underside glows.
- Gentle motion: root pulse, drifting spores, water ripples.

### Primary Asset Families

- `SM_Glassroot_RootColumn_S/M/L/Hero`
- `SM_Glassroot_HollowRootTunnel_A`
- `SM_Glassroot_Terrace_PearlStone_A/B`
- `SM_Glassroot_RootBridge_A`
- `SM_Glassroot_SapVein_A`
- `SM_Glassroot_PoolEdge_A`
- `SM_Glassroot_SporePod_A/B`
- `VFX_Glassroot_SporeMist`
- `M_Glassroot_TranslucentRoot_Master`
- `M_Glassroot_RedSap_Master`

### Discoveries

- `D_Bio_GlassrootColumn`: giant translucent root structure.
- `D_Bio_RedMineralSap`: conductive sap/mineral fluid.
- `D_Geo_PearlTerrace`: pale mineral floor built by root secretions.
- `D_Bio_SporeLantern`: small organism that lights safe paths.
- `D_Anomaly_RootSignalDelay`: roots respond to scanner pulses after a delay.

### Hazards

- Spore clouds that distort scanner readouts.
- Fragile terrace edges.
- Root gates that close after a timed interval.
- Pools that hide sinkholes.

### Sound Direction

Soft water drips, low resonant root creaks, distant glass chimes, faint biological pulses, muffled footfalls.

## Map 03 - Inner Sea

![Inner Sea](../Content/ArtDirection/WorldMaps/inner_sea_concept.png)

### Core Fantasy

A vast underground ocean inside Earth, with silver-black water, dark teal fog, gold plankton trails, half-submerged ruins, broken piers, distant islands, and hanging mineral shelves overhead.

### Role In Game

Expands scale horizontally after the verticality of the first maps. Introduces water traversal, navigation uncertainty, distant landmarks, and larger route planning.

### First Overlook

The player reaches a wet basalt dock above an underground sea. The water vanishes into blue-black distance. Gold plankton trails draw route lines across the surface. Broken ancient piers and half-submerged machine structures imply this sea drowned something older.

### Traversal Fantasy

- Navigate docks, stepping-stone ruins, and low platforms.
- Use beacons to mark return routes across similar-looking water spaces.
- Later: pilot a small survey skiff or deploy floating scanner buoys.
- Follow plankton trails that react to scanner pulses.
- Dive only in controlled pockets if underwater gameplay is added.

### Visual Pillars

- Silver reflections on black water.
- Dark teal atmospheric depth.
- Warm gold plankton ribbons.
- Half-submerged ancient ruins.
- Wet basalt docks and piers.
- Distant islands and cave walls.
- Hanging mineral shelves overhead.

### Primary Asset Families

- `SM_InnerSea_BasaltDock_A/B`
- `SM_InnerSea_BrokenPier_A/B`
- `SM_InnerSea_SubmergedRuin_A/B/C`
- `SM_InnerSea_MineralShelf_Ceiling_A`
- `SM_InnerSea_DistantIsland_A/B`
- `SM_InnerSea_Buoy_A`
- `BP_InnerSea_PlanktonTrailSpline`
- `M_InnerSea_SilverBlackWater_Master`
- `M_InnerSea_GoldPlankton_Master`

### Discoveries

- `D_Geo_AbyssalBrineSea`: impossible underground saltwater body.
- `D_Bio_GoldPlanktonTrail`: plankton that forms route-like currents.
- `D_Structure_DrownedPier`: ancient structure submerged by rising water.
- `D_Anomaly_TideWithoutMoon`: tide patterns with no surface lunar cause.
- `D_Human_ForwardDock`: temporary human staging dock.

### Hazards

- Flooding route changes.
- Low visibility water pockets.
- Electrical discharges in submerged machine ruins.
- Moving platforms or floating debris.

### Sound Direction

Deep water slosh, distant cavern groans, echoing droplets, faint whale-like low tones, plankton shimmer, creaking docks.

## Map 04 - Fossil Sky

![Fossil Sky](../Content/ArtDirection/WorldMaps/fossil_sky_concept.png)

### Core Fantasy

An immense dry cavern where the ceiling is lined with gigantic fossilized marine creatures, rib-like mineral arches, bone-white stone, amber dust shafts, black chasms, and ancient observation walkways.

### Role In Game

Adds deep-time awe and scientific mystery. The player should feel like they are walking through a natural archive that should be impossible at this depth.

### First Overlook

The player steps onto a suspended walkway and looks up, not down. A colossal fossil skeleton is embedded across the ceiling like a second firmament. Amber dust falls through the ribs. Faint cyan scanner-reactive veins trace through the bones.

### Traversal Fantasy

- Cross narrow observation walkways.
- Move through rib arches and fossil cavities.
- Use scanner to reconstruct fossil outlines and hidden route clues.
- Descend into black chasms between bone-white shelves.
- Activate old observation machines that project fossil silhouettes.

### Visual Pillars

- Ceiling-dominant composition.
- Giant fossil silhouettes.
- Pale bone-white and limestone materials.
- Amber dust shafts.
- Cyan fossil-vein accents.
- Suspended walkways.
- Black chasm contrast.

### Primary Asset Families

- `SM_FossilSky_GiantRib_A/B/C`
- `SM_FossilSky_CeilingSkeleton_Hero_A`
- `SM_FossilSky_BoneArch_A`
- `SM_FossilSky_ObservationWalkway_A/B`
- `SM_FossilSky_DustShaftCard_A`
- `SM_FossilSky_FossilVein_A`
- `SM_FossilSky_LimestoneShelf_A/B`
- `M_FossilSky_BoneStone_Master`
- `M_FossilSky_CyanFossilVein_Master`

### Discoveries

- `D_Geo_BoneWhiteLimestone`: pale mineral matrix preserving impossible fossils.
- `D_Anomaly_CeilingLeviathan`: vast fossil embedded overhead.
- `D_Structure_ObservationWalkway`: ancient route built to study the fossils.
- `D_Anomaly_CyanFossilVein`: scanner-reactive vein tracing extinct anatomy.
- `D_Bio_DustMoteColony`: microscopic life in amber dust shafts.

### Hazards

- Brittle walkways.
- Dust clouds that reduce visibility.
- Chasm crossings.
- Falling fossil fragments.

### Sound Direction

Dry wind through ribs, dust hiss, walkway creaks, distant stone cracks, low scanner harmonics.

## Map 05 - Gravity Well

![Gravity Well](../Content/ArtDirection/WorldMaps/gravity_well_concept.png)

### Core Fantasy

A colossal spherical cavern where basalt platforms, water ribbons, and crystal debris are suspended around a central gravitational anomaly. Ancient stabilizer towers curve around the chamber while blue-white lensing light bends through mist.

### Role In Game

Introduces the strongest traversal twist: altered gravity and spatial navigation. This map should feel surreal while staying grounded in the game's ancient-machine/geologic language.

### First Overlook

The player enters a circular chamber and sees the path continue sideways and upward around the void. Floating stone shelves arc around a blue-white anomaly. Water hangs in ribbons. Amber stabilizer lights show that something is actively holding the chamber together.

### Traversal Fantasy

- Descend a parkour approach corridor where gravity pulls strangely and ledges crumble — tethered floating rocks are the only safe anchors.
- Fire your tether at iron-ringed drifting rock shards to swing across void gaps and control your descent.
- Cross orbital floating platforms once inside the well proper.
- Reorient gravity across route gates — your sense of "down" shifts room by room.
- Chain-tether across multiple drifting objects for complex routes the stabilizer towers define.
- Track route direction by beacon color and scanner gravity-vector overlays.
- Navigate water ribbons as moving obstacles or temporary bridges.

### Visual Pillars

- Spherical cavern composition.
- Central blue-white anomaly.
- Floating basalt platforms.
- Curved stabilizer towers.
- Suspended water ribbons.
- Bent light/lensing effects.
- Amber machine stabilizer accents.

### Primary Asset Families

- `SM_GravityWell_FloatingPlatform_A/B/C`
- `SM_GravityWell_CurvedTower_A/B`
- `SM_GravityWell_AnchorGate_A`
- `SM_GravityWell_WaterRibbon_A`
- `SM_GravityWell_CrystalDebris_A/B`
- `SM_GravityWell_TetherRock_A/B`
- `SM_GravityWell_ParkourLedge_A`
- `SM_GravityWell_TetherAnchorPost_A`
- `BP_GravityWell_AnomalyCore`
- `BP_GravityWell_ReorientationVolume`
- `M_GravityWell_LensingEnergy_Master`
- `M_GravityWell_AmberStabilizer_Master`

### Discoveries

- `D_Anomaly_GravityCore`: central anomaly bending local gravity.
- `D_Structure_StabilizerTower`: curved tower regulating the anomaly.
- `D_Geo_SuspendedBasalt`: rock shelf held in nonstandard gravitational equilibrium.
- `D_Anomaly_WaterRibbon`: stream suspended across multiple gravity vectors.
- `D_Human_TetherAnchor`: human safety system adapted to the chamber.

### Hazards

- Misaligned gravity volumes.
- Floating debris impacts.
- Loss of route orientation.
- Timed stabilizer pulses.
- Tethered rock collision (a drifting rock carrying the player into a shear zone).
- Parkour ledge collapse (approach corridor crumbling stone).

### Sound Direction

Deep sub-bass gravitational hum, reversed droplets, spatially shifting stone impacts, electrical stabilizer pulses.

## Map 06 - Mantle Garden

![Mantle Garden](../Content/ArtDirection/WorldMaps/mantle_garden_concept.png)

### Core Fantasy

A beautiful but dangerous geothermal chamber near mantle-like heat: black obsidian terraces, white steam columns, orange heat blooms, magenta mineral flowers, molten cracks far below, and heat-resistant ancient machinery.

### Role In Game

Late vertical slice or later chapter map focused on environmental danger. It proves Abyssal Earth can be hazardous without becoming a combat game.

### First Overlook

The player emerges above a black obsidian amphitheater. White steam towers rise from cracks. Orange light pulses under the glassy floor. Magenta mineral blooms cluster only along safe cooler ridges. The route is a thin black path through lethal heat.

### Traversal Fantasy

- Read heat cycles and move during safe windows.
- Cross obsidian ridges between vent fields.
- Use scanner to detect cool paths and pressure buildup.
- Deploy beacons in low-visibility steam.
- Later: manage suit heat or temporary cooling.

### Visual Pillars

- Black obsidian.
- White steam.
- Orange heat glow.
- Magenta mineral flowers.
- Heat shimmer.
- Narrow safe ridges.
- Ancient heat-resistant machinery.

### Primary Asset Families

- `SM_MantleGarden_ObsidianRidge_A/B`
- `SM_MantleGarden_SteamVent_A/B`
- `SM_MantleGarden_MineralFlower_A/B/C`
- `SM_MantleGarden_HeatCrack_A`
- `SM_MantleGarden_ThermalMachine_A`
- `BP_MantleGarden_PressureVent`
- `BP_MantleGarden_HeatSafeWindow`
- `VFX_MantleGarden_WhiteSteamColumn`
- `M_MantleGarden_Obsidian_Master`
- `M_MantleGarden_HeatBloom_Master`

### Discoveries

- `D_Geo_ObsidianBloomTerrace`: glassy terrace formed by repeated heat pulses.
- `D_Bio_MagentaThermalBloom`: mineral-organic bloom living at heat boundaries.
- `D_Geo_PressureVent`: cyclic vent column.
- `D_Structure_ThermalRegulator`: ancient machinery surviving near extreme heat.
- `D_Anomaly_CoolRidgePattern`: safe path pattern too regular to be natural.

### Hazards

- Heat damage.
- Timed vent eruptions.
- Low visibility steam.
- Brittle obsidian edges.
- Pressure shockwaves.

### Sound Direction

Steam roar, glass crackle, deep heat pulses, muffled pressure booms, sharp mineral chimes.

## Global Map Design Rules

### Every Map Needs

- A first-overlook vista.
- A player-scale foreground object.
- A distant landmark visible from multiple route points.
- At least three discovery categories.
- A clear color triad.
- A route readable by light, geometry, or motion.
- A final reveal that points toward the next map.

### Every Map Must Avoid

- Flat arena layouts.
- One-note palettes.
- Generic fantasy caves.
- Clean sci-fi corridors.
- Decorative assets with no traversal or discovery purpose.
- Scale without human reference.

### Asset Production Pattern

For each map, create:

1. Hero reference image.
2. Map design brief.
3. Asset manifest.
4. Material spec subset.
5. Blockout checklist.
6. Discovery catalog rows.
7. Ambience cue rows.
8. Screenshot acceptance checklist.

### Long-Term Biome Candidates

These are not yet promoted to full map status:

- **Ashfall Cathedral**: a quiet ash-covered cavern of collapsed mineral vaults.
- **Magnetic Bloom Fields**: metallic flowers aligning to invisible magnetic waves.
- **Deep Bore City**: abandoned human/ancient hybrid research settlement.
- **Subcrust Observatory**: an ancient lens looking inward toward the planet's core.
- **Black Rain Vault**: a cavern where mineral condensation falls upward and downward in alternating cycles.
