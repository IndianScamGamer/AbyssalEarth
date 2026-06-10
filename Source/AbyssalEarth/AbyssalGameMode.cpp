#include "AbyssalGameMode.h"
#include "AbyssalPlayerCharacter.h"
#include "AbyssalPlayerController.h"
#include "AbyssalSaveSubsystem.h"
#include "NarrativeSubsystem.h"
#include "Engine/DataTable.h"

AAbyssalGameMode::AAbyssalGameMode()
{
    DefaultPawnClass       = AAbyssalPlayerCharacter::StaticClass();
    PlayerControllerClass  = AAbyssalPlayerController::StaticClass();
}

void AAbyssalGameMode::BeginPlay()
{
    Super::BeginPlay();

    // Load the profile slot once per session so checkpoint/inventory/objective
    // state restores on boot. Map transitions keep the already-active slot
    // (HasActiveSlot guard) instead of re-reading disk and clobbering memory.
    if (UGameInstance* GI = GetGameInstance())
    {
        if (UAbyssalSaveSubsystem* SaveSub = GI->GetSubsystem<UAbyssalSaveSubsystem>())
        {
            if (!SaveSub->HasActiveSlot())
            {
                SaveSub->LoadSlot(0);
            }
        }
    }

    if (NarrativeBeatTable)
    {
        if (UGameInstance* GI = GetGameInstance())
        {
            if (UNarrativeSubsystem* Narrative = GI->GetSubsystem<UNarrativeSubsystem>())
            {
                Narrative->SetBeatTable(NarrativeBeatTable);
            }
        }
    }
}

void AAbyssalGameMode::RespawnPlayer()
{
    APlayerController* PC = GetWorld()->GetFirstPlayerController();
    if (!PC)
    {
        return;
    }

    if (AAbyssalPlayerCharacter* Character = Cast<AAbyssalPlayerCharacter>(PC->GetPawn()))
    {
        Character->RespawnAtCheckpoint();
    }
}
