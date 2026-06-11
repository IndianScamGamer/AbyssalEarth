#pragma once

#include "CoreMinimal.h"
#include "AbyssalSaveSubsystem.h"
#include "Engine/DataTable.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "TimerManager.h"
#include "NarrativeSubsystem.generated.h"

/**
 * One narrative caption / VO line. DataTable row name = BeatId.
 * Import from Content/Design/PrologueNarrativeBeats.csv.
 */
USTRUCT(BlueprintType)
struct FAbyssalNarrativeBeat : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Narrative")
    FText Speaker;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Narrative", meta=(MultiLine=true))
    FText Caption;

    /** On-screen seconds. If <= 0 the caption stays until the next beat / manual clear. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Narrative", meta=(ClampMin="0.0"))
    float Duration = 4.0f;

    /** Optional voice-over line played with the caption. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Narrative")
    TSoftObjectPtr<USoundBase> VoiceOver;

    /** If true, the beat plays at most once per save (tracked + persisted). */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Narrative")
    bool bPlayOnce = true;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalBeatStartedSignature, const FAbyssalNarrativeBeat&, Beat);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalBeatFinishedSignature, FName, BeatId);

/**
 * Narrative playback authority (roadmap D1). Plays caption/VO beats sourced from a
 * DataTable, one at a time, with simple queueing. One-shot beats are tracked and
 * persisted through UAbyssalProfileSaveGame::Narrative so prologue lines never repeat.
 * UAbyssalCaptionWidget binds to OnBeatStarted/OnBeatFinished to render text.
 */
UCLASS()
class ABYSSALEARTH_API UNarrativeSubsystem : public UGameInstanceSubsystem, public IAbyssalSaveProvider
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // IAbyssalSaveProvider
    virtual void OnSaveRequested(UAbyssalProfileSaveGame* SaveGame) override;
    virtual void OnLoadCompleted(UAbyssalProfileSaveGame* SaveGame) override;

    /** Source table of FAbyssalNarrativeBeat rows. Set once (e.g. GameMode BeginPlay). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Narrative")
    void SetBeatTable(UDataTable* InBeatTable);

    /** Queue a beat by id. Plays immediately if nothing is active. Skips one-shots already played. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Narrative")
    bool PlayBeat(FName BeatId);

    /** Stop the active beat and clear the queue. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Narrative")
    void StopAll();

    /** Fire the post-credits double-pulse sensor beat (called by AAbyssalRiftActor after rift opens). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Narrative")
    void TriggerPostCreditsHook();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Narrative")
    bool HasPlayed(FName BeatId) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Narrative")
    bool IsPlaying() const { return !ActiveBeatId.IsNone(); }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Narrative")
    FName GetActiveBeatId() const { return ActiveBeatId; }

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Narrative")
    FAbyssalBeatStartedSignature OnBeatStarted;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Narrative")
    FAbyssalBeatFinishedSignature OnBeatFinished;

private:
    void StartBeat(FName BeatId, const FAbyssalNarrativeBeat& Beat);
    void FinishActiveBeat();
    void AdvanceQueue();

    UPROPERTY()
    TObjectPtr<UDataTable> BeatTable;

    UPROPERTY()
    TSet<FName> PlayedBeatIds;

    UPROPERTY()
    TArray<FName> Queue;

    UPROPERTY()
    FName ActiveBeatId;

    FTimerHandle BeatTimerHandle;
};
