# Backend Systems Roadmap

## Purpose

This document is the gameplay-systems (C++ / backend) plan for taking Abyssal
Earth from its current **Luminous Rift vertical slice** to the **full designed
game**: a 9-beat prologue, a 5-act arc, and six biomes
(`Docs/WORLD_ATLAS.md`).

It exists because the question "is the backend good enough for everything we
have planned?" has a clear answer: **the current backend is a solid single-map
slice, but most of the systems the full story and maps depend on do not exist
yet.** This roadmap names those systems, maps each one to the story acts and
biomes that need it, and orders them by dependency so work happens in the right
sequence.

### How the continuation loop should use this file

1. `git fetch --prune` and read this file plus `Docs/NEXT_TASKS.md`.
2. Pick the **lowest-numbered unstarted system whose dependencies are met** (or
   the next coherent sub-step of an in-progress one).
3. Implement it following the conventions in
   `Docs/BLUEPRINT_IMPLEMENTATION_NOTES.md` and the patterns of existing
   classes. Keep gameplay state in `UGameInstanceSubsystem`s and expose
   `BlueprintCallable`/`BlueprintAssignable` surfaces like the current code.
4. Update design data + `Scripts/validate_design_data.py` where relevant and run
   it. Update the status checklist at the bottom of this file.
5. Append a dated entry to `Docs/HOURLY_LOG.md`, commit, and push.

> **Build vs. compile note.** This (Linux) side authors and edits C++, docs, and
> design data. It cannot compile or PIE-test — that happens on the Windows/Unreal
> side. So new C++ must follow existing patterns closely and ship with a
> "Windows-side verification" note rather than a local build. Prefer changes that
> are also checkable here (data + `validate_design_data.py`).

---

## Current State (what already exists)

Source: `Source/AbyssalEarth/` (full inventory current as of this doc).

| Domain | Exists | Class(es) |
| --- | --- | --- |
| Player / movement | Basic FP walk/sprint/crouch/look (Enhanced Input) | `AAbyssalExplorerCharacter`, `AAbyssalEarthGameMode` |
| Scanning / discovery / journal | Scan → register → journal → categorize | `UScannerComponent`, `ADiscoveryActor`, `UDiscoverySubsystem`, `UAbyssalScannerReadoutWidget`, `UAbyssalJournalWidget` |
| Objectives | Linear, **hardcoded** 7-step route | `UObjectiveSubsystem`, `AObjectiveTriggerActor` |
| Navigation | Placeable persistent beacons | `ABeaconActor`, `UBeaconSubsystem` |
| Health | Health/damage/death only | `UAbyssalHealthComponent` |
| Audio | Event→cue routing (dispatch only, no playback) | `UAbyssalAudioCueSubsystem` |
| Hazards | One cyclic radial-damage vent | `AEmberVentHazard` |
| Save/load | Discoveries + beacons, single shared slot | `UDiscoverySaveGame` |
| Utility | BP subsystem accessors | `UAbyssalGameplayLibrary` |

This is enough for the **Luminous Rift** scan/explore/beacon loop. It is **not**
enough for the prologue, fabrication, multi-map travel, or the survival/traversal
themes of biomes 2–6.

---

## Gap Analysis: systems required by the full design

Mapped to the story (`Docs/NARRATIVE_FOUNDATION.md`) and biomes
(`Docs/WORLD_ATLAS.md`). "Status" = current implementation status.

| # | System | Needed by | Status |
| --- | --- | --- | --- |
| 1 | Save/persistence rework | Everything that must survive reload/map travel | Missing |
| 2 | Data-driven objectives + progress persistence | Prologue + 5-act arc, per-map objectives | Partial (hardcoded, not saved) |
| 3 | Interaction / "use" system | Prologue door pry; Act 3 operate machines; terminals; harvesting | Missing |
| 4 | Inventory / resources | Act 4 fabrication; harvestable discoveries | Missing |
| 5 | Fabrication / crafting + recipe unlocks | Acts 3–4 ("Make the Machine Answer", "Build a Way Out") | Missing |
| 6 | Survival vitals (oxygen/pressure, temperature, stamina) | Abyssal theme; Mantle Garden heat; pacing | Missing (only raw health) |
| 7 | World flow / level transitions | Six maps; Act 5 "Open the Rift" return | Missing |
| 8 | Traversal modifiers (gravity, climb, swim, tether) | Gravity Well, Inner Sea, Glassroot tunnels | Missing |
| 9 | Hazard framework (generalize the vent) | Every biome has a signature hazard | Partial (one hardcoded type) |
| 10 | Narrative / scripted-trigger + authored dialogue | Prologue beats 02–09 only (post-cavern is systemic) | Missing |
| 11 | HELIOS robot NPCs | Prologue Helios passage | Missing |
| 12 | Creatures / survival-pressure AI | "Survive monsters" tone goal | Missing |
| 13 | Equipment / upgrades | Scanner upgrades, suit insulation, traversal tools | Missing |
| 14 | Photo / observation mode | Awe pillar, marketing screenshots (planned early) | Missing |
| 15 | Abyssal Interface (diegetic LLM terminal) | Optional Act 2+ consult — **explicitly later** | Designed only (`Docs/ABYSSAL_INTERFACE_AI_SYSTEM.md`) |

