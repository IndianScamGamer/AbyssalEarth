#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "AbyssalSaveProvider.h"
#include "AbyssalUpgradeSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalUpgradeChangedSignature, FName, UpgradeItemId);

/**
 * Suit upgrade manager (roadmap N1). Tracks installed upgrades and applies
 * their effects to the player pawn’s vital components when
 * RegisterPlayerPawn is called (e.g. on BeginPlay and after respawn).
 *
 * Upgrade item ID → component effect mapping:
 *   ITEM_UPGRADE_PRESSURE_LINER   → UPressureComponent::AddPressureRating(+50)
 *   ITEM_UPGRADE_REBREATHER_MOD   → UOxygenComponent::AirCapacityBonus += 0.30
 *   ITEM_UPGRADE_THERMAL_WEAVE    → UTemperatureComponent::Insulation += 0.25
 *   ITEM_UPGRADE_ARMOR_PLATING    → UAbyssalHealthComponent::ArmorRating += 10
 *
 * IAbyssalSaveProvider — installed IDs written to Inventory blob.
 */
UCLASS()
class ABYSSALEARTH_API UAbyssalUpgradeSubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    /**
     * Install an upgrade. Consumes the item from UInventorySubsystem,
     * records it, and applies the effect if a pawn is registered.
     * Returns false if the item is not in the inventory or already installed.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Upgrades")
    bool InstallUpgrade(FName UpgradeItemId);

    /**
     * Uninstall an upgrade. Returns the item to UInventorySubsystem and
     * reverts the vital effect.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Upgrades")
    bool UninstallUpgrade(FName UpgradeItemId);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Upgrades")
    bool IsUpgradeInstalled(FName UpgradeItemId) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Upgrades")
    TArray<FName> GetInstalledUpgrades() const { return InstalledUpgrades.Array(); }

    /**
     * Call from AAbyssalPlayerCharacter::BeginPlay and after respawn to
     * re-apply all installed upgrade effects to the fresh pawn.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Upgrades")
    void RegisterPlayerPawn(APawn* PlayerPawn);

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Upgrades")
    FAbyssalUpgradeChangedSignature OnUpgradeInstalled;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Upgrades")
    FAbyssalUpgradeChangedSignature OnUpgradeUninstalled;

private:
    void ApplyUpgradeEffect(FName UpgradeItemId, float Direction);

    UPROPERTY()
    TSet<FName> InstalledUpgrades;

    UPROPERTY()
    TWeakObjectPtr<APawn> CachedPawn;
};
