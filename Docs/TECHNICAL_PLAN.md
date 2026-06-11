# Technical Plan

> **Historical document.** References to `AAbyssalExplorerCharacter`,
> `UScannerComponent`, `UInteractionComponent`, and `AAbyssalEarthGameMode`
> describe the legacy pawn stack, which has been **deleted**. The current
> stack is `AAbyssalGameMode` → `AAbyssalPlayerCharacter` (with
> `UAbyssalScanComponent` / `UAbyssalInteractionComponent`) and
> `AAbyssalPlayerController`. For in-editor work use `Docs/EditorGuides/`.

## Current Constraint

Unreal Editor is not installed or not discoverable from PATH on this machine. Work should remain UE-ready so the project can be opened and compiled once the engine is available.

## Gameplay Foundation

- `AAbyssalExplorerCharacter`: first-person pawn for exploration.
- `UScannerComponent`: finds nearby discovery actors and triggers scan feedback.
- `UAbyssalScannerReadoutWidget`: UMG base class that auto-binds to the owning pawn scanner and exposes Blueprint events for scan UI feedback.
- `UAbyssalJournalWidget`: UMG base class for the journal HUD; auto-binds to `UDiscoverySubsystem`, exposes per-category entry queries, and broadcasts a Blueprint event when a new discovery lands.
- `ADiscoveryActor`: placeable scan target with journal metadata.
- `ABeaconActor`: placeable navigation marker foundation.
- `AEmberVentHazard`: placeable cyclical hazard with Idle/Warning/Erupting/Cooldown phases, configurable radial damage during erupt, and Blueprint hooks per phase.
- `UAbyssalHealthComponent`: reusable actor component for max/current HP, damage, healing, death state, and Blueprint HUD/death delegates.
- `UDiscoverySubsystem`: stores discovered entries (id, display name, journal text, category) keyed by id, with an `OnDiscoveryAdded` delegate for journal/HUD toasts.
- `UDiscoverySaveGame`: persists discovery entries and saved beacons.
- `AAbyssalEarthGameMode`: assigns the explorer pawn.

## Next C++ Additions

- Add a small survival HUD base if Windows-side Blueprint binding to `UAbyssalHealthComponent` needs common helper text/progress functions.
- Optional: dedicated `IA_RemoveBeacon` input if the smart-context place/remove behavior is unclear in playtest.

## Gameplay Library

`UAbyssalGameplayLibrary` (`UBlueprintFunctionLibrary`) exposes one-call accessors for the three game-instance subsystems from any Blueprint with a world context:

- `GetDiscoverySubsystem(WorldContextObject)`
- `GetObjectiveSubsystem(WorldContextObject)`
- `GetBeaconSubsystem(WorldContextObject)`

All return `nullptr` when the world context is invalid or the subsystem hasn't initialized yet, so Blueprints can safely chain a null check before reading.

## Health & Damage

`AAbyssalExplorerCharacter` owns a `UAbyssalHealthComponent` named `HealthComponent` and exposes it through `GetHealthComponent()`.

`UAbyssalHealthComponent` binds to its owner's `OnTakeAnyDamage` in `BeginPlay`, logs damage at `Verbose`, subtracts HP, and broadcasts:

- `OnHealthChanged(CurrentHealth, MaxHealth, Delta)`: use for bars, vignette intensity, and survival HUD values.
- `OnDamaged(DamageAmount, DamageCauser, CurrentHealth)`: use for hit feedback, audio, and camera/UI response.
- `OnDeath(KilledActor, DamageCauser)`: use for fade-out, respawn, or fail-state prototypes.

The component also exposes `ApplyHealthDamage`, `Heal`, `RestoreFullHealth`, `Kill`, `GetCurrentHealth`, `GetMaxHealth`, `GetHealthPercent`, and `IsDead` for Blueprint. The character still forwards component damage through the existing `BP_OnTookDamage(Damage, DamageCauser)` event so any current Blueprint feedback hook remains usable.

In the first PIE test, place `BP_EmberVentHazard` near the player, shorten its cycle, and confirm radial damage reduces `HealthComponent` HP while `OnDamaged` and `OnHealthChanged` fire. Death currently only broadcasts; final respawn/fail behavior is intentionally left to the vertical-slice flow.

## Beacon Controls

- `ABeaconActor::SetBeaconLightColor(FLinearColor)`: callable from Blueprint at runtime; updates the point light and re-registers with `UBeaconSubsystem` so the change persists across saves.
- `UBeaconSubsystem::RemoveBeacon(ABeaconActor*)`: destroys the actor and strips it from the save list.
- `UBeaconSubsystem::RemoveBeaconById(WorldContext, FGuid)`: removes by ID; also cleans orphan save entries when no in-world actor matches.
- `AAbyssalExplorerCharacter::PlaceBeacon` is now smart-context: a beacon button press whose line trace hits an existing `ABeaconActor` removes it; otherwise it places a new one.

