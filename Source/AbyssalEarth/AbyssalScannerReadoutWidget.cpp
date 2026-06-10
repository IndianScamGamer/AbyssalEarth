#include "AbyssalScannerReadoutWidget.h"

#include "AbyssalScanComponent.h"
#include "AbyssalScannable.h"
#include "GameFramework/Pawn.h"

void UAbyssalScannerReadoutWidget::NativeConstruct()
{
    Super::NativeConstruct();

    if (!BoundScanComponent)
    {
        if (APawn* OwningPawn = GetOwningPlayerPawn())
        {
            BindToScanner(OwningPawn->FindComponentByClass<UAbyssalScanComponent>());
        }
    }
}

void UAbyssalScannerReadoutWidget::NativeDestruct()
{
    UnbindFromScanner();

    Super::NativeDestruct();
}

void UAbyssalScannerReadoutWidget::SetScanComponent(UAbyssalScanComponent* InScanComponent)
{
    BindToScanner(InScanComponent);
}

UAbyssalScanComponent* UAbyssalScannerReadoutWidget::GetBoundScanComponent() const
{
    return BoundScanComponent;
}

FAbyssalScanReadout UAbyssalScannerReadoutWidget::GetCurrentScanReadout() const
{
    return CurrentReadout;
}

FText UAbyssalScannerReadoutWidget::GetCurrentReadoutText() const
{
    if (!CurrentReadout.bHasSignal)
    {
        return FText::FromString(TEXT("No signal"));
    }

    const FText DiscoveryName = CurrentReadout.DisplayName.IsEmpty()
        ? FText::FromName(CurrentReadout.DiscoveryId)
        : CurrentReadout.DisplayName;

    return FText::Format(
        FText::FromString(TEXT("{0} | {1} m")),
        DiscoveryName,
        FText::AsNumber(FMath::RoundToInt(CurrentReadout.Distance / 100.0f)));
}

void UAbyssalScannerReadoutWidget::HandleScanPulseFired()
{
    BP_OnScannerPulseStarted();
}

void UAbyssalScannerReadoutWidget::HandleScanHit(AActor* ScannedActor, FName DiscoveryId)
{
    CurrentReadout = FAbyssalScanReadout();
    CurrentReadout.bHasSignal = true;
    CurrentReadout.DiscoveryId = DiscoveryId;

    if (ScannedActor)
    {
        CurrentReadout.FocusLocation = ScannedActor->GetActorLocation();
        if (ScannedActor->Implements<UAbyssalScannable>())
        {
            CurrentReadout.DisplayName = IAbyssalScannable::Execute_GetScanDisplayName(ScannedActor);
        }
        if (const APawn* OwningPawn = GetOwningPlayerPawn())
        {
            CurrentReadout.Distance = FVector::Dist(OwningPawn->GetActorLocation(), CurrentReadout.FocusLocation);
        }
    }

    BP_OnScannerHit(ScannedActor, DiscoveryId);
    BP_OnScannerReadoutChanged(CurrentReadout);
}

void UAbyssalScannerReadoutWidget::HandleScanMissed()
{
    CurrentReadout = FAbyssalScanReadout();
    BP_OnScannerMissed();
    BP_OnScannerReadoutChanged(CurrentReadout);
}

void UAbyssalScannerReadoutWidget::BindToScanner(UAbyssalScanComponent* InScanComponent)
{
    if (BoundScanComponent == InScanComponent)
    {
        return;
    }

    UnbindFromScanner();
    BoundScanComponent = InScanComponent;

    if (!BoundScanComponent)
    {
        CurrentReadout = FAbyssalScanReadout();
        return;
    }

    BoundScanComponent->OnScanPulseFired.AddDynamic(this, &UAbyssalScannerReadoutWidget::HandleScanPulseFired);
    BoundScanComponent->OnScanHit.AddDynamic(this, &UAbyssalScannerReadoutWidget::HandleScanHit);
    BoundScanComponent->OnScanMissed.AddDynamic(this, &UAbyssalScannerReadoutWidget::HandleScanMissed);
    BP_OnScannerReadoutChanged(CurrentReadout);
}

void UAbyssalScannerReadoutWidget::UnbindFromScanner()
{
    if (!BoundScanComponent)
    {
        return;
    }

    BoundScanComponent->OnScanPulseFired.RemoveDynamic(this, &UAbyssalScannerReadoutWidget::HandleScanPulseFired);
    BoundScanComponent->OnScanHit.RemoveDynamic(this, &UAbyssalScannerReadoutWidget::HandleScanHit);
    BoundScanComponent->OnScanMissed.RemoveDynamic(this, &UAbyssalScannerReadoutWidget::HandleScanMissed);
    BoundScanComponent = nullptr;
}
