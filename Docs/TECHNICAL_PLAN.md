# Technical Plan

## Current Constraint

Unreal Editor is not installed or not discoverable from PATH on this machine. Work should remain UE-ready so the project can be opened and compiled once the engine is available.

## Gameplay Foundation

- `AAbyssalExplorerCharacter`: first-person pawn for exploration.
- `UScannerComponent`: finds nearby discovery actors and triggers scan feedback.
- `UAbyssalScannerReadoutWidget`: UMG base class that auto-binds to the owning pawn scanner and exposes Blueprint events for scan UI feedback.
- `ADiscoveryActor`: placeable scan target with journal metadata.
- `ABeaconActor`: placeable navigation marker foundation.
- `UDiscoverySubsystem`: stores discovered IDs and saves new discoveries.
- `UDiscoverySaveGame`: simple save object for discovery persistence.
- `AAbyssalEarthGameMode`: assigns the explorer pawn.

## Next C++ Additions

- Beacon color/channel selection and optional beacon removal.
- Basic environmental hazard actor for Ember Vents timing.
- Journal shell helpers once the first scanner HUD is working in Blueprint.

## Scanner Implementation Notes

- `UScannerComponent` scans from the owning actor's eye viewpoint so first-person aiming matches player expectation.
- Discovery candidates can require visibility-channel line of sight before they are scored.
- Blueprint feedback hooks are available for pulse start, target found, and miss states.
- Scanner readouts can bind to `OnScanResultChanged` and consume `FAbyssalScanResult` for discovery name, category, distance, and new-vs-repeat state without duplicating scan scoring in UI Blueprints.
- `UAbyssalScannerReadoutWidget` handles the C++ delegate binding for `WBP_ScannerReadout`, caches the latest result, and provides `GetCurrentReadoutText` for a compact first-pass HUD label.
- `ADiscoveryActor::ScanFocusOffset` lets Blueprint children aim traces at the visible center of tall fungi, crystals, vents, or station props.

## Blueprint Plan

- `BP_AbyssalExplorerCharacter`: assign input actions and camera tuning.
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

## Rendering Defaults

- Lumen GI and reflections.
- Nanite enabled.
- Virtual textures enabled.
- Motion blur disabled by default for clearer exploration.
- Auto exposure enabled, but clamp per-volume in the cavern to avoid losing emissive detail.
