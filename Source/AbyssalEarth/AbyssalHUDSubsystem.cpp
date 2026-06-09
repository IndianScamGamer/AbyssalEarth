#include "AbyssalHUDSubsystem.h"
#include "AbyssalHealthComponent.h"
#include "OxygenComponent.h"
#include "StaminaComponent.h"
#include "TemperatureComponent.h"
#include "PressureComponent.h"
#include "GameFramework/Pawn.h"

void UAbyssalHUDSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
}

void UAbyssalHUDSubsystem::Deinitialize()
{
    UnbindVitalDelegates();
    Super::Deinitialize();
}

void UAbyssalHUDSubsystem::RegisterPlayerPawn(APawn* PlayerPawn)
{
    UnbindVitalDelegates();

    if (!PlayerPawn)
    {
        return;
    }

    HealthComp  = PlayerPawn->FindComponentByClass<UAbyssalHealthComponent>();
    OxygenComp  = PlayerPawn->FindComponentByClass<UOxygenComponent>();
    StaminaComp = PlayerPawn->FindComponentByClass<UStaminaComponent>();
    TempComp    = PlayerPawn->FindComponentByClass<UTemperatureComponent>();
    PressComp   = PlayerPawn->FindComponentByClass<UPressureComponent>();

    BindVitalDelegates();
    BroadcastReadout();
}

FAbyssalVitalReadout UAbyssalHUDSubsystem::GetVitalReadout() const
{
    FAbyssalVitalReadout R;

    if (HealthComp.IsValid())
    {
        R.HealthPercent = HealthComp->GetHealthPercent();
        R.bDead         = HealthComp->IsDead();
    }
    if (OxygenComp.IsValid())
    {
        R.OxygenPercent = OxygenComp->GetOxygenPercent() / 100.0f;
        R.bSubmerged    = OxygenComp->IsSubmerged();
    }
    if (StaminaComp.IsValid())
    {
        R.StaminaPercent = StaminaComp->GetStaminaPercent() / 100.0f;
        R.bExhausted     = StaminaComp->IsExhausted();
    }
    if (TempComp.IsValid())
    {
        R.HeatPercent  = TempComp->GetHeatPercent();
        R.bOverheating = TempComp->IsOverheating();
    }
    if (PressComp.IsValid())
    {
        R.PressurePercent       = PressComp->GetPressurePercent();
        R.bAbovePressureRating  = PressComp->IsAbovePressureRating();
    }

    return R;
}

void UAbyssalHUDSubsystem::BindVitalDelegates()
{
    if (HealthComp.IsValid())
    {
        HealthHandle = HealthComp->OnHealthChanged.AddLambda(
            [this](UAbyssalHealthComponent*, float, float) { BroadcastReadout(); });
    }
    if (OxygenComp.IsValid())
    {
        OxygenHandle = OxygenComp->OnOxygenChanged.AddLambda(
            [this](float, bool) { BroadcastReadout(); });
    }
    if (StaminaComp.IsValid())
    {
        StaminaHandle = StaminaComp->OnStaminaChanged.AddLambda(
            [this](float, bool) { BroadcastReadout(); });
    }
    if (TempComp.IsValid())
    {
        TempHandle = TempComp->OnTemperatureChanged.AddLambda(
            [this](float, bool) { BroadcastReadout(); });
    }
    if (PressComp.IsValid())
    {
        PressHandle = PressComp->OnPressureChanged.AddLambda(
            [this](float, bool) { BroadcastReadout(); });
    }
}

void UAbyssalHUDSubsystem::UnbindVitalDelegates()
{
    if (HealthComp.IsValid()  && HealthHandle.IsValid())  { HealthComp->OnHealthChanged.Remove(HealthHandle); }
    if (OxygenComp.IsValid()  && OxygenHandle.IsValid())  { OxygenComp->OnOxygenChanged.Remove(OxygenHandle); }
    if (StaminaComp.IsValid() && StaminaHandle.IsValid()) { StaminaComp->OnStaminaChanged.Remove(StaminaHandle); }
    if (TempComp.IsValid()    && TempHandle.IsValid())    { TempComp->OnTemperatureChanged.Remove(TempHandle); }
    if (PressComp.IsValid()   && PressHandle.IsValid())   { PressComp->OnPressureChanged.Remove(PressHandle); }

    HealthHandle  = FDelegateHandle();
    OxygenHandle  = FDelegateHandle();
    StaminaHandle = FDelegateHandle();
    TempHandle    = FDelegateHandle();
    PressHandle   = FDelegateHandle();
}

void UAbyssalHUDSubsystem::BroadcastReadout()
{
    OnVitalsUpdated.Broadcast(GetVitalReadout());
}
