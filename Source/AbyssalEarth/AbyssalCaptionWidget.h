#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "NarrativeSubsystem.h"
#include "AbyssalCaptionWidget.generated.h"

/**
 * Caption / subtitle widget base (roadmap D1). Binds to UNarrativeSubsystem and
 * forwards beats to Blueprint via ShowCaption / HideCaption implementable events,
 * where the UMG layout (speaker label, caption body, fade animation) lives.
 */
UCLASS(Abstract)
class ABYSSALEARTH_API UAbyssalCaptionWidget : public UUserWidget
{
    GENERATED_BODY()

public:
    virtual void NativeConstruct() override;
    virtual void NativeDestruct() override;

protected:
    /** Render a caption. Implement the UMG presentation in Blueprint. */
    UFUNCTION(BlueprintImplementableEvent, Category = "Narrative")
    void ShowCaption(const FText& Speaker, const FText& Caption, float Duration);

    /** Clear the caption (beat finished). Implement fade-out in Blueprint. */
    UFUNCTION(BlueprintImplementableEvent, Category = "Narrative")
    void HideCaption();

private:
    UFUNCTION()
    void HandleBeatStarted(const FAbyssalNarrativeBeat& Beat);

    UFUNCTION()
    void HandleBeatFinished(FName BeatId);

    UNarrativeSubsystem* GetNarrativeSubsystem() const;
};
