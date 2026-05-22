#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ObjectiveTriggerActor.generated.h"

class UBoxComponent;
class UPrimitiveComponent;
struct FHitResult;

UCLASS()
class ABYSSALEARTH_API AObjectiveTriggerActor : public AActor
{
    GENERATED_BODY()

public:
    AObjectiveTriggerActor();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    TObjectPtr<UBoxComponent> TriggerVolume;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    FName ObjectiveIdToComplete;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    bool bRequireCurrentObjective = true;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    bool bTriggerOnce = true;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    bool bOnlyPlayerControlledPawn = true;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Objectives")
    void OnObjectiveTriggerActivated(bool bObjectiveAdvanced);

private:
    UFUNCTION()
    void HandleTriggerOverlap(
        UPrimitiveComponent* OverlappedComponent,
        AActor* OtherActor,
        UPrimitiveComponent* OtherComp,
        int32 OtherBodyIndex,
        bool bFromSweep,
        const FHitResult& SweepResult);
};