## Discovery & Journal

- `FAbyssalDiscoveryEntry` (in `DiscoverySaveGame.h`) holds id, display name, journal text, and category, and is the unit stored and saved by `UDiscoverySubsystem`.
- `UDiscoverySubsystem::RegisterDiscoveryEntry` is the canonical scan path. `RegisterDiscovery(FName)` still exists as an id-only shortcut that fabricates a minimal entry.
- `UDiscoverySubsystem::OnDiscoveryAdded` (multicast) is broadcast exactly once when an entry first appears — perfect for toast UI without polling.
- `UDiscoverySubsystem` exposes `GetDiscoveredEntries`, `GetDiscoveredEntriesByCategory`, `GetDiscoveryEntry(Id, OutEntry)`, and `GetDiscoveredCount` for journal queries.
- `UAbyssalJournalWidget` (UMG base) auto-binds to the subsystem in `NativeConstruct`, exposes `SetJournalOpen`/`ToggleJournalOpen`/`IsJournalOpen`, and forwards `BP_OnJournalOpened`, `BP_OnJournalClosed`, `BP_OnNewDiscoveryAdded`, and `BP_OnEntriesRefreshed` to its Blueprint child.
- `AAbyssalExplorerCharacter::BP_ToggleJournal` is fired by the `IA_Journal` press and is the hook the Blueprint child uses to show/hide the journal widget.

## Ember Vent Hazard

- `AEmberVentHazard` runs a four-phase cycle (Idle -> Warning -> Erupting -> Cooldown -> Idle) driven by a single `FTimerHandle`. Phase durations are independently editable.
- `bRandomizeInitialPhaseOffset` (default true) randomizes the starting phase so a cluster of vents desyncs naturally without per-instance tweaking. Disable it to drive deterministic cycles via `InitialPhaseOffset` in `[0,1]`.
- During the Erupting phase the actor applies `DamagePerSecond * DamageTickInterval` of `EruptDamageType` damage via `UGameplayStatics::ApplyRadialDamage` on a looping timer (`DamageTickInterval`, default 0.25s). Set `EruptDamageType` once a project damage type asset exists; falls back to `UDamageType::StaticClass()` otherwise.
- Blueprint events `OnVentIdle`, `OnVentWarning`, `OnVentErupting`, `OnVentCooldown`, plus the `OnVentPhaseChanged` multicast, cover both per-phase reactions and generic listeners.
- `SetVentActive(false)` pauses the cycle (and clears damage timers); `SetVentActive(true)` resumes with a recomputed initial offset.

## Debug Commands

Available only in non-shipping builds. Type into the in-game console while a `BP_AbyssalExplorerCharacter` is possessed:

- `AbyssalDebugDiscoverAll`: registers every `ADiscoveryActor` in the current world.
- `AbyssalDebugResetDiscoveries`: clears the discovery save and resets the objective route.
- `AbyssalDebugAdvanceObjective`: completes the current objective (skips ahead one step).

## Scanner Implementation Notes

- `UScannerComponent` scans from the owning actor's eye viewpoint so first-person aiming matches player expectation.
- Discovery candidates can require visibility-channel line of sight before they are scored.
- Blueprint feedback hooks are available for pulse start, target found, and miss states.
- Scanner readouts can bind to `OnScanResultChanged` and consume `FAbyssalScanResult` for discovery name, category, distance, and new-vs-repeat state without duplicating scan scoring in UI Blueprints.
- `UAbyssalScannerReadoutWidget` handles the C++ delegate binding for `WBP_ScannerReadout`, caches the latest result, and provides `GetCurrentReadoutText` for a compact first-pass HUD label.
- `ADiscoveryActor::ScanFocusOffset` lets Blueprint children aim traces at the visible center of tall fungi, crystals, vents, or station props.

## Blueprint Plan

- `BP_AbyssalExplorerCharacter`: assign the skeletal mesh first (required — Blueprint editor crashes without it). Then assign input actions and tune camera. `FirstPersonCamera` currently attaches to the capsule root component; once a mesh with a `head` socket is assigned, re-parent the camera to that socket for animation-driven head bob and crouch dip.
- `BP_DiscoveryActor_Base`: mesh, outline, scan pulse response, scan focus offsets.
- `BP_BeaconActor`: mesh, light, color variants.
- `BP_LuminousRift_GameMode`: vertical slice rules.
- `WBP_ScannerReadout`: Blueprint child of `UAbyssalScannerReadoutWidget`; animate pulse, found, repeat, and miss states from the inherited events.
- `WBP_DiscoveryJournal`: milestone 3 journal shell.

