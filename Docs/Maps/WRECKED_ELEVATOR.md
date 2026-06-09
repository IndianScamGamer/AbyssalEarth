# Map 00 — Wrecked Elevator (Act 0 Exit / Prologue End)

## Overview
The first playable space after the crash. A crushed, tilted elevator cab wedged in a fractured shaft. Darkness except for emergency strip-lights and bioluminescent seepage through the cracks. Purpose: teach the player the interaction verb (pry doors), introduce ambient audio of the cavern beyond, and deliver the Luminous Rift reveal.

## Size
Small linear space — roughly 6 m × 3 m × 4 m. No combat. No vitals pressure.

## Zones

### Z0 — Crash Wake
- Player wakes on the floor, suit cracked, HUD glitching.
- Objective updates: **SURVIVE** fires here.
- Ambient: distant low hum, dripping, crack-light pulses.
- No interaction options yet — player must stand first (anim cue).

### Z1 — Jammed Doors
- Primary interaction: hold-to-pry or QTE depending on difficulty setting.
- Props: twisted door frame, bent HELIOS chassis fragment (foreshadow), torn briefing printout (collectible).
- Exit condition: doors open → Z2.

### Z2 — Shaft Ledge
- Brief platform outside the cab, shaft walls above and below.
- Bioluminescent lichen on shaft walls — first alien material contact.
- Camera auto-pans down to show the cavern abyss, then forward to the rift glow.
- Player line (narrative beat): **PRO_009** — "Oh... shit."
- Transition: step forward → level stream to `LUMINOUS_RIFT` map.

## Key Beats
| Beat ID | Trigger | Line |
|---------|---------|------|
| PRO_008_WAKE | Z0 enter | *(ambient groan, no caption)* |
| PRO_009 | Z2 enter | "Oh... shit." |

## Discoveries
| ID | Type | Location |
|----|------|----------|
| DIS_WRECKED_BRIEFING | Document | Torn printout in Z1 |
| DIS_HELIOS_FRAGMENT | Object scan | Bent chassis in Z1 |

## Notes
- No creature spawns. No hazard volumes. Pure atmosphere and pacing.
- The dripping sound is synced to the bioluminescent pulse rate — establishes the cavern as a living system.
- Load this map immediately after `PRO_007` (elevator fall blackout); fade-in from black.
