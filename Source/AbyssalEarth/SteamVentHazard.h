#pragma once

#include "CoreMinimal.h"
#include "AbyssalHazardBase.h"
#include "SteamVentHazard.generated.h"

/**
 * Vertical steam column hazard (C2 — Gravity Well / shaft biomes).
 * Fires on a fixed interval: Warning (visual steam build-up) → Active (full column,
 * overlap damage) → Cooldown (dissipation). Damage mode: Overlap.
 * Blueprint subclass adds particle system and audio; this class owns timing and damage.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API ASteamVentHazard : public AAbyssalHazardBase
{
    GENERATED_BODY()

public:
    ASteamVentHazard();

    /** Height of the steam column collision capsule in cm. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Steam", meta=(ClampMin="50.0"))
    float ColumnHeight = 400.0f;

    /** Radius of the steam column in cm. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Steam", meta=(ClampMin="10.0"))
    float ColumnRadius = 60.0f;

    /** Upward impulse applied to actors caught in the active column. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Steam", meta=(ClampMin="0.0"))
    float LaunchImpulse = 600.0f;

protected:
    virtual void BeginPlay() override;
    virtual void OnActivePhaseBegin_Implementation() override;
    virtual void OnCooldownPhaseBegin_Implementation() override;

private:
    UPROPERTY()
    TObjectPtr<class UCapsuleComponent> SteamColumn;

    UFUNCTION()
    void OnSteamOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
