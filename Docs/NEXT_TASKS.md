# Next Tasks

The hourly continuation worker should always pick the highest-impact available task from this list, update files directly, and append a short entry to `Docs/HOURLY_LOG.md`.

## Immediate

- Create `WBP_ScannerReadout` as a Blueprint child of `UAbyssalScannerReadoutWidget`; implement the four Blueprint events for result text, pulse animation, discovery flash, and miss state.
- Add input action asset creation notes or editor utility script once Unreal is available.
- Expand `LUMINOUS_RIFT_BLOCKOUT.md` into a room-by-room object placement checklist.
- Create Blueprint beacon visuals and verify saved beacon restore in a PIE session.
- Add optional beacon removal/recolor controls after the first blockout route is playable.
- Create Blueprint HUD/objective readout using `UObjectiveSubsystem::OnObjectiveChanged`, `OnObjectiveCompleted`, `OnRouteCompleted`, `GetObjectiveProgress`, and `GetObjectiveHudText`.
- Place `AObjectiveTriggerActor` volumes through the first route once `MAP_LuminousRift_Blockout` exists.
- Set `D_Anomaly_SecondSkyCavern.ObjectiveIdToCompleteOnScan` to `OBJ_SecondSkyOverlook` in the final discovery Blueprint.

## After Unreal Editor Is Available

- Generate project files and compile.
- Create `WBP_ScannerReadout` from `UAbyssalScannerReadoutWidget`, add it to the player HUD, and verify it auto-binds to the owning pawn scanner.
- Create `M_LuminousCrystal`, `M_WetBasalt`, `M_ShallowMirrorWater`, and `M_BioFungus`.
- Build `MAP_LuminousRift_Blockout`.
- Create Blueprint children for player, discovery actors, beacons, and scanner VFX.
- Create Blueprint children for objective triggers and bind simple HUD/objective feedback.
- Take screenshots and iterate composition.
