#include "AbyssalPowerNode.h"
#include "AbyssalInterfaceTerminal.h"

AAbyssalPowerNode::AAbyssalPowerNode()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AAbyssalPowerNode::SetPowerLevel(float NewPower)
{
    if (bPropagating)
    {
        return;
    }
    const float Clamped = FMath::Clamp(NewPower, 0.0f, 1.0f);
    if (FMath::IsNearlyEqual(Clamped, CurrentPower))
    {
        return;
    }
    CurrentPower = Clamped;
    OnPowerChanged.Broadcast(this, CurrentPower);
    BP_OnPowerChanged(CurrentPower);
    PropagatePower(CurrentPower, 0);
}

void AAbyssalPowerNode::Activate()
{
    if (NodeType != EAbyssalPowerNodeType::Source || bIsActive)
    {
        return;
    }
    bIsActive = true;
    BP_OnActivated();
    SetPowerLevel(SourceOutput);
}

void AAbyssalPowerNode::Deactivate()
{
    if (NodeType != EAbyssalPowerNodeType::Source || !bIsActive)
    {
        return;
    }
    bIsActive = false;
    BP_OnDeactivated();
    SetPowerLevel(0.0f);
}

bool AAbyssalPowerNode::CanInteract_Implementation(AActor* /*Interactor*/) const
{
    return NodeType == EAbyssalPowerNodeType::Source && !bIsActive;
}

void AAbyssalPowerNode::OnInteract_Implementation(AActor* /*Interactor*/)
{
    if (bIsActive)
    {
        Deactivate();
    }
    else
    {
        Activate();
    }
}

FText AAbyssalPowerNode::GetInteractPrompt_Implementation() const
{
    if (NodeType != EAbyssalPowerNodeType::Source)
    {
        return FText::GetEmpty();
    }
    return bIsActive
        ? FText::Format(NSLOCTEXT("AbyssalEarth", "PowerNodeDeactivate", "Deactivate {0}"), NodeLabel)
        : FText::Format(NSLOCTEXT("AbyssalEarth", "PowerNodeActivate",   "Activate {0}"),   NodeLabel);
}

void AAbyssalPowerNode::OnFocusBegin_Implementation(AActor* /*Interactor*/) { BP_OnFocusBegin(); }
void AAbyssalPowerNode::OnFocusEnd_Implementation(AActor* /*Interactor*/)   { BP_OnFocusEnd();   }

void AAbyssalPowerNode::PropagatePower(float Power, int32 Depth)
{
    // Guard against cycles and excessive chain depth
    if (Depth > 16 || bPropagating)
    {
        return;
    }

    bPropagating = true;

    // Apply relay loss before forwarding
    const float Forwarded = (NodeType == EAbyssalPowerNodeType::Relay)
        ? FMath::Max(0.0f, Power - RelayLoss)
        : Power;

    for (AAbyssalPowerNode* Node : ConnectedNodes)
    {
        if (Node)
        {
            Node->SetPowerLevel(Forwarded);
        }
    }

    for (AAbyssalInterfaceTerminal* Terminal : ConnectedTerminals)
    {
        if (Terminal)
        {
            Terminal->SetPowerLevel(Forwarded);
        }
    }

    bPropagating = false;
}
