#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HeatZoneVolume.generated.h"

class UBoxComponent;
class UPrimitiveComponent;
struct FHitResult;

/**
 * Box volume that flags an overlapping actor's UTemperatureComponent as "in a heat
 * zone", so the component accumulates heat exposure while inside and cools after
 * leaving. Pairs with UTemperatureComponent (roadmap B3). Use for Mantle Garden heat
 * fields and any hot region.
 *
 * Limitation (v1): a simple in/out toggle, not reference-counted, so overlapping heat
 * zones on the same pawn are not stacked; keep heat volumes non-overlapping, or the
 * last EndOverlap clears the flag. Per-zone heat intensity is a later addition.
 */
UCLASS()
class ABYSSALEARTH_API AHeatZoneVolume : public AActor
{
    GENERATED_BODY()

public:
    AHeatZoneVolume();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Survival")
    TObjectPtr<UBoxComponent> HeatVolume;

private:
    UFUNCTION()
    void HandleBeginOverlap(
        UPrimitiveComponent* OverlappedComponent,
        AActor* OtherActor,
        UPrimitiveComponent* OtherComp,
        int32 OtherBodyIndex,
        bool bFromSweep,
        const FHitResult& SweepResult);

    UFUNCTION()
    void HandleEndOverlap(
        UPrimitiveComponent* OverlappedComponent,
        AActor* OtherActor,
        UPrimitiveComponent* OtherComp,
        int32 OtherBodyIndex);
};
