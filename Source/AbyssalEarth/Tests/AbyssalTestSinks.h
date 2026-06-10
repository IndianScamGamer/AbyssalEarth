#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "AbyssalTestSinks.generated.h"

/**
 * Delegate sink for automation tests. Dynamic multicast delegates can only
 * bind UFUNCTION handlers on a UObject (AddDynamic), so tests route their
 * delegate-fired assertions through an instance of this class.
 */
UCLASS()
class UAbyssalTestDelegateSink : public UObject
{
    GENERATED_BODY()

public:
    int32 ObjectiveCompletedCount = 0;
    int32 ItemCraftedCount = 0;
    FName LastObjectiveId;
    FName LastRecipeId;

    UFUNCTION()
    void HandleObjectiveCompleted(FName ObjectiveId)
    {
        ++ObjectiveCompletedCount;
        LastObjectiveId = ObjectiveId;
    }

    UFUNCTION()
    void HandleItemCrafted(FName RecipeId)
    {
        ++ItemCraftedCount;
        LastRecipeId = RecipeId;
    }
};
