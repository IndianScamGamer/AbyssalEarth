#include "CheckpointSubsystem.h"
#include "AbyssalSaveSubsystem.h"
#include "AbyssalProfileSaveGame.h"

void UCheckpointSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    Collection.InitializeDependency(UAbyssalSaveSubsystem::StaticClass());
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->RegisterSaveProvider(this);
    }
}

void UCheckpointSubsystem::Deinitialize()
{
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->UnregisterSaveProvider(this);
    }
    Super::Deinitialize();
}

void UCheckpointSubsystem::OnSaveRequested(UAbyssalProfileSaveGame* SaveGame)
{
    SaveGame->WorldFlow.ActiveCheckpointId = ActiveCheckpointId;
}

void UCheckpointSubsystem::OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame)
{
    ActiveCheckpointId = SaveGame->WorldFlow.ActiveCheckpointId;
    // Note: Checkpoints themselves are re-registered each map load from actor BeginPlay;
    // we only restore which one is active from the save.
}

void UCheckpointSubsystem::RegisterCheckpoint(FName CheckpointId, FVector RespawnLocation, FName MapId)
{
    if (CheckpointId.IsNone())
    {
        return;
    }

    const int32 Existing = FindCheckpointIndex(CheckpointId);
    if (Existing != INDEX_NONE)
    {
        Checkpoints[Existing].RespawnLocation = RespawnLocation;
        Checkpoints[Existing].MapId = MapId;
        return;
    }

    FAbyssalCheckpointRecord Record;
    Record.CheckpointId = CheckpointId;
    Record.RespawnLocation = RespawnLocation;
    Record.MapId = MapId;
    Checkpoints.Add(Record);
}

bool UCheckpointSubsystem::SetActiveCheckpoint(FName CheckpointId)
{
    if (FindCheckpointIndex(CheckpointId) == INDEX_NONE)
    {
        return false;
    }
    if (ActiveCheckpointId == CheckpointId)
    {
        return true;
    }
    ActiveCheckpointId = CheckpointId;
    OnCheckpointActivated.Broadcast(CheckpointId);
    return true;
}

FVector UCheckpointSubsystem::GetRespawnLocation() const
{
    const int32 Idx = FindCheckpointIndex(ActiveCheckpointId);
    return Idx != INDEX_NONE ? Checkpoints[Idx].RespawnLocation : FVector::ZeroVector;
}

FName UCheckpointSubsystem::GetRespawnMapId() const
{
    const int32 Idx = FindCheckpointIndex(ActiveCheckpointId);
    return Idx != INDEX_NONE ? Checkpoints[Idx].MapId : NAME_None;
}

int32 UCheckpointSubsystem::FindCheckpointIndex(FName CheckpointId) const
{
    for (int32 i = 0; i < Checkpoints.Num(); ++i)
    {
        if (Checkpoints[i].CheckpointId == CheckpointId)
        {
            return i;
        }
    }
    return INDEX_NONE;
}
