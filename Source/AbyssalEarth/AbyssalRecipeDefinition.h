#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "AbyssalRecipeDefinition.generated.h"

/** One input or output line of a recipe: ItemId + quantity. */
USTRUCT(BlueprintType)
struct FAbyssalRecipeIngredient
{
    GENERATED_BODY()

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe")
    FName ItemId;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe", meta = (ClampMin = 1))
    int32 Count = 1;
};

/**
 * DataAsset defining a fabrication recipe.
 * Create instances in the Content Browser; ItemId references resolve against
 * UAbyssalItemDefinition assets. Primary asset type "AbyssalRecipe".
 */
UCLASS(BlueprintType)
class ABYSSALEARTH_API UAbyssalRecipeDefinition : public UPrimaryDataAsset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe")
    FName RecipeId;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe")
    FText DisplayName;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe", meta = (MultiLine = true))
    FText Description;

    /** Items consumed to craft this recipe. */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe")
    TArray<FAbyssalRecipeIngredient> Inputs;

    /** Item produced by crafting. */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe")
    FName OutputItemId;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe", meta = (ClampMin = 1))
    int32 OutputCount = 1;

    /** If true, the recipe must be unlocked (via UFabricationSubsystem::UnlockRecipe) before it can be crafted. */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe")
    bool bRequiresUnlock = false;

    /** Minimum fabricator-station tier required to craft. Stations advertise a tier; 0 = any/hand-craft. */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Recipe", meta = (ClampMin = 0))
    int32 RequiredStationTier = 0;

    virtual FPrimaryAssetId GetPrimaryAssetId() const override
    {
        return FPrimaryAssetId(TEXT("AbyssalRecipe"), RecipeId);
    }
};
