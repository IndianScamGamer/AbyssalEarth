#include "AbyssalGameMode.h"
#include "AbyssalPlayerCharacter.h"
#include "AbyssalPlayerController.h"
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
