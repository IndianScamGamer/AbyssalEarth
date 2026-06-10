#include "AbyssalAudioCueSubsystem.h"
#include "AbyssalScanComponent.h"
#include "DiscoverySubsystem.h"
#include "Engine/GameInstance.h"
#include "GameFramework/Actor.h"
#include "ObjectiveSubsystem.h"

void UAbyssalAudioCueSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    BindCoreSubsystems(Collection);
}

void UAbyssalAudioCueSubsystem::Deinitialize()
{
    UnbindCoreSubsystems();

    for (UAbyssalScanComponent* ScanComponent : RegisteredScanners)
    {
        if (!ScanComponent)
        {
            continue;
        }

        ScanComponent->OnScanPulseFired.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanPulseFired);
        ScanComponent->OnScanHit.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanHit);
        ScanComponent->OnScanMissed.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanMissed);
    }

    RegisteredScanners.Reset();
    Super::Deinitialize();
}

void UAbyssalAudioCueSubsystem::RegisterScanComponent(UAbyssalScanComponent* ScanComponent)
{
    if (!ScanComponent)
    {
        return;
    }

    CleanRegisteredScanners();
    if (RegisteredScanners.Contains(ScanComponent))
    {
        return;
    }

    RegisteredScanners.Add(ScanComponent);
    ScanComponent->OnScanPulseFired.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanPulseFired);
    ScanComponent->OnScanHit.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanHit);
    ScanComponent->OnScanMissed.AddDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanMissed);
}

void UAbyssalAudioCueSubsystem::UnregisterScanComponent(UAbyssalScanComponent* ScanComponent)
{
    if (!ScanComponent)
    {
        return;
    }

    ScanComponent->OnScanPulseFired.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanPulseFired);
    ScanComponent->OnScanHit.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanHit);
    ScanComponent->OnScanMissed.RemoveDynamic(this, &UAbyssalAudioCueSubsystem::HandleScanMissed);
    RegisteredScanners.Remove(ScanComponent);
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

void UAbyssalAudioCueSubsystem::HandleScanPulseFired()
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Scanner;
    CueEvent.CueId = FName(TEXT("SFX_Scanner_Pulse"));
    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::HandleScanHit(AActor* ScannedActor, FName DiscoveryId)
{
    FAbyssalAudioCueEvent CueEvent;
    CueEvent.CueType = EAbyssalAudioCueType::Scanner;
    CueEvent.CueId = FName(TEXT("SFX_Scanner_Found_New"));
    CueEvent.RelatedId = DiscoveryId;
    CueEvent.SourceObject = ScannedActor;

    if (ScannedActor)
    {
        CueEvent.WorldLocation = ScannedActor->GetActorLocation();
    }

    RequestAudioCue(CueEvent);
}

void UAbyssalAudioCueSubsystem::HandleScanMissed()
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
    RegisteredScanners.RemoveAll([](const UAbyssalScanComponent* ScanComponent)
    {
        return ScanComponent == nullptr;
    });
}
