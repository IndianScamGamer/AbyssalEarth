#include "AbyssalSaveSubsystem.h"
#include "AbyssalProfileSaveGame.h"
#include "Kismet/GameplayStatics.h"

static const FString SaveSlotPrefix = TEXT("AbyssalProfile_");

void UAbyssalSaveSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
}

void UAbyssalSaveSubsystem::Deinitialize()
{
    SaveProviders.Empty();
    Super::Deinitialize();
}

void UAbyssalSaveSubsystem::RegisterSaveProvider(IAbyssalSaveProvider* Provider)
{
    if (Provider && !SaveProviders.Contains(Provider))
    {
        SaveProviders.Add(Provider);
    }
}

void UAbyssalSaveSubsystem::UnregisterSaveProvider(IAbyssalSaveProvider* Provider)
{
    SaveProviders.Remove(Provider);
}

void UAbyssalSaveSubsystem::LoadSlot(int32 SlotIndex)
{
    ActiveSlotIndex = SlotIndex;
    const FString SlotName = MakeSlotName(SlotIndex);

    UAbyssalProfileSaveGame* Loaded = nullptr;
    if (UGameplayStatics::DoesSaveGameExist(SlotName, 0))
    {
        Loaded = Cast<UAbyssalProfileSaveGame>(UGameplayStatics::LoadGameFromSlot(SlotName, 0));
    }
    if (!Loaded)
    {
        Loaded = Cast<UAbyssalProfileSaveGame>(
            UGameplayStatics::CreateSaveGameObject(UAbyssalProfileSaveGame::StaticClass()));
    }

    ActiveSaveGame = Loaded;
    NotifyProvidersLoad(ActiveSaveGame);
    OnLoadCompleted.Broadcast(ActiveSaveGame != nullptr);
}

void UAbyssalSaveSubsystem::SaveActiveSlot()
{
    if (!ActiveSaveGame)
    {
        ActiveSaveGame = Cast<UAbyssalProfileSaveGame>(
            UGameplayStatics::CreateSaveGameObject(UAbyssalProfileSaveGame::StaticClass()));
    }

    NotifyProvidersSave(ActiveSaveGame);
    const bool bSuccess = UGameplayStatics::SaveGameToSlot(ActiveSaveGame, MakeSlotName(ActiveSlotIndex), 0);
    OnSaveCompleted.Broadcast(bSuccess);
}

void UAbyssalSaveSubsystem::DeleteSlot(int32 SlotIndex)
{
    UGameplayStatics::DeleteGameInSlot(MakeSlotName(SlotIndex), 0);
    if (SlotIndex == ActiveSlotIndex) { ActiveSaveGame = nullptr; }
}

bool UAbyssalSaveSubsystem::DoesSaveExist(int32 SlotIndex) const
{
    return UGameplayStatics::DoesSaveGameExist(MakeSlotName(SlotIndex), 0);
}

FString UAbyssalSaveSubsystem::MakeSlotName(int32 SlotIndex) const
{
    return SaveSlotPrefix + FString::FromInt(SlotIndex);
}

void UAbyssalSaveSubsystem::NotifyProvidersLoad(UAbyssalProfileSaveGame* SaveGame)
{
    for (IAbyssalSaveProvider* Provider : SaveProviders)
    {
        if (Provider) { Provider->OnLoadCompleted(SaveGame); }
    }
}

void UAbyssalSaveSubsystem::NotifyProvidersSave(UAbyssalProfileSaveGame* SaveGame)
{
    for (IAbyssalSaveProvider* Provider : SaveProviders)
    {
        if (Provider) { Provider->OnSaveRequested(SaveGame); }
    }
}
