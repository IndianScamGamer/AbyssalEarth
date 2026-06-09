#include "CheckpointActor.h"
#include "CheckpointSubsystem.h"
#include "Kismet/GameplayStatics.h"

ACheckpointActor::ACheckpointActor()
{
    PrimaryActorTick.bCanEverTick = false;
}

void ACheckpointActor::BeginPlay()
{
    Super::BeginPlay();

    if (CheckpointId.IsNone())
    {
        return;
    }

    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UCheckpointSubsystem* CheckpointSub = GI->GetSubsystem<UCheckpointSubsystem>())
        {
            CheckpointSub->RegisterCheckpoint(CheckpointId, GetActorLocation(), MapId);

            // If the save system already has this checkpoint active (from a loaded save),
            // restore our visual state without broadcasting the event again.
            if (CheckpointSub->GetActiveCheckpointId() == CheckpointId)
            {
                CurrentState = ECheckpointState::Active;
                BP_OnActivated();
            }
        }
    }
}

bool ACheckpointActor::CanInteract_Implementation(AActor* /*Interactor*/) const
{
    return CurrentState == ECheckpointState::Inactive;
}

void ACheckpointActor::OnInteract_Implementation(AActor* /*Interactor*/)
{
    if (CurrentState != ECheckpointState::Inactive || CheckpointId.IsNone())
    {
        return;
    }

    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UCheckpointSubsystem* CheckpointSub = GI->GetSubsystem<UCheckpointSubsystem>())
        {
            CheckpointSub->SetActiveCheckpoint(CheckpointId);

            // Trigger auto-save so the checkpoint survives a crash
            if (UAbyssalSaveSubsystem* SaveSub = GI->GetSubsystem<UAbyssalSaveSubsystem>())
            {
                SaveSub->SaveActiveSlot();
            }
        }
    }

    CurrentState = ECheckpointState::Active;
    OnCheckpointActivated.Broadcast(CheckpointId);
    BP_OnActivated();
}

FText ACheckpointActor::GetInteractPrompt_Implementation() const
{
    if (CurrentState == ECheckpointState::Active)
    {
        return NSLOCTEXT("AbyssalEarth", "CheckpointActive", "[Checkpoint Active]");
    }
    return NSLOCTEXT("AbyssalEarth", "CheckpointActivate", "Activate Checkpoint");
}

void ACheckpointActor::OnFocusBegin_Implementation(AActor* /*Interactor*/)
{
    BP_OnFocusBegin();
}

void ACheckpointActor::OnFocusEnd_Implementation(AActor* /*Interactor*/)
{
    BP_OnFocusEnd();
}
