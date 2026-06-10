#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "AbyssalPlayerController.generated.h"

class UInputAction;
class UInputMappingContext;

/**
 * Player controller for AbyssalEarth (roadmap P1-controller).
 *
 * Owns Enhanced Input setup: adds IMC_AbyssalDefault in BeginPlay and
 * binds the four gameplay actions (Interact, ScanPulse, ObservationMode,
 * Sprint) to forward calls to the possessed AAbyssalPlayerCharacter.
 *
 * All Input Action assets are EditDefaultsOnly — set them in the
 * BP_AbyssalPlayerController Blueprint subclass.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AAbyssalPlayerController : public APlayerController
{
    GENERATED_BODY()

public:
    AAbyssalPlayerController();

protected:
    virtual void BeginPlay() override;
    virtual void SetupInputComponent() override;

    // --- Input Action assets (assign in BP subclass) ---

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputMappingContext> DefaultMappingContext;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> MoveAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> LookAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> SprintAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> CrouchAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> InteractAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> ScanPulseAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> ObservationModeAction;

public:
    // --- Debug console commands (PIE / development builds) ---
    // Type into the ~ console. Exec routing reaches the PlayerController
    // automatically; no CheatManager needed.

    /** Complete the currently active objective. */
    UFUNCTION(Exec)
    void AbyssalCompleteObjective();

    /** Add Count of ItemId to the inventory (default 1). */
    UFUNCTION(Exec)
    void AbyssalGiveItem(FName ItemId, int32 Count = 1);

    /** Kill the player pawn to exercise the death → respawn flow. */
    UFUNCTION(Exec)
    void AbyssalKill();

    /** Flush the active profile slot to disk. */
    UFUNCTION(Exec)
    void AbyssalSave();

    /** Reload the active profile slot from disk. */
    UFUNCTION(Exec)
    void AbyssalLoad();

private:
    // --- Input handlers (forward to current pawn) ---

    void HandleMove(const struct FInputActionValue& Value);
    void HandleLook(const struct FInputActionValue& Value);
    void HandleSprintStart();
    void HandleSprintStop();
    void HandleCrouchStart();
    void HandleCrouchStop();
    void HandleInteract();
    void HandleScanPulse();
    void HandleObservationMode();

    class AAbyssalPlayerCharacter* GetAbyssalCharacter() const;
};
