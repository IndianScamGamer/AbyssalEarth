# Editor Guide: Act 1 Level Blockout (A1_001)

Step-by-step level construction for **A1_001 — Thermal Vent Field**. The player emerges from the submarine hatch and explores the abyssal floor for the first time: active geysers, gravity shear zones, and the start of the power puzzle network.

## Overview

200 × 200 m playable ocean-floor area. Three sub-regions:

```
[Landing Site / Entry] → [Vent Field] → [Relay Station (Power Puzzle)]
       30×30m                 100×100m           40×40m
```

## 1. Create the Level

1. **File → New Level → Empty Level**
2. Save as `Content/Maps/A1_001_ThermalVentField`
3. **World Settings → Game Mode Override**: `BP_AbyssalGameMode_Act1`
   - Create `BP_AbyssalGameMode_Act1` as child of `BP_AbyssalGameMode`, set **Narrative Beat Table** = `DT_Act1NarrativeBeats`
4. **World Settings → Kill Z**: `-50000` (kills player if they fall through geometry)

## 2. Terrain / Ocean Floor

1. Add a **Landscape** actor, 200×200m, 2m quad size
2. Sculpt: gentle undulations (displacement 50–200 cm), steeper ridges flanking the main path
3. Apply ocean-floor material (muddy basalt, displacement-mapped): `M_OceanFloor` from `Content/Materials/`
4. Add **Landscape Spline** for the main traversal path — slightly flatter ground to guide the player

**Ambient water fog:**
- Add **Exponential Height Fog**: Fog Density `0.05`, Fog Inscattering Color `(0.01, 0.06, 0.12)` (deep blue), Start Distance `500`, Fog Cutoff Distance `15000`

## 3. Lighting

**Sky Light** (SLS Captured Scene, intensity 0.05 — nearly no ambient).

**Directional Light**: intensity `0.1`, colour `(0.1, 0.2, 0.5)` cold blue, very low angle to simulate bioluminescent scatter.

**Practical lights** — Point Lights at each vent and relay station for local warm glow.

**Post-Process Volume** (Infinite):
- Chromatic Aberration: `0.6`
- Vignette: `0.7`
- Saturation: `(0.5, 0.5, 0.5, 1)`
- Bloom: Intensity `1.5`, Threshold `-1`

## 4. Hazards: Magma Geysers (×6)

Place `BP_MagmaGeyserHazard` actors across the Vent Field. Stagger their timings so they are never all active simultaneously:

| Actor | Position (approx) | Idle Duration | Warning | Active | Cooldown |
|---|---|---|---|---|---|
| Geyser_01 | `(3000, 1000, 0)` | `8.0` | `2.0` | `4.0` | `3.0` |
| Geyser_02 | `(4500, -500, 0)` | `6.0` | `2.0` | `4.0` | `3.0` |
| Geyser_03 | `(6000, 2000, 0)` | `10.0` | `2.0` | `4.0` | `3.0` |
| Geyser_04 | `(7500, 500, 0)` | `7.0` | `2.0` | `4.0` | `3.0` |
| Geyser_05 | `(9000, -1000, 0)` | `9.0` | `2.0` | `4.0` | `3.0` |
| Geyser_06 | `(10000, 1500, 0)` | `5.0` | `2.0` | `4.0` | `3.0` |

Set `bStartActive = false` on all. The staggered idle durations create a natural rhythm.

## 5. Hazards: Gravity Shear Zones (×2)

Place `BP_GravityShearHazard` flanking the main path near the Relay Station entrance:

- `GravityShear_Left`: position `(11000, -1500, 0)`, `bStartActive = true`
- `GravityShear_Right`: position `(11000, 1500, 0)`, `bStartActive = true`

These zones disorient the player's gravity, requiring `UAbyssalTraversalComponent::RequestGravityReorientation`. The player must pass between them — set their volumes so there is a 3 m safe gap in the centre.

## 6. Power Network (3-Node Chain)

This puzzle requires the **additive input summing fix** (Phase 1d — already implemented in C++).

Place three `BP_AbyssalPowerNode` actors:

| Actor | Type | Position | Settings |
|---|---|---|---|
| `PowerNode_Source_A` | Source | `(12000, -800, 100)` | SourceOutput=1.0, NodeLabel="VENT CORE A" |
| `PowerNode_Source_B` | Source | `(12000, 800, 100)` | SourceOutput=1.0, NodeLabel="VENT CORE B" |
| `PowerNode_Relay_01` | Relay | `(13500, 0, 100)` | RelayLoss=0.0, NodeLabel="RELAY ALPHA" |

Wiring:
- `PowerNode_Source_A` → ConnectedNodes: `[PowerNode_Relay_01]`
- `PowerNode_Source_B` → ConnectedNodes: `[PowerNode_Relay_01]`
- `PowerNode_Relay_01` → ConnectedTerminals: `[Terminal_Relay_01]`

Place `BP_AbyssalInterfaceTerminal` at `(14500, 0, 100)`:
- **Terminal Id**: `TERMINAL_RELAY_01`
- **Power Threshold**: `0.5` (activates when relay receives power from either source)
- **Response Mode**: `UNLOCK_CHECKPOINT`

The puzzle: player interacts with Source A OR Source B (or both) → relay powers up → terminal unlocks the second checkpoint.

## 7. Checkpoints

| Actor | Checkpoint Id | Map Id | Position |
|---|---|---|---|
| `BP_CheckpointActor` (Entry) | `CP_A1_ENTRY` | `A1_001` | `(500, 0, 100)` |
| `BP_CheckpointActor` (Relay) | `CP_A1_RELAY` | `A1_001` | `(14000, 0, 100)` |

The relay checkpoint is locked behind the power terminal (terminal's OnActivated sets `CheckpointSubsystem→SetActiveCheckpoint(CP_A1_RELAY)`).

## 8. Creature Patrols (×2)

Place two `BP_AbyssalCreature` actors patrolling the perimeter of the vent field:

1. `Creature_01` — Spline patrol from `(2000, -3000)` → `(10000, -3000)` → `(10000, 3000)` → loop
2. `Creature_02` — Spline patrol from `(3000, 3000)` → `(9000, 3000)` → `(9000, -3000)` → loop

Set **Patrol Speed**: `200`, **Detection Radius**: `600`. Creatures are territorial — they chase but do not follow the player out of their patrol zone.

## 9. Ambient Bioluminescence

Add particle systems `PS_BiolumPlankton` (from `Content/FX/`) scattered across the ocean floor for visual richness. Use `UNiagaraComponent` with LOD bias to keep performance manageable.

## 10. Build & PIE Checklist

- [ ] Player spawns at `CP_A1_ENTRY` (after crossing from PRO_001 via level streaming or standalone)
- [ ] Geysers cycle through phases; landing in Active phase damages player
- [ ] Gravity shear zones reorient player gravity when entered
- [ ] Creature patrols their route; chase starts when player enters detection radius
- [ ] Interacting with either power source → relay powers → terminal activates → checkpoint unlocks
- [ ] Both sources active → relay still powered (additive summing, not doubled)
- [ ] Source A deactivated while Source B active → relay remains powered (tests the summing fix)
- [ ] Death respawns at last checkpoint (Entry or Relay depending on progress)
- [ ] Save/load preserves checkpoint and objective state
