#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ReorientationVolume.generated.h"

class UBoxComponent;
class UPrimitiveComponent;

/**
 * Box trigger that reorients gravity for any pawn carrying a
 * UAbyssalTraversalComponent (roadmap C3; Gravity Well "Reorientation Passage").
 *
 * On overlap it calls RequestGravityReorientation(GravityDirection, ReorientDuration)
 * on the entering pawn's traversal component, which re-broadcasts so the character /
 * Blueprint applies the actual gravity-direction lerp. Place these in series to build
 * the 90°-per-room rotation sequence.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AReorientationVolume : public AActor
{
    GENERATED_BODY()

public:
    AReorientationVolume();

    /** Target gravity direction (world space) applied to pawns entering this volume. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Reorientation")
    FVector GravityDirection = FVector(0.0f, 0.0f, -1.0f);

    /** Seconds to lerp from current gravity to GravityDirection. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Reorientation", meta=(ClampMin="0.0"))
    float ReorientDuration = 0.5f;

protected:
    UFUNCTION()
    void HandleOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp,
        int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

    /** Fired after a valid pawn is reoriented; hook VFX/SFX. */
    UFUNCTION(BlueprintImplementableEvent, Category = "Reorientation")
    void BP_OnReoriented(AActor* Pawn);

private:
    UPROPERTY(VisibleAnywhere)
    TObjectPtr<UBoxComponent> TriggerBox;
};
