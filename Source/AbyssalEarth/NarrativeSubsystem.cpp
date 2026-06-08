#include "NarrativeSubsystem.h"
#include "AbyssalProfileSaveGame.h"
#include "Engine/World.h"

void UNarrativeSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    Collection.InitializeDependency(UAbyssalSaveSubsystem::StaticClass());
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->RegisterSaveProvider(this);
    }
}

void UNarrativeSubsystem::Deinitialize()
{
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->UnregisterSaveProvider(this);
    }
    Super::Deinitialize();
}

void UNarrativeSubsystem::OnSaveRequested(UAbyssalProfileSaveGame* SaveGame)
{
    SaveGame->Narrative.PlayedBeatIds = PlayedBeatIds.Array();
}

void UNarrativeSubsystem::OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame)
{
    PlayedBeatIds.Reset();
    for (const FName& Id : SaveGame->Narrative.PlayedBeatIds)
    {
        if (!Id.IsNone())
        {
            PlayedBeatIds.Add(Id);
        }
    }
}

void UNarrativeSubsystem::SetBeatTable(UDataTable* InBeatTable)
{
    if (InBeatTable && InBeatTable->GetRowStruct() == FAbyssalNarrativeBeat::StaticStruct())
    {
        BeatTable = InBeatTable;
    }
}

bool UNarrativeSubsystem::HasPlayed(FName BeatId) const
{
    return PlayedBeatIds.Contains(BeatId);
}

bool UNarrativeSubsystem::PlayBeat(FName BeatId)
{
    if (BeatId.IsNone() || !BeatTable)
    {
        return false;
    }

    static const FString Context(TEXT("UNarrativeSubsystem::PlayBeat"));
    const FAbyssalNarrativeBeat* Beat = BeatTable->FindRow<FAbyssalNarrativeBeat>(BeatId, Context);
    if (!Beat)
    {
        return false;
    }

    if (Beat->bPlayOnce && PlayedBeatIds.Contains(BeatId))
    {
        return false;
    }

    if (IsPlaying())
    {
        Queue.Add(BeatId);
        return true;
    }

    StartBeat(BeatId, *Beat);
    return true;
}

void UNarrativeSubsystem::StartBeat(FName BeatId, const FAbyssalNarrativeBeat& Beat)
{
    ActiveBeatId = BeatId;
    if (Beat.bPlayOnce)
    {
        PlayedBeatIds.Add(BeatId);
    }

    OnBeatStarted.Broadcast(Beat);

    if (Beat.Duration > 0.0f)
    {
        if (UWorld* World = GetWorld())
        {
            World->GetTimerManager().SetTimer(
                BeatTimerHandle, this, &UNarrativeSubsystem::FinishActiveBeat, Beat.Duration, false);
        }
    }
    // Duration <= 0: caption persists until StopAll() or the next PlayBeat that finishes it.
}

void UNarrativeSubsystem::FinishActiveBeat()
{
    if (ActiveBeatId.IsNone())
    {
        return;
    }

    const FName Finished = ActiveBeatId;
    ActiveBeatId = NAME_None;
    OnBeatFinished.Broadcast(Finished);

    AdvanceQueue();
}

void UNarrativeSubsystem::AdvanceQueue()
{
    while (Queue.Num() > 0)
    {
        const FName NextId = Queue[0];
        Queue.RemoveAt(0);

        if (!BeatTable)
        {
            return;
        }

        static const FString Context(TEXT("UNarrativeSubsystem::AdvanceQueue"));
        const FAbyssalNarrativeBeat* Beat = BeatTable->FindRow<FAbyssalNarrativeBeat>(NextId, Context);
        if (!Beat)
        {
            continue;
        }

        if (Beat->bPlayOnce && PlayedBeatIds.Contains(NextId))
        {
            continue;
        }

        StartBeat(NextId, *Beat);
        return;
    }
}

void UNarrativeSubsystem::StopAll()
{
    Queue.Reset();

    if (UWorld* World = GetWorld())
    {
        World->GetTimerManager().ClearTimer(BeatTimerHandle);
    }

    if (!ActiveBeatId.IsNone())
    {
        const FName Finished = ActiveBeatId;
        ActiveBeatId = NAME_None;
        OnBeatFinished.Broadcast(Finished);
    }
}
