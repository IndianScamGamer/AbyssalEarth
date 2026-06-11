#include "AbyssalRiftActor.h"
#include "InventorySubsystem.h"
#include "ObjectiveSubsystem.h"
#include "NarrativeSubsystem.h"
#include "Kismet/GameplayStatics.h"

AAbyssalRiftActor::AAbyssalRiftActor()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AAbyssalRiftActor::BeginPlay()
{
    Super::BeginPlay();
}

void AAbyssalRiftActor::SetPowerLevel(float NewPower)
{
    CurrentPower = FMath::Clamp(NewPower, 0.0f, 1.0f);
}

float AAbyssalRiftActor::GetChargePercent() const
{
    if (CurrentState != EAbyssalRiftState::Charging || ChargeDuration <= 0.0f)
    {
        return CurrentState == EAbyssalRiftState::Open || CurrentState == EAbyssalRiftState::Stable ? 1.0f : 0.0f;
    }
    // Progress comes straight from the charge timer; the actor never ticks.
    const float Elapsed = GetWorldTimerManager().GetTimerElapsed(ChargeTimer);
    return FMath::Clamp(Elapsed / ChargeDuration, 0.0f, 1.0f);
}

bool AAbyssalRiftActor::CanInteract_Implementation(AActor* Interactor)
{
    if (CurrentState != EAbyssalRiftState::Dormant)
    {
        return false;
    }
    return CheckActivationRequirements(Interactor);
}

void AAbyssalRiftActor::OnInteract_Implementation(AActor* Interactor)
{
    if (!CanInteract_Implementation(Interactor))
    {
        return;
    }

    UGameInstance* GI = UGameplayStatics::GetGameInstance(this);
    if (!GI)
    {
        return;
    }

    // Consume the stabiliser
    if (UInventorySubsystem* InvSub = GI->GetSubsystem<UInventorySubsystem>())
    {
        InvSub->RemoveItem(RequiredItemId, 1);
    }

    // Play activation beat
    if (UNarrativeSubsystem* NarSub = GI->GetSubsystem<UNarrativeSubsystem>())
    {
        NarSub->PlayBeat(FName(TEXT("RIFT_ACTIVATE_01")));
    }

    SetRiftState(EAbyssalRiftState::Charging);
    GetWorldTimerManager().SetTimer(ChargeTimer, this, &AAbyssalRiftActor::OnChargeComplete, ChargeDuration, false);
}

FText AAbyssalRiftActor::GetInteractionPrompt_Implementation()
{
    switch (CurrentState)
    {
        case EAbyssalRiftState::Dormant:
            if (CurrentPower < PowerThreshold)
            {
                return NSLOCTEXT("AbyssalEarth", "RiftNoPower", "Rift [INSUFFICIENT POWER]");
            }
            return NSLOCTEXT("AbyssalEarth", "RiftActivate", "Open the Rift");
        case EAbyssalRiftState::Charging:
            return NSLOCTEXT("AbyssalEarth", "RiftCharging", "Rift Charging...");
        case EAbyssalRiftState::Open:
        case EAbyssalRiftState::Stable:
            return NSLOCTEXT("AbyssalEarth", "RiftOpen", "[RIFT OPEN — Surface Return]");
    }
    return FText::GetEmpty();
}

void AAbyssalRiftActor::OnBeginFocus_Implementation(AActor* /*Interactor*/) { BP_OnFocusBegin(); }
void AAbyssalRiftActor::OnEndFocus_Implementation(AActor* /*Interactor*/)   { BP_OnFocusEnd();   }

void AAbyssalRiftActor::SetRiftState(EAbyssalRiftState NewState)
{
    if (CurrentState == NewState)
    {
        return;
    }
    CurrentState = NewState;
    OnRiftStateChanged.Broadcast(NewState);
    BP_OnStateChanged(NewState);
}

bool AAbyssalRiftActor::CheckActivationRequirements(AActor* Interactor) const
{
    if (CurrentPower < PowerThreshold)
    {
        return false;
    }

    if (!Interactor || RequiredItemId.IsNone())
    {
        return true;
    }

    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UInventorySubsystem* InvSub = GI->GetSubsystem<UInventorySubsystem>())
        {
            return InvSub->HasItem(RequiredItemId);
        }
    }
    return false;
}

void AAbyssalRiftActor::OnChargeComplete()
{
    SetRiftState(EAbyssalRiftState::Open);
    OnRiftOpened.Broadcast();
    BP_OnRiftOpened();

    // Complete the objective
    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UObjectiveSubsystem* ObjSub = GI->GetSubsystem<UObjectiveSubsystem>())
        {
            ObjSub->CompleteObjective(FName(TEXT("OBJ_OPEN_RIFT")));
        }

        if (UNarrativeSubsystem* NarSub = GI->GetSubsystem<UNarrativeSubsystem>())
        {
            NarSub->PlayBeat(FName(TEXT("RIFT_OPEN_01")));
            NarSub->TriggerPostCreditsHook();
        }
    }
}
