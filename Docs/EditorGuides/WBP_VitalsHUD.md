# Editor Guide: WBP_VitalsHUD

Widget Blueprint subclass of `UAbyssalVitalsWidget` (C++ base in
`Source/AbyssalEarth/AbyssalVitalsWidget.h`). The base class binds
`UAbyssalHUDSubsystem::OnVitalsUpdated` for you and pushes an initial
snapshot on construct — the Blueprint only has to implement **one event**
and lay out the bars.

> **Scale note:** `HealthPercent` / `OxygenPercent` / `StaminaPercent` are
> **0..1** fractions. `HeatPercent` / `PressurePercent` are **0..100** —
> divide by 100 before feeding a ProgressBar.

## 1. Create the Widget Blueprint

1. Content Browser → `Content/UI/` → **User Interface → Widget Blueprint**
2. Pick parent class: **AbyssalVitalsWidget**
3. Name: `WBP_VitalsHUD`

## 2. Layout (Designer panel)

Root: a `Canvas Panel` stretched full-screen; place sub-elements with
corner/edge anchors.

### Health Bar
- Widget: `ProgressBar` named `PB_Health`
- Anchor: bottom-left `(0.02, 0.88)`, size `(200, 16)`
- Fill Color: `(0.8, 0.1, 0.1, 1)` (red)

### Oxygen Meter
- Widget: `ProgressBar` named `PB_Oxygen` (or a radial material on an `Image`)
- Anchor: bottom-left, above the health bar
- Fill Color: `(0.4, 0.8, 1.0, 1)` (cyan)
- Create a widget animation `Anim_OxygenWarning`: opacity 1 → 0.3 → 1 over 0.5s, looping

### Stamina Bar
- Widget: `ProgressBar` named `PB_Stamina`
- Fill Color: `(0.2, 0.6, 1.0, 1)` (blue-white)

### Temperature Indicator (secondary)
- Widget: `ProgressBar` named `PB_Temperature`
- Fill Color: `(1.0, 0.4, 0.0, 1)` (orange)
- Default Visibility: **Collapsed**

### Pressure Indicator (secondary)
- Widget: `ProgressBar` named `PB_Pressure`
- Fill Color: `(0.5, 0.0, 0.8, 1)` (purple)
- Default Visibility: **Collapsed**

## 3. Implement the event (Event Graph)

Implement the single BlueprintImplementableEvent from the base class:

```
Event On Vitals Updated (Readout: AbyssalVitalReadout)
  → PB_Health.SetPercent(Readout.HealthPercent)
  → PB_Oxygen.SetPercent(Readout.OxygenPercent)
  → PB_Stamina.SetPercent(Readout.StaminaPercent)
  → PB_Temperature.SetPercent(Readout.HeatPercent / 100.0)
  → PB_Pressure.SetPercent(Readout.PressurePercent / 100.0)

  // Warnings / conditional visibility
  → If Readout.OxygenPercent < 0.2 AND Readout.bSubmerged:
        Play Animation (Anim_OxygenWarning, looping)
    Else: Stop Animation (Anim_OxygenWarning)
  → PB_Stamina.SetVisibility(Readout.StaminaPercent >= 0.95 ? Collapsed : Visible)
  → PB_Temperature.SetVisibility(Readout.HeatPercent > 10.0 ? Visible : Collapsed)
  → PB_Pressure.SetVisibility(Readout.PressurePercent > 5.0 ? Visible : Collapsed)
  → If Readout.bDead: Play Animation (Anim_DeathFade) [optional]
```

Useful flags on the readout struct: `bSubmerged`, `bOverheating`,
`bAbovePressureRating`, `bExhausted`, `bDead`.

## 4. Add to Viewport

In `BP_AbyssalPlayerController` Event Graph:

```
Event Begin Play
  → Create Widget (WBP_VitalsHUD, Owning Player = Self)
  → Add to Viewport (Z-Order = 0)
  → Store reference in variable "VitalsHUDWidget"
```

## 5. Verify

PIE → HUD appears at bottom-left with full bars (initial snapshot, no vital
change needed). Take damage → health bar decreases. Enter a water volume →
oxygen depletes; below 20% the warning animation pulses. Sprint → stamina
drains and the bar becomes visible. Stand in a heat zone → temperature bar
appears and fills.
