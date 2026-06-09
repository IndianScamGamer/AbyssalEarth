#include "AbyssalHUDSubsystem.h"
#include "AbyssalHealthComponent.h"
#include "OxygenComponent.h"
#include "StaminaComponent.h"
#include "TemperatureComponent.h"
#include "PressureComponent.h"
#include "GameFramework/Pawn.h"

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
        HealthComp->OnHealthChanged.AddDynamic(this, &UAbyssalHUDSubsystem::HandleHealthChanged);
    }
    if (OxygenComp.IsValid())
    {
        OxygenComp->OnOxygenChanged.AddDynamic(this, &UAbyssalHUDSubsystem::HandleOxygenChanged);
    }
    if (StaminaComp.IsValid())
    {
        StaminaComp->OnStaminaChanged.AddDynamic(this, &UAbyssalHUDSubsystem::HandleStaminaChanged);
    }
    if (TempComp.IsValid())
    {
        TempComp->OnTemperatureChanged.AddDynamic(this, &UAbyssalHUDSubsystem::HandleTemperatureChanged);
    }
    if (PressComp.IsValid())
    {
        PressComp->OnPressureChanged.AddDynamic(this, &UAbyssalHUDSubsystem::HandlePressureChanged);
    }
}

void UAbyssalHUDSubsystem::UnbindVitalDelegates()
{
    if (HealthComp.IsValid())
    {
        HealthComp->OnHealthChanged.RemoveDynamic(this, &UAbyssalHUDSubsystem::HandleHealthChanged);
    }
    if (OxygenComp.IsValid())
    {
        OxygenComp->OnOxygenChanged.RemoveDynamic(this, &UAbyssalHUDSubsystem::HandleOxygenChanged);
    }
    if (StaminaComp.IsValid())
    {
        StaminaComp->OnStaminaChanged.RemoveDynamic(this, &UAbyssalHUDSubsystem::HandleStaminaChanged);
    }
    if (TempComp.IsValid())
    {
        TempComp->OnTemperatureChanged.RemoveDynamic(this, &UAbyssalHUDSubsystem::HandleTemperatureChanged);
    }
    if (PressComp.IsValid())
    {
        PressComp->OnPressureChanged.RemoveDynamic(this, &UAbyssalHUDSubsystem::HandlePressureChanged);
    }
}

void UAbyssalHUDSubsystem::HandleHealthChanged(UAbyssalHealthComponent* /*HealthComponent*/, float /*NewHealth*/, float /*Delta*/)
{
    BroadcastReadout();
}

void UAbyssalHUDSubsystem::HandleOxygenChanged(float /*OxygenPercent*/, bool /*bSubmerged*/)
{
    BroadcastReadout();
}

void UAbyssalHUDSubsystem::HandleStaminaChanged(float /*StaminaPercent*/)
{
    BroadcastReadout();
}

void UAbyssalHUDSubsystem::HandleTemperatureChanged(float /*HeatPercent*/, bool /*bInHeatZone*/)
{
    BroadcastReadout();
}

void UAbyssalHUDSubsystem::HandlePressureChanged(float /*PressurePercent*/, bool /*bAboveRating*/)
{
    BroadcastReadout();
}

void UAbyssalHUDSubsystem::BroadcastReadout()
{
    OnVitalsUpdated.Broadcast(GetVitalReadout());
}
