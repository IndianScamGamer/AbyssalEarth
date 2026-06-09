#pragma once

#include "CoreMinimal.h"
#include "AbyssalHazardBase.h"
#include "SteamVentHazard.generated.h"

/**
 * Vertical steam column hazard (C2 — Gravity Well / shaft biomes).
 * Cycles through the base phase loop: Idle (vent quiet) → Warning (steam
 * build-up) → Active (full column, overlap damage via the base damage tick)
 * → Cooldown (dissipation). Damage mode: Overlap; the column capsule is
 * registered as a damage primitive so the base class handles per-tick damage.
 * Blueprint subclass adds particle system and audio; this class owns timing,
 * collision, and the entry launch impulse.
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

    /** Upward impulse applied to characters entering the active column. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Steam", meta=(ClampMin="0.0"))
    float LaunchImpulse = 600.0f;

protected:
    virtual void BeginPlay() override;
    virtual void OnPhaseChanged(EHazardPhase NewPhase) override;

private:
    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Hazard|Steam")
    TObjectPtr<USceneComponent> SceneRoot;

    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Hazard|Steam")
    TObjectPtr<class UCapsuleComponent> SteamColumn;

    UFUNCTION()
    void OnSteamOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
