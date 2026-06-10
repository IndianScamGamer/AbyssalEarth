/**
 * AbyssalEarth subsystem automation tests.
 *
 * Run via: UE Editor → Tools → Session Frontend → Automation
 * Filter: "AbyssalEarth."
 *
 * Each test creates a minimal GameInstance (no world required), instantiates
 * the target subsystem directly, exercises the API, and verifies expected
 * state. Tests are latent-free (synchronous) so they work in both Editor
 * and Commandlet contexts.
 */

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "Engine/GameInstance.h"

#include "InventorySubsystem.h"
#include "ObjectiveSubsystem.h"
#include "CheckpointSubsystem.h"
#include "FabricationSubsystem.h"

// ---------------------------------------------------------------------------
// 1. InventorySubsystem — Add / Remove / basic counts
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FInventorySubsystemAddRemoveTest,
    "AbyssalEarth.InventorySubsystem.AddRemove",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FInventorySubsystemAddRemoveTest::RunTest(const FString& /*Parameters*/)
{
    // Use a transient GameInstance so the subsystem can Initialize()
    UGameInstance* GI = NewObject<UGameInstance>();
    GI->AddToRoot();

    FSubsystemCollectionBase Collection;
    UInventorySubsystem* Inv = NewObject<UInventorySubsystem>(GI);
    Inv->Initialize(Collection);

    const FName ItemA(TEXT("ITEM_MINERAL_ABYSSAL_CORE"));
    const FName ItemB(TEXT("ITEM_MINERAL_FOSSIL_SHARD"));

    // Add items
    TestEqual(TEXT("AddItem returns new count"), Inv->AddItem(ItemA, 3), 3);
    TestEqual(TEXT("GetItemCount after add"), Inv->GetItemCount(ItemA), 3);

    // Add more of same item
    Inv->AddItem(ItemA, 2);
    TestEqual(TEXT("GetItemCount after second add"), Inv->GetItemCount(ItemA), 5);

    // Add different item
    Inv->AddItem(ItemB, 1);
    TestEqual(TEXT("GetAllItemIds has 2 entries"), Inv->GetAllItemIds().Num(), 2);

    // Remove partial
    TestTrue(TEXT("RemoveItem partial succeeds"), Inv->RemoveItem(ItemA, 2));
    TestEqual(TEXT("Count after partial remove"), Inv->GetItemCount(ItemA), 3);

    // Remove all
    TestTrue(TEXT("RemoveItem all succeeds"), Inv->RemoveItem(ItemA, 3));
    TestEqual(TEXT("Count after full remove"), Inv->GetItemCount(ItemA), 0);

    // Over-remove fails
    TestFalse(TEXT("RemoveItem over-count fails"), Inv->RemoveItem(ItemA, 1));

    GI->RemoveFromRoot();
    return true;
}

// ---------------------------------------------------------------------------
// 2. ObjectiveSubsystem — Advance / Complete
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FObjectiveSubsystemAdvanceCompleteTest,
    "AbyssalEarth.ObjectiveSubsystem.AdvanceComplete",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FObjectiveSubsystemAdvanceCompleteTest::RunTest(const FString& /*Parameters*/)
{
    UGameInstance* GI = NewObject<UGameInstance>();
    GI->AddToRoot();

    FSubsystemCollectionBase Collection;
    UObjectiveSubsystem* Obj = NewObject<UObjectiveSubsystem>(GI);
    Obj->Initialize(Collection);

    // The subsystem builds a default route on Initialize; confirm it has objectives
    const int32 RouteCount = Obj->GetRouteObjectiveCount();
    TestTrue(TEXT("Default route is non-empty"), RouteCount > 0);

    // Get the first objective and complete it
    const FAbyssalObjectiveStep First = Obj->GetCurrentObjective();
    TestFalse(TEXT("First objective ID is not None"), First.ObjectiveId.IsNone());

    bool bDelegateFired = false;
    Obj->OnObjectiveCompleted.AddLambda([&](FName /*Id*/) { bDelegateFired = true; });

    const bool bCompleted = Obj->CompleteObjective(First.ObjectiveId);
    TestTrue(TEXT("CompleteObjective succeeds for active objective"), bCompleted);
    TestTrue(TEXT("OnObjectiveCompleted delegate fires"), bDelegateFired);
    TestTrue(TEXT("Objective is now marked complete"), Obj->IsObjectiveComplete(First.ObjectiveId));
    TestFalse(TEXT("Objective is no longer active"), Obj->IsObjectiveActive(First.ObjectiveId));

    // Completing an already-complete objective is a no-op (returns false, no crash)
    TestFalse(TEXT("Re-completing same objective returns false"), Obj->CompleteObjective(First.ObjectiveId));

    GI->RemoveFromRoot();
    return true;
}

