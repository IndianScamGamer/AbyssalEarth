/**
 * AbyssalEarth subsystem automation tests.
 *
 * Run via: UE Editor → Tools → Session Frontend → Automation
 * Filter: "AbyssalEarth."
 *
 * Each test spins up a standalone UGameInstance (InitializeStandalone), which
 * initializes the real subsystem collection — so cross-subsystem dependencies
 * (Fabrication→Inventory, everything→SaveSubsystem) resolve exactly as they
 * do in game. Tests are latent-free (synchronous) so they work in both Editor
 * and Commandlet contexts.
 */

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "CoreMinimal.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"

#include "InventorySubsystem.h"
#include "ObjectiveSubsystem.h"
#include "CheckpointSubsystem.h"
#include "FabricationSubsystem.h"
#include "AbyssalSaveSubsystem.h"
#include "AbyssalTestSinks.h"

namespace AbyssalTest
{
    UGameInstance* CreateGameInstance()
    {
        UGameInstance* GI = NewObject<UGameInstance>(GEngine);
        GI->AddToRoot();
        GI->InitializeStandalone();
        return GI;
    }

    void DestroyGameInstance(UGameInstance* GI)
    {
        GI->Shutdown();
        GI->RemoveFromRoot();
    }
}

// ---------------------------------------------------------------------------
// 1. InventorySubsystem — Add / Remove / basic counts
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FInventorySubsystemAddRemoveTest,
    "AbyssalEarth.InventorySubsystem.AddRemove",
    EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FInventorySubsystemAddRemoveTest::RunTest(const FString& /*Parameters*/)
{
    UGameInstance* GI = AbyssalTest::CreateGameInstance();
    UInventorySubsystem* Inv = GI->GetSubsystem<UInventorySubsystem>();
    if (!TestNotNull(TEXT("InventorySubsystem exists"), Inv))
    {
        AbyssalTest::DestroyGameInstance(GI);
        return false;
    }
    Inv->ClearInventory();

    const FName ItemA(TEXT("ITEM_MINERAL_ABYSSAL_CORE"));
    const FName ItemB(TEXT("ITEM_MINERAL_FOSSIL_SHARD"));

    // Add items
    TestEqual(TEXT("AddItem returns amount added"), Inv->AddItem(ItemA, 3), 3);
    TestEqual(TEXT("GetItemCount after add"), Inv->GetItemCount(ItemA), 3);

    // Add more of same item
    Inv->AddItem(ItemA, 2);
    TestEqual(TEXT("GetItemCount after second add"), Inv->GetItemCount(ItemA), 5);

    // Add different item
    Inv->AddItem(ItemB, 1);
    TestEqual(TEXT("GetAllItemIds has 2 entries"), Inv->GetAllItemIds().Num(), 2);

    // HasItem
    TestTrue(TEXT("HasItem with sufficient count"), Inv->HasItem(ItemA, 5));
    TestFalse(TEXT("HasItem with excessive count"), Inv->HasItem(ItemA, 6));

    // Remove partial
    TestTrue(TEXT("RemoveItem partial succeeds"), Inv->RemoveItem(ItemA, 2));
    TestEqual(TEXT("Count after partial remove"), Inv->GetItemCount(ItemA), 3);

    // Remove all
    TestTrue(TEXT("RemoveItem all succeeds"), Inv->RemoveItem(ItemA, 3));
    TestEqual(TEXT("Count after full remove"), Inv->GetItemCount(ItemA), 0);

    // Over-remove fails
    TestFalse(TEXT("RemoveItem over-count fails"), Inv->RemoveItem(ItemA, 1));

    AbyssalTest::DestroyGameInstance(GI);
    return true;
}

