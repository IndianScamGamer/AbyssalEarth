#include "WorldFlowSubsystem.h"
#include "AbyssalProfileSaveGame.h"
#include "Kismet/GameplayStatics.h"

void UWorldFlowSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    Collection.InitializeDependency(UAbyssalSaveSubsystem::StaticClass());
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->RegisterSaveProvider(this);
    }
}

void UWorldFlowSubsystem::Deinitialize()
{
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->UnregisterSaveProvider(this);
    }
    Super::Deinitialize();
}

void UWorldFlowSubsystem::OnSaveRequested(UAbyssalProfileSaveGame* SaveGame)
{
    SaveGame->WorldFlow.LastMapId = LastMapId;
    SaveGame->WorldFlow.LastEntryTag = LastEntryTag;
}

void UWorldFlowSubsystem::OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame)
{
    LastMapId = SaveGame->WorldFlow.LastMapId;
    LastEntryTag = SaveGame->WorldFlow.LastEntryTag;
}

void UWorldFlowSubsystem::TravelToMap(UObject* WorldContextObject, FName MapId, FName EntryTag)
{
    if (MapId.IsNone())
    {
        return;
    }

    LastMapId = MapId;
    LastEntryTag = EntryTag;

    OnPreTravel.Broadcast(MapId, EntryTag);

    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->SaveActiveSlot();
    }

    UGameplayStatics::OpenLevel(WorldContextObject, MapId);
}
