#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "DiscoverySubsystem.generated.h"

UCLASS()
class ABYSSALEARTH_API UDiscoverySubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    bool RegisterDiscovery(FName DiscoveryId);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    bool IsDiscovered(FName DiscoveryId) const;

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Discovery")
    TArray<FName> GetDiscoveredIds() const;

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    void SaveDiscoveries();

    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Discovery")
    void LoadDiscoveries();

private:
    UPROPERTY()
    TSet<FName> DiscoveredIds;

    UPROPERTY()
    FString SaveSlotName = TEXT("AbyssalEarth_Discoveries");

    UPROPERTY()
    int32 SaveUserIndex = 0;
};
