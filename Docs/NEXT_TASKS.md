# Next Tasks

The hourly continuation worker should always pick the highest-impact available task from this list, update files directly, and append a short entry to `Docs/HOURLY_LOG.md`.

## Immediate (Code or Docs, No Editor Required)

- Author a `DT_LuminousRiftAmbience.csv` placeholder (audio cue ids per zone) so the M2 audio pass has a starting point.
- Sketch a `UAbyssalAudioCueSubsystem` that subscribes to scanner/discovery/objective delegates and forwards to a single Blueprint-implementable event, keeping audio logic out of gameplay code.
- Decide on a health/HP component shape (subclass `UActorComponent`, integer + max, OnDamaged/OnDeath delegates) before placing vents in the blockout.

## Blocked on Unreal Editor

- Generate project files and compile to confirm the new crouch wiring, mesh-attached camera, beacon remove/recolor, ember vent hazard, journal widget, and `IA_Journal` toggle all build.
- Create `WBP_ScannerReadout` as a Blueprint child of `UAbyssalScannerReadoutWidget`; implement the four Blueprint events for result text, pulse animation, discovery flash, and miss state. Add it to the player HUD and verify it auto-binds.
- Create `WBP_AbyssalJournal` as a Blueprint child of `UAbyssalJournalWidget`; build a category-tabbed list, wire `BP_OnNewDiscoveryAdded` to a toast notification, and wire `BP_OnJournalOpened`/`Closed` to slide-in/out animations.
- Create `BP_EmberVentHazard` as a Blueprint child of `AEmberVentHazard`: attach a `SM_Blockout_VentCone` mesh, drive `VentLight` intensity + a Niagara steam system from the four `OnVent*` events.
- Create `M_LuminousCrystal`, `M_WetBasalt`, `M_ShallowMirrorWater`, `M_BioFungus`, `M_EmberVent`, and `M_Beacon` master materials per `MATERIAL_SPECS.md`.
- Build `MAP_LuminousRift_Blockout` using the room-by-room checklist in `LUMINOUS_RIFT_BLOCKOUT.md`.
- Create the input assets in `Content/Input/` per `TECHNICAL_PLAN.md > Input Asset Creation Checklist`, including the new `IA_Crouch` and `IA_Journal` slots.
- Create Blueprint children for player (`BP_AbyssalExplorerCharacter`), discovery actors, beacons, scanner VFX, and objective triggers.
- Set `D_Anomaly_SecondSkyCavern.ObjectiveIdToCompleteOnScan` to `OBJ_SecondSkyOverlook` in the final discovery Blueprint.
- Create Blueprint HUD/objective readout using `UObjectiveSubsystem::OnObjectiveChanged`, `OnObjectiveCompleted`, `OnRouteCompleted`, `GetObjectiveProgress`, and `GetObjectiveHudText`.
- PIE test: place a beacon, save, reload, confirm restoration; aim at a beacon and press the beacon key, confirm it removes; call `SetBeaconLightColor` from a debug widget to verify recolor persists.
- PIE test journal end-to-end: console `AbyssalDebugDiscoverAll`, open the journal, confirm all entries render with display name + journal text + category; then `AbyssalDebugResetDiscoveries` and confirm the journal empties.
- PIE test Ember Vent cycle: place 3-4 `BP_EmberVentHazard` instances in a cluster with default offsets, confirm phases desync naturally and `OnVentErupting` fires the visual; step into the radius during erupt and confirm damage event reaches the pawn (via debug log hook above).
- Take screenshots from each zone in `LUMINOUS_RIFT_BLOCKOUT.md` to iterate composition.
