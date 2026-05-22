#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "AbyssalExplorerCharacter.generated.h"

class UCameraComponent;
class UInputAction;
class UInputMappingContext;
class UScannerComponent;
class ABeaconActor;
struct FInputActionValue;

UCLASS()
class ABYSSALEARTH_API AAbyssalExplorerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AAbyssalExplorerCharacter();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Scanner")
    UScannerComponent* GetScannerComponent() const;

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Journal", meta = (DisplayName = "Toggle Journal"))
    void BP_ToggleJournal();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Damage", meta = (DisplayName = "Took Damage"))
    void BP_OnTookDamage(float DamageAmount, AActor* DamageCauser);

#if !UE_BUILD_SHIPPING
    UFUNCTION(Exec)
    void AbyssalDebugDiscoverAll();

    UFUNCTION(Exec)
    void AbyssalDebugResetDiscoveries();

    UFUNCTION(Exec)
    void AbyssalDebugAdvanceObjective();
#endif

protected:
    virtual void BeginPlay() override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

private:
    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Camera")
    TObjectPtr<UCameraComponent> FirstPersonCamera;

    UPROPERTY(VisibleAnywhere, Category = "Abyssal Earth|Scanner")
    TObjectPtr<UScannerComponent> ScannerComponent;

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
    TObjectPtr<UInputAction> ScanAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> PlaceBeaconAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> JournalAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Beacon")
    TSubclassOf<ABeaconActor> BeaconClass;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Beacon")
    float MaxBeaconPlacementDistance = 900.0f;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Movement")
    float WalkSpeed = 420.0f;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Movement")
    float SprintSpeed = 680.0f;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Movement", meta=(ClampMin="0.0"))
    float CrouchedHalfHeight = 52.0f;

    void Move(const FInputActionValue& Value);
    void Look(const FInputActionValue& Value);
    void StartSprint();
    void StopSprint();
    void StartCrouch();
    void StopCrouch();
    void TriggerScan();
    void PlaceBeacon();
    void ToggleJournal();

    UFUNCTION()
    void HandleTakeAnyDamage(AActor* DamagedActor, float Damage, const class UDamageType* DamageType, class AController* InstigatedBy, AActor* DamageCauser);
};
