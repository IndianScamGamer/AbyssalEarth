#include "AbyssalScanComponent.h"
#include "AbyssalScannable.h"
#include "DiscoverySubsystem.h"
#include "DiscoverySaveGame.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/OverlapResult.h"

UAbyssalScanComponent::UAbyssalScanComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UAbyssalScanComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UAbyssalScanComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (CooldownRemaining > 0.0f)
    {
        CooldownRemaining = FMath::Max(0.0f, CooldownRemaining - DeltaTime);
        if (FMath::IsNearlyZero(CooldownRemaining))
        {
            OnScanCooldownComplete.Broadcast();
        }
    }
}

bool UAbyssalScanComponent::ScanPulse()
{
    if (CooldownRemaining > 0.0f)
    {
        return false;
    }

    UWorld* World = GetWorld();
    if (!World)
    {
        return false;
    }

    CooldownRemaining = CooldownDuration;
    OnScanPulseFired.Broadcast();

    UDiscoverySubsystem* DiscoverySub = nullptr;
    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        DiscoverySub = GI->GetSubsystem<UDiscoverySubsystem>();
    }

    const FVector Origin = GetOwner()->GetActorLocation();
    FCollisionShape Sphere = FCollisionShape::MakeSphere(ScanRadius);
    TArray<FOverlapResult> Overlaps;
    World->OverlapMultiByChannel(Overlaps, Origin, FQuat::Identity, ECC_Visibility, Sphere);

    TSet<AActor*> HitActors;
    for (const FOverlapResult& Overlap : Overlaps)
    {
        AActor* Actor = Overlap.GetActor();
        if (!Actor || Actor == GetOwner() || HitActors.Contains(Actor))
        {
            continue;
        }
        if (!Actor->Implements<UAbyssalScannable>())
        {
            continue;
        }
        HitActors.Add(Actor);

        const FName ScanId = IAbyssalScannable::Execute_GetScanId(Actor);
        const FText DisplayName = IAbyssalScannable::Execute_GetScanDisplayName(Actor);

        if (ScanId.IsNone())
        {
            continue;
        }

        const bool bAlreadyKnown = DiscoverySub && DiscoverySub->IsDiscovered(ScanId);

        if (DiscoverySub)
        {
            FAbyssalDiscoveryEntry Entry;
            Entry.DiscoveryId = ScanId;
            Entry.DisplayName = DisplayName;
            DiscoverySub->RegisterDiscoveryEntry(Entry);
        }

        IAbyssalScannable::Execute_OnScanned(Actor, GetOwner());

        if (!bAlreadyKnown || bRescanKnownActors)
        {
            OnScanHit.Broadcast(Actor, ScanId);
        }
    }

    return true;
}

float UAbyssalScanComponent::GetCooldownPercent() const
{
    if (CooldownDuration <= 0.0f)
    {
        return 1.0f;
    }
    return FMath::Clamp(1.0f - (CooldownRemaining / CooldownDuration), 0.0f, 1.0f);
}
