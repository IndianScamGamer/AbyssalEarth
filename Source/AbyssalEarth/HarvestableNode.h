#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AbyssalInteractable.h"
#include "HarvestableNode.generated.h"

class UAbyssalItemDefinition;
class UStaticMeshComponent;

/**
 * An actor in the world the player can interact with to receive items.
 * Implements IAbyssalInteractable; UInteractionComponent handles the focus/hold.
 * Set ItemDefinition and HarvestCount in the Details panel per-instance.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AHarvestableNode : public AActor, public IAbyssalInteractable
{
    GENERATED_BODY()

public:
    AHarvestableNode();

    // IAbyssalInteractable
    virtual bool CanInteract_Implementation(AActor* Interactor) override;
    virtual FText GetInteractionPrompt_Implementation() override;
    virtual void OnInteract_Implementation(AActor* Interactor) override;
    virtual void OnBeginFocus_Implementation(AActor* Interactor) override;
    virtual void OnEndFocus_Implementation(AActor* Interactor) override;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Harvest")
    TObjectPtr<UAbyssalItemDefinition> ItemDefinition;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Harvest", meta = (ClampMin = 1))
    int32 HarvestCount = 1;

    /** Seconds until the node re-enables. 0 = single-use (no respawn). */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Harvest", meta = (ClampMin = 0.0f))
    float RespawnTime = 30.0f;

    UFUNCTION(BlueprintPure, Category = "Harvest")
    bool IsHarvested() const { return bHarvested; }

protected:
    virtual void BeginPlay() override;

    UFUNCTION(BlueprintImplementableEvent, Category = "Harvest")
    void BP_OnHarvestBegin();

    UFUNCTION(BlueprintImplementableEvent, Category = "Harvest")
    void BP_OnHarvestRespawn();

    UFUNCTION(BlueprintImplementableEvent, Category = "Harvest")
    void BP_OnFocusBegin();

    UFUNCTION(BlueprintImplementableEvent, Category = "Harvest")
    void BP_OnFocusEnd();

private:
    UPROPERTY(VisibleAnywhere)
    TObjectPtr<UStaticMeshComponent> MeshComponent;

    bool bHarvested = false;
    FTimerHandle RespawnTimerHandle;

    void Respawn();
};
