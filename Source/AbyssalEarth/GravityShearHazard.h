#pragma once

#include "CoreMinimal.h"
#include "AbyssalHazardBase.h"
#include "GravityShearHazard.generated.h"

/**
 * A gravity-inversion zone hazard (C2 — Gravity Well biome). While Active,
 * any character entering the overlap volume is redirected along GravityDirection
 * via UAbyssalTraversalComponent::RequestGravityReorientation. Deals no direct
 * damage but disorients and reorients the player into dangerous terrain.
 * Damage mode: None (environmental traversal effect only).
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
    virtual void BeginPlay() override;
    virtual void OnActivePhaseBegin_Implementation() override;
    virtual void OnCooldownPhaseBegin_Implementation() override;

private:
    UPROPERTY()
    TObjectPtr<class UBoxComponent> ShearVolume;

    UFUNCTION()
    void OnShearOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
