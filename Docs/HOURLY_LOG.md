# AbyssalEarth Hourly Dev Log

Each entry = one autonomous tick. Branch → push → squash-merge to main.

---

## Tick 01–16 — (see prior entries)

## Tick 17 — HUD Subsystem + Item Database + Fossil Sky Upper Map
**Branch**: roadmap-tick-18 | **Merged**: PR #18 (pending)  
`UAbyssalHUDSubsystem` — game-instance subsystem; `RegisterPlayerPawn` binds all five vital component delegates and fires `OnVitalsUpdated` on every change; `GetVitalReadout()` returns `FAbyssalVitalReadout` snapshot (health/oxygen/stamina/heat/pressure + boolean states); `FAbyssalItemTableRow : FTableRowBase` for DataTable-driven item definitions; `UAbyssalItemDatabase` game-instance subsystem for O(1) `GetItemData(FName)` lookups; `DT_ItemDatabase.csv` with 11 items across Material/Tool/Upgrade/Quest categories; `FOSSIL_SKY_UPPER.md` Act 2 approach zone (bone forest, ancient kill site, scale reveal at shelf edge).

---
