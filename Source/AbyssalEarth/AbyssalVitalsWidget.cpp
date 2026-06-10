#include "AbyssalVitalsWidget.h"

void UAbyssalVitalsWidget::NativeConstruct()
{
    Super::NativeConstruct();

    UGameInstance* GI = GetGameInstance();
    if (!GI)
    {
        return;
    }

    if (UAbyssalHUDSubsystem* HUD = GI->GetSubsystem<UAbyssalHUDSubsystem>())
    {
        HUD->OnVitalsUpdated.AddDynamic(this, &UAbyssalVitalsWidget::HandleVitalsUpdated);

        // Initial push so bars are correct before the first vital change fires
        OnVitalsUpdated(HUD->GetVitalReadout());
    }
}

void UAbyssalVitalsWidget::NativeDestruct()
{
    if (UGameInstance* GI = GetGameInstance())
    {
        if (UAbyssalHUDSubsystem* HUD = GI->GetSubsystem<UAbyssalHUDSubsystem>())
        {
            HUD->OnVitalsUpdated.RemoveDynamic(this, &UAbyssalVitalsWidget::HandleVitalsUpdated);
        }
    }
    Super::NativeDestruct();
}

void UAbyssalVitalsWidget::HandleVitalsUpdated(const FAbyssalVitalReadout& Readout)
{
    OnVitalsUpdated(Readout);
}
