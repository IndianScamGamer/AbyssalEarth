#pragma once

#include "CoreMinimal.h"
#include "AbyssalHazardBase.h"
#include "StructuralHazards.generated.h"

/**
 * A walkway section that fractures under repeated weight. Each time a pawn
 * steps on the trigger, integrity decreases. At zero integrity the hazard
 * activates: instant Warning (creak) then Active (collision drops away,
 * the player falls). If RespawnDelay > 0 the walkway restores after the
 * cooldown; otherwise it stays collapsed. Damage mode: None.
 * Biome: Fossil Sky (ancient bone structures).
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API ABrittleWalkwaySection : public AAbyssalHazardBase
{
    GENERATED_BODY()

public:
    ABrittleWalkwaySection();

    /** How many pawn-steps before the walkway collapses. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Structural", meta=(ClampMin="1"))
    int32 MaxIntegrity = 3;

    /** Seconds after collapse before the walkway respawns (0 = no respawn). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Structural", meta=(ClampMin="0.0"))
    float RespawnDelay = 0.0f;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard|Structural")
    int32 GetCurrentIntegrity() const { return CurrentIntegrity; }

protected:
    virtual void BeginPlay() override;
    virtual void OnPhaseChanged(EHazardPhase NewPhase) override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard|Structural")
    void BP_OnIntegrityChanged(int32 NewIntegrity);

private:
    UPROPERTY()
    int32 CurrentIntegrity = 0;

    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Hazard|Structural")
    TObjectPtr<USceneComponent> SceneRoot;

    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Hazard|Structural")
    TObjectPtr<class UBoxComponent> WeightTrigger;

    bool bCollapsedOnce = false;

    UFUNCTION()
    void OnPawnStepped(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

    void SetWalkwaySolid(bool bSolid);
};

// ---------------------------------------------------------------------------

/**
 * A ceiling fragment that falls when the player enters the proximity trigger.
 * One-shot: trigger → Warning (shake) → Active (physics drop + impact radial
 * damage) → permanently deactivated. Damage mode: None (the impact damage is
 * applied manually on activation). Biome: Fossil Sky, Gravity Well ceilings.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API ACeilingFragmentHazard : public AAbyssalHazardBase
{
    GENERATED_BODY()

public:
    ACeilingFragmentHazard();

    /** Detection radius below the fragment that triggers the fall. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Structural", meta=(ClampMin="10.0"))
    float ProximityRadius = 250.0f;

    /** Impact damage radius when the fragment drops. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Structural", meta=(ClampMin="10.0"))
    float ImpactRadius = 120.0f;

    /** Impact damage dealt by the drop. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Structural", meta=(ClampMin="0.0"))
    float ImpactDamage = 40.0f;

protected:
    virtual void BeginPlay() override;
    virtual void OnPhaseChanged(EHazardPhase NewPhase) override;

private:
    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Hazard|Structural")
    TObjectPtr<USceneComponent> SceneRoot;

    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Hazard|Structural")
    TObjectPtr<class USphereComponent> ProximityTrigger;

    bool bTriggered = false;

    UFUNCTION()
    void OnProximityOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
