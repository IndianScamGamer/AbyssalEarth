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
    TObjectPtr<UInputAction> ScanAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Input")
    TObjectPtr<UInputAction> PlaceBeaconAction;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Beacon")
    TSubclassOf<ABeaconActor> BeaconClass;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Beacon")
    float MaxBeaconPlacementDistance = 900.0f;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Movement")
    float WalkSpeed = 420.0f;

    UPROPERTY(EditDefaultsOnly, Category = "Abyssal Earth|Movement")
    float SprintSpeed = 680.0f;

    void Move(const FInputActionValue& Value);
    void Look(const FInputActionValue& Value);
    void StartSprint();
    void StopSprint();
    void TriggerScan();
    void PlaceBeacon();
};
