# AbyssalEarth Hourly Dev Log

Each entry = one autonomous tick. Branch → push → squash-merge to main.

---

## Tick 01–18 — (see prior entries)

## Tick 19 — ScanComponent + InventoryWidget + Mantle Garden Deep Map
**Branch**: roadmap-tick-20 | **Merged**: PR #20 (pending)  
`IAbyssalScannable` interface (`GetScanId`, `GetScanDisplayName`, `OnScanned`); `UAbyssalScanComponent` sphere-overlap pulse scanner with cooldown, `bRescanKnownActors` flag, `OnScanHit`/`OnScanPulseFired`/`OnScanCooldownComplete` delegates; feeds `UDiscoverySubsystem`; `UAbyssalInventoryWidget` UUserWidget base binds `UInventorySubsystem` item delegates, builds slot list from `UAbyssalItemDatabase`, exposes `RefreshInventory`/`OnInventoryItemAdded`/`OnInventoryItemRemoved` BP events; `MANTLE_GARDEN_DEEP.md` Act 4 fabrication zone with tier-3 station gated behind brittle walkway, dual vital pressure (heat + depth), Rift Stabiliser crafting location; `MantleGardenDeepNarrativeBeats.csv` (4 beats).

---
