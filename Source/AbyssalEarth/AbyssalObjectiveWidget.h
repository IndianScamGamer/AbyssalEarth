#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "ObjectiveSubsystem.h"
#include "AbyssalObjectiveWidget.generated.h"

/**
 * HUD widget base for displaying the current objective (roadmap J2).
 * Binds UObjectiveSubsystem::OnObjectiveChanged and OnRouteCompleted in
 * NativeConstruct; unbinds in NativeDestruct. Blueprint subclass implements
 * ShowObjective, OnObjectiveComplete, and OnAllObjectivesComplete to drive
 * the actual UMG animations.
 */
UCLASS(Abstract, Blueprintable)
class ABYSSALEARTH_API UAbyssalObjectiveWidget : public UUserWidget
{
    GENERATED_BODY()

protected:
    virtual void NativeConstruct() override;
    virtual void NativeDestruct() override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|HUD")
    void ShowObjective(const FText& Title, const FText& Description);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|HUD")
    void OnObjectiveComplete(const FText& CompletedTitle);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|HUD")
    void OnAllObjectivesComplete();

private:
    UFUNCTION()
    void HandleObjectiveChanged(FAbyssalObjectiveStep Step);

    UFUNCTION()
    void HandleRouteCompleted();

    FDelegateHandle ObjectiveChangedHandle;
    FDelegateHandle RouteCompletedHandle;

    // Track last-known title so we can pass it to OnObjectiveComplete
    UPROPERTY()
    FText LastObjectiveTitle;
};
