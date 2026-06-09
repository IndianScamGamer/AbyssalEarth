#include "HeliosRobot.h"
#include "NarrativeSubsystem.h"
#include "Components/SkeletalMeshComponent.h"
#include "Kismet/GameplayStatics.h"

AHeliosRobot::AHeliosRobot()
{
    PrimaryActorTick.bCanEverTick = false;

    Mesh = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("Mesh"));
    RootComponent = Mesh;

    UnitName = NSLOCTEXT("HeliosRobot", "DefaultUnitName", "HELIOS");
}

bool AHeliosRobot::CanInteract_Implementation(AActor* Interactor)
{
    return State != EHeliosState::Disabled && DialogueBeatIds.Num() > 0;
}

FText AHeliosRobot::GetInteractionPrompt_Implementation()
{
    return FText::Format(
        NSLOCTEXT("HeliosRobot", "TalkPrompt", "Talk to {0}"), UnitName);
}

void AHeliosRobot::OnInteract_Implementation(AActor* Interactor)
{
    if (DialogueBeatIds.Num() == 0)
    {
        return;
    }

    const int32 LineIndex = FMath::Clamp(DialogueIndex, 0, DialogueBeatIds.Num() - 1);
    const FName BeatId = DialogueBeatIds[LineIndex];

    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UNarrativeSubsystem* Narrative = GI->GetSubsystem<UNarrativeSubsystem>())
        {
            Narrative->PlayBeat(BeatId);
        }
    }

    BP_OnDialogueLine(BeatId, LineIndex);

    // Advance to the next line for the following interaction.
    if (DialogueIndex < DialogueBeatIds.Num() - 1)
    {
        ++DialogueIndex;
    }
    else if (bLoopDialogue)
    {
        DialogueIndex = 0;
    }
}

void AHeliosRobot::OnBeginFocus_Implementation(AActor* Interactor)
{
    BP_OnFocusBegin();
}

void AHeliosRobot::OnEndFocus_Implementation(AActor* Interactor)
{
    BP_OnFocusEnd();
}

void AHeliosRobot::SetHeliosState(EHeliosState NewState)
{
    if (State == NewState)
    {
        return;
    }

    const EHeliosState OldState = State;
    State = NewState;
    OnHeliosStateChanged.Broadcast(State, OldState);
    BP_OnStateChanged(State);
}
