#pragma once

#include "CoreMinimal.h"
#include "AbyssalSaveSubsystem.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "FabricationSubsystem.generated.h"

class UAbyssalRecipeDefinition;

UENUM(BlueprintType)
enum class EAbyssalCraftResult : uint8
{
    Success           UMETA(DisplayName = "Success"),
    MissingIngredients UMETA(DisplayName = "Missing Ingredients"),
    Locked            UMETA(DisplayName = "Recipe Locked"),
    StationTierTooLow UMETA(DisplayName = "Station Tier Too Low"),
    InvalidRecipe     UMETA(DisplayName = "Invalid Recipe"),
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalRecipeUnlockedSignature, FName, RecipeId);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalItemCraftedSignature, FName, RecipeId);

/**
 * Crafting authority. Holds the set of registered recipes and which are unlocked,
 * checks/consumes ingredients through UInventorySubsystem, and produces outputs.
 * Unlocked recipe IDs persist through UAbyssalProfileSaveGame::Fabrication.
 */
UCLASS()
class ABYSSALEARTH_API UFabricationSubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    /** Make a recipe known to the subsystem. Recipes without bRequiresUnlock are craftable immediately. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Fabrication")
    void RegisterRecipe(UAbyssalRecipeDefinition* Recipe);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Fabrication")
    void UnlockRecipe(FName RecipeId);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Fabrication")
    bool IsRecipeUnlocked(FName RecipeId) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Fabrication")
    bool IsRecipeRegistered(FName RecipeId) const;

    /** Whether the recipe can currently be crafted at the given station tier. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Fabrication")
    EAbyssalCraftResult CanCraft(FName RecipeId, int32 StationTier = 0) const;

    /** Attempt to craft: consumes inputs and adds the output to the inventory. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Fabrication")
    EAbyssalCraftResult Craft(FName RecipeId, int32 StationTier = 0);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Fabrication")
    TArray<FName> GetUnlockedRecipeIds() const;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Fabrication")
    FAbyssalRecipeUnlockedSignature OnRecipeUnlocked;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Fabrication")
    FAbyssalItemCraftedSignature OnItemCrafted;

private:
    UPROPERTY()
    TMap<FName, TObjectPtr<UAbyssalRecipeDefinition>> Recipes;

    UPROPERTY()
    TSet<FName> UnlockedRecipeIds;

    UAbyssalRecipeDefinition* FindRecipe(FName RecipeId) const;
};
