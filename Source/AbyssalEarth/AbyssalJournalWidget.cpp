#include "AbyssalJournalWidget.h"
#include "DiscoverySubsystem.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"

void UAbyssalJournalWidget::NativeConstruct()
{
    Super::NativeConstruct();
    BindToSubsystem();
    BP_OnEntriesRefreshed();
}

void UAbyssalJournalWidget::NativeDestruct()
{
    UnbindFromSubsystem();
    Super::NativeDestruct();
}

void UAbyssalJournalWidget::SetJournalOpen(bool bOpen)
{
    if (bJournalOpen == bOpen)
    {
        return;
    }

    bJournalOpen = bOpen;
    if (bJournalOpen)
    {
        BP_OnEntriesRefreshed();
        BP_OnJournalOpened();
    }
    else
    {
        BP_OnJournalClosed();
    }
}

void UAbyssalJournalWidget::ToggleJournalOpen()
{
    SetJournalOpen(!bJournalOpen);
}

bool UAbyssalJournalWidget::IsJournalOpen() const
{
    return bJournalOpen;
}

TArray<FAbyssalDiscoveryEntry> UAbyssalJournalWidget::GetAllEntries() const
{
    return BoundDiscoverySubsystem ? BoundDiscoverySubsystem->GetDiscoveredEntries() : TArray<FAbyssalDiscoveryEntry>{};
}

TArray<FAbyssalDiscoveryEntry> UAbyssalJournalWidget::GetEntriesByCategory(EDiscoveryCategory InCategory) const
{
    return BoundDiscoverySubsystem ? BoundDiscoverySubsystem->GetDiscoveredEntriesByCategory(InCategory) : TArray<FAbyssalDiscoveryEntry>{};
}

int32 UAbyssalJournalWidget::GetEntryCount() const
{
    return BoundDiscoverySubsystem ? BoundDiscoverySubsystem->GetDiscoveredCount() : 0;
}

void UAbyssalJournalWidget::HandleDiscoveryAdded(const FAbyssalDiscoveryEntry& Entry)
{
    BP_OnNewDiscoveryAdded(Entry);
    BP_OnEntriesRefreshed();
}

void UAbyssalJournalWidget::BindToSubsystem()
{
    UnbindFromSubsystem();

    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    UGameInstance* GameInstance = World->GetGameInstance();
    if (!GameInstance)
    {
        return;
    }

    BoundDiscoverySubsystem = GameInstance->GetSubsystem<UDiscoverySubsystem>();
    if (BoundDiscoverySubsystem)
    {
        BoundDiscoverySubsystem->OnDiscoveryAdded.AddDynamic(this, &UAbyssalJournalWidget::HandleDiscoveryAdded);
    }
}

void UAbyssalJournalWidget::UnbindFromSubsystem()
{
    if (BoundDiscoverySubsystem)
    {
        BoundDiscoverySubsystem->OnDiscoveryAdded.RemoveDynamic(this, &UAbyssalJournalWidget::HandleDiscoveryAdded);
        BoundDiscoverySubsystem = nullptr;
    }
}
