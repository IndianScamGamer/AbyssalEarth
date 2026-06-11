#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "AbyssalHUDSubsystem.h"
#include "AbyssalVitalsWidget.generated.h"

/**
 * HUD widget base for the vitals readout (health, oxygen, stamina,
 * temperature, pressure). Binds UAbyssalHUDSubsystem::OnVitalsUpdated in
 * NativeConstruct and pushes an initial snapshot so the bars are correct on
 * the first frame. Blueprint subclass implements OnVitalsUpdated to drive
 * the actual progress bars and warning animations.
 *
 * Scale note: HealthPercent/OxygenPercent/StaminaPercent are 0..1 fractions;
 * HeatPercent/PressurePercent are 0..100 (see FAbyssalVitalReadout).
 */
UCLASS(Abstract, Blueprintable)
class ABYSSALEARTH_API UAbyssalVitalsWidget : public UUserWidget
{
    GENERATED_BODY()

protected:
    virtual void NativeConstruct() override;
    virtual void NativeDestruct() override;

    /** Implement in the Blueprint subclass: update all bars from the snapshot. */
    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|HUD")
    void OnVitalsUpdated(const FAbyssalVitalReadout& Readout);

private:
    UFUNCTION()
    void HandleVitalsUpdated(const FAbyssalVitalReadout& Readout);
};
