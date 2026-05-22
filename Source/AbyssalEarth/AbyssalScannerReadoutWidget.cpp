#include "AbyssalScannerReadoutWidget.h"

#include "GameFramework/Pawn.h"

void UAbyssalScannerReadoutWidget::NativeConstruct()
{
    Super::NativeConstruct();

    if (!BoundScannerComponent)
    {
        if (APawn* OwningPawn = GetOwningPlayerPawn())
        {
            BindToScanner(OwningPawn->FindComponentByClass<UScannerComponent>());
        }
    }
}

void UAbyssalScannerReadoutWidget::NativeDestruct()
{
    UnbindFromScanner();

    Super::NativeDestruct();
}

void UAbyssalScannerReadoutWidget::SetScannerComponent(UScannerComponent* InScannerComponent)
{
    BindToScanner(InScannerComponent);
}

UScannerComponent* UAbyssalScannerReadoutWidget::GetBoundScannerComponent() const
{
    return BoundScannerComponent;
}

FAbyssalScanResult UAbyssalScannerReadoutWidget::GetCurrentScanResult() const
{
    return CurrentScanResult;
}

FText UAbyssalScannerReadoutWidget::GetCurrentReadoutText() const
{
    if (!CurrentScanResult.bHasDiscovery)
    {
        return FText::FromString(TEXT("No signal"));
    }

    const FText DiscoveryName = CurrentScanResult.DisplayName.IsEmpty()
        ? FText::FromName(CurrentScanResult.DiscoveryId)
        : CurrentScanResult.DisplayName;

    const FText StatusText = CurrentScanResult.bNewDiscovery
        ? FText::FromString(TEXT("New discovery"))
        : FText::FromString(TEXT("Logged discovery"));

    return FText::Format(
        FText::FromString(TEXT("{0} | {1} | {2} m")),
        DiscoveryName,
        StatusText,
        FText::AsNumber(FMath::RoundToInt(CurrentScanResult.Distance / 100.0f)));
}

void UAbyssalScannerReadoutWidget::HandleScannerResultChanged(const FAbyssalScanResult& ScanResult)
{
    CurrentScanResult = ScanResult;
    BP_OnScannerResultChanged(CurrentScanResult);
}

void UAbyssalScannerReadoutWidget::HandleScannerPulseStarted(FVector ScanOrigin, float EffectiveRadius)
{
    BP_OnScannerPulseStarted(ScanOrigin, EffectiveRadius);
}

void UAbyssalScannerReadoutWidget::HandleScannerDiscoveryFound(ADiscoveryActor* Discovery, bool bNewDiscovery)
{
    BP_OnScannerDiscoveryFound(Discovery, bNewDiscovery);
}

void UAbyssalScannerReadoutWidget::HandleScannerMissed()
{
    CurrentScanResult = FAbyssalScanResult();
    BP_OnScannerMissed();
}

void UAbyssalScannerReadoutWidget::BindToScanner(UScannerComponent* InScannerComponent)
{
    if (BoundScannerComponent == InScannerComponent)
    {
        return;
    }

    UnbindFromScanner();
    BoundScannerComponent = InScannerComponent;

    if (!BoundScannerComponent)
    {
        CurrentScanResult = FAbyssalScanResult();
        return;
    }

    CurrentScanResult = BoundScannerComponent->GetLastScanResult();
    BoundScannerComponent->OnScanResultChanged.AddDynamic(this, &UAbyssalScannerReadoutWidget::HandleScannerResultChanged);
    BoundScannerComponent->OnScanPulseStartedEvent.AddDynamic(this, &UAbyssalScannerReadoutWidget::HandleScannerPulseStarted);
    BoundScannerComponent->OnScanDiscoveryFoundEvent.AddDynamic(this, &UAbyssalScannerReadoutWidget::HandleScannerDiscoveryFound);
    BoundScannerComponent->OnScanMissedEvent.AddDynamic(this, &UAbyssalScannerReadoutWidget::HandleScannerMissed);
    BP_OnScannerResultChanged(CurrentScanResult);
}

void UAbyssalScannerReadoutWidget::UnbindFromScanner()
{
    if (!BoundScannerComponent)
    {
        return;
    }

    BoundScannerComponent->OnScanResultChanged.RemoveDynamic(this, &UAbyssalScannerReadoutWidget::HandleScannerResultChanged);
    BoundScannerComponent->OnScanPulseStartedEvent.RemoveDynamic(this, &UAbyssalScannerReadoutWidget::HandleScannerPulseStarted);
    BoundScannerComponent->OnScanDiscoveryFoundEvent.RemoveDynamic(this, &UAbyssalScannerReadoutWidget::HandleScannerDiscoveryFound);
    BoundScannerComponent->OnScanMissedEvent.RemoveDynamic(this, &UAbyssalScannerReadoutWidget::HandleScannerMissed);
    BoundScannerComponent = nullptr;
}
