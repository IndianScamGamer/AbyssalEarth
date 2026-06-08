#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/DamageType.h"
#include "AbyssalHazardBase.generated.h"

/**
 * How the hazard delivers damage during its active phase.
 */
UENUM(BlueprintType)
enum class EHazardDamageMode : uint8
{
    /** ApplyRadialDamage centred on the hazard actor origin. */
    Radial,
    /** Damage every actor that overlaps a registered primitive component. */
    Overlap,
    /** No automatic damage — derived class or Blueprint handles it entirely. */
    None
};

/**
 * Lifecycle phase shared by all Abyssal Earth environmental hazards.
 * Idle → Warning → Active → Cooldown → (loop)
 */
UENUM(BlueprintType)
enum class EHazardPhase : uint8
{
    Idle,
    Warning,
    Active,
    Cooldown
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FHazardPhaseChangedSignature, EHazardPhase, NewPhase);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FHazardActivationChangedSignature);

/**
 * Abstract base for every environmental hazard in Abyssal Earth.
 *
 * Implements the Idle → Warning → Active → Cooldown phase loop and optionally
 * deals damage (radial or overlap-based) during the Active phase.  Derived
 * actors supply visual components and override the BlueprintImplementableEvent
 * hooks for VFX / SFX.
 *
 * AEmberVentHazard predates this class and implements its own loop directly.
 * New hazards (acid seeps, cryo jets, pressure vents, gravity shears, etc.)
 * should derive from AAbyssalHazardBase instead.
 *
 * Activation:  SetHazardActive(true/false) enables/disables the phase loop.
 * Serialisation: bStartActive + bRandomizeInitialPhaseOffset are the level-
 *   design knobs; place multiple hazards with different offsets for staggered
 *   rhythms without additional Blueprint logic.
 */
UCLASS(Abstract, Blueprintable)
class ABYSSALEARTH_API AAbyssalHazardBase : public AActor
{
    GENERATED_BODY()

public:
    AAbyssalHazardBase();

    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    // -------------------------------------------------------------------------
    // Runtime control
    // -------------------------------------------------------------------------

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Hazard")
    void SetHazardActive(bool bNewActive);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    bool IsHazardActive() const { return bHazardActive; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    EHazardPhase GetCurrentPhase() const { return CurrentPhase; }

    /** 0-1 progress through the current phase. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetPhaseProgress() const;

    /** Seconds elapsed since the current phase began. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetTimeInCurrentPhase() const;

    /** Total duration of the current phase (0 = instantaneous). */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetCurrentPhaseDuration() const { return GetPhaseDuration(CurrentPhase); }

    // -------------------------------------------------------------------------
    // Overlap-mode helpers (only meaningful when DamageMode == Overlap)
    // -------------------------------------------------------------------------

    /** Register a primitive so its overlap events drive damage during Active. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Hazard")
    void RegisterDamagePrimitive(UPrimitiveComponent* Primitive);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Hazard")
    void UnregisterDamagePrimitive(UPrimitiveComponent* Primitive);

    // -------------------------------------------------------------------------
    // Delegates
    // -------------------------------------------------------------------------

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Hazard")
    FHazardPhaseChangedSignature OnHazardPhaseChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Hazard")
    FHazardActivationChangedSignature OnHazardActivated;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Hazard")
    FHazardActivationChangedSignature OnHazardDeactivated;

    // -------------------------------------------------------------------------
    // Blueprint phase hooks (override in derived BP/C++ classes for VFX/SFX)
    // -------------------------------------------------------------------------

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnHazardIdle();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnHazardWarning();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnHazardActive();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnHazardCooldown();

    // -------------------------------------------------------------------------
    // Designer tunables
    // -------------------------------------------------------------------------

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Timing", meta = (ClampMin = "0.0"))
    float IdleDuration = 4.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Timing", meta = (ClampMin = "0.0"))
    float WarningDuration = 1.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Timing", meta = (ClampMin = "0.0"))
    float ActiveDuration = 2.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Timing", meta = (ClampMin = "0.0"))
    float CooldownDuration = 2.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage")
    EHazardDamageMode DamageMode = EHazardDamageMode::Radial;

    /** Radial-mode: world-unit radius centred on actor origin. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage",
        meta = (ClampMin = "0.0", EditCondition = "DamageMode == EHazardDamageMode::Radial"))
    float DamageRadius = 200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage", meta = (ClampMin = "0.0"))
    float DamagePerSecond = 25.0f;

    /** How often the damage tick fires while Active (seconds). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage",
        meta = (ClampMin = "0.05", ClampMax = "1.0"))
    float DamageTickInterval = 0.25f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage")
    TSubclassOf<UDamageType> HazardDamageType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard")
    bool bStartActive = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard")
    bool bRandomizeInitialPhaseOffset = true;

    /** Fraction [0,1] into the Idle phase to start when not randomising. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard",
        meta = (ClampMin = "0.0", ClampMax = "1.0", EditCondition = "!bRandomizeInitialPhaseOffset"))
    float InitialPhaseOffset = 0.0f;

protected:
    /** Override to add extra per-tick damage logic (called while Active, before standard damage). */
    virtual void OnActiveDamageTick(float DeltaDamage) {}

private:
    EHazardPhase CurrentPhase = EHazardPhase::Idle;
    bool bHazardActive = false;
    float PhaseStartTime = 0.0f;

    FTimerHandle PhaseTimerHandle;
    FTimerHandle DamageTimerHandle;

    TArray<TWeakObjectPtr<UPrimitiveComponent>> DamagePrimitives;
    TSet<TObjectPtr<AActor>> OverlappingActors;

    void EnterPhase(EHazardPhase NewPhase);
    void AdvancePhase();
    void StartDamageTick();
    void StopDamageTick();
    void TickDamage();
    void ClearTimers();

    float GetPhaseDuration(EHazardPhase Phase) const;
    EHazardPhase GetNextPhase(EHazardPhase Phase) const;
    void BroadcastPhaseEvent(EHazardPhase Phase);

    UFUNCTION()
    void HandleOverlapBegin(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

    UFUNCTION()
    void HandleOverlapEnd(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);
};
