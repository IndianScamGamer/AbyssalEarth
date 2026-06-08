#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "AbyssalSaveSubsystem.generated.h"

class UAbyssalProfileSaveGame;

UINTERFACE(MinimalAPI, Blueprintable)
class UAbyssalSaveProvider : public UInterface
{
    GENERATED_BODY()
};

class IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) = 0;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) = 0;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalSaveCompletedSignature, bool, bSuccess);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalLoadCompletedSignature, bool, bSuccess);

/**
 * Central save/load authority for Abyssal Earth.
 *
 * Owns the active UAbyssalProfileSaveGame slot and coordinates all domain
 * subsystems through IAbyssalSaveProvider. Replaces per-subsystem
 * UGameplayStatics::SaveGameToSlot calls that previously lived in
 * UDiscoverySubsystem.
 *
 * Slot naming: "AbyssalProfile_<SlotIndex>" (0-based). Default slot is 0.
 * Blueprint access: UAbyssalGameplayLibrary::GetSaveSubsystem(WorldContext).
 */
UCLASS()
class ABYSSALEARTH_API UAbyssalSaveSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    void RegisterSaveProvider(IAbyssalSaveProvider* Provider);
    void UnregisterSaveProvider(IAbyssalSaveProvider* Provider);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Save")
    void LoadSlot(int32 SlotIndex = 0);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Save")
    void SaveActiveSlot();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Save")
    void DeleteSlot(int32 SlotIndex);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Save")
    int32 GetActiveSlotIndex() const { return ActiveSlotIndex; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Save")
    bool HasActiveSlot() const { return ActiveSaveGame != nullptr; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Save")
    bool DoesSaveExist(int32 SlotIndex) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Save")
    UAbyssalProfileSaveGame* GetActiveSaveGame() const { return ActiveSaveGame; }

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