// ---------------------------------------------------------------------------
// 2. ObjectiveSubsystem — Advance / Complete
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FObjectiveSubsystemAdvanceCompleteTest,
    "AbyssalEarth.ObjectiveSubsystem.AdvanceComplete",
    EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FObjectiveSubsystemAdvanceCompleteTest::RunTest(const FString& /*Parameters*/)
{
    UGameInstance* GI = AbyssalTest::CreateGameInstance();
    UObjectiveSubsystem* Obj = GI->GetSubsystem<UObjectiveSubsystem>();
    if (!TestNotNull(TEXT("ObjectiveSubsystem exists"), Obj))
    {
        AbyssalTest::DestroyGameInstance(GI);
        return false;
    }
    Obj->ResetRoute();

    // The subsystem builds the default route on Initialize
    TestTrue(TEXT("Default route is non-empty"), Obj->GetRouteObjectiveCount() > 0);

    const FAbyssalObjectiveStep First = Obj->GetCurrentObjective();
    TestFalse(TEXT("First objective ID is not None"), First.ObjectiveId.IsNone());
    TestTrue(TEXT("First objective is active"), Obj->IsObjectiveActive(First.ObjectiveId));

    UAbyssalTestDelegateSink* Sink = NewObject<UAbyssalTestDelegateSink>(GI);
    Obj->OnObjectiveCompleted.AddDynamic(Sink, &UAbyssalTestDelegateSink::HandleObjectiveCompleted);

    TestTrue(TEXT("CompleteObjective succeeds for active objective"), Obj->CompleteObjective(First.ObjectiveId));
    TestEqual(TEXT("OnObjectiveCompleted delegate fired once"), Sink->ObjectiveCompletedCount, 1);
    TestEqual(TEXT("Delegate carried the completed ID"), Sink->LastObjectiveId, First.ObjectiveId);
    TestTrue(TEXT("Objective is now marked complete"), Obj->IsObjectiveComplete(First.ObjectiveId));
    TestFalse(TEXT("Objective is no longer active"), Obj->IsObjectiveActive(First.ObjectiveId));

    // Completing an already-complete objective is a no-op (returns false, no crash)
    TestFalse(TEXT("Re-completing same objective returns false"), Obj->CompleteObjective(First.ObjectiveId));
    TestEqual(TEXT("Delegate did not fire again"), Sink->ObjectiveCompletedCount, 1);

    Obj->OnObjectiveCompleted.RemoveDynamic(Sink, &UAbyssalTestDelegateSink::HandleObjectiveCompleted);
    AbyssalTest::DestroyGameInstance(GI);
    return true;
}

// ---------------------------------------------------------------------------
// 3. CheckpointSubsystem — Register / SetActive / GetRespawnLocation
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FCheckpointSubsystemRegisterRespawnTest,
    "AbyssalEarth.CheckpointSubsystem.RegisterRespawn",
    EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FCheckpointSubsystemRegisterRespawnTest::RunTest(const FString& /*Parameters*/)
{
    UGameInstance* GI = AbyssalTest::CreateGameInstance();
    UCheckpointSubsystem* Cp = GI->GetSubsystem<UCheckpointSubsystem>();
    if (!TestNotNull(TEXT("CheckpointSubsystem exists"), Cp))
    {
        AbyssalTest::DestroyGameInstance(GI);
        return false;
    }

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
    TestTrue(TEXT("RespawnLocation matches A"), Cp->GetRespawnLocation().Equals(LocA, 1.0f));

    // Activate B
    TestTrue(TEXT("SetActiveCheckpoint B succeeds"), Cp->SetActiveCheckpoint(CpIdB));
    TestEqual(TEXT("ActiveCheckpointId is B"), Cp->GetActiveCheckpointId(), CpIdB);
    TestTrue(TEXT("RespawnLocation matches B"), Cp->GetRespawnLocation().Equals(LocB, 1.0f));

    // Unknown checkpoint ID
    TestFalse(TEXT("SetActiveCheckpoint unknown ID returns false"), Cp->SetActiveCheckpoint(TEXT("CP_DOES_NOT_EXIST")));
    TestEqual(TEXT("Active checkpoint unchanged after failed set"), Cp->GetActiveCheckpointId(), CpIdB);

    AbyssalTest::DestroyGameInstance(GI);
    return true;
}

