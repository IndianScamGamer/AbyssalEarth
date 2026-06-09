#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "AbyssalPlayerCharacter.generated.h"

/**
 * The player character (roadmap P1). Wires together every gameplay component
 * authored in Phases B/D/F/I/L/N into one pawn:
 *
 *   Vitals:      UAbyssalHealthComponent, UOxygenComponent, UStaminaComponent,
 *                UTemperatureComponent, UPressureComponent
 *   Interaction: UAbyssalInteractionComponent, UAbyssalScanComponent
 *   Traversal:   UAbyssalTraversalComponent
 *   Observation: UObservationModeComponent
 *
 * On BeginPlay it registers itself with UAbyssalHUDSubsystem and
 * UAbyssalUpgradeSubsystem so vital readouts and installed upgrades follow
 * the pawn across respawns. On death (UAbyssalHealthComponent::OnDeath) it
 * notifies the game mode to begin the respawn flow via UCheckpointSubsystem.
 *
 * Depth tracking: each tick the character converts its world Z position to
 * a depth-below-sea-level value and feeds UPressureComponent. SeaLevelZ is
 * configured per map (cm); DepthScale converts cm to metres (default 0.01).
 *
 * Input is bound by the PlayerController / Enhanced Input assets in BP —
 * this class exposes the action entry points only.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AAbyssalPlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AAbyssalPlayerCharacter();

    virtual void Tick(float DeltaTime) override;

    // --- Input action entry points (call from PlayerController / Enhanced Input) ---

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Player")
    void Input_Interact();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Player")
    void Input_ScanPulse();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Player")
    void Input_ToggleObservationMode();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Player")
    void Input_SprintStart();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Player")
    void Input_SprintStop();

    // --- Component accessors ---

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UAbyssalHealthComponent* GetHealthComponent() const { return HealthComponent; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UOxygenComponent* GetOxygenComponent() const { return OxygenComponent; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UStaminaComponent* GetStaminaComponent() const { return StaminaComponent; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UTemperatureComponent* GetTemperatureComponent() const { return TemperatureComponent; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UPressureComponent* GetPressureComponent() const { return PressureComponent; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UAbyssalInteractionComponent* GetInteractionComponent() const { return InteractionComponent; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UAbyssalScanComponent* GetScanComponent() const { return ScanComponent; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UAbyssalTraversalComponent* GetTraversalComponent() const { return TraversalComponent; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Player")
    class UObservationModeComponent* GetObservationComponent() const { return ObservationComponent; }

    // --- Configuration ---

    /** World Z (cm) corresponding to sea level for this map. Used for depth/pressure. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Player")
    float SeaLevelZ = 0.0f;

    /** Conversion from world cm to depth metres (default: 1 cm = 0.01 m). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Player", meta=(ClampMin="0.0001"))
    float DepthScale = 0.01f;

    /** Walk speed multiplier while sprinting (gated by stamina). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Player", meta=(ClampMin="1.0"))
    float SprintSpeedMultiplier = 1.6f;

protected:
    virtual void BeginPlay() override;
    virtual void EndPlay(EEndPlayReason::Type EndPlayReason) override;

    UFUNCTION()
    void HandleDeath(class UAbyssalHealthComponent* HealthComp);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Player")
    void BP_OnDeath();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Player")
    void BP_OnRespawned();

public:
    /** Teleport to the active checkpoint and restore vitals. Called by game mode on respawn. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Player")
    void RespawnAtCheckpoint();

private:
    void UpdateDepth();
    void ApplySprintState(bool bSprinting);

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UAbyssalHealthComponent> HealthComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UOxygenComponent> OxygenComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UStaminaComponent> StaminaComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UTemperatureComponent> TemperatureComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UPressureComponent> PressureComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UAbyssalInteractionComponent> InteractionComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UAbyssalScanComponent> ScanComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UAbyssalTraversalComponent> TraversalComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta=(AllowPrivateAccess="true"))
    TObjectPtr<class UObservationModeComponent> ObservationComponent;

    float BaseWalkSpeed = 0.0f;
    bool bWantsSprint = false;
};