---

## Dependency-ordered build plan

Each entry lists **proposed C++**, the **key API**, **data** it needs, and
**verification**. Reuse existing patterns and `UAbyssalGameplayLibrary` for BP
access. New subsystems should add accessors there.

### Phase A — Foundations (unblock everything)

**A1. Save/persistence rework.** Today two subsystems share one fixed
`UDiscoverySaveGame` slot and only persist discoveries + beacons. Before adding
more persisted systems, introduce a central save owner.
- *C++:* `UAbyssalSaveSubsystem` (GameInstance) owning a single
  `UAbyssalProfileSaveGame` with named slots; existing
  `FAbyssalDiscoveryEntry` / `FAbyssalBeaconSaveData` move under it. Discovery and
  Beacon subsystems read/write through it instead of `UGameplayStatics` directly.
- *API:* `SaveProfile()`, `LoadProfile(slot)`, `GetActiveSlot()`,
  per-domain `RegisterSaveProvider(IAbyssalSaveProvider*)` so each subsystem
  serializes its own blob.
- *Data:* none (engine SaveGame).
- *Verify (Windows):* save → reload restores discoveries + beacons exactly as
  today; add a second slot and confirm isolation.

**A2. Data-driven objectives + progress persistence.** Route is hardcoded in
`UObjectiveSubsystem::BuildDefaultRoute`; `Content/Design/MainObjectiveArc.csv`
already mirrors it (the validator cross-checks IDs).
- *C++:* load the route from a `UDataTable` (row struct mirroring
  `FAbyssalObjectiveStep`) instead of hardcoding; persist
  `CurrentObjectiveIndex` + `CompletedObjectiveIds` via A1.
- *Data:* promote `MainObjectiveArc.csv` to the DataTable source of truth; keep
  `validate_design_data.py`'s ID cross-check pointed at it.
- *Verify:* `AbyssalDebugAdvanceObjective` walks the full arc; progress survives
  reload.

**A3. Interaction / "use" system.** Foundational for the prologue and Act 3.
- *C++:* `UInteractableInterface` (UINTERFACE) with `CanInteract`,
  `GetInteractPrompt`, `OnInteract(instigator)`, optional hold-duration; a
  `UInteractionComponent` on the character doing a forward trace each frame and
  exposing `OnFocusChanged` / `TryInteract()` for an `IA_Interact` input.
- *Data:* none.
- *Verify:* place a test actor implementing the interface; prompt appears, press
  interacts, hold variant fires after duration (prologue door pry, beat 08).

### Phase B — Core survival/fabrication loop

**B1. Inventory / resources.** Backs fabrication and harvesting.
- *C++:* `UAbyssalItemDefinition` (DataAsset: id, display, category, stack),
  `UInventoryComponent` (add/remove/query, `OnInventoryChanged`), and a
  harvestable interactable (an `ADiscoveryActor` sibling or component) yielding
  items. Persist via A1.
- *Data:* `Content/Design/ItemCatalog.csv` (+ validator coverage).
- *Verify:* harvest a node → item appears → persists across reload.

**B2. Fabrication / crafting + recipe unlocks.** Realizes Acts 3–4.
- *C++:* `UFabricationRecipe` (DataAsset: inputs, output, required discoveries),
  `UFabricationSubsystem` (`CanCraft`, `Craft`, `GetUnlockedRecipes`), a
  fabricator interactable. Unlock recipes when matching discoveries register
  (subscribe to `UDiscoverySubsystem::OnDiscoveryAdded`).
- *Data:* `Content/Design/FabricationRecipes.csv` (+ validator: inputs/outputs
  exist in ItemCatalog, discovery refs exist in DiscoveryCatalog).
- *Verify:* discovering the right entries unlocks a recipe; crafting consumes
  inputs and yields the output.

**B3. Survival vitals.** Generalize beyond raw health.
- *C++:* `UAbyssalVitalsComponent` (or discrete `UOxygenComponent`,
  `UTemperatureComponent`, `UStaminaComponent`) with drain/recover curves,
  thresholds, and `OnVitalChanged` / `OnVitalCritical`. Route hazard damage and
  environment exposure here; sprint draws stamina.
- *Data:* tunables on the component; per-zone exposure rates via volumes.
- *Verify:* heat zone raises temperature, insulation slows it, critical vital
  triggers damage through `UAbyssalHealthComponent`.

### Phase C — Maps and world

**C1. World flow / level transitions.** Required to have more than one map.
- *C++:* `UWorldFlowSubsystem`: `TravelToMap(id, entryTag)`, save-on-exit
  (A1), restore player at the tagged entry on arrive; a `ALevelTransitionActor`
  interactable (uses A3). Handles the Act 5 rift return.
