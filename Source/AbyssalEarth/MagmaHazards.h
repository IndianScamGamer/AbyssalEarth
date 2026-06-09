#pragma once

#include "CoreMinimal.h"
#include "AbyssalHazardBase.h"
#include "MagmaHazards.generated.h"

/**
 * Geyser that erupts on a timed cycle. Warning phase: low-pressure bubble and
 * ground glow. Active phase: radial blast at the apex that damages and knocks
 * back nearby actors. Damage mode: Radial (AAbyssalHazardBase handles ApplyRadialDamage).
 * Biome: Mantle Garden.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AMagmaGeyserHazard : public AAbyssalHazardBase
{
    GENERATED_BODY()

public:
    AMagmaGeyserHazard();

    /** Radial damage radius at eruption apex in cm. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Magma", meta=(ClampMin="50.0"))
    float EruptionRadius = 350.0f;

    /** Height offset above the actor root at which the radial damage origin is placed. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Magma", meta=(ClampMin="0.0"))
    float ApexHeight = 500.0f;

    /** Radial knockback impulse magnitude (applied to characters in blast radius). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Magma", meta=(ClampMin="0.0"))
    float KnockbackImpulse = 900.0f;

protected:
    virtual void OnActivePhaseBegin_Implementation() override;
};

// ---------------------------------------------------------------------------

/**
 * Periodic radial magma pulse. No warning phase: Idle → Active (radial damage
 * burst) → Cooldown loop. Tighter radius than the geyser; high frequency.
 * Biome: Mantle Garden deep channels.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AMagmaPulseHazard : public AAbyssalHazardBase
{
    GENERATED_BODY()

public:
    AMagmaPulseHazard();

    /** Radius of each pulse in cm. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Magma", meta=(ClampMin="10.0"))
    float PulseRadius = 180.0f;

protected:
    virtual void OnActivePhaseBegin_Implementation() override;
};
