#pragma once

#include "CoreMinimal.h"
#include "AbyssalSaveSubsystem.h"
#include "Engine/DataTable.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "ObjectiveSubsystem.generated.h"

USTRUCT(BlueprintType)
struct FAbyssalObjectiveStep
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    FName ObjectiveId;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    FText Title;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives", meta=(MultiLine=true))
    FText Description;
};

/**
 * DataTable row type for the main objective arc.
 * The row name is used as the ObjectiveId. Import from
 * Content/Design/MainObjectiveArc.csv (columns: Title, Description).
 * Rows are loaded in table order to form the route.
 */
USTRUCT(BlueprintType)
struct FAbyssalObjectiveTableRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    FText Title;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Objectives", meta=(MultiLine=true))
    FText Description;
};

USTRUCT(BlueprintType)
struct FAbyssalObjectiveProgress
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    int32 CurrentStepNumber = 0;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    int32 TotalSteps = 0;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    int32 CompletedSteps = 0;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    bool bRouteComplete = false;

    UPROPERTY(BlueprintReadOnly, Category = "Abyssal Earth|Objectives")
    FText ProgressText;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalObjectiveChangedSignature, const FAbyssalObjectiveStep&, Objective);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalObjectiveCompletedSignature, FName, ObjectiveId);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAbyssalRouteCompletedSignature);

UCLASS()
class ABYSSALEARTH_API UObjectiveSubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    /**
     * Replace the route with rows loaded from a DataTable of
     * FAbyssalObjectiveTableRow (row name = ObjectiveId, table order = route order).
     * Resets progress. Returns the number of objectives loaded.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Objectives")
    int32 BuildRouteFromTable(UDataTable* RouteTable);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Objectives")
    void ResetRoute();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Objectives")
    bool CompleteObjective(FName ObjectiveId);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Objectives")
    bool CompleteCurrentObjective();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Objectives")
    bool AdvanceToObjective(FName ObjectiveId);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    bool IsObjectiveActive(FName ObjectiveId) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    bool IsObjectiveComplete(FName ObjectiveId) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    bool IsRouteComplete() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    FAbyssalObjectiveStep GetCurrentObjective() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    TArray<FAbyssalObjectiveStep> GetRouteObjectives() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    int32 GetCurrentObjectiveIndex() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    int32 GetCompletedObjectiveCount() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    int32 GetRouteObjectiveCount() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    FAbyssalObjectiveProgress GetObjectiveProgress() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Objectives")
    FText GetObjectiveHudText() const;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Objectives")
    FAbyssalObjectiveChangedSignature OnObjectiveChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Objectives")
    FAbyssalObjectiveCompletedSignature OnObjectiveCompleted;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Objectives")
    FAbyssalRouteCompletedSignature OnRouteCompleted;

private:
    UPROPERTY()
    TArray<FAbyssalObjectiveStep> RouteObjectives;

    UPROPERTY()
    int32 CurrentObjectiveIndex = 0;

    UPROPERTY()
    TSet<FName> CompletedObjectiveIds;

    void BuildDefaultRoute();
    void BroadcastCurrentObjective();
    int32 FindObjectiveIndex(FName ObjectiveId) const;
};
