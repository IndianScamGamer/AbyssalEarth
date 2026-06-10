# Editor Guide: WBP_VitalsHUD

Widget Blueprint subclass of `UAbyssalHUDWidget` (the existing C++ HUD base). Displays the five vital readouts bound through `UAbyssalHUDSubsystem`.

## 1. Create the Widget Blueprint

1. Content Browser → `Content/UI/` → **User Interface → Widget Blueprint**
2. Parent class: **AbyssalHUDWidget**
3. Name: `WBP_VitalsHUD`

## 2. Layout (Designer panel)

Recommended anchor: stretch-fill the full screen, then place sub-elements with anchors at screen corners/edges.

### Health Bar
- Widget: `UProgressBar` named `PB_Health`
- Anchor: bottom-left corner `(0.02, 0.88)`, size `(200, 16)`
- Fill Color: `(0.8, 0.1, 0.1, 1)` (red)
- Percent binding: `Get Health Percent` from `UAbyssalHUDSubsystem`

### Oxygen Meter (circular)
- Widget: `UCircularThrobber` or a custom radial `UImage` driven by material
- Anchor: bottom-left near health bar
- Bind fill percentage to `Get Oxygen Percent`
- Below 20%: trigger a **pulsing** animation (Timeline → opacity 1→0.3→1, 0.5s loop)

### Stamina Bar
- Widget: `UProgressBar` named `PB_Stamina`
- Fill Color: `(0.2, 0.6, 1.0, 1)` (blue-white)
- Bind percent to `Get Stamina Percent`
- Visibility binding: **Collapsed** when percent ≥ 0.95 (fades out when full)

### Temperature Indicator (secondary)
- Widget: `UTextBlock` + `UProgressBar` named `PB_Temperature`
- Fill Color: `(1.0, 0.4, 0.0, 1)` (orange)
- Visibility: **Collapsed** unless `Get Heat Percent > 0.1`

### Pressure Indicator (secondary)
- Widget: `UProgressBar` named `PB_Pressure`
- Fill Color: `(0.5, 0.0, 0.8, 1)` (purple)
- Visibility: **Collapsed** unless `Get Pressure Percent > 0.05`

## 3. Bind Data (Event Graph)

`UAbyssalHUDWidget` calls these BlueprintImplementableEvents — implement them:

```
Event OnHealthChanged (HealthComp, NewHealth, Delta)
  → Set Percent (PB_Health, NewHealth / HealthComp.MaxHealth)
  → [optional] Play Hit Flash animation if Delta < 0

Event OnOxygenChanged (OxygenPercent, bSubmerged)
  → Set Percent (oxygen meter, OxygenPercent)
  → Set Visibility (oxygen warning anim, OxygenPercent < 0.2 ? Visible : Collapsed)

Event OnStaminaChanged (StaminaPercent)
  → Set Percent (PB_Stamina, StaminaPercent)
  → Set Visibility (PB_Stamina, StaminaPercent < 0.95 ? Visible : Collapsed)

Event OnTemperatureChanged (HeatPercent, bInHeatZone)
  → Set Percent (PB_Temperature, HeatPercent)
  → Set Visibility (temperature row, HeatPercent > 0.1 ? Visible : Collapsed)

Event OnPressureChanged (PressurePercent, bAboveRating)
  → Set Percent (PB_Pressure, PressurePercent)
  → Set Visibility (pressure row, PressurePercent > 0.05 ? Visible : Collapsed)
```

## 4. Add to Viewport

In `BP_AbyssalPlayerController` Event Graph:

```
Event Begin Play
  → Create Widget (WBP_VitalsHUD, Owning Player = Self)
  → Add to Viewport (Z-Order = 0)
  → Store reference in variable "VitalsHUDWidget"
```

## 5. Verify

PIE → HUD appears at bottom-left. Take damage → health bar decreases. Dive under water volume → oxygen meter starts depleting. Sprint → stamina bar appears and drains.
