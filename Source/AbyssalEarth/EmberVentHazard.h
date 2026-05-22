#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/DamageType.h"
#include "EmberVentHazard.generated.h"

class USceneComponent;
class UStaticMeshComponent;
class UPointLightComponent;

UENUM(BlueprintType)
enum class EEmberVentPhase : uint8
{
    Idle,
    Warning,
    Erupting,
    Cooldown
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FAbyssalVentPhaseChangedSignature, EEmberVentPhase, NewPhase);

UCLASS()
class ABYSSALEARTH_API AEmberVentHazard : public AActor
{
    GENERATED_BODY()

public:
    AEmberVentHazard();

    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Hazard")
    void SetVentActive(bool bNewActive);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    bool IsVentActive() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    EEmberVentPhase GetCurrentPhase() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetTimeInCurrentPhase() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetCurrentPhaseDuration() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Hazard")
    float GetCurrentPhaseProgress() const;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnVentIdle();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnVentWarning();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnVentErupting();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Hazard")
    void OnVentCooldown();

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Hazard")
    FAbyssalVentPhaseChangedSignature OnVentPhaseChanged;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Timing", meta = (ClampMin = "0.0"))
    float IdleDuration = 4.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Timing", meta = (ClampMin = "0.0"))
    float WarningDuration = 1.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Timing", meta = (ClampMin = "0.0"))
    float EruptDuration = 2.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Timing", meta = (ClampMin = "0.0"))
    float CooldownDuration = 2.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage", meta = (ClampMin = "0.0"))
    float DamageRadius = 200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage", meta = (ClampMin = "0.0"))
    float DamagePerSecond = 25.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage", meta = (ClampMin = "0.05", ClampMax = "1.0"))
    float DamageTickInterval = 0.25f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard|Damage")
    TSubclassOf<UDamageType> EruptDamageType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard")
    bool bStartActive = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard")
    bool bRandomizeInitialPhaseOffset = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Hazard", meta = (ClampMin = "0.0", ClampMax = "1.0", EditCondition = "!bRandomizeInitialPhaseOffset"))
    float InitialPhaseOffset = 0.0f;

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Hazard")
    TObjectPtr<USceneComponent> SceneRoot;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Hazard")
    TObjectPtr<UStaticMeshComponent> VentMesh;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Hazard")
    TObjectPtr<UPointLightComponent> VentLight;

private:
    UPROPERTY()
    EEmberVentPhase CurrentPhase = EEmberVentPhase::Idle;

    UPROPERTY()
    bool bVentActive = false;

    float PhaseStartTime = 0.0f;

    FTimerHandle PhaseTimerHandle;
    FTimerHandle DamageTimerHandle;

    void EnterPhase(EEmberVentPhase NewPhase);
    void AdvancePhase();
    void TickDamage();
    void ClearTimers();
    float GetPhaseDuration(EEmberVentPhase Phase) const;
    EEmberVentPhase GetNextPhase(EEmberVentPhase Phase) const;
    void BroadcastPhaseEvent(EEmberVentPhase Phase);
};
