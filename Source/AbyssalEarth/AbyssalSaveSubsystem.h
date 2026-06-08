#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "AbyssalSaveSubsystem.generated.h"

class UAbyssalProfileSaveGame;

/**
 * Implement on any subsystem that wants to persist data through the central
 * save slot.  RegisterSaveProvider() / UnregisterSaveProvider() are called
 * by the subsystem itself in its Initialize / Deinitialize.
 */
UINTERFACE(MinimalAPI, Blueprintable)
class UAbyssalSaveProvider : public UInterface
{
    GENERATED_BODY()
};

class IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    /** Write your state into SaveGame before the slot is written to disk. */
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) = 0;

    /** Restore your state from SaveGame after a slot has been loaded. */
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) = 0;
};

// ---------------------------------------------------------------------------

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalSaveCompletedSignature, bool, bSuccess);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalLoadCompletedSignature, bool, bSuccess);

/**
 * Central save/load authority for Abyssal Earth.
 *
 * Owns the active UAbyssalProfileSaveGame slot and coordinates all
 * domain subsystems (discovery, beacons, objectives, inventory, …) through
 * the IAbyssalSaveProvider interface.  Replaces the per-subsystem calls to
 * UGameplayStatics::SaveGameToSlot / LoadGameFromSlot that previously lived
 * inside UDiscoverySubsystem.
 *
 * Slot naming: "AbyssalProfile_<SlotIndex>" (0-based).  Default slot is 0.
 * The subsystem always keeps one active slot loaded; domain providers read
 * and write through it.
 *
 * Usage (domain subsystem example):
 *   UAbyssalSaveSubsystem* Save = GameInstance->GetSubsystem<UAbyssalSaveSubsystem>();
 *   Save->RegisterSaveProvider(this);            // in Initialize()
 *   Save->UnregisterSaveProvider(this);          // in Deinitialize()
 *   Save->SaveActiveSlot();                      // triggers all providers
 *
 * Blueprint access: UAbyssalGameplayLibrary::GetSaveSubsystem(WorldContext).
 */
UCLASS()
class ABYSSALEARTH_API UAbyssalSaveSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // -------------------------------------------------------------------------
    // Provider registration
    // -------------------------------------------------------------------------

    void RegisterSaveProvider(IAbyssalSaveProvider* Provider);
    void UnregisterSaveProvider(IAbyssalSaveProvider* Provider);

    // -------------------------------------------------------------------------
    // Slot management
    // -------------------------------------------------------------------------

    /** Load the given slot index (0-based) as the active slot.
     *  If no save exists at that slot, creates a fresh one. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Save")
    void LoadSlot(int32 SlotIndex = 0);

    /** Write all registered providers into the active slot and flush to disk. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Save")
    void SaveActiveSlot();

    /** Delete the save at the given slot index. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Save")
    void DeleteSlot(int32 SlotIndex);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Save")
    int32 GetActiveSlotIndex() const { return ActiveSlotIndex; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Save")
    bool HasActiveSlot() const { return ActiveSaveGame != nullptr; }

    /** Returns true if a save file exists for the given slot (disk check). */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Save")
    bool DoesSaveExist(int32 SlotIndex) const;

    /** Direct access to the active save object (nullptr until LoadSlot called). */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Save")
    UAbyssalProfileSaveGame* GetActiveSaveGame() const { return ActiveSaveGame; }

    // -------------------------------------------------------------------------
    // Delegates
    // -------------------------------------------------------------------------

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Save")
    FAbyssalSaveCompletedSignature OnSaveCompleted;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Save")
    FAbyssalLoadCompletedSignature OnLoadCompleted;

private:
    UPROPERTY()
    TObjectPtr<UAbyssalProfileSaveGame> ActiveSaveGame;

    int32 ActiveSlotIndex = 0;

    TArray<IAbyssalSaveProvider*> SaveProviders;

    FString MakeSlotName(int32 SlotIndex) const;
    void NotifyProvidersLoad(UAbyssalProfileSaveGame* SaveGame);
    void NotifyProvidersSave(UAbyssalProfileSaveGame* SaveGame);
};
