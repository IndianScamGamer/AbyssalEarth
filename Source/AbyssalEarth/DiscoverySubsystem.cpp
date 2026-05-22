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

    const bool bAlreadyKnown = DiscoveredIds.Contains(DiscoveryId);
    DiscoveredIds.Add(DiscoveryId);

    if (!bAlreadyKnown)
    {
        SaveDiscoveries();
    }

    return !bAlreadyKnown;
}

bool UDiscoverySubsystem::IsDiscovered(FName DiscoveryId) const
{
    return DiscoveredIds.Contains(DiscoveryId);
}

TArray<FName> UDiscoverySubsystem::GetDiscoveredIds() const
{
    return DiscoveredIds.Array();
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

    SaveGame->DiscoveredIds = DiscoveredIds.Array();
    UGameplayStatics::SaveGameToSlot(SaveGame, SaveSlotName, SaveUserIndex);
}

void UDiscoverySubsystem::LoadDiscoveries()
{
    DiscoveredIds.Reset();

    USaveGame* LoadedObject = UGameplayStatics::LoadGameFromSlot(SaveSlotName, SaveUserIndex);
    UDiscoverySaveGame* SaveGame = Cast<UDiscoverySaveGame>(LoadedObject);
    if (!SaveGame)
    {
        return;
    }

    for (const FName& DiscoveryId : SaveGame->DiscoveredIds)
    {
        if (!DiscoveryId.IsNone())
        {
            DiscoveredIds.Add(DiscoveryId);
        }
    }
}
