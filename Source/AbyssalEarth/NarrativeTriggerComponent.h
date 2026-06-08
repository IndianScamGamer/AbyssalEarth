#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "NarrativeTriggerComponent.generated.h"

class UPrimitiveComponent;

/**
 * Drops onto any trigger actor to fire a narrative beat (roadmap D1).
 * If bTriggerOnOverlap is set and the owner has a primitive root, it plays BeatId
 * the first time a pawn overlaps. Otherwise call Trigger() from Blueprint / sequencer.
 * One-shot semantics are enforced by UNarrativeSubsystem (per-beat bPlayOnce).
 */
UCLASS(ClassGroup=(AbyssalEarth), meta=(BlueprintSpawnableComponent))
class ABYSSALEARTH_API UNarrativeTriggerComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UNarrativeTriggerComponent();

    /** Beat row id to play (resolved against the subsystem's beat table). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Narrative")
    FName BeatId;

    /** Auto-fire when a pawn overlaps the owner's primitive root. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Narrative")
    bool bTriggerOnOverlap = true;

    /** Only pawns (player/controlled) trigger the beat, not arbitrary actors. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Narrative")
    bool bPawnOnly = true;

    /** Fire the configured beat now. */
    UFUNCTION(BlueprintCallable, Category = "Narrative")
    bool Trigger();

protected:
    virtual void BeginPlay() override;

    UFUNCTION()
    void HandleOwnerOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp,
        int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
