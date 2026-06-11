#include "AbyssalObjectiveWidget.h"

void UAbyssalObjectiveWidget::NativeConstruct()
{
    Super::NativeConstruct();

    UGameInstance* GI = GetGameInstance();
    if (!GI)
    {
        return;
    }

    if (UObjectiveSubsystem* ObjSub = GI->GetSubsystem<UObjectiveSubsystem>())
    {
        ObjSub->OnObjectiveChanged.AddDynamic(this, &UAbyssalObjectiveWidget::HandleObjectiveChanged);
        ObjSub->OnRouteCompleted.AddDynamic(this, &UAbyssalObjectiveWidget::HandleRouteCompleted);

        // Initialise with current objective if one is active
        const FAbyssalObjectiveStep Current = ObjSub->GetCurrentObjective();
        if (!Current.ObjectiveId.IsNone())
        {
            LastObjectiveTitle = Current.Title;
            ShowObjective(Current.Title, Current.Description);
        }
    }
}

void UAbyssalObjectiveWidget::NativeDestruct()
{
    if (UGameInstance* GI = GetGameInstance())
    {
        if (UObjectiveSubsystem* ObjSub = GI->GetSubsystem<UObjectiveSubsystem>())
        {
            ObjSub->OnObjectiveChanged.RemoveDynamic(this, &UAbyssalObjectiveWidget::HandleObjectiveChanged);
            ObjSub->OnRouteCompleted.RemoveDynamic(this, &UAbyssalObjectiveWidget::HandleRouteCompleted);
        }
    }
    Super::NativeDestruct();
}

void UAbyssalObjectiveWidget::HandleObjectiveChanged(const FAbyssalObjectiveStep& Objective)
{
    // Fire completion notification for the previous objective first
    if (!LastObjectiveTitle.IsEmpty() && !LastObjectiveTitle.EqualTo(Objective.Title))
    {
        OnObjectiveComplete(LastObjectiveTitle);
    }
    LastObjectiveTitle = Objective.Title;
    ShowObjective(Objective.Title, Objective.Description);
}

void UAbyssalObjectiveWidget::HandleRouteCompleted()
{
    if (!LastObjectiveTitle.IsEmpty())
    {
        OnObjectiveComplete(LastObjectiveTitle);
    }
    OnAllObjectivesComplete();
}
