#include "FabricatorStation.h"
#include "AbyssalRecipeDefinition.h"
#include "FabricationSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Kismet/GameplayStatics.h"

AFabricatorStation::AFabricatorStation()
{
    PrimaryActorTick.bCanEverTick = false;

    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    RootComponent = MeshComponent;
}

bool AFabricatorStation::CanInteract_Implementation(AActor* Interactor)
{
    return AvailableRecipes.Num() > 0;
}

FText AFabricatorStation::GetInteractionPrompt_Implementation()
{
    return NSLOCTEXT("FabricatorStation", "FabricatePrompt", "Use Fabricator");
}

void AFabricatorStation::OnInteract_Implementation(AActor* Interactor)
{
    RegisterRecipesWithSubsystem();
    BP_OnFabricatorActivated(Interactor);
}

void AFabricatorStation::OnBeginFocus_Implementation(AActor* Interactor)
{
    BP_OnFocusBegin();
}

void AFabricatorStation::OnEndFocus_Implementation(AActor* Interactor)
{
    BP_OnFocusEnd();
}

bool AFabricatorStation::CraftAtStation(FName RecipeId)
{
    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UFabricationSubsystem* Fabrication = GI->GetSubsystem<UFabricationSubsystem>())
        {
            return Fabrication->Craft(RecipeId, StationTier) == EAbyssalCraftResult::Success;
        }
    }
    return false;
}

void AFabricatorStation::RegisterRecipesWithSubsystem()
{
    UGameInstance* GI = UGameplayStatics::GetGameInstance(this);
    if (!GI)
    {
        return;
    }

    UFabricationSubsystem* Fabrication = GI->GetSubsystem<UFabricationSubsystem>();
    if (!Fabrication)
    {
        return;
    }

    for (UAbyssalRecipeDefinition* Recipe : AvailableRecipes)
    {
        Fabrication->RegisterRecipe(Recipe);
    }
}
