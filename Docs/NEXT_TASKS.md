# Next Tasks

The hourly continuation worker should always pick the highest-impact available task from this list, update files directly, append a short entry to `Docs/HOURLY_LOG.md`, commit, and push when the change is coherent.

## Operating Rules

- Always `git fetch --prune` before doing Abyssal Earth work.
- Inspect `git status` before editing.
- Do not overwrite Windows/Claude/Unreal Editor work.
- Unreal Editor and Blender are expected to be handled mainly on the Windows side.
- This side should aggressively improve docs, manifests, prompts, code scaffolding, review notes, and asset-production instructions.
- If a task produces useful repo state, commit and push it.

## Current Strategic Priority

The project now has two planning layers:

1. **P0 vertical slice**: make `MAP_LuminousRift` match `Content/ArtDirection/References/luminous_rift_core_reference.png`.
2. **P0 asset production**: generate, import, and place the first usable Luminous Rift art kit.
3. **P0 game development**: movement, scanner, beacons, objectives, HUD/journal, survival pressure, and blockout playability.
4. **P1 prologue**: implement the submarine-to-crash opening after the core cavern loop is playable.
5. **Later add-on**: keep the Abyssal Interface design in mind, but do not prioritize it until the game is much further along.
6. **World atlas**: define the broader Abyssal Earth map sequence using `Docs/WORLD_ATLAS.md` and the generated concept images in `Content/ArtDirection/WorldMaps/`.

Do not let worldbuilding, story polish, or the Abyssal Interface distract from P0 implementation. The immediate push is assets plus playable game development.

## P0 - Asset Production Starting Order

Start here. These are the assets Vivek and Claude should build first because they make the map look like the concept fastest and unblock Unreal placement.

1. **Blue crystal clusters**
   - `SM_Rift_CrystalCluster_S_A/B/C`
   - `SM_Rift_CrystalCluster_M_A/B/C`
   - `SM_Rift_CrystalCluster_L_A/B`
   - `SM_Rift_CrystalCluster_Hero_A`
   - Why first: fast to make, instantly improves lighting/route language, reusable everywhere.
2. **Foreground reveal ledge and rock frame**
   - `SM_Rift_ForegroundLedge_A`
   - `SM_Rift_RockArch_A/B`
   - `SM_Rift_Overhang_A/B`
   - Why next: required for the first screenshot and the Luminous Rift reveal.
3. **Ancient bridge/platform kit**
   - `SM_Rift_BridgeSpan_A`
   - `SM_Rift_BridgeSpan_B_Broken`
   - `SM_Rift_PlatformNode_A`
   - Why next: turns the cavern into a playable route.
4. **Hex collector panels**
   - `SM_Rift_HexCollector_Tile_A`
   - `SM_Rift_HexCollector_Cluster_A`
   - `SM_Rift_HexCollector_Cluster_B_Broken`
   - Why next: essential visual identity from the core reference.
5. **Orb apparatus**
   - `SM_Rift_OrbFrame_A`
   - `SM_Rift_OrbHub_A`
   - `SM_Rift_BeamEmitterNode_A`
   - `BP_RiftEnergyOrb`
   - `BP_RiftGoldBeamSpline`
   - Why next: central focal landmark and lighting source.
6. **Ancient gate wall**
   - `SM_Rift_AncientWall_Gate_A`
   - Why next: major right-side landmark, sells scale.
7. **Background depth kit**
   - `SM_Rift_TowerSegment_A/B/C`
   - `SM_Rift_HangingSlab_A/B/C`
   - `SM_Rift_DistantSpire_A/B`
   - Why next: makes the abyss feel huge.
8. **Human survey kit**
   - `SM_Human_SurveyCrate_A`
   - `SM_Human_PortableLamp_A`
   - `SM_Human_CableCoil_A`
   - `SM_Human_FieldConsole_A`
   - Why next: scale and prologue dressing.

## P1 - Story And Prologue Work

- Build the opening sequence described in `Docs/NARRATIVE_FOUNDATION.md`: ocean surface, submarine room, briefing display, Helios shaft dock, robot passage, elevator descent, elevator failure, crushed elevator, Luminous Rift reveal.
- Create `MAP_Prologue_Submarine` or a prototype room/map for the submarine intro.
- Create `MAP_Prologue_ElevatorShaft` or a connected sequence for docking, Helios robots, and elevator descent.
- Create a wall tablet/briefing display asset with the headline FIRST MAJOR EXPLORATION EXPEDITION OF EARTH'S ABYSSAL PLAINS.
- Create placeholder Helios humanoid robot actors with short pre-cavern text bubble interactions.
- Add an objective path for `OBJ_VERIFY_HELIOS` -> `OBJ_SURVIVE` using `Content/Design/MainObjectiveArc.csv`.
- Prototype the crushed-elevator door interaction/QTE or hold-to-pry interaction.
- Ensure all normal story/dialogue stops after the Luminous Rift reveal.
- Add end-credit image/vignette planning for player return, public discovery, and future scientific progress.

