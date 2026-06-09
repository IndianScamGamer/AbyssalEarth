#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Perception/AIPerceptionComponent.h"
#include "AbyssalCreature.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalCreatureStateChangedSignature, class AAbyssalCreature*, Creature, EAbyssalCreatureState, NewState);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalCreaturePerceivedSignature, class AAbyssalCreature*, Creature, AActor*, PerceivedActor);

UENUM(BlueprintType)
enum class EAbyssalCreatureState : uint8
{
    Passive     UMETA(DisplayName = "Passive"),
    Curious     UMETA(DisplayName = "Curious"),
    Fleeing     UMETA(DisplayName = "Fleeing"),
    Aggressive  UMETA(DisplayName = "Aggressive"),
    Dead        UMETA(DisplayName = "Dead"),
};

/**
 * Base creature actor for AbyssalEarth fauna (roadmap D3).
 * Drives a five-state machine (Passive/Curious/Fleeing/Aggressive/Dead) via
 * UAIPerceptionComponent sight stimuli. Uses UCharacterMovementComponent
 * with per-state walk speeds and RVO avoidance for crowd navigation.
 * Subclass in Blueprint to add mesh, animations, and attack logic.
 */
UCLASS(Abstract, Blueprintable)
class ABYSSALEARTH_API AAbyssalCreature : public ACharacter
{
    GENERATED_BODY()

public:
    AAbyssalCreature();

    virtual void BeginPlay() override;
    virtual float TakeDamage(float DamageAmount, const FDamageEvent& DamageEvent,
        AController* EventInstigator, AActor* DamageCauser) override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Creature")
    void SetCreatureState(EAbyssalCreatureState NewState);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Creature")
    EAbyssalCreatureState GetCreatureState() const { return CurrentState; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Creature")
    bool IsDead() const { return CurrentState == EAbyssalCreatureState::Dead; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Creature")
    AActor* GetThreatTarget() const { return ThreatTarget.Get(); }

    // Delegates
    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Creature")
    FAbyssalCreatureStateChangedSignature OnCreatureStateChanged;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Creature")
    FAbyssalCreaturePerceivedSignature OnThreatPerceived;

    // Stats
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Creature", meta=(ClampMin="0.0"))
    float MaxHealth = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Creature", meta=(ClampMin="0.0"))
    float PassiveSpeed = 150.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Creature", meta=(ClampMin="0.0"))
    float CuriousSpeed = 200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Creature", meta=(ClampMin="0.0"))
    float FleeSpeed = 450.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Creature", meta=(ClampMin="0.0"))
    float AggressiveSpeed = 380.0f;

    /** Fraction of MaxHealth below which a passive creature flees rather than ignoring threats. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Creature", meta=(ClampMin="0.0", ClampMax="1.0"))
    float FleeHealthThreshold = 0.3f;

    /** If true, seeing a player makes the creature aggressive; if false, it flees. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Creature")
    bool bIsAggressive = false;

protected:
    UFUNCTION()
    void OnPerceptionUpdated(const TArray<AActor*>& UpdatedActors);

    void ApplySpeedForState(EAbyssalCreatureState State);

    // Blueprint hooks
    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Creature")
    void BP_OnStateChanged(EAbyssalCreatureState NewState);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Creature")
    void BP_OnDeath();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Creature")
    void BP_OnThreatPerceived(AActor* PerceivedActor);

private:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Creature", meta=(AllowPrivateAccess="true"))
    TObjectPtr<UAIPerceptionComponent> PerceptionComponent;

    UPROPERTY()
    EAbyssalCreatureState CurrentState = EAbyssalCreatureState::Passive;

    UPROPERTY()
    float CurrentHealth = 0.0f;

    UPROPERTY()
    TWeakObjectPtr<AActor> ThreatTarget;
};
