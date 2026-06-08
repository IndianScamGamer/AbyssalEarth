#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AbyssalInteractable.h"
#include "FabricatorStation.generated.h"

class UAbyssalRecipeDefinition;
class UStaticMeshComponent;

/**
 * A world-placed crafting station. Implements IAbyssalInteractable; on interact
 * it registers its recipe list with UFabricationSubsystem and fires a Blueprint
 * event so the UI can present the craftable list. StationTier gates which
 * recipes (UAbyssalRecipeDefinition::RequiredStationTier) can be crafted here.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AFabricatorStation : public AActor, public IAbyssalInteractable
{
    GENERATED_BODY()

public:
    AFabricatorStation();

    // IAbyssalInteractable
    virtual bool CanInteract_Implementation(AActor* Interactor) override;
    virtual FText GetInteractionPrompt_Implementation() override;
    virtual void OnInteract_Implementation(AActor* Interactor) override;
    virtual void OnBeginFocus_Implementation(AActor* Interactor) override;
    virtual void OnEndFocus_Implementation(AActor* Interactor) override;

    /** Recipes this station offers. Registered with UFabricationSubsystem on interact. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Fabricator")
    TArray<TObjectPtr<UAbyssalRecipeDefinition>> AvailableRecipes;

    /** Station tier; recipes with a higher RequiredStationTier cannot be crafted here. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Fabricator", meta = (ClampMin = 0))
    int32 StationTier = 1;

    /** Convenience: craft a recipe at this station's tier via the subsystem. */
    UFUNCTION(BlueprintCallable, Category = "Fabricator")
    bool CraftAtStation(FName RecipeId);

protected:
    UFUNCTION(BlueprintImplementableEvent, Category = "Fabricator")
    void BP_OnFabricatorActivated(AActor* Interactor);

    UFUNCTION(BlueprintImplementableEvent, Category = "Fabricator")
    void BP_OnFocusBegin();

    UFUNCTION(BlueprintImplementableEvent, Category = "Fabricator")
    void BP_OnFocusEnd();

private:
    UPROPERTY(VisibleAnywhere)
    TObjectPtr<UStaticMeshComponent> MeshComponent;

    void RegisterRecipesWithSubsystem();
};
