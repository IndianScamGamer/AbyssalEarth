#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "AbyssalSaveProvider.h"
#include "CheckpointSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalCheckpointActivatedSignature, FName, CheckpointId);

USTRUCT(BlueprintType)
struct FAbyssalCheckpointRecord
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    FName CheckpointId;

    UPROPERTY(BlueprintReadOnly)
    FVector RespawnLocation = FVector::ZeroVector;

    /** Slot index identifying the target map for respawn (matches UWorldFlowSubsystem map IDs). */
    UPROPERTY(BlueprintReadOnly)
    FName MapId;
};

/**
 * Checkpoint / mid-level save trigger subsystem (roadmap A3). Actors in the
 * world (e.g. beacon pillars, HELIOS docks) call RegisterCheckpoint to
 * publish themselves; the player interaction or proximity triggers
 * SetActiveCheckpoint. On respawn UWorldFlowSubsystem uses GetRespawnMapId
 * to load the correct level and the player character uses GetRespawnLocation
 * to place the pawn. Integrates with IAbyssalSaveProvider — the active
 * checkpoint ID is written into UAbyssalProfileSaveGame::WorldFlow.
 */
UCLASS()
class ABYSSALEARTH_API UCheckpointSubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    /**
     * Register a checkpoint. Safe to call multiple times for the same ID
     * (updates location/mapId). Typically called from BeginPlay of a
     * checkpoint actor.
     */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Checkpoint")
    void RegisterCheckpoint(FName CheckpointId, FVector RespawnLocation, FName MapId);

    /** Activate a checkpoint as the current respawn point. Broadcasts OnCheckpointActivated. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Checkpoint")
    bool SetActiveCheckpoint(FName CheckpointId);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Checkpoint")
    FName GetActiveCheckpointId() const { return ActiveCheckpointId; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Checkpoint")
    FVector GetRespawnLocation() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Checkpoint")
    FName GetRespawnMapId() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Checkpoint")
    bool HasActiveCheckpoint() const { return !ActiveCheckpointId.IsNone(); }

    /** Returns all registered checkpoints in registration order. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Checkpoint")
    TArray<FAbyssalCheckpointRecord> GetAllCheckpoints() const { return Checkpoints; }

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Checkpoint")
    FAbyssalCheckpointActivatedSignature OnCheckpointActivated;

private:
    int32 FindCheckpointIndex(FName CheckpointId) const;

    UPROPERTY()
    TArray<FAbyssalCheckpointRecord> Checkpoints;

    UPROPERTY()
    FName ActiveCheckpointId;
};
