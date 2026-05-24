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
2. **World atlas**: define the broader Abyssal Earth map sequence using `Docs/WORLD_ATLAS.md` and the generated concept images in `Content/ArtDirection/WorldMaps/`.

Do not let worldbuilding distract from P0 implementation, but use the atlas to make asset, material, audio, and code decisions extensible.

## P0 - Luminous Rift Immediate Work

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
- Add `Content/Design/DT_LuminousRiftAmbience.csv` with ambience cue rows for each zone.
- Add `Content/Design/LuminousRiftBlockoutChecklist.csv` so Unreal placement work can be tracked outside markdown.
- Add `Docs/BLUEPRINT_IMPLEMENTATION_NOTES.md` with step-by-step instructions for:
  - `BP_RiftEnergyOrb`
  - `BP_RiftGoldBeamSpline`
  - `BP_HexCollectorCluster`
  - `WBP_ScannerReadout`
  - `WBP_AbyssalJournal`
  - objective HUD widget
- Sketch `UAbyssalAudioCueSubsystem` that listens to scanner/discovery/objective delegates and forwards to Blueprint events.
- Design `UAbyssalHealthComponent` with max/current HP, damage, death, and Blueprint delegates.
- Review `AEmberVentHazard` and plan how it becomes the base for future Mantle Garden pressure vents.
- Add automated CSV validation script or documentation for design CSV formats.

### Unreal Editor / Windows Side

- Generate project files and compile.
- Create input assets in `Content/Input/`.
- Create Blueprint children for player, discovery actor, objective trigger, beacon actor, scanner readout, journal, and objective HUD.
- Build `MAP_LuminousRift_Blockout` from `Docs/LUMINOUS_RIFT_BLOCKOUT.md`.
- Import or create P0 mesh proxies for the Luminous Rift kit.
- Create master materials and instances from `Docs/MATERIAL_SPECS.md`.
- Place objective triggers in the revised route:
  - `OBJ_DescentElevator`
  - `OBJ_FirstOverlook`
  - `OBJ_AbyssalApproach`
  - `OBJ_CrystalGalleries`
  - `OBJ_CollectorArray`
  - `OBJ_AncientGate`
  - `OBJ_SecondSkyOverlook`
- Set `D_Anomaly_SecondSkyCavern.ObjectiveIdToCompleteOnScan = OBJ_SecondSkyOverlook`.

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
- Final scan completes `OBJ_SecondSkyOverlook`.
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
