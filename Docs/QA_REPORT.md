# AbyssalEarth — QA / Bug Review Report (Tick 24)

Full static review of all 119 C++ source files plus design CSVs, focused on
compile correctness, Unreal API misuse, cross-file consistency, and logic bugs.
No engine was available in the review environment, so this is a static pass;
all findings below were fixed in the same change.

## Summary

| Severity | Count | Status |
|----------|-------|--------|
| Compile-blocking | 9 classes of error across 21 files | **Fixed** |
| Data / asset-import bugs | 2 | **Fixed** |
| Logic / design notes | 3 | Documented below |

The root cause of most issues: systems authored in later ticks (13–22) were
written against assumed API names instead of the actual signatures in the
earlier base classes (ticks 3–10).

---

## Compile-blocking bugs (fixed)

### 1. Non-dynamic binding on dynamic multicast delegates
`AddLambda` / `AddUObject` / `FDelegateHandle` are not valid on
`DECLARE_DYNAMIC_MULTICAST_DELEGATE` types — only `AddDynamic`/`RemoveDynamic`
with exact-signature `UFUNCTION` handlers.
- `AbyssalHUDSubsystem.h/.cpp` — rewritten with 5 UFUNCTION handlers. Also
  fixed: `OnStaminaChanged` is one-param (float), not (float, bool).
- `AbyssalObjectiveWidget.h/.cpp` — rewritten; handler now takes
  `const FAbyssalObjectiveStep&` to match the delegate exactly.
- `AbyssalInventoryWidget.h/.cpp` — rewritten.

### 2. IAbyssalInteractable name/constness mismatches
The interface declares `CanInteract`, `GetInteractionPrompt`, `OnInteract`,
`OnBeginFocus`, `OnEndFocus` — all non-const. Four newer actors overrode
nonexistent `GetInteractPrompt` / `OnFocusBegin` / `OnFocusEnd` and added
`const` qualifiers that break `_Implementation` override matching:
- `CheckpointActor`, `AAbyssalPowerNode`, `AAbyssalRiftActor`,
  `AAbyssalInterfaceTerminal` — all corrected.
- `UAbyssalInteractionComponent` — `Execute_*` calls corrected to the real
  generated names.

### 3. Hazard subclasses written against a nonexistent base API
`AAbyssalHazardBase` exposes `bStartActive`, `SetHazardActive()`,
`GetCurrentPhase()`, `IdleDuration`, and BlueprintImplementableEvents for
phases (not C++-overridable). The six C2 subclasses referenced fictional
`bAutoActivate`, `ActivateHazard()`, `CurrentState`, and
`On*PhaseBegin_Implementation` overrides.
- Added a native hook to the base: `virtual void OnPhaseChanged(EHazardPhase)`
  called from `EnterPhase` (additive, no behaviour change for existing BP).
- Rewrote `ASteamVentHazard`, `AMagmaGeyserHazard`, `AMagmaPulseHazard`,
  `ABrittleWalkwaySection`, `ACeilingFragmentHazard`, `AGravityShearHazard`
  against the real API. Triggered hazards (walkway/ceiling) now use
  `IdleDuration = 0` + `SetHazardActive(true)` and deactivate for one-shot
  semantics; the steam vent registers its capsule via
  `RegisterDamagePrimitive` so the base overlap damage tick works.

### 4. Components attached to a null root
`AAbyssalHazardBase` creates no root component; subclasses called
`SetupAttachment(RootComponent)` on a null root. All four hazard subclass
constructors now create a `SceneRoot` first (matching `AEmberVentHazard`).

### 5. Enum referenced before declaration
`EAbyssalCreatureState` (AbyssalCreature.h) and `EAbyssalRiftState`
(AbyssalRiftActor.h) were used in delegate declarations above the `UENUM`
definitions. Reordered.

### 6. Duplicate delegate type definition
`FAbyssalFocusChangedSignature` was defined in both the legacy
`InteractionComponent.h` and the new `AbyssalInteractionComponent.h`.
Renamed the new one to `FAbyssalInteractionFocusSignature`.

### 7. Save blobs missing fields
- `FAbyssalWorldFlowSaveBlob` lacked `ActiveCheckpointId`
  (written by `UCheckpointSubsystem`). Added.
- `FAbyssalInventorySaveBlob` lacked `InstalledUpgradeIds`
  (written by `UAbyssalUpgradeSubsystem`). Added.

### 8. Nonexistent function calls
- `UDiscoverySubsystem::RegisterDiscovery(FName, FText)` — real signature is
  single-arg. `ObservationModeComponent` now calls the single-arg form;
  `UAbyssalScanComponent` uses `RegisterDiscoveryEntry` to preserve the
  display name.
- `UOxygenComponent::ResetOxygen()` — real API is `RefillOxygen()`.
  Fixed in `AAbyssalPlayerCharacter::RespawnAtCheckpoint`.

### 9. Missing module dependencies and includes
- `AbyssalEarth.Build.cs` — added `AIModule` + `GameplayTasks` (required by
  `AAbyssalCreature`'s `UAIPerceptionComponent`) and `Slate`/`SlateCore`.
- `CheckpointActor.h` now includes `CheckpointSubsystem.h` (delegate type),
  and the .cpp includes `AbyssalSaveSubsystem.h`.

---

## Data bugs (fixed)

1. **`DT_ItemDatabase.csv` category values** used `Material/Tool/Upgrade/Quest`
   but `EAbyssalItemCategory` only defines `Resource/Crafting/Equipment/
   Consumable` — the DataTable import would fail per-row. Remapped, and
   `FAbyssalItemTableRow`'s invalid default (`::Material`) corrected to
   `::Resource`.
2. **Missing item row**: `ITEM_UPGRADE_ARMOR_PLATING` was referenced by
   `RECIPE_ARMOR_PLATING` and `UAbyssalUpgradeSubsystem` but absent from the
   item database. Added.

---

## Logic / design notes (no code change)

1. **Power summing**: `AAbyssalPowerNode` propagation is last-writer-wins; two
   sources feeding one relay do not sum. The GRAVITY_WELL_LOWER and
   RIFT_CHAMBER docs describe additive networks — either sum inputs in a
   future pass or configure thresholds per-node in-editor. Cycle safety is
   handled by the per-node propagation guard.
2. **`CompleteObjective(OBJ_OPEN_RIFT)`** only succeeds if that objective is
   currently active; if a designer triggers the rift early it silently no-ops.
   Acceptable for the shipping flow (the stabiliser gates it), worth a log
   line later.
3. **Legacy duplicates retained**: `InteractionComponent`/`ScannerComponent`/
   `AbyssalExplorerCharacter` (legacy) coexist with
   `AbyssalInteractionComponent`/`AbyssalScanComponent`/
   `AbyssalPlayerCharacter` (current). No symbol clashes remain after the
   delegate rename; consolidation is editor-side cleanup once Blueprints
   choose a pawn class.

## Verification performed
- Grep-verified zero remaining references to the removed/incorrect APIs
  (`bAutoActivate`, `ActivateHazard`, `On*PhaseBegin`, `AddLambda`,
  `AddUObject`, `FDelegateHandle`, `GetInteractPrompt`,
  `OnFocusBegin/End_Implementation`, duplicate delegate name).
- Cross-checked every delegate binding signature against its declaration.
- Cross-checked all save-blob field accesses against `AbyssalProfileSaveGame.h`.
- Cross-checked CSV enum/ID values against C++ enums and item/recipe IDs.