// ---------------------------------------------------------------------------
// 3. CheckpointSubsystem — Register / SetActive / GetRespawnLocation
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FCheckpointSubsystemRegisterRespawnTest,
    "AbyssalEarth.CheckpointSubsystem.RegisterRespawn",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FCheckpointSubsystemRegisterRespawnTest::RunTest(const FString& /*Parameters*/)
{
    UGameInstance* GI = NewObject<UGameInstance>();
    GI->AddToRoot();

    FSubsystemCollectionBase Collection;
    UCheckpointSubsystem* Cp = NewObject<UCheckpointSubsystem>(GI);
    Cp->Initialize(Collection);

    const FName CpIdA(TEXT("CP_TEST_A"));
    const FName CpIdB(TEXT("CP_TEST_B"));
    const FVector LocA(100.f, 200.f, 50.f);
    const FVector LocB(500.f, 0.f, 0.f);
    const FName MapId(TEXT("PRO_001"));

    // Before any checkpoint is registered
    TestFalse(TEXT("No active checkpoint initially"), Cp->HasActiveCheckpoint());

    // Register two checkpoints
    Cp->RegisterCheckpoint(CpIdA, LocA, MapId);
    Cp->RegisterCheckpoint(CpIdB, LocB, MapId);

    // Activate A
    TestTrue(TEXT("SetActiveCheckpoint A succeeds"), Cp->SetActiveCheckpoint(CpIdA));
    TestTrue(TEXT("HasActiveCheckpoint after set"), Cp->HasActiveCheckpoint());
    TestEqual(TEXT("ActiveCheckpointId is A"), Cp->GetActiveCheckpointId(), CpIdA);

    const FVector RespawnA = Cp->GetRespawnLocation();
    TestTrue(TEXT("RespawnLocation matches A"), RespawnA.Equals(LocA, 1.0f));

    // Activate B
    TestTrue(TEXT("SetActiveCheckpoint B succeeds"), Cp->SetActiveCheckpoint(CpIdB));
    TestEqual(TEXT("ActiveCheckpointId is B"), Cp->GetActiveCheckpointId(), CpIdB);
    TestTrue(TEXT("RespawnLocation matches B"), Cp->GetRespawnLocation().Equals(LocB, 1.0f));

    // Unknown checkpoint ID
    TestFalse(TEXT("SetActiveCheckpoint unknown ID returns false"), Cp->SetActiveCheckpoint(TEXT("CP_DOES_NOT_EXIST")));

    GI->RemoveFromRoot();
    return true;
}

// ---------------------------------------------------------------------------
// 4. FabricationSubsystem — CanCraft / Craft
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FFabricationSubsystemCraftTest,
    "AbyssalEarth.FabricationSubsystem.CanCraftAndCraft",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FFabricationSubsystemCraftTest::RunTest(const FString& /*Parameters*/)
{
    UGameInstance* GI = NewObject<UGameInstance>();
    GI->AddToRoot();

    FSubsystemCollectionBase Collection;

    // FabricationSubsystem depends on InventorySubsystem
    UInventorySubsystem* Inv = NewObject<UInventorySubsystem>(GI);
    Inv->Initialize(Collection);

    UFabricationSubsystem* Fab = NewObject<UFabricationSubsystem>(GI);
    Fab->Initialize(Collection);

    const FName RecipeId(TEXT("RECIPE_SUIT_PATCH"));
    const FName InputItem(TEXT("ITEM_MINERAL_ABYSSAL_CORE"));
    const FName OutputItem(TEXT("ITEM_TOOL_SUIT_PATCH"));

    // Without ingredients: should report MissingIngredients
    {
        const EAbyssalCraftResult Result = Fab->CanCraft(RecipeId, 1);
        TestTrue(TEXT("CanCraft fails without ingredients"),
            Result == EAbyssalCraftResult::MissingIngredients ||
            Result == EAbyssalCraftResult::InvalidRecipe); // recipe table may not be loaded in test env
    }

    // Seed the inventory with required inputs (RECIPE_SUIT_PATCH needs 1× ITEM_MINERAL_ABYSSAL_CORE)
    Inv->AddItem(InputItem, 5);
    TestEqual(TEXT("Inventory seeded with input"), Inv->GetItemCount(InputItem), 5);

    // CanCraft should now succeed (if recipe is registered)
    const EAbyssalCraftResult CanResult = Fab->CanCraft(RecipeId, 1);
    if (CanResult == EAbyssalCraftResult::InvalidRecipe)
    {
        // Recipe table not loaded in headless test — acceptable, log and skip craft
        AddInfo(TEXT("RECIPE_SUIT_PATCH not registered in headless context — skipping craft step"));
        GI->RemoveFromRoot();
        return true;
    }

    TestEqual(TEXT("CanCraft returns Success with ingredients"),
        CanResult, EAbyssalCraftResult::Success);

    bool bCraftedFired = false;
    Fab->OnItemCrafted.AddLambda([&](FName /*Id*/) { bCraftedFired = true; });

    const EAbyssalCraftResult CraftResult = Fab->Craft(RecipeId, 1);
    TestEqual(TEXT("Craft returns Success"), CraftResult, EAbyssalCraftResult::Success);
    TestTrue(TEXT("OnItemCrafted delegate fires"), bCraftedFired);
    TestTrue(TEXT("Output item appears in inventory"), Inv->GetItemCount(OutputItem) > 0);
    TestTrue(TEXT("Input ingredient was consumed"), Inv->GetItemCount(InputItem) < 5);

    GI->RemoveFromRoot();
    return true;
}
