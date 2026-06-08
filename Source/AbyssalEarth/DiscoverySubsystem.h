#pragma once

#include "CoreMinimal.h"
#include "AbyssalSaveSubsystem.h"
#include "DiscoverySaveGame.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "DiscoverySubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalDiscoveryAddedSignature, const FAbyssalDiscoveryEntry&, Entry);

UCLASS()
class ABYSSALEARTH_API UDiscoverySubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    bool RegisterDiscovery(FName DiscoveryId);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    bool RegisterDiscoveryEntry(const FAbyssalDiscoveryEntry& Entry);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    bool IsDiscovered(FName DiscoveryId) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    TArray<FName> GetDiscoveredIds() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    TArray<FAbyssalDiscoveryEntry> GetDiscoveredEntries() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    TArray<FAbyssalDiscoveryEntry> GetDiscoveredEntriesByCategory(EDiscoveryCategory Category) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    bool GetDiscoveryEntry(FName DiscoveryId, FAbyssalDiscoveryEntry& OutEntry) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    int32 GetDiscoveredCount() const;

    /** Routes through UAbyssalSaveSubsystem::SaveActiveSlot. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    void SaveDiscoveries();

    /** No-op: load is driven by UAbyssalSaveSubsystem::LoadSlot. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    void LoadDiscoveries();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    void ClearAllDiscoveries();

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Discovery")
    FAbyssalDiscoveryAddedSignature OnDiscoveryAdded;

private:
    UPROPERTY()
    TMap<FName, FAbyssalDiscoveryEntry> Entries;
};
