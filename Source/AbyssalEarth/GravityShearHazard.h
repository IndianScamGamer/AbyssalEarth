#pragma once

#include "CoreMinimal.h"
#include "AbyssalHazardBase.h"
#include "GravityShearHazard.generated.h"

/**
 * A gravity-inversion zone hazard (C2 — Gravity Well biome). While in the
 * Active phase, any actor with a UAbyssalTraversalComponent entering the
 * overlap volume is redirected along GravityDirection via
 * RequestGravityReorientation. Deals no direct damage but disorients and
 * reorients the player. Damage mode: None.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AGravityShearHazard : public AAbyssalHazardBase
{
    GENERATED_BODY()

public:
    AGravityShearHazard();

    /** Target gravity direction applied to traversal components inside the volume. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Gravity")
    FVector GravityDirection = FVector(0.0f, 0.0f, -1.0f);

    /** Duration of the reorientation blend (seconds). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Gravity", meta=(ClampMin="0.1"))
    float ReorientDuration = 0.6f;

protected:
    virtual void OnPhaseChanged(EHazardPhase NewPhase) override;

private:
    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Hazard|Gravity")
    TObjectPtr<USceneComponent> SceneRoot;

    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Hazard|Gravity")
    TObjectPtr<class UBoxComponent> ShearVolume;

    UFUNCTION()
    void OnShearOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
