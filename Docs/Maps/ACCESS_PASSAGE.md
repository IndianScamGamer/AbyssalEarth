# Map PRO-B — Access Passage (Prologue Helios Corridor)

## Overview
The short corridor between the submarine dock and the descent elevator. HELIOS construction robots are active here, performing final calibration checks on the shaft infrastructure. The player overhears — and can interact with — two or three HELIOS units who deliver the anomaly warning (PRO_005). Tone: polite, professional concern from machines that are doing exactly what they were programmed to do.

## Dimensions
Linear corridor, approximately 40 m × 5 m. One branching alcove. No hazards. No creatures.

---

## Zones

### Z1 — Dock Egress
Immediate exit from the submarine dock hatch. HELIOS unit **HEL-07** stands at a wall panel running diagnostics. Interaction fires dialogue beat `HEL_GREETING` (auto or on interact, depending on PRO_005 scripting).

**Props**: HELIOS tool rack, shaft pressure gauge (wall-mounted), emergency vent panel.

### Z2 — Construction Alcove
A side alcove where HELIOS unit **HEL-12** is mid-weld on a structural brace. A monitoring tablet shows the anomaly reading (discoverable: `DIS_ANOMALY_READOUT`). Two interact options:
- Interact with HEL-12 → `HEL_ANOMALY_WARNING` beat
- Inspect tablet → `DIS_ANOMALY_READOUT` discovery + `HEL_RECOMMEND_DELAY` beat

### Z3 — Elevator Approach
Straight run to the elevator doors. HELIOS unit **HEL-03** blocks the doorway briefly; on approach fires `HEL_OVERRIDE_ACKNOWLEDGED` automatically and steps aside. Elevator call button becomes interactable. Objective marker points here.

**Exit condition**: Player enters elevator → level streams to `DESCENT_ELEVATOR` map.

---

## Narrative Beats (HELIOS dialogue — from HeliosDialogueBeats.csv)
| Beat ID | Trigger | HELIOS Unit |
|---------|---------|-------------|
| HEL_GREETING | Z1 enter / HEL-07 interact | HEL-07 |
| HEL_ANOMALY_WARNING | HEL-12 interact | HEL-12 |
| HEL_RECOMMEND_DELAY | Tablet inspect | HEL-12 |
| HEL_OVERRIDE_ACKNOWLEDGED | Z3 approach | HEL-03 |

## Discoveries
| ID | Type | Zone |
|----|------|------|
| DIS_ANOMALY_READOUT | Document | Z2 |
| DIS_HELIOS_CALIBRATION_LOG | Document | Z1 (wall panel) |

## HELIOS Robot Instances
| Unit | Zone | State | Notes |
|------|------|-------|-------|
| HEL-07 | Z1 | Working | Runs diagnostics loop animation |
| HEL-12 | Z2 | Working | Welding animation; stops on interact |
| HEL-03 | Z3 | Warning | Blocks door briefly then steps aside |

## Notes
- All three HELIOS units use `AHeliosRobot` with `EHeliosState::Working` (HEL-07, HEL-12) or `Warning` (HEL-03).
- HEL-03’s warning state should not feel aggressive — the machines are calm, just flagging a protocol concern.
- If the player ignores all three and goes straight to the elevator, the `HEL_OVERRIDE_ACKNOWLEDGED` beat fires automatically on Z3 proximity — they can’t miss the warning.
- Lighting: cool blue HELIOS work lights mixed with amber from the shaft-side door glow. Contrast with the submarine’s warmer tone — signals entry into HELIOS-built infrastructure.
