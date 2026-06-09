#include "AbyssalObjectiveWidget.h"
#include "Kismet/GameplayStatics.h"

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
        ObjectiveChangedHandle = ObjSub->OnObjectiveChanged.AddUObject(
            this, &UAbyssalObjectiveWidget::HandleObjectiveChanged);
        RouteCompletedHandle = ObjSub->OnRouteCompleted.AddUObject(
            this, &UAbyssalObjectiveWidget::HandleRouteCompleted);

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
            ObjSub->OnObjectiveChanged.Remove(ObjectiveChangedHandle);
            ObjSub->OnRouteCompleted.Remove(RouteCompletedHandle);
        }
    }
    Super::NativeDestruct();
}

void UAbyssalObjectiveWidget::HandleObjectiveChanged(FAbyssalObjectiveStep Step)
{
    // Fire completion notification for the previous objective first
    if (!LastObjectiveTitle.IsEmpty())
    {
        OnObjectiveComplete(LastObjectiveTitle);
    }
    LastObjectiveTitle = Step.Title;
    ShowObjective(Step.Title, Step.Description);
}

void UAbyssalObjectiveWidget::HandleRouteCompleted()
{
    if (!LastObjectiveTitle.IsEmpty())
    {
        OnObjectiveComplete(LastObjectiveTitle);
    }
    OnAllObjectivesComplete();
}