- *Data:* map registry (extend `WorldMapManifest.csv`), per-map entry tags.
- *Verify:* walk through a transition actor, arrive in the second map at the
  correct entry, state preserved.

**C2. Hazard framework.** Generalize `AEmberVentHazard`.
- *C++:* extract `AAbyssalHazardBase` (phase state machine + damage routing);
  refactor the ember vent to derive from it; add derivations for biome signature
  hazards: brittle walkway (Fossil Sky), spore cloud (Glassroot), flood/electrical
  (Inner Sea), gravity hazard (Gravity Well), steam/heat vent (Mantle Garden).
- *Verify:* existing ember vent behavior unchanged after refactor; one new
  hazard type works.

**C3. Traversal modifiers.** Biome-specific movement.
- *C++:* `AReorientationVolume` / `UGravityModifierComponent` (Gravity Well),
  climb + swim states on the character (Glassroot tunnels, Inner Sea),
  tether/anchor for safety lines.
- *Verify:* gravity volume reorients the pawn predictably; swim works in a water
  volume.

**C4. Per-biome content scaffolding (repeats for maps 2–6).** For each of
Glassroot Forest, Inner Sea, Fossil Sky, Gravity Well, Mantle Garden, author the
data + docs the slice needs (this is mostly Linux-doable and a good loop staple):
`Docs/Maps/<MAP>.md` blockout, discovery-catalog rows, ambience rows, asset
manifest rows, then the map-specific hazard/traversal hookup from C2/C3.

### Phase D — Narrative, agents, and meta

**D1. Narrative / scripted-trigger + authored dialogue.** Only the prologue uses
authored dialogue; post-cavern stays systemic (hard rule in
`NARRATIVE_FOUNDATION.md`).
- *C++:* `UNarrativeTriggerComponent` / sequence hooks for prologue beats; a
  minimal data-driven dialogue/caption widget for the briefing display, Helios
  warnings, and the two scripted player lines.
- *Data:* `PrologueSequence.csv` already defines the 9 beats.

**D2. HELIOS robot NPCs.** Prologue Helios passage only.
- *C++:* `AHeliosRobot` with interaction (A3) → caption dialogue (D1); no combat.

**D3. Creatures / survival-pressure AI.** Non-combat-first threat.
- *C++:* `AAbyssalCreature` + perception/avoidance; tune for pressure, not
  shooter gameplay.

**D4. Photo / observation mode.** Supports the awe pillar.
- *C++:* `UObservationModeComponent` (free/lock camera, hide HUD, capture).

**D5. Abyssal Interface (LATER).** Diegetic terminal consult. Keep deferred until
the core loop and several maps exist; design is in
`Docs/ABYSSAL_INTERFACE_AI_SYSTEM.md` with the context schema/response modes in
`Content/Design/`.

---

## Cross-cutting concerns

- **Localization:** hardcoded English strings exist in
  `UAbyssalScannerReadoutWidget` and elsewhere; wrap user-facing text in
  `NSLOCTEXT`/`FText` like `UObjectiveSubsystem` already does.
- **Controller/HUD ownership:** there is no C++ `APlayerController`/`AHUD`. Decide
  whether input-mapping and HUD ownership should move there as systems grow.
- **Equipment/upgrades (#13):** scanner radius etc. are fixed `UPROPERTY`s; once
  fabrication (B2) exists, route upgrades through it.
- **Validation:** every new design CSV gets a spec + check in
  `Scripts/validate_design_data.py` so docs/code/data cannot silently drift (the
  pattern used for objective IDs and discovery categories).

---

## Status checklist

Update as systems land. `[ ]` not started · `[~]` in progress · `[x]` done.

- [ ] A1 Save/persistence rework
- [~] A2 Data-driven objectives (hardcoded route + CSV mirror exist; not yet data-driven or persisted)
- [~] A3 Interaction / use system — `IAbyssalInteractable` interface + `UInteractionComponent` added (C++ authored on Linux, **Windows compile/PIE pending**); character + `IA_Interact` input wiring is the next step
- [ ] B1 Inventory / resources
- [ ] B2 Fabrication / recipe unlocks
- [ ] B3 Survival vitals
- [ ] C1 World flow / level transitions
- [~] C2 Hazard framework (one concrete hazard exists; not yet generalized)
- [ ] C3 Traversal modifiers
- [~] C4 Per-biome content scaffolding — Glassroot Forest blockout done (`Docs/Maps/GLASSROOT_FOREST.md`); Inner Sea / Fossil Sky / Gravity Well / Mantle Garden pending
- [ ] D1 Narrative triggers + prologue dialogue
- [ ] D2 HELIOS robot NPCs
- [ ] D3 Creatures / survival AI
- [ ] D4 Photo / observation mode
- [ ] D5 Abyssal Interface (deferred)
