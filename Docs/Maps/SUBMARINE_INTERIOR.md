# Map PRO — Submarine Interior (Prologue Start)

## Overview
The game’s first playable space. A compact deep-sea research submarine on the surface of the ocean, preparing to dock with the HELIOS-built elevator shaft. The player learns to move, interact, and read the world before anything goes wrong. Tone: mundane professional competence — this is a funded scientific expedition, not a disaster movie. The disaster comes later.

## Dimensions
Small linear interior — approximately 22 m × 4 m corridor-plan. Two main rooms plus a narrow walkway. No combat, no hazards, no creatures.

---

## Zones

### Z1 — Briefing Room (PRO_002)
The player wakes/arrives in their diving suit. A wall tablet displays the mission headline: **FIRST MAJOR EXPLORATION EXPEDITION OF EARTH’S ABYSSAL PLAINS**. Sub props: sealed equipment lockers, a folded dive checklist, a framed depth chart. Sunlight through the port windows fades as the sub begins its descent.

**Interactions**:
- Inspect wall tablet → narrative beat `SUB_BRIEF_01` (mission brief readout)
- Inspect dive checklist → narrative beat `SUB_BRIEF_02` (player character notes everything is accounted for)
- Inspect depth chart → discovery `DIS_SUB_DEPTH_CHART`

**Exit condition**: Player gains control after CinematicToPlayable blend (PRO_002).

### Z2 — Walkway
Narrow connecting passage. Overheard audio from off-screen crew members (no visible NPCs — the player character is alone in this section). Props: hanging equipment bags, a mounted emergency suit patch kit, HELIOS schematic printout pinned to the wall.

**Interactions**:
- Inspect HELIOS schematic → discovery `DIS_HELIOS_SCHEMATIC`

### Z3 — Observation Room (PRO_003 walkaround)
The forward-most room. A large curved viewport faces the dark water. Sub running lights activate as the last sunlight vanishes. A monitor bank shows depth, pressure, hull integrity. The docking sequence HUD element appears in the corner.

**Interactions**:
- Inspect viewport → narrative beat `SUB_WINDOW_01` (player line: *"Nothing but black."*)
- Inspect depth monitor → narrative beat `SUB_DEPTH_01` (current depth readout)
- Stand near viewport long enough → docking proximity trigger fires

**Exit condition**: Docking sequence begins (PRO_004).

### Z4 — Dock Hatch (PRO_004 transition)
A short sealed airlock between the sub hull and the HELIOS shaft dock. Cinematic only: the sub docks with a clunk, hatch indicators turn green, the hatch opens. Objective `OBJ_VERIFY_HELIOS` appears. Player steps through → level streams to `ACCESS_PASSAGE` map.

---

## Key Narrative Beats
| Beat ID | Zone | Speaker | Line |
|---------|------|---------|------|
| SUB_BRIEF_01 | Z1 | Terminal | *[Mission brief text display]* |
| SUB_BRIEF_02 | Z1 | Player | "All signed off. Let’s see what’s down there." |
| SUB_WINDOW_01 | Z3 | Player | "Nothing but black." |
| SUB_DEPTH_01 | Z3 | Terminal | *[Depth readout: 6,200 m]* |

## Discoveries
| ID | Type | Zone |
|----|------|------|
| DIS_SUB_DEPTH_CHART | Document | Z1 |
| DIS_HELIOS_SCHEMATIC | Document | Z2 |

## Notes
- No `UOxygenComponent` pressure in this map — the player is inside a pressurised hull.
- The sunlight-to-sub-lights transition in Z1 is a post-process blend triggered at a depth threshold (cosmetic only).
- Audio design: surface ocean ambience through Z1–Z2; transition to low hull-creak pressure tone by Z3.
- HELIOS schematic in Z2 should match the robot chassis design from `AHeliosRobot` — textural continuity.
- Map loads immediately on new game; fade-in from black after the PRO_001 ocean surface cinematic.
