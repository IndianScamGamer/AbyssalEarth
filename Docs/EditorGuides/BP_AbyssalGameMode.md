# Editor Guide: BP_AbyssalGameMode

Blueprint subclass of `AAbyssalGameMode`. This replaces the default GameMode in all Prologue and Act 1 levels.

## 1. Create the Blueprint

1. Content Browser → right-click in `Content/Blueprints/` → **Blueprint Class**
2. Search for and select **AbyssalGameMode** as the parent class
3. Name it `BP_AbyssalGameMode`

## 2. Set Class Defaults

Open **BP_AbyssalGameMode** → **Class Defaults**:

| Property | Value |
|---|---|
| Default Pawn Class | `BP_PlayerCharacter` |
| Player Controller Class | `BP_AbyssalPlayerController` |
| HUD Class | `BP_AbyssalHUD` (or None until HUD BP exists) |
| Narrative Beat Table | `DT_PrologueNarrativeBeats` (for Prologue levels) |

For Act 1 levels create a child BP (`BP_AbyssalGameMode_Act1`) and set **Narrative Beat Table** to `DT_Act1NarrativeBeats`.

## 3. Assign to Levels

**Per-level override** (preferred — do this for each map):
1. Open the level
2. **World Settings** panel → **Game Mode Override** → `BP_AbyssalGameMode`

**Project-wide default** (fallback):
1. **Edit → Project Settings → Maps & Modes**
2. **Default GameMode** → `BP_AbyssalGameMode`

## 4. Verify

Press **Play In Editor (PIE)**. In the **Details** panel of the spawned pawn, confirm:
- Pawn class shows `BP_PlayerCharacter`
- All 9 components (HealthComponent, OxygenComponent, etc.) appear in the components list

If the pawn class is wrong, confirm the level's World Settings override is set (it takes priority over the project default).
