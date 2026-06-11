#include "DiscoverySubsystem.h"
#include "AbyssalProfileSaveGame.h"

void UDiscoverySubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    Collection.InitializeDependency(UAbyssalSaveSubsystem::StaticClass());
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->RegisterSaveProvider(this);
    }
}

void UDiscoverySubsystem::Deinitialize()
{
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->UnregisterSaveProvider(this);
    }
    Super::Deinitialize();
}

void UDiscoverySubsystem::OnSaveRequested(UAbyssalProfileSaveGame* SaveGame)
{
    SaveGame->Discoveries.DiscoveredEntries.Reset();
    SaveGame->Discoveries.DiscoveredIds_Legacy.Reset();
    for (const TPair<FName, FAbyssalDiscoveryEntry>& Pair : Entries)
    {
        SaveGame->Discoveries.DiscoveredEntries.Add(Pair.Key, Pair.Value);
    }
}

void UDiscoverySubsystem::OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame)
{
    Entries.Reset();
    for (const TPair<FName, FAbyssalDiscoveryEntry>& Pair : SaveGame->Discoveries.DiscoveredEntries)
    {
        if (!Pair.Key.IsNone())
        {
            Entries.Add(Pair.Key, Pair.Value);
        }
    }
    for (const FName& LegacyId : SaveGame->Discoveries.DiscoveredIds_Legacy)
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

    // First write wins: a rich entry from the scanner (real display name,
    // category) must not be clobbered by a later bare RegisterDiscovery(Id)
    // from observation-mode tag scans.
    if (Entries.Contains(Entry.DiscoveryId))
    {
        return false;
    }

    Entries.Add(Entry.DiscoveryId, Entry);
    OnDiscoveryAdded.Broadcast(Entry);
    // Disk write deferred to next SaveActiveSlot call; no per-discovery flush.
    return true;
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
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->SaveActiveSlot();
    }
}

void UDiscoverySubsystem::LoadDiscoveries()
{
    // Load is now driven by UAbyssalSaveSubsystem::LoadSlot -> OnLoadCompleted.
}

void UDiscoverySubsystem::ClearAllDiscoveries()
{
    Entries.Reset();
    SaveDiscoveries();
}
