# Blueprint Implementation Notes

> **Historical document.** Mentions of `BP_AbyssalExplorerCharacter` /
> `AAbyssalExplorerCharacter` refer to the deleted legacy pawn; the current
> pawn is `AAbyssalPlayerCharacter` (`BP_PlayerCharacter`). Canonical
> step-by-step editor instructions live in `Docs/EditorGuides/`.

These notes are for the Windows/Unreal Editor pass. They convert the current C++ and design docs into concrete Blueprint assets for the Luminous Rift vertical slice.

Read alongside:

- `Docs/CORE_REFERENCE_LUMINOUS_RIFT.md`
- `Docs/LUMINOUS_RIFT_BLOCKOUT.md`
- `Docs/MATERIAL_SPECS.md`
- `Content/Design/LuminousRiftBlockoutChecklist.csv`

## Global Setup

Recommended folders:

- `Content/Blueprints/LuminousRift/`
- `Content/Blueprints/UI/`
- `Content/Blueprints/Discovery/`
- `Content/Blueprints/Objectives/`
- `Content/Materials/LuminousRift/`
- `Content/VFX/LuminousRift/`

Create Blueprint children or widgets:

| Asset | Parent | Purpose |
|---|---|---|
| `BP_RiftEnergyOrb` | `Actor` | Central orb mesh, lights, pulse, motes, and beam anchors. |
| `BP_RiftGoldBeamSpline` | `Actor` | Gold spline beam between orb/hub/emitter/collector points. |
| `BP_HexCollectorCluster` | `Actor` | Places one collector cluster mesh plus beam target sockets/lights. |
| `BP_DiscoveryActor` | `ADiscoveryActor` | Generic placeable discovery marker with scan feedback. |
| `BP_ObjectiveTrigger` | `AObjectiveTriggerActor` | Route objective trigger volumes. |
| `WBP_ScannerReadout` | `UAbyssalScannerReadoutWidget` | Scan result HUD feedback. |
| `WBP_AbyssalJournal` | `UAbyssalJournalWidget` | Discovery journal shell. |
| `WBP_ObjectiveHUD` | `UserWidget` | Current objective and progress display. |
| `WBP_SurvivalHUD` | `UserWidget` | Health bar/vignette/debug readout bound to `UAbyssalHealthComponent`. |
| `WBP_DiscoveryToast` | `UserWidget` | Short new-discovery popup used by scanner/journal HUD. |

The current C++ exposes the subsystem accessors through `UAbyssalGameplayLibrary`:

- `GetDiscoverySubsystem(WorldContextObject)`
- `GetObjectiveSubsystem(WorldContextObject)`
- `GetBeaconSubsystem(WorldContextObject)`
- `GetAudioCueSubsystem(WorldContextObject)`

Use those from widgets rather than manually walking through Game Instance nodes each time.

## WBP_SurvivalHUD

Goal: make damage from hazards visible during the first playable route without locking in a final survival UI style.

Data source:

- `BP_AbyssalExplorerCharacter.GetHealthComponent()`
- `UAbyssalHealthComponent.OnHealthChanged`
- `UAbyssalHealthComponent.OnDamaged`
- `UAbyssalHealthComponent.OnDeath`

Suggested widget:

- A thin health bar in the lower-left or lower-center HUD.
- Optional red/blue damage vignette flash when `OnDamaged` fires.
- Optional compact debug text: `CurrentHealth / MaxHealth` while tuning hazards.

Blueprint setup:

1. On Construct, get owning player pawn and cast to `BP_AbyssalExplorerCharacter`.
2. Call `GetHealthComponent`; if valid, read `GetHealthPercent` for initial bar state.
3. Bind `OnHealthChanged` to update the bar percent and optional text.
4. Bind `OnDamaged` to play a short damage feedback animation.
5. Bind `OnDeath` to trigger the temporary fail-state animation or fade.

PIE checks:

