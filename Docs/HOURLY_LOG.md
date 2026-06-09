# AbyssalEarth Hourly Dev Log

Each entry = one autonomous tick. Branch → push → squash-merge to main.

---

## Tick 01–17 — (see prior entries)

## Tick 18 — Power Node Routing + Objective Widget + Gravity Well Lower Map
**Branch**: roadmap-tick-19 | **Merged**: PR #19 (pending)  
`AAbyssalPowerNode` Source/Relay/Sink actor with graph propagation (cycle guard, 16-hop depth limit, relay loss); `IAbyssalInteractable` for Source nodes — player toggles activation; `ConnectedTerminals` drives `AAbyssalInterfaceTerminal::SetPowerLevel` directly; `UAbyssalObjectiveWidget` UUserWidget base — binds `OnObjectiveChanged`/`OnRouteCompleted` in NativeConstruct, fires `ShowObjective`/`OnObjectiveComplete`/`OnAllObjectivesComplete` BP events; `GRAVITY_WELL_LOWER.md` Act 3 multi-axis gravity puzzle area with 3-terminal power network and objective completion trigger.

---
