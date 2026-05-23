# Next Tasks

The hourly continuation worker should always pick the highest-impact available task from this list, update files directly, and append a short entry to `Docs/HOURLY_LOG.md`.

## Current Priority

The project has pivoted the first map around the core concept image:

`Content/ArtDirection/References/luminous_rift_core_reference.png`

Hourly work should prioritize asset pipeline and map composition tasks that make the Unreal project match that image: vertical rift, central orb, hex collectors, gold beams, blue crystals, ancient gate wall, dark rock frame, and human scale.

## Immediate (No Unreal Editor Required)

- Create `ArtSource/Blender/LuminousRift/ASSET_NOTES.md` with initial entries for the P0 asset families in `BLENDER_ASSET_PIPELINE.md`.
- Draft individual Claude/Blender task prompts for:
  - `SM_Rift_CrystalCluster_S/M/L/Hero`
  - `SM_Rift_ForegroundLedge_A`
  - `SM_Rift_BridgeSpan_A/B_Broken`
  - `SM_Rift_HexCollector_Tile_A` and `SM_Rift_HexCollector_Cluster_A/B`
  - `SM_Rift_OrbFrame_A`, `SM_Rift_OrbHub_A`, and `SM_Rift_BeamEmitterNode_A`
  - `SM_Rift_AncientWall_Gate_A`
- Add a `Content/Design/LuminousRiftAssetManifest.csv` listing asset name, priority, dimensions, material slots, and status.
- Update `Content/Design/DiscoveryCatalog.csv` in any future C++/Blueprint pass if additional discovery metadata is needed beyond the new concept-art route.
- Sketch `BP_RiftEnergyOrb` and `BP_RiftGoldBeamSpline` Blueprint implementation notes in `TECHNICAL_PLAN.md`.
- Author a `DT_LuminousRiftAmbience.csv` placeholder using the new zones: Descent Elevator, First Overlook, Abyssal Approach, Crystal Galleries, Collector Array, Ancient Gate, Second Sky Overlook.
- Sketch `UAbyssalAudioCueSubsystem` that subscribes to scanner/discovery/objective delegates and forwards to a Blueprint-implementable event.
- Decide on a health/HP component shape before reintroducing hazards.

## Claude/Blender Asset Work Order

Use `Docs/BLENDER_ASSET_PIPELINE.md` as the worker contract.

1. Blue crystal clusters: fastest path to visual improvement and route language.
2. Foreground ledge + rock arch/overhang: needed for the first concept-art screenshot.
3. Bridge/platform kit: needed for playable traversal.
4. Hex collector tile and cluster system: essential concept identity.
5. Orb frame, hub, and beam emitter nodes: central focal point.
6. Ancient gate wall: right-side monumental structure.
7. Distant towers, hanging slabs, and spires: scale/depth pass.
8. Human survey kit: scale cues and start-area dressing.

## Blocked On Unreal Editor

- Generate project files and compile to confirm the new crouch wiring, mesh-attached camera, beacon remove/recolor, ember vent hazard, journal widget, and `IA_Journal` toggle all build.
- Create input assets in `Content/Input/` per `TECHNICAL_PLAN.md > Input Asset Creation Checklist`.
- Build `MAP_LuminousRift_Blockout` using the revised concept-art route in `LUMINOUS_RIFT_BLOCKOUT.md`.
- Create `BP_RiftEnergyOrb`: central orb mesh, emissive material, point lights, Niagara motes, and beam anchor points.
- Create `BP_RiftGoldBeamSpline`: spline-based gold beam with endpoint glow and fog readability.
- Create `BP_HexCollectorCluster` if static imported clusters need Blueprint lights or beam sockets.
- Create `WBP_ScannerReadout` as a Blueprint child of `UAbyssalScannerReadoutWidget`.
- Create `WBP_AbyssalJournal` as a Blueprint child of `UAbyssalJournalWidget`.
- Create Blueprint children for player, discovery actors, beacons, scanner VFX, and objective triggers.
- Set `D_Anomaly_SecondSkyCavern.ObjectiveIdToCompleteOnScan` to `OBJ_SecondSkyOverlook` in the final discovery Blueprint.
- Create Blueprint HUD/objective readout using `UObjectiveSubsystem::OnObjectiveChanged`, `OnObjectiveCompleted`, `OnRouteCompleted`, `GetObjectiveProgress`, and `GetObjectiveHudText`.
- Create master materials and instances from `MATERIAL_SPECS.md`, especially `M_Rift_EnergyOrb_Master`, `M_Rift_GoldEnergy_Master`, `M_Rift_CollectorGlass_Master`, `M_Rift_AncientMachine_Master`, `M_Rift_WetBasalt_Master`, and `M_Rift_BlueCrystal_Master`.

## PIE Test Targets

- Verify player movement, sprint, crouch, scan, beacon placement/removal, and journal toggle.
- Console `AbyssalDebugDiscoverAll`, open journal, confirm entries render with display name + journal text + category.
- Place a beacon, save, reload, confirm restoration.
- Aim at a beacon and press the beacon key, confirm it removes.
- Reach each revised objective trigger in order.
- Scan `D_Anomaly_SecondSkyCavern`, confirm `OBJ_SecondSkyOverlook` completes the route.

## Screenshot Targets

Take and compare screenshots against the concept reference from:

- First Overlook: must match core composition.
- Abyssal Approach: orb partly occluded, deep abyss visible.
- Crystal Galleries: close crystal detail with distant machine framing.
- Collector Array: orb, hex panels, gold beams dominant.
- Ancient Gate: huge wall, circular blue cores, tiny player scale.
- Second Sky Overlook: lower rift reveal.
