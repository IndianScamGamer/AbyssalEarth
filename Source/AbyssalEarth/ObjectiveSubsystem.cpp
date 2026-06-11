#include "ObjectiveSubsystem.h"
#include "AbyssalProfileSaveGame.h"

void UObjectiveSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    Collection.InitializeDependency(UAbyssalSaveSubsystem::StaticClass());
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->RegisterSaveProvider(this);
    }

    BuildDefaultRoute();
    ResetRoute();
}

void UObjectiveSubsystem::Deinitialize()
{
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->UnregisterSaveProvider(this);
    }
    Super::Deinitialize();
}

void UObjectiveSubsystem::OnSaveRequested(UAbyssalProfileSaveGame* SaveGame)
{
    SaveGame->Objectives.CurrentObjectiveIndex = CurrentObjectiveIndex;
    SaveGame->Objectives.CompletedObjectiveIds = CompletedObjectiveIds.Array();
}

void UObjectiveSubsystem::OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame)
{
    CompletedObjectiveIds.Reset();
    for (const FName& Id : SaveGame->Objectives.CompletedObjectiveIds)
    {
        if (!Id.IsNone())
        {
            CompletedObjectiveIds.Add(Id);
        }
    }

    const int32 SavedIndex = SaveGame->Objectives.CurrentObjectiveIndex;
    if (SavedIndex == INDEX_NONE || RouteObjectives.IsValidIndex(SavedIndex))
    {
        CurrentObjectiveIndex = SavedIndex;
    }
    else
    {
        // Saved index outside the current route (route changed); clamp to end.
        CurrentObjectiveIndex = RouteObjectives.Num() > 0 ? RouteObjectives.Num() - 1 : INDEX_NONE;
    }

    BroadcastCurrentObjective();
}

int32 UObjectiveSubsystem::BuildRouteFromTable(UDataTable* RouteTable)
{
    if (!RouteTable || RouteTable->GetRowStruct() != FAbyssalObjectiveTableRow::StaticStruct())
    {
        return 0;
    }

    RouteObjectives.Reset();

    static const FString Context(TEXT("UObjectiveSubsystem::BuildRouteFromTable"));
    for (const FName& RowName : RouteTable->GetRowNames())
    {
        const FAbyssalObjectiveTableRow* Row = RouteTable->FindRow<FAbyssalObjectiveTableRow>(RowName, Context);
        if (!Row)
        {
            continue;
        }

        FAbyssalObjectiveStep Step;
        Step.ObjectiveId = RowName;
        Step.Title = Row->Title;
        Step.Description = Row->Description;
        RouteObjectives.Add(Step);
    }

    ResetRoute();
    return RouteObjectives.Num();
}

void UObjectiveSubsystem::ResetRoute()
{
    CompletedObjectiveIds.Reset();
    CurrentObjectiveIndex = RouteObjectives.Num() > 0 ? 0 : INDEX_NONE;
    BroadcastCurrentObjective();
}

bool UObjectiveSubsystem::CompleteObjective(FName ObjectiveId)
{
    if (ObjectiveId.IsNone() || !IsObjectiveActive(ObjectiveId))
    {
        UE_LOG(LogTemp, Warning,
            TEXT("UObjectiveSubsystem::CompleteObjective — '%s' is not currently active (already complete, not in route, or wrong order). Call is a no-op."),
            *ObjectiveId.ToString());
        return false;
    }

    CompletedObjectiveIds.Add(ObjectiveId);
    OnObjectiveCompleted.Broadcast(ObjectiveId);

    if (CurrentObjectiveIndex + 1 >= RouteObjectives.Num())
    {
        CurrentObjectiveIndex = INDEX_NONE;
        OnRouteCompleted.Broadcast();
        return true;
    }

    ++CurrentObjectiveIndex;
    BroadcastCurrentObjective();
    return true;
}

bool UObjectiveSubsystem::CompleteCurrentObjective()
{
    if (IsRouteComplete())
    {
        return false;
    }

    return CompleteObjective(RouteObjectives[CurrentObjectiveIndex].ObjectiveId);
}

bool UObjectiveSubsystem::AdvanceToObjective(FName ObjectiveId)
{
    if (IsRouteComplete())
    {
        return false;
    }

    const int32 TargetIndex = FindObjectiveIndex(ObjectiveId);
    if (TargetIndex == INDEX_NONE || TargetIndex <= CurrentObjectiveIndex)
    {
        return false;
    }

    for (int32 Index = CurrentObjectiveIndex; Index < TargetIndex; ++Index)
    {
        CompletedObjectiveIds.Add(RouteObjectives[Index].ObjectiveId);
        OnObjectiveCompleted.Broadcast(RouteObjectives[Index].ObjectiveId);
    }

    CurrentObjectiveIndex = TargetIndex;
    BroadcastCurrentObjective();
    return true;
}

bool UObjectiveSubsystem::IsObjectiveActive(FName ObjectiveId) const
{
    return !IsRouteComplete() && RouteObjectives[CurrentObjectiveIndex].ObjectiveId == ObjectiveId;
}

bool UObjectiveSubsystem::IsObjectiveComplete(FName ObjectiveId) const
{
    return CompletedObjectiveIds.Contains(ObjectiveId);
}

bool UObjectiveSubsystem::IsRouteComplete() const
{
    return CurrentObjectiveIndex == INDEX_NONE || !RouteObjectives.IsValidIndex(CurrentObjectiveIndex);
}

FAbyssalObjectiveStep UObjectiveSubsystem::GetCurrentObjective() const
{
    if (IsRouteComplete())
    {
        return FAbyssalObjectiveStep();
    }

    return RouteObjectives[CurrentObjectiveIndex];
}

