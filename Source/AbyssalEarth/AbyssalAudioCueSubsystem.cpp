#include "AbyssalAudioCueSubsystem.h"
#include "DiscoveryActor.h"
#include "DiscoverySubsystem.h"
#include "Engine/GameInstance.h"
#include "ObjectiveSubsystem.h"
#include "ScannerComponent.h"

namespace
{
    constexpr float ScannerPulseReferenceRadius = 1800.0f;
}

void UAbyssalAudioCueSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    BindCoreSubsystems(Collection);
}

void UAbyssalAudioCueSubsystem::Deinitialize()
{
    UnbindCoreSubsystems();

    for (UScannerComponent* ScannerComponent : RegisteredScanners)
    {
        if (!ScannerComponent)
        {
            continue;
        }

        ScannerComponent->OnScanPulseStartedEvent.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerPulseStarted);
        ScannerComponent->OnScanDiscoveryFoundEvent.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerDiscoveryFound);
        ScannerComponent->OnScanMissedEvent.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerMissed);
    }

    RegisteredScanners.Reset();
    Super::Deinitialize();
}

void UAbyssalAudioCueSubsystem::RegisterScannerComponent(UScannerComponent* ScannerComponent)
{
    if (!ScannerComponent)
    {
        return;
    }

    CleanRegisteredScanners();
    if (RegisteredScanners.Contains(ScannerComponent))
    {
        return;
    }

    RegisteredScanners.Add(ScannerComponent);
    ScannerComponent->OnScanPulseStartedEvent.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerPulseStarted);
    ScannerComponent->OnScanDiscoveryFoundEvent.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerDiscoveryFound);
    ScannerComponent->OnScanMissedEvent.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerMissed);
}

void UAbyssalAudioCueSubsystem::UnregisterScannerComponent(UScannerComponent* ScannerComponent)
{
    if (!ScannerComponent)
    {
        return;
    }

    ScannerComponent->OnScanPulseStartedEvent.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerPulseStarted);
    ScannerComponent->OnScanDiscoveryFoundEvent.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerDiscoveryFound);
    ScannerComponent->OnScanMissedEvent.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScannerMissed);
    RegisteredScanners.Remove(ScannerComponent);
}

void UAbyssalAudioCueSubsystem::RequestAmbienceCue(FName CueId, FVector WorldLocation, float Intensity)
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Ambience;
    CueEvent.CueId = CueId;
    CueEvent.WorldLocation = WorldLocation;
    CueEvent.Intensity = Intensity;
    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::RequestAudioCue(const FAbyssalAudioCueEvent& CueEvent)
{
    if (!CueEvent.CueId.IsNone())
    {
        OnAudioCueRequested.Broadcast(CueEvent);
    }
}

void UAbyssalAudioCueSubsystem::HandleDiscoveryAdded(const FAbyssalDiscoveryEntry& Entry)
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Discovery;
    CueEvent.CueId = FName(TEXT("SFX_Discovery_New"));
    CueEvent.RelatedId = Entry.DiscoveryId;
    CueEvent.DisplayText = Entry.DisplayName;
    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::HandleObjectiveChanged(const FAbyssalObjectiveStep& Objective)
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Objective;
    CueEvent.CueId = FName(TEXT("SFX_Objective_New"));
    CueEvent.RelatedId = Objective.ObjectiveId;
    CueEvent.DisplayText = Objective.Title;
    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::HandleObjectiveCompleted(FName ObjectiveId)
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Objective;
    CueEvent.CueId = FName(TEXT("SFX_Objective_Complete"));
    CueEvent.RelatedId = ObjectiveId;
    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::HandleRouteCompleted()
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::RouteComplete;
    CueEvent.CueId = FName(TEXT("MX_Route_Complete"));
    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::HandleScannerPulseStarted(FVector ScanOrigin, float EffectiveRadius)
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Scanner;
    CueEvent.CueId = FName(TEXT("SFX_Scanner_Pulse"));
    CueEvent.WorldLocation = ScanOrigin;
    CueEvent.Intensity = FMath::Max(0.25f, EffectiveRadius / ScannerPulseReferenceRadius);
    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::HandleScannerDiscoveryFound(ADiscoveryActor* Discovery, bool bNewDiscovery)
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Scanner;
    CueEvent.CueId = bNewDiscovery ? FName(TEXT("SFX_Scanner_Found_New")) : FName(TEXT("SFX_Scanner_Found_Known"));
    CueEvent.SourceObject = Discovery;

    if (Discovery)
    {
        CueEvent.RelatedId = Discovery->DiscoveryId;
        CueEvent.WorldLocation = Discovery->GetScanFocusLocation();
        CueEvent.DisplayText = Discovery->DisplayName;
    }

    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::HandleScannerMissed()
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Scanner;
    CueEvent.CueId = FName(TEXT("SFX_Scanner_Miss"));
    CueEvent.Intensity = 0.5f;
    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::BindCoreSubsystems(FSubsystemCollectionBase& Collection)
{
    Collection.InitializeDependency<UDiscoverySubsystem>();
    Collection.InitializeDependency<UObjectiveSubsystem>();

    UGameInstance* GameInstance = GetGameInstance();
    if (!GameInstance)
    {
        return;
    }

    if (UDiscoverySubsystem* DiscoverySubsystem = GameInstance->GetSubsystem<UDiscoverySubsystem>())
    {
        DiscoverySubsystem->OnDiscoveryAdded.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleDiscoveryAdded);
    }

    if (UObjectiveSubsystem* ObjectiveSubsystem = GameInstance->GetSubsystem<UObjectiveSubsystem>())
    {
        ObjectiveSubsystem->OnObjectiveChanged.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleObjectiveChanged);
        ObjectiveSubsystem->OnObjectiveCompleted.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleObjectiveCompleted);
        ObjectiveSubsystem->OnRouteCompleted.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleRouteCompleted);
    }
}

void UAbyssalAudioCueSubsystem::UnbindCoreSubsystems()
{
    UGameInstance* GameInstance = GetGameInstance();
    if (!GameInstance)
    {
        return;
    }

    if (UDiscoverySubsystem* DiscoverySubsystem = GameInstance->GetSubsystem<UDiscoverySubsystem>())
    {
        DiscoverySubsystem->OnDiscoveryAdded.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleDiscoveryAdded);
    }

    if (UObjectiveSubsystem* ObjectiveSubsystem = GameInstance->GetSubsystem<UObjectiveSubsystem>())
    {
        ObjectiveSubsystem->OnObjectiveChanged.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleObjectiveChanged);
        ObjectiveSubsystem->OnObjectiveCompleted.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleObjectiveCompleted);
        ObjectiveSubsystem->OnRouteCompleted.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleRouteCompleted);
    }
}

void UAbyssalAudioCueSubsystem::CleanRegisteredScanners()
{
    RegisteredScanners.RemoveAll([](const UScannerComponent* ScannerComponent)
    {
        return ScannerComponent == nullptr;
    });
}
