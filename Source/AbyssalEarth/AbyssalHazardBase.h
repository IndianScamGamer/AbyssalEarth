#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/DamageType.h"
#include "AbyssalHazardBase.generated.h"

UENUM(BlueprintType)
enum class EHazardDamageMode : uint8
{
    Radial,
    Overlap,
    None
};

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
 * Implements the Idle -> Warning -> Active -> Cooldown phase loop and optionally
 * deals damage (radial or overlap-based) during the Active phase.  Derived
 * actors supply visual components and override the BlueprintImplementableEvent
 * hooks for VFX / SFX.
 *
 * AEmberVentHazard predates this class and implements its own loop directly.
 * New hazards derive from AAbyssalHazardBase instead.
 */
UCLASS(Abstract, Blueprintable)
class ABYSSALEARTH_API AAbyssalHazardBase : public AActor
{
    GENERATED_BODY()

public:
    AAbyssalHazardBase();

    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Hazard")
    void SetHazardActive(bool bNewActive);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    bool IsHazardActive() const { return bHazardActive; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    EHazardPhase GetCurrentPhase() const { return CurrentPhase; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetPhaseProgress() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetTimeInCurrentPhase() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetCurrentPhaseDuration() const { return GetPhaseDuration(CurrentPhase); }

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Hazard")
    void RegisterDamagePrimitive(UPrimitiveComponent* Primitive);

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Hazard")
    void UnregisterDamagePrimitive(UPrimitiveComponent* Primitive);

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Hazard")
    FHazardPhaseChangedSignature OnHazardPhaseChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Hazard")
    FHazardActivationChangedSignature OnHazardActivated;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Hazard")
    FHazardActivationChangedSignature OnHazardDeactivated;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnHazardIdle();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnHazardWarning();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnHazardActive();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnHazardCooldown();

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

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage",
        meta = (ClampMin = "0.0", EditCondition = "DamageMode == EHazardDamageMode::Radial"))
    float DamageRadius = 200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage", meta = (ClampMin = "0.0"))
    float DamagePerSecond = 25.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage",
        meta = (ClampMin = "0.05", ClampMax = "1.0"))
    float DamageTickInterval = 0.25f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage")
    TSubclassOf<UDamageType> HazardDamageType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard")
    bool bStartActive = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard")
    bool bRandomizeInitialPhaseOffset = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard",
        meta = (ClampMin = "0.0", ClampMax = "1.0", EditCondition = "!bRandomizeInitialPhaseOffset"))
    float InitialPhaseOffset = 0.0f;

protected:
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
