#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "AbyssalGameMode.generated.h"

/**
 * Game mode for all AbyssalEarth levels.
 *
 * Wires DefaultPawnClass → AAbyssalPlayerCharacter and
 * PlayerControllerClass → AAbyssalPlayerController so the new player
 * pawn is instantiated on PIE/launch rather than the legacy explorer.
 *
 * RespawnPlayer() is the single entry point for the death→respawn flow:
 * AAbyssalPlayerCharacter::HandleDeath fires it after RespawnDelay seconds,
 * and it delegates the actual teleport + vitals restore to the pawn's
 * RespawnAtCheckpoint().
 *
 * NarrativeBeatTable: assign DT_PrologueNarrativeBeats (and the appropriate
 * act table) in each level's GameMode override to feed UNarrativeSubsystem.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AAbyssalGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    AAbyssalGameMode();

    virtual void BeginPlay() override;

    /** Called by AAbyssalPlayerCharacter after the death timer expires. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|GameMode")
    void RespawnPlayer();

    /** DataTable of FAbyssalNarrativeBeat rows for the current level.
     *  Set this to the matching DT_*NarrativeBeats asset in the BP subclass. */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Abyssal Earth|Narrative")
    TObjectPtr<class UDataTable> NarrativeBeatTable;
};
