#include "FabricationSubsystem.h"
#include "AbyssalRecipeDefinition.h"
#include "AbyssalProfileSaveGame.h"
#include "InventorySubsystem.h"

void UFabricationSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    Collection.InitializeDependency(UAbyssalSaveSubsystem::StaticClass());
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->RegisterSaveProvider(this);
    }
}

void UFabricationSubsystem::Deinitialize()
{
    if (UAbyssalSaveSubsystem* SaveSub = GetGameInstance()->GetSubsystem<UAbyssalSaveSubsystem>())
    {
        SaveSub->UnregisterSaveProvider(this);
    }
    Super::Deinitialize();
}

void UFabricationSubsystem::OnSaveRequested(UAbyssalProfileSaveGame* SaveGame)
{
    SaveGame->Fabrication.UnlockedRecipeIds = UnlockedRecipeIds.Array();
}

void UFabricationSubsystem::OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame)
{
    UnlockedRecipeIds.Reset();
    for (const FName& Id : SaveGame->Fabrication.UnlockedRecipeIds)
    {
        if (!Id.IsNone())
        {
            UnlockedRecipeIds.Add(Id);
        }
    }
}

void UFabricationSubsystem::RegisterRecipe(UAbyssalRecipeDefinition* Recipe)
{
    if (!Recipe || Recipe->RecipeId.IsNone())
    {
        return;
    }

    Recipes.Add(Recipe->RecipeId, Recipe);

    // Recipes that do not require an explicit unlock are available from the start.
    if (!Recipe->bRequiresUnlock)
    {
        UnlockedRecipeIds.Add(Recipe->RecipeId);
    }
}

void UFabricationSubsystem::UnlockRecipe(FName RecipeId)
{
    if (RecipeId.IsNone() || UnlockedRecipeIds.Contains(RecipeId))
    {
        return;
    }

    UnlockedRecipeIds.Add(RecipeId);
    OnRecipeUnlocked.Broadcast(RecipeId);
}

bool UFabricationSubsystem::IsRecipeUnlocked(FName RecipeId) const
{
    return UnlockedRecipeIds.Contains(RecipeId);
}

bool UFabricationSubsystem::IsRecipeRegistered(FName RecipeId) const
{
    return Recipes.Contains(RecipeId);
}

EAbyssalCraftResult UFabricationSubsystem::CanCraft(FName RecipeId, int32 StationTier) const
{
    UAbyssalRecipeDefinition* Recipe = FindRecipe(RecipeId);
    if (!Recipe)
    {
        return EAbyssalCraftResult::InvalidRecipe;
    }

    if (Recipe->bRequiresUnlock && !UnlockedRecipeIds.Contains(RecipeId))
    {
        return EAbyssalCraftResult::Locked;
    }

    if (StationTier < Recipe->RequiredStationTier)
    {
        return EAbyssalCraftResult::StationTierTooLow;
    }

    const UInventorySubsystem* Inventory = GetGameInstance()->GetSubsystem<UInventorySubsystem>();
    if (!Inventory)
    {
        return EAbyssalCraftResult::MissingIngredients;
    }

    for (const FAbyssalRecipeIngredient& Input : Recipe->Inputs)
    {
        if (!Inventory->HasItem(Input.ItemId, Input.Count))
        {
            return EAbyssalCraftResult::MissingIngredients;
        }
    }

    return EAbyssalCraftResult::Success;
}

EAbyssalCraftResult UFabricationSubsystem::Craft(FName RecipeId, int32 StationTier)
{
    const EAbyssalCraftResult Check = CanCraft(RecipeId, StationTier);
    if (Check != EAbyssalCraftResult::Success)
    {
        return Check;
    }

    UAbyssalRecipeDefinition* Recipe = FindRecipe(RecipeId);
    UInventorySubsystem* Inventory = GetGameInstance()->GetSubsystem<UInventorySubsystem>();
    if (!Recipe || !Inventory)
    {
        return EAbyssalCraftResult::InvalidRecipe;
    }

    // CanCraft already verified sufficiency; consume inputs then produce output.
    for (const FAbyssalRecipeIngredient& Input : Recipe->Inputs)
    {
        Inventory->RemoveItem(Input.ItemId, Input.Count);
    }

    if (!Recipe->OutputItemId.IsNone())
    {
        Inventory->AddItem(Recipe->OutputItemId, Recipe->OutputCount);
    }

    OnItemCrafted.Broadcast(RecipeId);
    return EAbyssalCraftResult::Success;
}

TArray<FName> UFabricationSubsystem::GetUnlockedRecipeIds() const
{
    return UnlockedRecipeIds.Array();
}

UAbyssalRecipeDefinition* UFabricationSubsystem::FindRecipe(FName RecipeId) const
{
    const TObjectPtr<UAbyssalRecipeDefinition>* Found = Recipes.Find(RecipeId);
    return Found ? *Found : nullptr;
}