## Input Actions

- `IA_Move`: Vector2D WASD/left stick.
- `IA_Look`: Vector2D mouse/right stick.
- `IA_Sprint`: Shift/gamepad left stick press.
- `IA_Crouch`: Ctrl/gamepad B.
- `IA_Scan`: Right mouse/gamepad left trigger.
- `IA_PlaceBeacon`: B/gamepad Y.
- `IA_Journal`: J/gamepad menu.

## Input Asset Creation Checklist (Editor)

Once Unreal Editor is available, create these assets under `Content/Input/`. Names below match the `UPROPERTY` slots on `BP_AbyssalExplorerCharacter` (derived from `AAbyssalExplorerCharacter`) so the references will auto-resolve when assigned.

### Input Actions (`Content/Input/Actions/`)

| Asset | Value Type | Triggers |
|---|---|---|
| `IA_Move` | Axis2D (Vector2D) | Default |
| `IA_Look` | Axis2D (Vector2D) | Default |
| `IA_Sprint` | Digital (bool) | Pressed/Released — C++ uses `Started` and `Completed` |
| `IA_Crouch` | Digital (bool) | Pressed/Released — C++ uses `Started` and `Completed` |
| `IA_Scan` | Digital (bool) | Pressed — C++ uses `Started` only |
| `IA_PlaceBeacon` | Digital (bool) | Pressed — C++ uses `Started` only |
| `IA_Journal` | Digital (bool) | Pressed — not yet bound in C++; reserved for M3 journal shell |

### Input Mapping Context (`Content/Input/IMC_AbyssalExplorer`)

Assign this asset to `DefaultMappingContext` on `BP_AbyssalExplorerCharacter`. Mappings:

- `IA_Move`:
  - W = (Y +1.0), S = (Y -1.0), A = (X -1.0), D = (X +1.0).
  - Gamepad Left Thumbstick 2D-Axis with `Dead Zone` modifier (Lower 0.2, Upper 1.0).
- `IA_Look`:
  - Mouse XY 2D-Axis with `Negate` modifier on Y (UE mouse Y is inverted relative to look convention) and a `Scalar` modifier (X 1.0, Y 1.0).
  - Gamepad Right Thumbstick 2D-Axis with `Dead Zone` modifier and a `Scalar` modifier (X 90.0, Y 60.0) so stick sensitivity matches a typical mouse feel — tune in playtest.
- `IA_Sprint`: Left Shift, Gamepad Left Thumbstick Button.
- `IA_Crouch`: Left Ctrl, Gamepad Face Button Right (B/Circle).
- `IA_Scan`: Right Mouse Button, Gamepad Left Trigger.
- `IA_PlaceBeacon`: B key, Gamepad Face Button Top (Y/Triangle).
- `IA_Journal`: J key, Gamepad Special Right (View/Menu).

### Blueprint Wiring

On `BP_AbyssalExplorerCharacter` defaults, assign every `UInputAction*` property in the Details panel:

- `DefaultMappingContext` -> `IMC_AbyssalExplorer`
- `MoveAction` -> `IA_Move`
- `LookAction` -> `IA_Look`
- `SprintAction` -> `IA_Sprint`
- `CrouchAction` -> `IA_Crouch`
- `ScanAction` -> `IA_Scan`
- `PlaceBeaconAction` -> `IA_PlaceBeacon`

`IA_Journal` is intentionally not yet wired in C++; leave it unassigned until the journal shell exists in M3.

### Verification Steps

1. Drop a `BP_AbyssalExplorerCharacter` into the level, set it as default pawn on the game mode.
2. PIE, confirm WASD moves, mouse looks, Shift sprints, Ctrl crouches (capsule should visibly shrink), Right Mouse fires a scan, B places a beacon when aimed at a surface within 9m.
3. If any action is dead, first verify the IMC asset is assigned and the IA is bound on the BP defaults — that is the most common failure mode.

## Rendering Defaults

- Lumen GI and reflections.
- Nanite enabled.
- Virtual textures enabled.
- Motion blur disabled by default for clearer exploration.
- Auto exposure enabled, but clamp per-volume in the cavern to avoid losing emissive detail.

## Core Reference Implementation

The Luminous Rift map is now anchored to `Content/ArtDirection/References/luminous_rift_core_reference.png`. The first playable map should prioritize the concept-art route documented in `LUMINOUS_RIFT_BLOCKOUT.md`: Descent Elevator -> First Overlook -> Abyssal Approach -> Crystal Galleries -> Collector Array -> Ancient Gate -> Second Sky Overlook.

### BP_RiftEnergyOrb

Create this as the central landmark actor for the Collector Array.

