# AbyssalEarth Hourly Dev Log

Each entry = one autonomous tick. Branch → push → squash-merge to main.

---

## Tick 01–19 — (see prior entries)

## Tick 20 — RiftActor + UpgradeSubsystem + Rift Chamber Endgame Map
**Branch**: roadmap-tick-21 | **Merged**: PR #21 (pending)  
`AAbyssalRiftActor` power-gated + item-gated endgame portal; consumes `ITEM_KEY_RIFT_STABILISER` on activation; `ChargeDuration` timer then fires `OnRiftOpened` + completes `OBJ_OPEN_RIFT` via `UObjectiveSubsystem`; `ERiftState` (Dormant/Charging/Open/Stable); `UAbyssalUpgradeSubsystem` IAbyssalSaveProvider — maps 4 upgrade IDs to vital component tweaks (`AddPressureRating`, `AirCapacityBonus`, `Insulation`, `ArmorRating`); reapplies all upgrades on `RegisterPlayerPawn`; `RiftNarrativeBeats.csv` (5 beats covering activation → opening → entry); `RIFT_CHAMBER.md` Act 5 endgame circular chamber with 6-source power network, 2 Confluence Watcher creatures, complete narrative beat sequence.

**Milestone**: Core gameplay loop is now fully designed and coded end-to-end — prologue to rift opening.

---