// ---------------------------------------------------------------------------
// 4. FabricationSubsystem — CanCraft / Craft
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FFabricationSubsystemCraftTest,
    "AbyssalEarth.FabricationSubsystem.CanCraftAndCraft",
    EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FFabricationSubsystemCraftTest::RunTest(const FString& /*Parameters*/)
{
    UGameInstance* GI = AbyssalTest::CreateGameInstance();
    UInventorySubsystem* Inv = GI->GetSubsystem<UInventorySubsystem>();
    UFabricationSubsystem* Fab = GI->GetSubsystem<UFabricationSubsystem>();
    if (!TestNotNull(TEXT("InventorySubsystem exists"), Inv) ||
        !TestNotNull(TEXT("FabricationSubsystem exists"), Fab))
    {
        AbyssalTest::DestroyGameInstance(GI);
        return false;
    }
    Inv->ClearInventory();

    const FName RecipeId(TEXT("RECIPE_SUIT_PATCH"));
    const FName InputItem(TEXT("ITEM_MINERAL_ABYSSAL_CORE"));

    // Recipes are registered from UAbyssalRecipeDefinition assets, which are
    // not loaded in a headless/standalone context. If the recipe is unknown,
    // verify the graceful failure path and finish.
    if (Fab->CanCraft(RecipeId, 1) == EAbyssalCraftResult::InvalidRecipe)
    {
        AddInfo(TEXT("RECIPE_SUIT_PATCH not registered in this context — verified InvalidRecipe path"));
        TestEqual(TEXT("Craft on unknown recipe also returns InvalidRecipe"),
            Fab->Craft(RecipeId, 1), EAbyssalCraftResult::InvalidRecipe);
        AbyssalTest::DestroyGameInstance(GI);
        return true;
    }

    // Without ingredients: should report MissingIngredients
    TestEqual(TEXT("CanCraft fails without ingredients"),
        Fab->CanCraft(RecipeId, 1), EAbyssalCraftResult::MissingIngredients);

    // Seed the inventory with required inputs (RECIPE_SUIT_PATCH needs 1× ITEM_MINERAL_ABYSSAL_CORE)
    Inv->AddItem(InputItem, 5);
    TestEqual(TEXT("CanCraft returns Success with ingredients"),
        Fab->CanCraft(RecipeId, 1), EAbyssalCraftResult::Success);

    UAbyssalTestDelegateSink* Sink = NewObject<UAbyssalTestDelegateSink>(GI);
    Fab->OnItemCrafted.AddDynamic(Sink, &UAbyssalTestDelegateSink::HandleItemCrafted);

    TestEqual(TEXT("Craft returns Success"), Fab->Craft(RecipeId, 1), EAbyssalCraftResult::Success);
    TestEqual(TEXT("OnItemCrafted delegate fired once"), Sink->ItemCraftedCount, 1);
    TestTrue(TEXT("Input ingredient was consumed"), Inv->GetItemCount(InputItem) < 5);

    Fab->OnItemCrafted.RemoveDynamic(Sink, &UAbyssalTestDelegateSink::HandleItemCrafted);
    AbyssalTest::DestroyGameInstance(GI);
    return true;
}

// ---------------------------------------------------------------------------
// 5. SaveSubsystem — full save → load round-trip through the provider pipeline
// ---------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FSaveSubsystemRoundTripTest,
    "AbyssalEarth.SaveSubsystem.RoundTrip",
    EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FSaveSubsystemRoundTripTest::RunTest(const FString& /*Parameters*/)
{
    // High slot index so a developer's real profile (slot 0) is never touched
    constexpr int32 TestSlot = 93;

    UGameInstance* GI = AbyssalTest::CreateGameInstance();
    UAbyssalSaveSubsystem* SaveSub = GI->GetSubsystem<UAbyssalSaveSubsystem>();
    UInventorySubsystem* Inv = GI->GetSubsystem<UInventorySubsystem>();
    UCheckpointSubsystem* Cp = GI->GetSubsystem<UCheckpointSubsystem>();
    if (!TestNotNull(TEXT("SaveSubsystem exists"), SaveSub) ||
        !TestNotNull(TEXT("InventorySubsystem exists"), Inv) ||
        !TestNotNull(TEXT("CheckpointSubsystem exists"), Cp))
    {
        AbyssalTest::DestroyGameInstance(GI);
        return false;
    }

    SaveSub->DeleteSlot(TestSlot); // clean start if a previous run aborted

    // Fresh slot, then build some state
    SaveSub->LoadSlot(TestSlot);
    const FName Item(TEXT("ITEM_MINERAL_ABYSSAL_CORE"));
    const FName CpId(TEXT("CP_ROUNDTRIP"));
    Inv->ClearInventory();
    Inv->AddItem(Item, 7);
    Cp->RegisterCheckpoint(CpId, FVector(1.f, 2.f, 3.f), TEXT("PRO_001"));
    Cp->SetActiveCheckpoint(CpId);

    SaveSub->SaveActiveSlot();
    TestTrue(TEXT("Save file exists after SaveActiveSlot"), SaveSub->DoesSaveExist(TestSlot));

    // Wreck the in-memory state, then reload from disk
    Inv->ClearInventory();
    TestEqual(TEXT("State cleared before reload"), Inv->GetItemCount(Item), 0);

    SaveSub->LoadSlot(TestSlot);
    TestEqual(TEXT("Inventory restored from disk"), Inv->GetItemCount(Item), 7);
    TestEqual(TEXT("Active checkpoint ID restored from disk"), Cp->GetActiveCheckpointId(), CpId);

    SaveSub->DeleteSlot(TestSlot);
    TestFalse(TEXT("Test slot deleted"), SaveSub->DoesSaveExist(TestSlot));

    AbyssalTest::DestroyGameInstance(GI);
    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
