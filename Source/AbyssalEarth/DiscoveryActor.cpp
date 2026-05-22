#include "DiscoveryActor.h"
#include "DiscoverySubsystem.h"
#include "ObjectiveSubsystem.h"
#include "Engine/GameInstance.h"

ADiscoveryActor::ADiscoveryActor()
{
    PrimaryActorTick.bCanEverTick = false;
}

bool ADiscoveryActor::RegisterScan()
{
    bool bWasAlreadyDiscovered = bDiscovered;
    if (UGameInstance* GameInstance = GetGameInstance())
    {
        if (UDiscoverySubsystem* DiscoverySubsystem = GameInstance->GetSubsystem<UDiscoverySubsystem>())
        {
            const FName IdToRegister = DiscoveryId.IsNone() ? FName(*GetName()) : DiscoveryId;
            bWasAlreadyDiscovered = DiscoverySubsystem->IsDiscovered(IdToRegister);
            DiscoverySubsystem->RegisterDiscovery(IdToRegister);
        }

        if (!ObjectiveIdToCompleteOnScan.IsNone() && (!bCompleteObjectiveOnlyOnNewDiscovery || !bWasAlreadyDiscovered))
        {
            if (UObjectiveSubsystem* ObjectiveSubsystem = GameInstance->GetSubsystem<UObjectiveSubsystem>())
            {
                ObjectiveSubsystem->CompleteObjective(ObjectiveIdToCompleteOnScan);
            }
        }
    }

    bDiscovered = true;
    OnScanned(bWasAlreadyDiscovered);
    return !bWasAlreadyDiscovered;
}

FVector ADiscoveryActor::GetScanFocusLocation() const
{
    return GetActorLocation() + ScanFocusOffset;
}
