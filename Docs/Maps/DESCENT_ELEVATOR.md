# Map PRO-C — Descent Elevator (PRO_006 / PRO_007)

## Overview
The point of no return. A compact elevator cab descending a 6,000 m shaft that HELIOS constructed over three months. Thirty seconds of false calm, then catastrophic failure. The player has no control over the disaster — only how they respond to it.

This map is almost entirely cinematic but with one critical LimitedPlayable beat (PRO_006) giving the player a few seconds to look around and hear the cable hum before the warnings fire.

## Dimensions
Very small — 2.5 m × 2.5 m elevator cab interior. The illusion of space comes from the shaft walls visible through the grated cab floor and a small window slit. No traversal options; no interactions. The environment is the narrative.

---

## Timeline

### T+0:00 — Descent Begins (PRO_006 enter)
- Player gains limited movement inside the cab.
- Ambient: low rhythmic cable hum, distant machinery, the sub’s departure muffled above.
- Props: descent speed indicator (counting down depth), emergency stop button (non-functional — player can interact, nothing happens, which is worse), handrail.
- Post-process: slowly dims exterior light through grated floor as depth increases.

### T+0:08 — Player Line
- Narrative beat `PRO_006_LINE` fires automatically (no trigger required):
  > *"Sounds like those bastards were lying."*
- Reference: PRO_005 — HELIOS warned of an anomaly. The player is acknowledging they probably should have listened.

### T+0:22 — Warning State Begins
- Three HUD warning indicators flash: CABLE TENSION • SHAFT ANOMALY • EMERGENCY PROTOCOL.
- Narrative beat `PRO_007_WARNING` (terminal voice):
  > *"[ALERT] Structural anomaly detected in shaft sector 7. Emergency brake activation—"*
- Beat cuts off mid-sentence.

### T+0:26 — Cable Cut
- Jolt. Ambient sound cuts to silence for 0.3 s.
- Then: metal screech, rushing air, the depth indicator spinning.
- Post-process: severe chromatic aberration, vignette, motion blur.
- Player loses all movement input (cinematic takeover).

### T+0:32 — Blackout
- Impact. Cut to black. Audio: silence, then a single creak.
- Level streams to `WRECKED_ELEVATOR` map.

---

## Key Narrative Beats
| Beat ID | Time | Trigger | Line |
|---------|------|---------|------|
| PRO_006_LINE | T+0:08 | Auto timer | "Sounds like those bastards were lying." |
| PRO_007_WARNING | T+0:22 | Auto timer | "[ALERT] Structural anomaly detected…" |

## Notes
- The emergency stop button interaction (`IAbyssalInteractable`) should return a custom `CanInteract = false` with prompt text: *"[INOPERATIVE]"* — the player’s attempt to do something feels right; the futility is the point.
- No checkpoint registered in this map. Death here respawns to the last valid checkpoint (the ACCESS_PASSAGE dock, typically).
- The shaft walls visible through the cab grate should show HELIOS construction markings passing at increasing speed — a simple material scrolling UV effect.
- Audio design: cable hum at 60 Hz, rises to 80 Hz over the 30-second descent, then silence-to-scream at T+0:26.
