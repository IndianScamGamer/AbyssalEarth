#pragma once

#include "CoreMinimal.h"
#include "AbyssalHazardBase.h"
#include "StructuralHazards.generated.h"

/**
 * A walkway section that fractures under repeated weight. Each time a pawn
 * lands on or stands on the trigger, integrity decreases. At zero integrity
 * the section enters Active phase: platform actors detach, simulating collapse.
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

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Hazard|Structural")
    int32 GetCurrentIntegrity() const { return CurrentIntegrity; }

protected:
    virtual void BeginPlay() override;
    virtual void OnActivePhaseBegin_Implementation() override;
    virtual void OnIdlePhaseBegin_Implementation() override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard|Structural")
    void BP_OnIntegrityChanged(int32 NewIntegrity);

private:
    UPROPERTY()
    int32 CurrentIntegrity = 0;

    UPROPERTY()
    TObjectPtr<class UBoxComponent> WeightTrigger;

    UFUNCTION()
    void OnPawnLanded(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};

// ---------------------------------------------------------------------------

/**
 * A ceiling fragment that falls when the player enters the proximity trigger.
 * Deals impact damage on landing via radial damage. One-shot by default;
 * RespawnDelay > 0 resets it. Biome: Fossil Sky, Gravity Well ceilings.
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

    /** Impact damage radius when the fragment hits the ground. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Structural", meta=(ClampMin="10.0"))
    float ImpactRadius = 120.0f;

    /** Impact damage dealt on landing. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Structural", meta=(ClampMin="0.0"))
    float ImpactDamage = 40.0f;

protected:
    virtual void BeginPlay() override;
    virtual void OnWarningPhaseBegin_Implementation() override;
    virtual void OnActivePhaseBegin_Implementation() override;

private:
    UPROPERTY()
    TObjectPtr<class USphereComponent> ProximityTrigger;

    FVector FallOrigin;

    UFUNCTION()
    void OnProximityOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
