#include "DiscoverySubsystem.h"
#include "DiscoverySaveGame.h"
#include "Kismet/GameplayStatics.h"

void UDiscoverySubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    LoadDiscoveries();
}

bool UDiscoverySubsystem::RegisterDiscovery(FName DiscoveryId)
{
    if (DiscoveryId.IsNone())
    {
        return false;
    }

    FAbyssalDiscoveryEntry Entry;
    Entry.DiscoveryId = DiscoveryId;
    Entry.DisplayName = FText::FromName(DiscoveryId);
    Entry.Category = EDiscoveryCategory::Geology;
    return RegisterDiscoveryEntry(Entry);
}

bool UDiscoverySubsystem::RegisterDiscoveryEntry(const FAbyssalDiscoveryEntry& Entry)
{
    if (Entry.DiscoveryId.IsNone())
    {
        return false;
    }

    const bool bAlreadyKnown = Entries.Contains(Entry.DiscoveryId);
    Entries.Add(Entry.DiscoveryId, Entry);

    if (!bAlreadyKnown)
    {
        OnDiscoveryAdded.Broadcast(Entry);
        SaveDiscoveries();
    }

    return !bAlreadyKnown;
}

bool UDiscoverySubsystem::IsDiscovered(FName DiscoveryId) const
{
    return Entries.Contains(DiscoveryId);
}

TArray<FName> UDiscoverySubsystem::GetDiscoveredIds() const
{
    TArray<FName> Ids;
    Entries.GetKeys(Ids);
    return Ids;
}

TArray<FAbyssalDiscoveryEntry> UDiscoverySubsystem::GetDiscoveredEntries() const
{
    TArray<FAbyssalDiscoveryEntry> Result;
    Result.Reserve(Entries.Num());
    for (const TPair<FName, FAbyssalDiscoveryEntry>& Pair : Entries)
    {
        Result.Add(Pair.Value);
    }
    return Result;
}

TArray<FAbyssalDiscoveryEntry> UDiscoverySubsystem::GetDiscoveredEntriesByCategory(EDiscoveryCategory Category) const
{
    TArray<FAbyssalDiscoveryEntry> Result;
    for (const TPair<FName, FAbyssalDiscoveryEntry>& Pair : Entries)
    {
        if (Pair.Value.Category == Category)
        {
            Result.Add(Pair.Value);
        }
    }
    return Result;
}

bool UDiscoverySubsystem::GetDiscoveryEntry(FName DiscoveryId, FAbyssalDiscoveryEntry& OutEntry) const
{
    if (const FAbyssalDiscoveryEntry* Found = Entries.Find(DiscoveryId))
    {
        OutEntry = *Found;
        return true;
    }
    return false;
}

int32 UDiscoverySubsystem::GetDiscoveredCount() const
{
    return Entries.Num();
}

void UDiscoverySubsystem::SaveDiscoveries()
{
    UDiscoverySaveGame* SaveGame = Cast<UDiscoverySaveGame>(
        UGameplayStatics::LoadGameFromSlot(SaveSlotName, SaveUserIndex));

    if (!SaveGame)
    {
        SaveGame = Cast<UDiscoverySaveGame>(
            UGameplayStatics::CreateSaveGameObject(UDiscoverySaveGame::StaticClass()));
    }

    if (!SaveGame)
    {
        return;
    }

    SaveGame->DiscoveredIds.Reset(Entries.Num());
    SaveGame->DiscoveredEntries.Reset(Entries.Num());
    for (const TPair<FName, FAbyssalDiscoveryEntry>& Pair : Entries)
    {
        SaveGame->DiscoveredIds.Add(Pair.Key);
        SaveGame->DiscoveredEntries.Add(Pair.Value);
    }
    UGameplayStatics::SaveGameToSlot(SaveGame, SaveSlotName, SaveUserIndex);
}

void UDiscoverySubsystem::ClearAllDiscoveries()
{
    Entries.Reset();
    SaveDiscoveries();
}

void UDiscoverySubsystem::LoadDiscoveries()
{
    Entries.Reset();

    USaveGame* LoadedObject = UGameplayStatics::LoadGameFromSlot(SaveSlotName, SaveUserIndex);
    UDiscoverySaveGame* SaveGame = Cast<UDiscoverySaveGame>(LoadedObject);
    if (!SaveGame)
    {
        return;
    }

    for (const FAbyssalDiscoveryEntry& Entry : SaveGame->DiscoveredEntries)
    {
        if (!Entry.DiscoveryId.IsNone())
        {
            Entries.Add(Entry.DiscoveryId, Entry);
        }
    }

    for (const FName& LegacyId : SaveGame->DiscoveredIds)
    {
        if (LegacyId.IsNone() || Entries.Contains(LegacyId))
        {
            continue;
        }

        FAbyssalDiscoveryEntry Entry;
        Entry.DiscoveryId = LegacyId;
        Entry.DisplayName = FText::FromName(LegacyId);
        Entry.Category = EDiscoveryCategory::Geology;
        Entries.Add(LegacyId, Entry);
    }
}
