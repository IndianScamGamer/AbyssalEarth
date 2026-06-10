# Editor Guide: Prologue Level Blockout (PRO_001)

Step-by-step level construction for **PRO_001 — Submarine Interior**. This is the first playable level: 4-room sequence ending at the airlock where the player descends to the abyssal floor.

## Overview

```
[Bunk Room] → [Corridor] → [Engine Room] → [Airlock / Descent Chamber]
    10×6×3m       20×4×3m       8×8×4m            6×6×4m
```
Total play space: ~44m long, narrow, claustrophobic.

## 1. Create the Level

1. **File → New Level → Empty Level**
2. Save as `Content/Maps/PRO_001_SubmarineInterior`
3. **World Settings → Game Mode Override**: `BP_AbyssalGameMode`
4. In `BP_AbyssalGameMode` CDO (or a child BP): **Narrative Beat Table** = `DT_PrologueNarrativeBeats`

## 2. Geometry (BSP Brush or Static Mesh)

Use BSP or modular submarine mesh kit. Reference measurements in Unreal units (1 unit = 1 cm):

| Room | Add Brush | Size (X×Y×Z cm) |
|---|---|---|
| Bunk Room | Box (Subtractive) | 1000 × 600 × 300 |
| Corridor | Box (Subtractive) | 2000 × 400 × 300 |
| Engine Room | Box (Subtractive) | 800 × 800 × 400 |
| Airlock | Box (Subtractive) | 600 × 600 × 400 |

Add floor, ceiling, and wall static meshes from `Content/Meshes/Submarine/` to dress the geometry.

## 3. Player Start

Place a **PlayerStart** actor at the foot of the Bunk Room (origin `(0, 0, 100)`). The GameMode spawns `BP_PlayerCharacter` here.

## 4. Lighting

All lighting: **Stationary** point lights (for baked shadows + dynamic specular).

| Room | Light Color | Intensity | Attenuation Radius |
|---|---|---|---|
| Bunk Room | `(0.8, 0.1, 0.1)` red | 800 | 200 |
| Corridor | `(0.8, 0.15, 0.1)` red-orange | 600 | 150 |
| Engine Room | `(0.6, 0.3, 0.05)` amber | 1200 | 250 |
| Airlock | `(0.2, 0.4, 0.8)` cold blue | 500 | 180 |

Add 1-2 flickering lights in the corridor (enable **Use IES Profile** or a simple Timeline-driven intensity animation in a BP_FlickerLight actor).

## 5. Post-Process Volume

Place a **PostProcessVolume** (Infinite Extent = true) with:

| Setting | Value |
|---|---|
| Vignette Intensity | `0.5` |
| Chromatic Aberration (Fringe Intensity) | `0.4` |
| Color Saturation | `(0.7, 0.7, 0.7, 1)` (slight desaturation) |
| Ambient Occlusion Intensity | `0.8` |
| Depth of Field — Focal Distance | `200` |

## 6. Hazard: Steam Vent

Place `BP_SteamVentHazard` in the Engine Room:
- Position: `(2500, 200, 0)` (floor vent near left wall)
- Settings:
  - `Idle Duration`: `5.0`
  - `Warning Duration`: `2.0`
  - `Active Duration`: `3.0`
  - `Cooldown Duration`: `1.5`
  - `bStartActive`: `false`

## 7. Checkpoint

Place `BP_CheckpointActor` at the Airlock entrance door:
- **Checkpoint Id**: `CP_PRO_AIRLOCK`
- **Respawn Location Offset**: `(0, 0, 100)` (just inside airlock)
- **Map Id**: `PRO_001`

## 8. Interface Terminal

Place `BP_AbyssalInterfaceTerminal` at the Engine Room console:
- **Terminal Id**: `TERMINAL_ENGINE_01`
- **Requires Power**: `false` (already powered — narrative context)
- **Response Mode**: `NARRATIVE` (plays `NAR_PRO_HELIOS_WARN` when activated)

Wire the terminal's **OnTerminalActivated** event to call `NarrativeSubsystem → PlayBeat("NAR_PRO_HELIOS_WARN")`.

## 9. Water Volume (Airlock Exit)

At the bottom of the Airlock (leading to the open ocean):
1. Place a **UPhysicsVolume** or a custom BP trigger box
2. Tag: `WaterVolume`
3. In the trigger overlap, call `OxygenComponent → SetSubmerged(true)` on the player character

Alternatively add a **WaterBodyOcean** actor and rely on the depth-tracking in `AAbyssalPlayerCharacter::UpdateDepth()` — the OxygenComponent starts depleting automatically when the component detects the character is below `SeaLevelZ`.

## 10. Narrative Trigger

First create `BP_NarrativeTriggerActor` (one-time setup, reused in every level):

1. Content Browser → `Content/Blueprints/` → **Blueprint Class** → parent **Actor**
2. Add a **Box Collision** component and make it the root (drag onto DefaultSceneRoot)
   - Collision Preset: `Trigger` (Overlap Pawn)
3. Add a **Narrative Trigger** component (`UNarrativeTriggerComponent`)
   - It auto-fires when a pawn overlaps the owner's primitive root
     (`bTriggerOnOverlap` and `bPawnOnly` default to true)

Then place one at the top of the Airlock stairs:
- **Beat Id**: `NAR_PRO_BRIEFING`
- One-shot behaviour comes from the beat itself (`bPlayOnce` in the beat
  table row), not from the trigger — no extra setting needed.

## 11. Build Lighting

**Build → Build Lighting Only** (Preview quality for iteration; Production quality before shipping).

## 12. PIE Checklist

- [ ] Player spawns at PlayerStart, not origin
- [ ] Vitals HUD visible (health, oxygen, stamina)
- [ ] Walk bunk → corridor → engine → airlock without falling through geometry
- [ ] Steam vent damages player in Active phase
- [ ] Touching airlock checkpoint → `CP_PRO_AIRLOCK` becomes active (verify with `AbyssalDebugAdvanceObjective` console command)
- [ ] Terminal activates → `NAR_PRO_HELIOS_WARN` caption appears on screen
- [ ] Crossing water volume → oxygen starts depleting
- [ ] Die → respawn at `CP_PRO_AIRLOCK` after 2 seconds
