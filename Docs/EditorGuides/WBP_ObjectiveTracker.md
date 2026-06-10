# Editor Guide: WBP_ObjectiveTracker

Widget Blueprint subclass of `UAbyssalObjectiveWidget`. Displays the current objective title and description; animates completion.

## 1. Create

1. `Content/UI/` → **Widget Blueprint**
2. Parent: **AbyssalObjectiveWidget**
3. Name: `WBP_ObjectiveTracker`

## 2. Layout

Anchor at top-right `(0.98, 0.04)`, right-aligned, auto-sized vertically.

Components:
- `Box_Objective` — `UVerticalBox` (full container, starts off-screen to the right)
  - `TB_ObjectiveLabel` — `UTextBlock`, font size 11, uppercase, grey `(0.5, 0.5, 0.5, 1)`, text: "OBJECTIVE"
  - `TB_ObjectiveTitle` — `UTextBlock`, font size 16, bold white
  - `TB_ObjectiveDescription` — `UTextBlock`, font size 12, grey, wrap at 300px

Add a **UWidgetAnimation** named `Anim_SlideIn`:
- Translate `Box_Objective` from `(400, 0)` → `(0, 0)` over 0.4s (ease out)
- Fade opacity 0 → 1 over 0.3s

Add **UWidgetAnimation** `Anim_Complete`:
- `TB_ObjectiveTitle` colour → green `(0.2, 1.0, 0.3, 1)` over 0.2s
- Strike-through effect (custom material or overlay line)
- Fade entire `Box_Objective` to 0 over 0.5s starting at 0.5s (total 1.0s)

## 3. Implement BlueprintImplementableEvents

```
Event ShowObjective (Title, Description)
  → Set Text (TB_ObjectiveTitle, Title)
  → Set Text (TB_ObjectiveDescription, Description)
  → Play Animation (Anim_SlideIn, from start)

Event OnObjectiveComplete (CompletedTitle)
  → Set Text (TB_ObjectiveTitle, CompletedTitle)
  → Play Animation (Anim_Complete, from start)

Event OnAllObjectivesComplete
  → [optional] Show full-screen "ROUTE COMPLETE" flash:
       Create WBP_RouteComplete widget → Add to Viewport → auto-destroy after 3s
```

## 4. Add to Viewport

In `BP_AbyssalPlayerController` BeginPlay (alongside WBP_VitalsHUD):

```
→ Create Widget (WBP_ObjectiveTracker)
→ Add to Viewport (Z-Order = 1)
```

## 5. Verify

PIE → start a level that has a DataTable objective route loaded in `BP_AbyssalGameMode`. Confirm the objective text slides in from the right. Trigger `ObjectiveSubsystem::CompleteCurrentObjective()` via the console exec `AbyssalDebugAdvanceObjective` — confirm the completion animation fires.
