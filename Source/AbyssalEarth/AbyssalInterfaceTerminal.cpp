#include "AbyssalInterfaceTerminal.h"
#include "NarrativeSubsystem.h"
#include "Kismet/GameplayStatics.h"

AAbyssalInterfaceTerminal::AAbyssalInterfaceTerminal()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AAbyssalInterfaceTerminal::BeginPlay()
{
    Super::BeginPlay();
}

void AAbyssalInterfaceTerminal::SetPowerLevel(float NewPower)
{
    CurrentPower = FMath::Clamp(NewPower, 0.0f, 1.0f);

    if (CurrentState == EAbyssalTerminalState::Dormant && CurrentPower >= ActivationThreshold)
    {
        SetTerminalState(EAbyssalTerminalState::Powering);
    }
    else if (CurrentState == EAbyssalTerminalState::Powering && CurrentPower < ActivationThreshold)
    {
        // Power dropped during startup — abort
        GetWorldTimerManager().ClearTimer(PowerUpTimer);
        SetTerminalState(EAbyssalTerminalState::Dormant);
    }
}

void AAbyssalInterfaceTerminal::SetTerminalState(EAbyssalTerminalState NewState)
{
    if (CurrentState == NewState)
    {
        return;
    }

    CurrentState = NewState;

    if (NewState == EAbyssalTerminalState::Powering)
    {
        GetWorldTimerManager().SetTimer(PowerUpTimer, this,
            &AAbyssalInterfaceTerminal::OnPowerUpComplete, PowerUpDuration, false);
    }
    else if (NewState == EAbyssalTerminalState::Active)
    {
        OnTerminalActivated.Broadcast(this);
    }

    BP_OnStateChanged(NewState);
}

void AAbyssalInterfaceTerminal::LockTerminal()
{
    GetWorldTimerManager().ClearTimer(PowerUpTimer);
    SetTerminalState(EAbyssalTerminalState::Locked);
}

void AAbyssalInterfaceTerminal::UnlockTerminal()
{
    if (CurrentState == EAbyssalTerminalState::Locked)
    {
        const EAbyssalTerminalState Target = (CurrentPower >= ActivationThreshold)
            ? EAbyssalTerminalState::Active
            : EAbyssalTerminalState::Dormant;
        SetTerminalState(Target);
    }
}

bool AAbyssalInterfaceTerminal::IsDataExhausted() const
{
    return DataBeatIds.Num() > 0 && DataBeatIndex >= DataBeatIds.Num();
}

bool AAbyssalInterfaceTerminal::CanInteract_Implementation(AActor* /*Interactor*/) const
{
    return CurrentState == EAbyssalTerminalState::Active && !IsDataExhausted();
}

void AAbyssalInterfaceTerminal::OnInteract_Implementation(AActor* /*Interactor*/)
{
    if (!CanInteract_Implementation(nullptr))
    {
        return;
    }

    const FName BeatId = DataBeatIds[DataBeatIndex];
    ++DataBeatIndex;

    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UNarrativeSubsystem* Narrative = GI->GetSubsystem<UNarrativeSubsystem>())
        {
            Narrative->PlayBeat(BeatId);
        }
    }

    OnDataReadout.Broadcast(this, BeatId);
    BP_OnDataReadout(BeatId);

    if (IsDataExhausted())
    {
        OnDataExhausted.Broadcast(this);
        BP_OnDataExhausted();
    }
}

FText AAbyssalInterfaceTerminal::GetInteractPrompt_Implementation() const
{
    if (CurrentState == EAbyssalTerminalState::Locked)
    {
        return NSLOCTEXT("AbyssalEarth", "TerminalLocked", "[LOCKED]");
    }
    if (CurrentState != EAbyssalTerminalState::Active)
    {
        return FText::Format(
            NSLOCTEXT("AbyssalEarth", "TerminalInactive", "{0} [OFFLINE]"),
            TerminalLabel);
    }
    return FText::Format(
        NSLOCTEXT("AbyssalEarth", "TerminalActive", "Interface: {0}"),
        TerminalLabel);
}

void AAbyssalInterfaceTerminal::OnFocusBegin_Implementation(AActor* /*Interactor*/)
{
    BP_OnFocusBegin();
}

void AAbyssalInterfaceTerminal::OnFocusEnd_Implementation(AActor* /*Interactor*/)
{
    BP_OnFocusEnd();
}

void AAbyssalInterfaceTerminal::OnPowerUpComplete()
{
    SetTerminalState(EAbyssalTerminalState::Active);
}