## Later Add-On - Abyssal Interface AI Work

Not a current production priority. Keep this design available for later, after the core game loop, assets, maps, survival, discovery, and fabrication systems are much further along.

- Implement the first text-only `WBP_AbyssalInterfaceTerminal` UI.
- Add `AAbyssalInterfaceTerminal` interactable actor or Blueprint equivalent.
- Add `UAbyssalInterfaceSubsystem` or Blueprint subsystem for request/response handling.
- Use `Content/Design/AbyssalInterfaceContextSchema.json` as the context/response contract.
- Use `Content/Design/AbyssalInterfaceResponseModes.csv` for allowed response modes.
- Create a local backend endpoint prototype: `POST /abyssal-interface/respond`.
- Send compact context: map, zone, objective, inventory, discoveries, recent scans, recent actions, known lore facts.
- Display diegetic failure states when backend is unavailable.
- Add strict validation so LLM-suggested events cannot directly execute gameplay changes.
- Draft the Interface tone prompt: eerie, ancient, concise, lore-aware, useful but incomplete.
- Add a first terminal placement to the Collector Array or Ancient Gate route.

## P0 - Luminous Rift Game Development Work

### No Unreal Editor Required

- Create detailed Claude/Blender prompt files under `Docs/AssetPrompts/LuminousRift/` for:
  - `SM_Rift_CrystalCluster_S/M/L/Hero`
  - `SM_Rift_ForegroundLedge_A`
  - `SM_Rift_RockArch_A` and `SM_Rift_Overhang_A`
  - `SM_Rift_BridgeSpan_A/B_Broken`
  - `SM_Rift_HexCollector_Tile_A`
  - `SM_Rift_HexCollector_Cluster_A/B_Broken`
  - `SM_Rift_OrbFrame_A`, `SM_Rift_OrbHub_A`, `SM_Rift_BeamEmitterNode_A`
  - `SM_Rift_AncientWall_Gate_A`
- Extend `Docs/BLUEPRINT_IMPLEMENTATION_NOTES.md` after Windows-side testing with any actual Blueprint names, screenshots, and deviations from the planned setup.
- In Unreal, create `BP_AudioCueRouter` from the `UAbyssalAudioCueSubsystem` notes and bind temporary SoundCue/MetaSound assets to the emitted cue ids.
- Compile and PIE-test `UAbyssalHealthComponent`, then create `WBP_SurvivalHUD` and bind it to the component's health/damage/death delegates.
- Review `AEmberVentHazard` and plan how it becomes the base for future Mantle Garden pressure vents.
- Add automated CSV validation script or documentation for design CSV formats.

### Unreal Editor / Windows Side

- Generate project files and compile.
- Create input assets in `Content/Input/`.
- Create Blueprint children for player, discovery actor, objective trigger, beacon actor, scanner readout, journal, and objective HUD.
- Build `MAP_LuminousRift_Blockout` from `Docs/LUMINOUS_RIFT_BLOCKOUT.md`.
- Import or create P0 mesh proxies for the Luminous Rift kit.
- Create master materials and instances from `Docs/MATERIAL_SPECS.md`.
- Wire objective progression to the main arc:
  - `OBJ_VERIFY_HELIOS` during the prologue shaft descent.
  - `OBJ_SURVIVE` after the elevator crash and Luminous Rift reveal.
  - `OBJ_DISCOVER_PLACE` after initial stable traversal and first scans.
  - `OBJ_MAKE_MACHINE_ANSWER` when the player reaches the first Abyssal Interface or operable ancient system.
  - `OBJ_BUILD_WAY_OUT` after the first alien-tech fabrication path is understood.
  - `OBJ_OPEN_RIFT` for the eventual endgame return portal.

## P1 - World Atlas Planning Work

- Expand each map in `Docs/WORLD_ATLAS.md` into its own blockout document:
  - `Docs/Maps/GLASSROOT_FOREST.md`
  - `Docs/Maps/INNER_SEA.md`
  - `Docs/Maps/FOSSIL_SKY.md`
  - `Docs/Maps/GRAVITY_WELL.md`
  - `Docs/Maps/MANTLE_GARDEN.md`
- For each future map, create:
  - zone list
  - first-overlook composition
  - route beats
  - traversal mechanics
  - discoveries
  - hazards
  - asset manifest
  - material list
  - ambience direction
  - screenshot acceptance checklist
