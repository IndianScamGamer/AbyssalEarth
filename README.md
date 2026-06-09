# AbyssalEarth

A single-player survival-exploration game built in Unreal Engine 5. You are a structural engineer sent to verify a robot-built elevator shaft into Earth's abyssal plains. The verification does not go to plan.

## Project Status

**Backend: feature-complete.** All C++ gameplay systems are authored (see `Docs/BACKEND_SYSTEMS_ROADMAP.md`).  
**Story: complete.** Full narrative script, story bible, and ending design (see `Docs/Story/`).  
**Remaining work** is editor-side: Blueprint subclasses, UMG layouts, level blockouts, art, animation, and audio assets.

## Repository Layout

```
Source/AbyssalEarth/        All C++ gameplay systems
Content/Design/             DataTable CSVs (items, recipes, objectives, narrative beats)
Docs/
  BACKEND_SYSTEMS_ROADMAP.md  System inventory, phase by phase
  HOURLY_LOG.md               Development log, tick by tick
  Maps/                       14 map design docs (blockout-ready)
  Story/                      Story bible, epilogue design
```

## The Player Journey

| Act | Objective | Maps |
|-----|-----------|------|
| Prologue | Verify the AI Robot Fleet HELIOS's work | Submarine Interior → Access Passage → Descent Elevator → Wrecked Elevator |
| 1 | SURVIVE | Luminous Rift → Deep Channel |
| 2 | DISCOVER WHAT THIS PLACE IS | Fossil Sky Upper → Fossil Sky |
| 3 | MAKE THE MACHINE ANSWER | Gravity Well → Gravity Well Lower |
| 4 | BUILD A WAY OUT | Mantle Garden → Mantle Garden Deep |
| 5 | OPEN THE RIFT | Rift Chamber |

## System Architecture (one paragraph)

Everything persistent lives behind `UAbyssalSaveSubsystem` + `IAbyssalSaveProvider` (7 domain blobs in one `USaveGame`). The player pawn (`AAbyssalPlayerCharacter`) wires five vital components (health, oxygen, stamina, temperature, pressure), interaction, scanning, traversal, and observation mode; `UAbyssalHUDSubsystem` aggregates vitals for UMG. World content is driven by `AAbyssalHazardBase` subclasses (six biome hazards), `AAbyssalCreature` perception AI, `AHeliosRobot` NPCs, DataTable-driven objectives/items/recipes, a power-routing graph (`AAbyssalPowerNode`) feeding alien terminals, and the endgame `AAbyssalRiftActor`. Narrative is caption-beat based (`UNarrativeSubsystem` + CSVs per act).
