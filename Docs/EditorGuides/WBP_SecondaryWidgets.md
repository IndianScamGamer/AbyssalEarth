# Editor Guide: Secondary Widgets (Journal, Captions)

Covers the remaining HUD widget bases. Both are optional for the first
playable slice but cheap to stand up.

## WBP_Journal — discovery journal (parent: `UAbyssalJournalWidget`)

Full-screen overlay listing everything the player has scanned/observed.

### Layout
- Root overlay with dark translucent background `(0,0,0,0.8)`
- Left column: category tabs (one Button per `EDiscoveryCategory`)
- Right area: `ScrollBox` named `SB_Entries` of entry rows
  (`TB_DisplayName` + `TB_Description` per row)
- Header: `TB_EntryCount` ("{n} discoveries")

### Wiring
The C++ base already binds the DiscoverySubsystem. Use:
- `GetAllEntries()` / `GetEntriesByCategory(Category)` to build the list
- `GetEntryCount()` for the header
- Implement **Journal Opened** / **Journal Closed** → play open/close animations
- Implement **New Discovery Added (Entry)** → if the journal is closed, show a
  small toast ("New entry: {DisplayName}"); if open, refresh the list
- Implement **Entries Refreshed** → rebuild the visible list

Open/close from `BP_AbyssalPlayerController` (e.g. a `J`-key Input Action) by
calling `ToggleJournalOpen()` — the base tracks open state for you
(`IsJournalOpen`).

## WBP_Caption — narrative captions (parent: `UAbyssalCaptionWidget`)

Bottom-centre subtitle box driven by `UNarrativeSubsystem` beats.

### Layout
- Anchor bottom-centre `(0.5, 0.92)`
- `Border` named `B_CaptionBox` (translucent dark, padding 12) containing:
  - `TB_Speaker` — small caps, accent colour
  - `TB_Caption` — wrap at 700px, white

### Wiring
Implement the two BlueprintImplementableEvents:
```
Event ShowCaption (Speaker, Caption, Duration)
  → Set Text (TB_Speaker, Speaker)
  → Set Text (TB_Caption, Caption)
  → Play Animation (Anim_FadeIn)
  → Set Timer by Event (Duration) → call HideCaption flow

Event HideCaption
  → Play Animation (Anim_FadeOut)
```
The C++ base subscribes to the narrative subsystem — beats with caption text
arrive automatically once the widget is on screen. Add to viewport in
`BP_AbyssalPlayerController::BeginPlay` (Z-Order 2, above the vitals HUD).

## WBP_ScannerReadout — SKIP for the slice

`UAbyssalScannerReadoutWidget` binds the **legacy** `UScannerComponent`, which
the new `AAbyssalPlayerCharacter` does not carry (it uses
`UAbyssalScanComponent`). Do not add this widget to the slice HUD; scan
feedback already reaches the HUD through `UAbyssalScanComponent::OnScanHit`
and the discovery toast in WBP_Journal. The widget will either be ported to
`UAbyssalScanComponent` or deleted with the rest of the legacy pawn stack.
