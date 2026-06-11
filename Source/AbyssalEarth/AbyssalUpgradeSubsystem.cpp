#include "AbyssalUpgradeSubsystem.h"
#include "AbyssalSaveSubsystem.h"
#include "AbyssalProfileSaveGame.h"
#include "InventorySubsystem.h"
#include "PressureComponent.h"
#include "OxygenComponent.h"
#include "TemperatureComponent.h"
#include "AbyssalHealthComponent.h"
#include "GameFramework/Pawn.h"

void UAbyssalUpgradeSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    Collection.InitializeDependency(UAbyssalSaveSubsystem::StaticClass());
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->RegisterSaveProvider(this);
    }
}

void UAbyssalUpgradeSubsystem::Deinitialize()
{
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->UnregisterSaveProvider(this);
    }
    Super::Deinitialize();
}

void UAbyssalUpgradeSubsystem::OnSaveRequested(UAbyssalProfileSaveGame* SaveGame)
{
    SaveGame->Inventory.InstalledUpgradeIds = InstalledUpgrades.Array();
}

void UAbyssalUpgradeSubsystem::OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame)
{
    InstalledUpgrades.Reset();
    for (const FName& Id : SaveGame->Inventory.InstalledUpgradeIds)
    {
        if (!Id.IsNone())
        {
            InstalledUpgrades.Add(Id);
        }
    }
}

bool UAbyssalUpgradeSubsystem::InstallUpgrade(FName UpgradeItemId)
{
    if (UpgradeItemId.IsNone() || InstalledUpgrades.Contains(UpgradeItemId))
    {
        return false;
    }

    UInventorySubsystem* InvSub = GetGameInstance()->GetSubsystem<UInventorySubsystem>();
    if (!InvSub || !InvSub->HasItem(UpgradeItemId))
    {
        return false;
    }

    InvSub->RemoveItem(UpgradeItemId, 1);
    InstalledUpgrades.Add(UpgradeItemId);
    ApplyUpgradeEffect(UpgradeItemId, 1.0f);
    OnUpgradeInstalled.Broadcast(UpgradeItemId);
    return true;
}

bool UAbyssalUpgradeSubsystem::UninstallUpgrade(FName UpgradeItemId)
{
    if (!InstalledUpgrades.Contains(UpgradeItemId))
    {
        return false;
    }

    InstalledUpgrades.Remove(UpgradeItemId);
    ApplyUpgradeEffect(UpgradeItemId, -1.0f); // Revert

    if (UInventorySubsystem* InvSub = GetGameInstance()->GetSubsystem<UInventorySubsystem>())
    {
        InvSub->AddItem(UpgradeItemId, 1);
    }

    OnUpgradeUninstalled.Broadcast(UpgradeItemId);
    return true;
}

bool UAbyssalUpgradeSubsystem::IsUpgradeInstalled(FName UpgradeItemId) const
{
    return InstalledUpgrades.Contains(UpgradeItemId);
}

void UAbyssalUpgradeSubsystem::RegisterPlayerPawn(APawn* PlayerPawn)
{
    // Same pawn instance re-registering (e.g. checkpoint respawn teleports the
    // existing pawn): its components already carry the upgrade effects, so
    // re-applying would stack them again on every death.
    if (CachedPawn.Get() == PlayerPawn)
    {
        return;
    }

    CachedPawn = PlayerPawn;
    if (!PlayerPawn)
    {
        return;
    }
    // Apply all installed upgrades to the fresh pawn
    for (const FName& Id : InstalledUpgrades)
    {
        ApplyUpgradeEffect(Id, 1.0f);
    }
}

void UAbyssalUpgradeSubsystem::ApplyUpgradeEffect(FName UpgradeItemId, float Direction)
{
    APawn* Pawn = CachedPawn.Get();
    if (!Pawn)
    {
        return;
    }

    if (UpgradeItemId == FName(TEXT("ITEM_UPGRADE_PRESSURE_LINER")))
    {
        if (UPressureComponent* Comp = Pawn->FindComponentByClass<UPressureComponent>())
        {
            Comp->AddPressureRating(50.0f * Direction);
        }
    }
    else if (UpgradeItemId == FName(TEXT("ITEM_UPGRADE_REBREATHER_MOD")))
    {
        if (UOxygenComponent* Comp = Pawn->FindComponentByClass<UOxygenComponent>())
        {
            Comp->AirCapacityBonus += 0.30f * Direction;
        }
    }
    else if (UpgradeItemId == FName(TEXT("ITEM_UPGRADE_THERMAL_WEAVE")))
    {
        if (UTemperatureComponent* Comp = Pawn->FindComponentByClass<UTemperatureComponent>())
        {
            Comp->Insulation = FMath::Clamp(Comp->Insulation + 0.25f * Direction, 0.0f, 1.0f);
        }
    }
    else if (UpgradeItemId == FName(TEXT("ITEM_UPGRADE_ARMOR_PLATING")))
    {
        if (UAbyssalHealthComponent* Comp = Pawn->FindComponentByClass<UAbyssalHealthComponent>())
        {
            Comp->ArmorRating = FMath::Max(0.0f, Comp->ArmorRating + 10.0f * Direction);
        }
    }
}