- Run near `BP_EmberVentHazard` while it erupts and confirm HP drops by radial damage.
- Confirm the health bar updates once per damage tick and does not continue after death unless `bCanTakeDamageWhenDead` is enabled.
- Confirm `BP_AbyssalExplorerCharacter.BP_OnTookDamage` still fires if any existing Blueprint feedback is wired there.

## BP_RiftEnergyOrb

Goal: make the central orb the dominant focal point from First Overlook and Collector Array without blowing out into a flat white disk.

Blueprint class:

- Parent: `Actor`
- Location target from blockout: around `(11200, 0, -600)`
- Approximate orb diameter: 1800-2800 cm

Components:

- `SceneRoot`
- `OrbShell_Outer`: sphere static mesh, scale to target diameter, material `MI_Rift_EnergyOrb_Primary`
- `OrbShell_Inner`: smaller sphere, brighter core material instance if available
- `PointLight_Core`: cool blue-white, large attenuation radius
- `PointLight_AbyssFill`: dimmer cyan fill aimed downward/around lower rift
- `Niagara_Motes`: optional slow blue motes around orb
- `BeamAnchor_Root`: scene component at orb center
- `BeamAnchor_North`, `BeamAnchor_South`, `BeamAnchor_East`, `BeamAnchor_West`: scene components 1200-1800 cm from center for beam starts

Suggested exposed variables:

- `OrbDiameterCm` default `2400`
- `PulseSpeed` default `0.08`
- `CoreLightIntensity` default `120000`, tune in level
- `CoreLightRadius` default `9000`
- `bEnableMotes` default `true`
- `BeamAnchorRadiusCm` default `1600`

Construction Script:

1. Set orb mesh scale from `OrbDiameterCm`.
2. Position beam anchors on a rough radial ring around the orb, not perfectly flat if possible.
3. Set light attenuation radius from `CoreLightRadius`.

Event Graph:

1. On `BeginPlay`, create a Dynamic Material Instance for each orb shell.
2. On Tick or Timeline, drive the material `PulseSpeed`/`PulseContrast` parameters slowly.
3. Keep pulse subtle: the orb should feel massive and stable, not like an alarm.

Placement notes:

- It should remain visible from Zone 2 First Overlook, Zone 5 Collector Array, and Zone 6 Ancient Gate.
- Add fog and exposure tuning in the level after placement. If the orb loses texture detail, reduce bloom/light intensity before darkening the material.
- The orb actor should not block traversal in the first pass.

PIE checks:

- From the first overlook, the orb is the brightest object.
- The orb still shows internal/noise detail while blooming.
- Blue light reaches nearby bridge and collector silhouettes.

## BP_RiftGoldBeamSpline

Goal: create the warm gold beam network that connects the orb apparatus to hex collector panels. This is required for concept-art accuracy.

Blueprint class:

- Parent: `Actor`

Components:

- `SceneRoot`
- `Spline_BeamPath`
- Optional `PointLight_Start`
- Optional `PointLight_End`

Recommended implementation:

1. Add a spline with two or more points.
2. In Construction Script, rebuild spline mesh segments between points.
3. Use a thin cylinder or beam mesh as the spline mesh source.
4. Assign `MI_Rift_GoldBeam_Primary` or a material instance from `M_Rift_GoldEnergy_Master`.
5. Add small warm point lights only at important endpoints.

Suggested exposed variables:

- `BeamRadiusCm` default `10` to `18`
- `BeamIntensity` default `8` for material parameter
- `EndpointLightIntensity` default `2500`
- `EndpointLightRadius` default `900`
- `bEnableEndpointLights` default `true`
- `bUseBrokenSegment` default `false`

Visual rules:

- Beam color should stay gold/amber, not orange-red.
- Beam lines should be thin and precise; do not turn them into fat glowing tubes.
- Use several angled splines, not a perfect symmetric star, so the system feels ancient and damaged.

Placement notes:

- Connect orb anchors to `BP_HexCollectorCluster` anchors.
- Add at least three readable beams before screenshot review: one left/up, one right/up, and one down or across the bridge route.
- Let fog catch the beams, but keep beam geometry readable without relying entirely on bloom.

PIE checks:

- Gold beams are visible from First Overlook.
- Beam endpoints line up with collector panels or emitter nodes.
- The beams add warm contrast against the cyan orb/crystals.

## BP_HexCollectorCluster

Goal: make the flower-like hex collectors from the reference easy to place, rotate, break, and connect to beam splines.

Blueprint class:

- Parent: `Actor`

Components:

- `SceneRoot`
- `ClusterMesh`: `SM_Rift_HexCollector_Cluster_A` or broken variant when imported
- `BeamTarget_Center`: scene component for beam connection
- `PanelLight_Center`: optional small warm/cool light at the receiver node
- `DiscoveryMarker`: optional child actor using `BP_DiscoveryActor` for the first scannable collector

Suggested exposed variables:

- `ClusterMeshAsset`
- `bBrokenVariant`
- `PanelGlowStrength`
- `EndpointLightIntensity` default `1500`
- `DiscoveryId` default empty unless this specific cluster is scannable

Construction Script:

1. Assign `ClusterMeshAsset` to `ClusterMesh`.
2. If `bBrokenVariant` is true, prefer `SM_Rift_HexCollector_Cluster_B_Broken` once available.
3. Offset `BeamTarget_Center` slightly forward from the panel face so beam splines do not z-fight.

Recommended first placements:

- `Collector_LeftHigh`: high-left of orb, tilted slightly toward player.
- `Collector_RightHigh`: near the ancient gate side, partially broken.
- `Collector_LowerRoute`: lower or nearer to bridge path as a scannable route landmark.

Discovery setup for one cluster:

- Actor class: `BP_DiscoveryActor`
- `DiscoveryId`: `DIS_LUM_RIFT_COLLECTOR_ARRAY`
- `DisplayName`: `Collector Array`
- `Category`: `Anomaly`
- `ObjectiveIdToCompleteOnScan`: `OBJ_DISCOVER_PLACE` if this is the intended first major post-survival scan
- `ScanFocusOffset`: set so scanner traces toward the visible panel center

PIE checks:

- At least one collector cluster clearly reads as hexagonal from the overlook.
- Broken variants look damaged, not simply hidden.
- One scannable collector can complete its linked objective when intended.

## WBP_ScannerReadout

Goal: provide immediate scan feedback without blocking the screen or explaining controls in-world.

Parent class:

- `UAbyssalScannerReadoutWidget`

Binding:

1. On owning player pawn begin play or widget construct, cast to `AAbyssalExplorerCharacter`.
2. Call `GetScannerComponent()`.
3. Pass that component into `SetScannerComponent`.

Use Blueprint events already exposed by C++:

- `Scanner Result Changed`
- `Scanner Pulse Started`
- `Scanner Discovery Found`
- `Scanner Missed`

Suggested UI elements:

- Compact reticle-adjacent text for current scan result.
- Small category chip using `EDiscoveryCategory`.
- Distance text in meters.
- Brief pulse ring or line animation on scan start.
- Different color/animation for new discovery vs repeated scan.

Display text logic:

- If `bHasDiscovery == false`: short miss state, then fade.
- If `bNewDiscovery == true`: show display name, category, and `NEW DISCOVERY`.
- If already discovered: show display name and category in a quieter state.
- Use `GetCurrentReadoutText()` for a simple fallback.

PIE checks:

- Press scan with no target: miss state appears and fades.
- Scan a `BP_DiscoveryActor`: readout shows name/category/distance.
- Re-scan same actor: repeated state is quieter than first discovery.

## WBP_AbyssalJournal

Goal: give the player a durable record of discoveries using the existing `UDiscoverySubsystem` data.

Parent class:

- `UAbyssalJournalWidget`