TArray<FAbyssalObjectiveStep> UObjectiveSubsystem::GetRouteObjectives() const
{
    return RouteObjectives;
}

int32 UObjectiveSubsystem::GetCurrentObjectiveIndex() const
{
    return IsRouteComplete() ? INDEX_NONE : CurrentObjectiveIndex;
}

int32 UObjectiveSubsystem::GetCompletedObjectiveCount() const
{
    return CompletedObjectiveIds.Num();
}

int32 UObjectiveSubsystem::GetRouteObjectiveCount() const
{
    return RouteObjectives.Num();
}

FAbyssalObjectiveProgress UObjectiveSubsystem::GetObjectiveProgress() const
{
    FAbyssalObjectiveProgress Progress;
    Progress.TotalSteps = RouteObjectives.Num();
    Progress.CompletedSteps = CompletedObjectiveIds.Num();
    Progress.bRouteComplete = IsRouteComplete();

    if (Progress.bRouteComplete)
    {
        Progress.CurrentStepNumber = Progress.TotalSteps;
        Progress.CompletedSteps = Progress.TotalSteps;
        Progress.ProgressText = FText::Format(
            NSLOCTEXT("AbyssalEarthObjectives", "RouteCompleteProgress", "{0}/{1} route complete"),
            FText::AsNumber(Progress.CompletedSteps),
            FText::AsNumber(Progress.TotalSteps));
        return Progress;
    }

    Progress.CurrentStepNumber = CurrentObjectiveIndex + 1;
    Progress.ProgressText = FText::Format(
        NSLOCTEXT("AbyssalEarthObjectives", "RouteActiveProgress", "{0}/{1} objectives"),
        FText::AsNumber(Progress.CurrentStepNumber),
        FText::AsNumber(Progress.TotalSteps));

    return Progress;
}

FText UObjectiveSubsystem::GetObjectiveHudText() const
{
    if (IsRouteComplete())
    {
        return NSLOCTEXT("AbyssalEarthObjectives", "RouteCompleteHudText", "Rift opened - surface return achieved");
    }

    const FAbyssalObjectiveStep& Objective = RouteObjectives[CurrentObjectiveIndex];
    const FAbyssalObjectiveProgress Progress = GetObjectiveProgress();
    return FText::Format(
        NSLOCTEXT("AbyssalEarthObjectives", "ObjectiveHudText", "{0}: {1}"),
        Progress.ProgressText,
        Objective.Title);
}

void UObjectiveSubsystem::BuildDefaultRoute()
{
    RouteObjectives.Reset();

    auto AddObjective = [this](const TCHAR* ObjectiveId, const FText& Title, const FText& Description)
    {
        FAbyssalObjectiveStep Step;
        Step.ObjectiveId = FName(ObjectiveId);
        Step.Title = Title;
        Step.Description = Description;
        RouteObjectives.Add(Step);
    };

    AddObjective(
        TEXT("OBJ_VERIFY_HELIOS"),
        NSLOCTEXT("AbyssalEarthObjectives", "VerifyHeliosTitle", "Verify the AI Robot Fleet HELIOS's work"),
        NSLOCTEXT("AbyssalEarthObjectives", "VerifyHeliosDescription", "Descend into the elevator shaft and inspect the autonomous construction work."));

    AddObjective(
        TEXT("OBJ_SURVIVE"),
        NSLOCTEXT("AbyssalEarthObjectives", "SurviveTitle", "SURVIVE"),
        NSLOCTEXT("AbyssalEarthObjectives", "SurviveDescription", "Recover from the elevator crash, escape the wreck, and find a stable path through the Luminous Rift."));

    AddObjective(
        TEXT("OBJ_DISCOVER_PLACE"),
        NSLOCTEXT("AbyssalEarthObjectives", "DiscoverPlaceTitle", "DISCOVER WHAT THIS PLACE IS"),
        NSLOCTEXT("AbyssalEarthObjectives", "DiscoverPlaceDescription", "Scan alien structures, hostile environments, and impossible materials until the cavern begins to make sense."));

    AddObjective(
        TEXT("OBJ_MAKE_MACHINE_ANSWER"),
        NSLOCTEXT("AbyssalEarthObjectives", "MakeMachineAnswerTitle", "MAKE THE MACHINE ANSWER"),
        NSLOCTEXT("AbyssalEarthObjectives", "MakeMachineAnswerDescription", "Learn how to operate ancient systems, route power, and communicate with the Abyssal Interface."));

    AddObjective(
        TEXT("OBJ_BUILD_WAY_OUT"),
        NSLOCTEXT("AbyssalEarthObjectives", "BuildWayOutTitle", "BUILD A WAY OUT"),
        NSLOCTEXT("AbyssalEarthObjectives", "BuildWayOutDescription", "Use discovered alien technology to fabricate tools, stabilize energy, and construct a return mechanism."));

    AddObjective(
        TEXT("OBJ_OPEN_RIFT"),
        NSLOCTEXT("AbyssalEarthObjectives", "OpenRiftTitle", "OPEN THE RIFT"),
        NSLOCTEXT("AbyssalEarthObjectives", "OpenRiftDescription", "Activate the constructed rift and return to the surface."));
}

void UObjectiveSubsystem::BroadcastCurrentObjective()
{
    if (!IsRouteComplete())
    {
        OnObjectiveChanged.Broadcast(RouteObjectives[CurrentObjectiveIndex]);
    }
}

int32 UObjectiveSubsystem::FindObjectiveIndex(FName ObjectiveId) const
{
    for (int32 Index = 0; Index < RouteObjectives.Num(); ++Index)
    {
        if (RouteObjectives[Index].ObjectiveId == ObjectiveId)
        {
            return Index;
        }
    }

    return INDEX_NONE;
}
