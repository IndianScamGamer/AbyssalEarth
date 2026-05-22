#include "BeaconSubsystem.h"
#include "BeaconActor.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Kismet/GameplayStatics.h"

void UBeaconSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    LoadBeacons();
}

void UBeaconSubsystem::RegisterBeacon(ABeaconActor* Beacon)
{
    if (!Beacon)
    {
        return;
    }

    FAbyssalBeaconSaveData BeaconData;
    BeaconData.BeaconId = Beacon->GetBeaconId().IsValid() ? Beacon->GetBeaconId() : FGuid::NewGuid();
    BeaconData.Transform = Beacon->GetActorTransform();
    BeaconData.LightColor = Beacon->GetBeaconLightColor();

    if (BeaconData.BeaconId != Beacon->GetBeaconId())
    {
        Beacon->InitializeBeacon(BeaconData.BeaconId, BeaconData.LightColor);
    }

    const int32 ExistingIndex = FindBeaconIndex(BeaconData.BeaconId);
    if (ExistingIndex == INDEX_NONE)
    {
        SavedBeacons.Add(BeaconData);
    }
    else
    {
        SavedBeacons[ExistingIndex] = BeaconData;
    }

    RestoredBeaconIds.Add(BeaconData.BeaconId);
    SaveBeacons();
}

bool UBeaconSubsystem::RemoveBeacon(ABeaconActor* Beacon)
{
    if (!Beacon)
    {
        return false;
    }

    const FGuid BeaconId = Beacon->GetBeaconId();
    bool bMutated = false;

    const int32 ExistingIndex = FindBeaconIndex(BeaconId);
    if (ExistingIndex != INDEX_NONE)
    {
        SavedBeacons.RemoveAt(ExistingIndex);
        bMutated = true;
    }

    if (BeaconId.IsValid())
    {
        RestoredBeaconIds.Remove(BeaconId);
    }

    Beacon->Destroy();

    if (bMutated)
    {
        SaveBeacons();
    }

    return bMutated;
}

bool UBeaconSubsystem::RemoveBeaconById(UObject* WorldContextObject, FGuid BeaconId)
{
    UWorld* World = GEngine ? GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::ReturnNull) : nullptr;
    if (!World || !BeaconId.IsValid())
    {
        return false;
    }

    ABeaconActor* MatchedActor = nullptr;
    for (TActorIterator<ABeaconActor> It(World); It; ++It)
    {
        if (*It && It->GetBeaconId() == BeaconId)
        {
            MatchedActor = *It;
            break;
        }
    }

    if (MatchedActor)
    {
        return RemoveBeacon(MatchedActor);
    }

    const int32 ExistingIndex = FindBeaconIndex(BeaconId);
    if (ExistingIndex != INDEX_NONE)
    {
        SavedBeacons.RemoveAt(ExistingIndex);
        RestoredBeaconIds.Remove(BeaconId);
        SaveBeacons();
        return true;
    }

    return false;
}

int32 UBeaconSubsystem::RestoreSavedBeacons(UObject* WorldContextObject, TSubclassOf<ABeaconActor> BeaconClass)
{
    UWorld* World = GEngine ? GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::ReturnNull) : nullptr;
    if (!World || !BeaconClass)
    {
        return 0;
    }

    int32 RestoredCount = 0;
    for (const FAbyssalBeaconSaveData& BeaconData : SavedBeacons)
    {
        if (!BeaconData.BeaconId.IsValid() || RestoredBeaconIds.Contains(BeaconData.BeaconId))
        {
            continue;
        }

        ABeaconActor* Beacon = World->SpawnActor<ABeaconActor>(BeaconClass, BeaconData.Transform);
        if (!Beacon)
        {
            continue;
        }

        Beacon->InitializeBeacon(BeaconData.BeaconId, BeaconData.LightColor);
        RestoredBeaconIds.Add(BeaconData.BeaconId);
        ++RestoredCount;
    }

    return RestoredCount;
}

TArray<FAbyssalBeaconSaveData> UBeaconSubsystem::GetSavedBeacons() const
{
    return SavedBeacons;
}

void UBeaconSubsystem::SaveBeacons()
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

    SaveGame->SavedBeacons = SavedBeacons;
    UGameplayStatics::SaveGameToSlot(SaveGame, SaveSlotName, SaveUserIndex);
}

void UBeaconSubsystem::LoadBeacons()
{
    SavedBeacons.Reset();
    RestoredBeaconIds.Reset();

    USaveGame* LoadedObject = UGameplayStatics::LoadGameFromSlot(SaveSlotName, SaveUserIndex);
    UDiscoverySaveGame* SaveGame = Cast<UDiscoverySaveGame>(LoadedObject);
    if (!SaveGame)
    {
        return;
    }

    for (const FAbyssalBeaconSaveData& BeaconData : SaveGame->SavedBeacons)
    {
        if (BeaconData.BeaconId.IsValid())
        {
            SavedBeacons.Add(BeaconData);
        }
    }
}

int32 UBeaconSubsystem::FindBeaconIndex(FGuid BeaconId) const
{
    for (int32 Index = 0; Index < SavedBeacons.Num(); ++Index)
    {
        if (SavedBeacons[Index].BeaconId == BeaconId)
        {
            return Index;
        }
    }

    return INDEX_NONE;
}