Relevant C++ functions/events:

- `SetJournalOpen(bool)`
- `ToggleJournalOpen()`
- `GetAllEntries()`
- `GetEntriesByCategory(Category)`
- `GetEntryCount()`
- `Journal Opened`
- `Journal Closed`
- `New Discovery Added`
- `Entries Refreshed`

Recommended UI structure:

- Left column: category filters.
- Main list: discovered entry names.
- Detail panel: selected entry name, category, journal text.
- Empty state: keep it short and diegetic, no tutorial copy.

Category filters:

- Geology
- Biology
- Anomaly
- HumanMade

Implementation flow:

1. On `Entries Refreshed`, rebuild the entry list from `GetAllEntries()` or the active category filter.
2. On `New Discovery Added`, update list and optionally select the new entry if the journal is open.
3. `Journal Opened` should make the widget visible/focusable and pause look input only if the player controller setup supports it cleanly.
4. `Journal Closed` should return focus to gameplay.

Player binding:

- `AAbyssalExplorerCharacter::BP_ToggleJournal` is called from the `IA_Journal` input action.
- In the player Blueprint child, implement `BP_ToggleJournal` to create the widget once, add it to viewport, and call `ToggleJournalOpen()`.

Debug testing:

- In PIE console, run `AbyssalDebugDiscoverAll`.
- Open the journal and verify all placed discovery actors populate the list.
- Run `AbyssalDebugResetDiscoveries` and verify the list empties after refresh.

PIE checks:

- Journal toggles from input.
- New discoveries appear without restarting PIE.
- Category filters do not lose entries.

## WBP_ObjectiveHUD

Goal: keep the current objective readable during the 10-15 minute route and expose progression changes from `UObjectiveSubsystem`.

Parent class:

- `UserWidget`

Binding:

1. On construct, call `GetObjectiveSubsystem(WorldContextObject)` from `UAbyssalGameplayLibrary`.
2. Bind to:
   - `OnObjectiveChanged`
   - `OnObjectiveCompleted`
   - `OnRouteCompleted`
3. On construct and after each event, call:
   - `GetCurrentObjective()`
   - `GetObjectiveProgress()`
   - `GetObjectiveHudText()`

Suggested UI elements:

- Current objective title.
- One-line description.
- Progress text from `FAbyssalObjectiveProgress.ProgressText`.
- Subtle completion flash when `OnObjectiveCompleted` fires.

Current default route:

1. `OBJ_VERIFY_HELIOS`
2. `OBJ_SURVIVE`
3. `OBJ_DISCOVER_PLACE`
4. `OBJ_MAKE_MACHINE_ANSWER`
5. `OBJ_BUILD_WAY_OUT`
6. `OBJ_OPEN_RIFT`

For the immediate Luminous Rift slice:

- It is acceptable for later objectives to remain placeholder text.
- Make `OBJ_SURVIVE` and `OBJ_DISCOVER_PLACE` testable first.
- Objective trigger volumes and scannable discoveries should complete objectives, not the HUD widget itself.

Debug testing:

- In PIE console, run `AbyssalDebugAdvanceObjective` repeatedly.
- Verify title, description, and progress text update each time.

PIE checks:

- HUD initializes with a current objective.
- Completing a trigger or debug command updates the HUD immediately.
- Route completion produces a distinct quiet state rather than stale objective text.

## BP_AudioCueRouter

Goal: keep first-pass audio implementation data-driven and Blueprint-owned while C++ forwards gameplay events into one central place.

Recommended Blueprint:

- Class: `Actor` placed once in the active map, or a widget/HUD-owned object if preferred.
- On Begin Play, call `GetAudioCueSubsystem(WorldContextObject)` from `UAbyssalGameplayLibrary`.
- Bind to `OnAudioCueRequested`.
- Switch on `FAbyssalAudioCueEvent.CueId` and play temporary SoundCues, MetaSounds, or Niagara/audio feedback.