Suggested components:

- `USceneComponent` root at orb center.
- `UStaticMeshComponent` `OrbSphere` using a sphere/proxy mesh and `M_Rift_EnergyOrb_Master`.
- `UStaticMeshComponent` `OrbFrame` using `SM_Rift_OrbFrame_A`.
- `UStaticMeshComponent` `OrbHub` using `SM_Rift_OrbHub_A`.
- 1-3 point lights or rect lights for cool blue-white GI contribution.
- Niagara component for slow blue motes around the orb.
- Optional child scene components named `BeamAnchor_01`...`BeamAnchor_N` for beam spline attachment.

Behavior:

- Expose `OrbGlowStrength`, `PulseSpeed`, and `bOrbActive`.
- Drive material scalar parameters from Blueprint for slow pulse.
- Do not put gameplay collision on the orb in the first pass.
- Pair with a `BP_DiscoveryActor_Base` configured as `D_Anomaly_RiftEnergyOrb`.

### BP_RiftGoldBeamSpline

Create a reusable Blueprint actor for the warm beam lines visible in the reference.

Suggested components:

- `USplineComponent` for beam path.
- Spline mesh or Niagara beam renderer using `M_Rift_GoldEnergy_Master`.
- Small endpoint point lights with warm gold color.
- Optional endpoint static mesh using `SM_Rift_BeamEmitterNode_A`.

Behavior:

- Expose `BeamIntensity`, `BeamWidth`, `EndpointGlowStrength`, and `bBeamActive`.
- Support direct placement between orb/hub anchors and hex collector cluster centers.
- Beam should be visible in volumetric fog but thin enough not to obscure the orb.

### BP_HexCollectorCluster

Optional wrapper for imported collector clusters.

Suggested components:

- Static mesh cluster using `SM_Rift_HexCollector_Cluster_A` or broken variant.
- Scene component `BeamTarget` at cluster center.
- Optional point light for center node.
- Optional material parameter controls for pane glow.

Behavior:

- Expose `CollectorGlowStrength` and `bCollectorActive`.
- Broken/dark variants should remain placeable without active light.

### Revised Objective IDs

`UObjectiveSubsystem::BuildDefaultRoute` now uses the main survival/alien-tech objective arc:

- `OBJ_VERIFY_HELIOS`
- `OBJ_SURVIVE`
- `OBJ_DISCOVER_PLACE`
- `OBJ_MAKE_MACHINE_ANSWER`
- `OBJ_BUILD_WAY_OUT`
- `OBJ_OPEN_RIFT`

If older prototype saves contain previous route ids, reset route state in non-shipping builds with `AbyssalDebugResetDiscoveries`.

## Abyssal Interface Technical Plan

The in-game LLM system is documented in `Docs/ABYSSAL_INTERFACE_AI_SYSTEM.md`. The first implementation should be a simple text terminal that sends compact game context to a backend/agent service and renders a short diegetic response.

### Version 0 Scope

- Text-only terminal UI in Unreal.
- Player input string.
- Compact context payload containing map, zone, current objective, inventory, discoveries, recent scans, and recent actions.
- Backend returns constrained JSON with response mode, speaker, text, confidence, suggested events, and memory tags.
- Unreal displays text and ignores event suggestions until validation logic exists.

### Proposed Unreal Types

- `FAbyssalInterfaceContext`: serializable request payload.
- `FAbyssalInterfaceResponse`: constrained response payload.
- `UAbyssalInterfaceSubsystem`: owns request throttling, active session id, backend endpoint config, and response parsing.
- `AAbyssalInterfaceTerminal`: interactable world actor.
- `UAbyssalInterfaceComponent`: optional component for terminal actors or future portable interface devices.
- `WBP_AbyssalInterfaceTerminal`: input box, send button, response log, failure state display.

### Backend Contract

Initial endpoint:

- `POST /abyssal-interface/respond`

Design schema:

- `Content/Design/AbyssalInterfaceContextSchema.json`

Response modes:

- `Content/Design/AbyssalInterfaceResponseModes.csv`

Unreal must validate all model-suggested events. The LLM cannot directly execute gameplay changes.

### Tone Constraints

Responses should be short, eerie, intelligent, lore-aware, and incomplete. The Interface is not Shinrou in fiction and must never expose model/provider details.

### Failure Handling

If the backend is unavailable, show diegetic failure text such as `signal incomplete`, `translation failed`, or `interface dormant`. Do not expose raw network errors to the player.

### Future Versions

- Context-aware terminal using real discoveries and inventory.
- Fabrication guidance after prerequisite discoveries.
- Voice/TTS with processed ancient-machine tone.
- Portable shard/device interface.
- AI director suggestions for atmospheric events, always Unreal-validated.