- Convert `Content/Design/WorldAssetManifest.csv` into per-map asset task prompts.
- Add map rows to a future `Content/Design/DiscoveryCatalog_World.csv`.
- Add world ambience rows to `Content/Design/DT_WorldAmbience.csv`.
- Create `Docs/WORLD_PROGRESSION.md` describing how mechanics unlock across maps.
- Create `Docs/PLAYER_EQUIPMENT_ROADMAP.md` covering scanner upgrades, beacons, climbing tools, heat protection, water traversal, tether/gravity equipment, and journal upgrades.
- Create `Docs/NARRATIVE_FOUNDATION.md` covering the explorer premise, field expedition tone, ancient system mystery, and how to reveal lore without exposition dumps.

## P1 - Generated Concept Image Follow-Ups

Images now live at:

- `Content/ArtDirection/WorldMaps/glassroot_forest_concept.png`
- `Content/ArtDirection/WorldMaps/inner_sea_concept.png`
- `Content/ArtDirection/WorldMaps/fossil_sky_concept.png`
- `Content/ArtDirection/WorldMaps/gravity_well_concept.png`
- `Content/ArtDirection/WorldMaps/mantle_garden_concept.png`

Follow-up tasks:

- Inspect each generated image and write a precise acceptance/revision note.
- Generate second-pass variants for any map whose concept is too generic.
- Create a contact-sheet image for README/wiki use.
- Add image prompt metadata to a durable doc so future generations are reproducible.
- Use the images to derive exact color palettes and material instances.
- Mark which visual elements are canonical and which are optional.

## P1 - Glassroot Forest Tasks

- Write `Docs/Maps/GLASSROOT_FOREST.md`.
- Create `Content/Design/GlassrootForestAssetManifest.csv`.
- Draft Claude/Blender prompts for root columns, root bridges, pearl terraces, red sap veins, spore pods, and shallow pool edges.
- Define `M_Glassroot_TranslucentRoot_Master`, `M_Glassroot_RedSap_Master`, and `M_Glassroot_PearlStone_Master`.
- Prototype scanner-delayed root response design.
- Design spore cloud behavior and how it affects scanner readability.

## P1 - Inner Sea Tasks

- Write `Docs/Maps/INNER_SEA.md`.
- Create `Content/Design/InnerSeaAssetManifest.csv`.
- Draft Claude/Blender prompts for basalt docks, broken piers, submerged ruins, ceiling shelves, distant islands, and floating buoys.
- Define `M_InnerSea_SilverBlackWater_Master` and `M_InnerSea_GoldPlankton_Master`.
- Design whether water traversal is walking-only, skiff-based, or staged for later.
- Prototype `BP_InnerSea_PlanktonTrailSpline` as a route-reading VFX actor.

## P2 - Fossil Sky Tasks

- Write `Docs/Maps/FOSSIL_SKY.md`.
- Create prompts for ceiling leviathan fossil, rib arches, bone walkways, amber dust shafts, and cyan fossil veins.
- Define fossil scanner reconstruction mechanics.
- Design brittle walkway hazard and falling fragment warnings.

## P2 - Gravity Well Tasks

- Write `Docs/Maps/GRAVITY_WELL.md`.
- Create prompts for floating platforms, curved stabilizer towers, anchor gates, crystal debris, and anomaly core.
- Design gravity reorientation volumes in C++/Blueprint.
- Define player tether behavior and route readability rules.
- Create a technical risk note before implementation because gravity changes can destabilize traversal.

## P2 - Mantle Garden Tasks

- Write `Docs/Maps/MANTLE_GARDEN.md`.
- Create prompts for obsidian ridges, steam vents, heat cracks, mineral flowers, and thermal machinery.
- Generalize `AEmberVentHazard` or derive `APressureVentHazard`.
- Define heat exposure, safe windows, and low-visibility steam.
- Create material specs for obsidian, heat bloom, white steam, and magenta mineral petals.

## Testing And Verification Targets

### Source/Docs

- CSV files parse cleanly.
- Markdown links resolve.
- Image files exist and render on GitHub.
- Objective IDs in docs match `UObjectiveSubsystem::BuildDefaultRoute`.
- Asset names are stable across atlas docs, manifests, and Blender prompts.

### Unreal PIE

- Player movement, sprint, crouch, scan, beacon placement/removal, and journal toggle.
- Route objectives fire in order.
- Main objective arc can advance from `OBJ_VERIFY_HELIOS` through `OBJ_OPEN_RIFT`.
- Save/load restores discoveries and beacons.
- Debug commands work:
  - `AbyssalDebugDiscoverAll`
  - `AbyssalDebugResetDiscoveries`
  - `AbyssalDebugAdvanceObjective`

### Screenshot Review

- Luminous Rift First Overlook matches the core reference.
- Each future map has a distinct color triad and first-overlook composition.
- Human scale is visible in every major vista.
- No map reads as a generic cave, generic sci-fi corridor, or flat arena.