Events currently emitted by C++:

| CueId | Source | First-pass use |
|---|---|---|
| `SFX_Scanner_Pulse` | player scanner | short scanner ping. |
| `SFX_Scanner_Found_New` | player scanner | brighter scan success plus discovery toast accent. |
| `SFX_Scanner_Found_Known` | player scanner | quieter repeat-scan confirmation. |
| `SFX_Scanner_Miss` | player scanner | soft failed scan tick. |
| `SFX_Discovery_New` | discovery subsystem | journal/discovery stinger. |
| `SFX_Objective_New` | objective subsystem | new objective accent. |
| `SFX_Objective_Complete` | objective subsystem | completion accent. |
| `MX_Route_Complete` | objective subsystem | route-complete music/stinger hook. |

Ambience data:

- Use `Content/Design/DT_LuminousRiftAmbience.csv` as the first map ambience table.
- Create one ambience trigger or zone manager per route zone.
- On zone enter, call `RequestAmbienceCue(CueId, Location, Intensity)` on `UAbyssalAudioCueSubsystem`, then let `BP_AudioCueRouter` fade loops according to the CSV row.
- The CSV uses placeholder cue asset names for now; replace them with real SoundCue/MetaSound asset paths after audio assets exist.

PIE checks:

- Scanner pulse/found/miss produce distinct temporary sounds.
- `AbyssalDebugDiscoverAll` fires discovery cue requests.
- `AbyssalDebugAdvanceObjective` fires objective cue requests.
- Moving between hand-placed ambience triggers requests the expected `AMB_LR_*` cue ids.

## Discovery And Objective Placement Rules

Use `Content/Design/LuminousRiftBlockoutChecklist.csv` as the placement tracker.

Recommended first scannables:

| Actor label | DiscoveryId | Category | Objective link |
|---|---|---|---|
| `D_FirstOverlook_RiftVista` | `DIS_LUM_RIFT_FIRST_OVERLOOK` | `Anomaly` | optional `OBJ_SURVIVE` completion after reveal |
| `D_CrystalGallery_BlueCrystals` | `DIS_LUM_RIFT_CRYSTAL_GALLERY` | `Geology` | none |
| `D_CollectorArray_Core` | `DIS_LUM_RIFT_COLLECTOR_ARRAY` | `Anomaly` | `OBJ_DISCOVER_PLACE` |
| `D_AncientGate_Base` | `DIS_LUM_RIFT_ANCIENT_GATE` | `Anomaly` | later route objective if needed |

Keep `ScanFocusOffset` pointed toward visible geometry, not buried actor origins.

## First Editor Session Order

1. Create `WBP_ObjectiveHUD`, add it to the player HUD flow, and verify `AbyssalDebugAdvanceObjective`.
2. Create `WBP_ScannerReadout`, bind it to the player scanner, and verify scan miss/found feedback.
3. Create `WBP_AbyssalJournal`, bind `BP_ToggleJournal`, and verify `AbyssalDebugDiscoverAll`.
4. Create `BP_RiftEnergyOrb` and place it at the Collector Array.
5. Create `BP_RiftGoldBeamSpline` and connect at least three beams to provisional targets.
6. Create `BP_HexCollectorCluster` and place three collector clusters around the orb.
7. Add `BP_AudioCueRouter`, bind it to `UAbyssalAudioCueSubsystem`, and test scanner/discovery/objective cue requests with temporary sounds.
8. Add or update checklist statuses in `Content/Design/LuminousRiftBlockoutChecklist.csv`.

## Screenshot Acceptance For This Pass

Before calling the pass good, capture or inspect from First Overlook:

- The orb is the dominant focal point.
- At least three gold beams connect toward collector panels.
- One or more hex collector clusters are readable.
- Blue crystals remain secondary accents.
- The right-side gate area still has room for `SM_Rift_AncientWall_Gate_A`.
- HUD elements do not cover the orb or the player route.
