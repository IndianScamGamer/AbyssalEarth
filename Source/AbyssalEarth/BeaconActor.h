#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "BeaconActor.generated.h"

class UPointLightComponent;
class UStaticMeshComponent;

UCLASS()
class ABYSSALEARTH_API ABeaconActor : public AActor
{
    GENERATED_BODY()

public:
    ABeaconActor();

    virtual void BeginPlay() override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    void InitializeBeacon(FGuid InBeaconId, FLinearColor InLightColor);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Beacon")
    FGuid GetBeaconId() const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Beacon")
    FLinearColor GetBeaconLightColor() const;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Beacon")
    void SetBeaconLightColor(FLinearColor NewLightColor);

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Beacon")
    TObjectPtr<UStaticMeshComponent> Mesh;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Beacon")
    TObjectPtr<UPointLightComponent> Light;

    UPROPERTY(VisibleInstanceOnly, BlueprintReadOnly, Category = "Abyssal Earth|Beacon")
    FGuid BeaconId;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Abyssal Earth|Beacon")
    FLinearColor BeaconLightColor = FLinearColor(0.2f, 0.85f, 1.0f);

    void ApplyBeaconVisuals();
};
