#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "DiscoveryActor.h"
#include "DiscoverySaveGame.h"
#include "AbyssalJournalWidget.generated.h"

class UDiscoverySubsystem;

UCLASS()
class ABYSSALEARTH_API UAbyssalJournalWidget : public UUserWidget
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Journal")
    void SetJournalOpen(bool bOpen);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Journal")
    void ToggleJournalOpen();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Journal")
    bool IsJournalOpen() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Journal")
    TArray<FAbyssalDiscoveryEntry> GetAllEntries() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Journal")
    TArray<FAbyssalDiscoveryEntry> GetEntriesByCategory(EDiscoveryCategory InCategory) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Journal")
    int32 GetEntryCount() const;

protected:
    virtual void NativeConstruct() override;
    virtual void NativeDestruct() override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Journal", meta = (DisplayName = "Journal Opened"))
    void BP_OnJournalOpened();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Journal", meta = (DisplayName = "Journal Closed"))
    void BP_OnJournalClosed();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Journal", meta = (DisplayName = "New Discovery Added"))
    void BP_OnNewDiscoveryAdded(const FAbyssalDiscoveryEntry& Entry);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Journal", meta = (DisplayName = "Entries Refreshed"))
    void BP_OnEntriesRefreshed();

private:
    UFUNCTION()
    void HandleDiscoveryAdded(const FAbyssalDiscoveryEntry& Entry);

    void BindToSubsystem();
    void UnbindFromSubsystem();

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Journal", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<UDiscoverySubsystem> BoundDiscoverySubsystem;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Journal", meta = (AllowPrivateAccess = "true"))
    bool bJournalOpen = false;
};
