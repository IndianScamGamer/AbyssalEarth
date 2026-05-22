#include "ScannerComponent.h"
#include "DiscoveryActor.h"
#include "CollisionQueryParams.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"

UScannerComponent::UScannerComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UScannerComponent::Scan()
{
    AActor* Owner = GetOwner();
    if (!Owner)
    {
        return;
    }

    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    TArray<AActor*> Candidates;
    UGameplayStatics::GetAllActorsOfClass(World, ADiscoveryActor::StaticClass(), Candidates);

    ADiscoveryActor* BestDiscovery = nullptr;
    float BestScore = TNumericLimits<float>::Lowest();

    FVector ScanOrigin;
    FRotator ScanRotation;
    Owner->GetActorEyesViewPoint(ScanOrigin, ScanRotation);
    const FVector OwnerForward = ScanRotation.Vector();
    const float MaxScanDistance = ScanRadius + ForwardBonusDistance;

    LastScanResult = FAbyssalScanResult();
    OnScanPulseStarted(ScanOrigin, MaxScanDistance);
    OnScanPulseStartedEvent.Broadcast(ScanOrigin, MaxScanDistance);

    for (AActor* Candidate : Candidates)
    {
        ADiscoveryActor* Discovery = Cast<ADiscoveryActor>(Candidate);
        if (!Discovery)
        {
            continue;
        }

        const FVector ToDiscovery = Discovery->GetScanFocusLocation() - ScanOrigin;
        const float Distance = ToDiscovery.Length();
        const float FacingScore = FVector::DotProduct(OwnerForward, ToDiscovery.GetSafeNormal());
        const float AllowedDistance = ScanRadius + FMath::Max(FacingScore, 0.0f) * ForwardBonusDistance;
        if (Distance > AllowedDistance)
        {
            continue;
        }

        if (bRequireLineOfSight && !HasLineOfSightToDiscovery(Owner, ScanOrigin, Discovery))
        {
            continue;
        }

        const float DistanceScore = 1.0f - FMath::Clamp(Distance / FMath::Max(AllowedDistance, KINDA_SMALL_NUMBER), 0.0f, 1.0f);
        const float Score = DistanceScore + FMath::Max(FacingScore, 0.0f);

        if (Score > BestScore)
        {
            BestScore = Score;
            BestDiscovery = Discovery;
        }
    }

    LastDiscovery = BestDiscovery;
    if (LastDiscovery)
    {
        const bool bNewDiscovery = LastDiscovery->RegisterScan();
        LastScanResult.bHasDiscovery = true;
        LastScanResult.bNewDiscovery = bNewDiscovery;
        LastScanResult.Discovery = LastDiscovery;
        LastScanResult.DiscoveryId = LastDiscovery->DiscoveryId.IsNone() ? FName(*LastDiscovery->GetName()) : LastDiscovery->DiscoveryId;
        LastScanResult.DisplayName = LastDiscovery->DisplayName;
        LastScanResult.Category = LastDiscovery->Category;
        LastScanResult.FocusLocation = LastDiscovery->GetScanFocusLocation();
        LastScanResult.Distance = FVector::Distance(ScanOrigin, LastScanResult.FocusLocation);
        OnScanDiscoveryFound(LastDiscovery, bNewDiscovery);
        OnScanDiscoveryFoundEvent.Broadcast(LastDiscovery, bNewDiscovery);
    }
    else
    {
        OnScanMissed();
        OnScanMissedEvent.Broadcast();
    }

    OnScanResultChanged.Broadcast(LastScanResult);
}

FAbyssalScanResult UScannerComponent::GetLastScanResult() const
{
    return LastScanResult;
}

bool UScannerComponent::HasLineOfSightToDiscovery(const AActor* Owner, const FVector& ScanOrigin, const ADiscoveryActor* Discovery) const
{
    UWorld* World = GetWorld();
    if (!World || !Discovery)
    {
        return false;
    }

    FCollisionQueryParams Params(SCENE_QUERY_STAT(AbyssalScannerLineOfSight), false);
    Params.AddIgnoredActor(Owner);

    FHitResult Hit;
    const FVector ScanTarget = Discovery->GetScanFocusLocation();
    if (!World->LineTraceSingleByChannel(Hit, ScanOrigin, ScanTarget, LineOfSightTraceChannel, Params))
    {
        return true;
    }

    return Hit.GetActor() == Discovery;
}
