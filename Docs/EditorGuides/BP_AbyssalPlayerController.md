# Editor Guide: BP_AbyssalPlayerController

Blueprint subclass of `AAbyssalPlayerController`. Handles Enhanced Input context and all input action asset bindings.

## 1. Create the Blueprint

1. Content Browser → `Content/Blueprints/` → **Blueprint Class**
2. Parent: **AbyssalPlayerController**
3. Name: `BP_AbyssalPlayerController`

## 2. Create or Locate Input Assets

All input assets live in `Content/Input/`. Create any that are missing.

### Input Mapping Context
- Asset: `IMC_AbyssalDefault` (type: **Input Mapping Context**)

### Input Action Assets

| Asset Name | Value Type | Notes |
|---|---|---|
| `IA_Move` | Axis2D (Vector2D) | WASD / left stick |
| `IA_Look` | Axis2D (Vector2D) | Mouse / right stick |
| `IA_Sprint` | Digital (bool) | Pressed/Released |
| `IA_Crouch` | Digital (bool) | Pressed/Released |
| `IA_Interact` | Digital (bool) | Pressed only |
| `IA_ScanPulse` | Digital (bool) | Pressed only |
| `IA_ObservationMode` | Digital (bool) | Pressed only (toggle) |

### IMC_AbyssalDefault — Key Mappings

Open `IMC_AbyssalDefault` and add the following mappings:

| Action | Keyboard | Gamepad |
|---|---|---|
| IA_Move | WASD (with Swizzle/Negate modifiers per axis) | Left Thumbstick |
| IA_Look | Mouse XY | Right Thumbstick (+ Dead Zone + Scalar X:90 Y:60) |
| IA_Sprint | Left Shift | Left Thumbstick Button |
| IA_Crouch | Left Ctrl | Gamepad Face Button Right (B/Circle) |
| IA_Interact | E | Gamepad Face Button Bottom (A/Cross) |
| IA_ScanPulse | Right Mouse Button | Gamepad Left Trigger |
| IA_ObservationMode | Tab | Gamepad Right Thumbstick Button |

## 3. Assign Input Actions in BP_AbyssalPlayerController

Open **BP_AbyssalPlayerController** → **Class Defaults**:

| Property | Asset |
|---|---|
| Default Mapping Context | `IMC_AbyssalDefault` |
| Move Action | `IA_Move` |
| Look Action | `IA_Look` |
| Sprint Action | `IA_Sprint` |
| Crouch Action | `IA_Crouch` |
| Interact Action | `IA_Interact` |
| Scan Pulse Action | `IA_ScanPulse` |
| Observation Mode Action | `IA_ObservationMode` |

The C++ `SetupInputComponent` reads these and binds all actions automatically. No Blueprint Event Graph work is needed.

## 4. Assign to GameMode

Confirm `BP_AbyssalGameMode` → Class Defaults → **Player Controller Class** = `BP_AbyssalPlayerController`.

## 5. Verify

PIE → open **Output Log** → confirm `EnhancedInput: Added mapping context IMC_AbyssalDefault`. Press each key and confirm the pawn responds.
