# Map 07 — Rift Chamber (Act 5 — OBJ_OPEN_RIFT)

## Overview
The heart of the Confluence. A cathedral-scale void at the absolute geometric centre of the cavern system — the monolith array from LUMINOUS_RIFT, now assembled into a complete ring around a dormant `AAbyssalRiftActor`. Every surface is carved alien geometry. The bioluminescence here is deep amber, not the cold blue of the upper caves. It feels warm. Ancient. Like something is watching.

This is the only place in the game where all five survival vitals (health, oxygen, stamina, temperature, pressure) are simultaneously at risk — but managed: the hazards are deliberate, not accidental. This is a designed arena, not a cave.

## Dimensions
Circular chamber — approximately 120 m diameter, 40 m ceiling. Central platform 20 m diameter, raised 3 m. Outer ring walkway 8 m wide. Six alcoves evenly distributed around the outer ring, each containing a power source node.

---

## Zones

### Z1 — Outer Ring
Entry from MANTLE_GARDEN_DEEP or a dedicated `UWorldFlowSubsystem` direct-travel node. Six `AAbyssalPowerNode` (Source type) actors in the alcoves — each requires the player to navigate past a hazard to activate. Checkpoint: `CHK_RIFT_CHAMBER_OUTER`.

**Hazard distribution**:
- Alcoves 1–2: `AMagmaPulseHazard` (timed dodge window)
- Alcoves 3–4: `ASteamVentHazard` (vertical column; timing required)
- Alcoves 5–6: `AGravityShearHazard` active zone (brief disorientation)

### Z2 — Central Platform
Reachable once at least 4 of 6 power sources are active (power threshold 0.8 on `AAbyssalRiftActor`). The `AAbyssalRiftActor` sits at the platform centre, dormant until all conditions are met.

**Creatures**: No hostile creatures. Two passive Confluence Watchers (creature type unique to this area; `bIsAggressive = false`; large, slow, orbit the rift actor) — they don’t attack but their bulk blocks pathing if the player isn’t careful.

### Z3 — Rift Activation Sequence
Once the player interacts with `AAbyssalRiftActor`:
1. Narrative beat `RIFT_ACTIVATE_01` fires.
2. Charging phase: 8 seconds. `RIFT_CHARGING_01` terminal beat plays.
3. Rift opens. `RIFT_OPEN_01` + `RIFT_OPEN_02` beat sequence.
4. `OBJ_OPEN_RIFT` completes; `OnRouteCompleted` fires on `UObjectiveSubsystem`.
5. Player walks into the rift opening → `RIFT_ENTER_01` triggers.
6. Fade to white. Credits / epilogue.

---

## Power Network
```
Sources 1–6 (Alcoves) ─> Central Relay ─> AAbyssalRiftActor
```
Each source contributes ~0.167 power. Central Relay sums inputs and forwards to the rift. Rift threshold 0.8 requires 5 of 6 sources active — one failure is forgiven.

## Creatures
| Species | State Default | Count | Zone |
|---------|--------------|-------|------|
| Confluence Watcher | Passive | 2 | Z2 central platform |

## Discoveries
| ID | Type | Zone | Notes |
|----|------|------|-------|
| DIS_RIFT_CHAMBER_MONOLITH | Scan | Z1 | Complete monolith ring |
| DIS_CONFLUENCE_CORE | Scan | Z2 | The dormant rift before activation |

## Narrative Beats (in sequence)
| Beat ID | Trigger | Speaker |
|---------|---------|------|
| RIFT_ACTIVATE_01 | Rift interact | Player |
| RIFT_CHARGING_01 | Charging start | Terminal |
| RIFT_OPEN_01 | Rift opens | Player |
| RIFT_OPEN_02 | 3 s after RIFT_OPEN_01 | Player |
| RIFT_ENTER_01 | Player walks into rift (proximity trigger) | Player |

## Notes
- The Confluence Watchers should feel like the Luminous Rift creatures grown enormous — textural continuity from map 01 to map 07.
- All six power sources should be visually distinct in lighting from the rest of the chamber — the player should be able to see all six alcoves from the entry and understand the task immediately.
- The amber bioluminescence brightens slowly during the charging phase, reaching full intensity when the rift opens. Audio: silence drops to zero at activation, then builds to a resonant hum.
- The fade-to-white on rift entry is the only hard cut in the entire game. Everything else is streaming transitions.
