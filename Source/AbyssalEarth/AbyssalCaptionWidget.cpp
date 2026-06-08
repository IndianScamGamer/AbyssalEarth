#include "AbyssalCaptionWidget.h"
#include "Engine/GameInstance.h"

UNarrativeSubsystem* UAbyssalCaptionWidget::GetNarrativeSubsystem() const
{
    if (const UGameInstance* GI = GetGameInstance())
    {
        return GI->GetSubsystem<UNarrativeSubsystem>();
    }
    return nullptr;
}

void UAbyssalCaptionWidget::NativeConstruct()
{
    Super::NativeConstruct();

    if (UNarrativeSubsystem* Narrative = GetNarrativeSubsystem())
    {
        Narrative->OnBeatStarted.AddDynamic(this, &UAbyssalCaptionWidget::HandleBeatStarted);
        Narrative->OnBeatFinished.AddDynamic(this, &UAbyssalCaptionWidget::HandleBeatFinished);
    }
}

void UAbyssalCaptionWidget::NativeDestruct()
{
    if (UNarrativeSubsystem* Narrative = GetNarrativeSubsystem())
    {
        Narrative->OnBeatStarted.RemoveDynamic(this, &UAbyssalCaptionWidget::HandleBeatStarted);
        Narrative->OnBeatFinished.RemoveDynamic(this, &UAbyssalCaptionWidget::HandleBeatFinished);
    }

    Super::NativeDestruct();
}

void UAbyssalCaptionWidget::HandleBeatStarted(const FAbyssalNarrativeBeat& Beat)
{
    ShowCaption(Beat.Speaker, Beat.Caption, Beat.Duration);
}

void UAbyssalCaptionWidget::HandleBeatFinished(FName BeatId)
{
    HideCaption();
}
