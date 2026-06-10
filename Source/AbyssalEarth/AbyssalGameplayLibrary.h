#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "AbyssalGameplayLibrary.generated.h"

class UDiscoverySubsystem;
class UObjectiveSubsystem;
class UBeaconSubsystem;
class UAbyssalAudioCueSubsystem;
class UAbyssalSaveSubsystem;
class UWorldFlowSubsystem;

UCLASS()
class ABYSSALEARTH_API UAbyssalGameplayLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Subsystems", meta = (WorldContext = "WorldContextObject"))
    static UDiscoverySubsystem* GetDiscoverySubsystem(const UObject* WorldContextObject);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Subsystems", meta = (WorldContext = "WorldContextObject"))
    static UObjectiveSubsystem* GetObjectiveSubsystem(const UObject* WorldContextObject);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Subsystems", meta = (WorldContext = "WorldContextObject"))
    static UBeaconSubsystem* GetBeaconSubsystem(const UObject* WorldContextObject);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Subsystems", meta = (WorldContext = "WorldContextObject"))
    static UAbyssalAudioCueSubsystem* GetAudioCueSubsystem(const UObject* WorldContextObject);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Subsystems", meta = (WorldContext = "WorldContextObject"))
    static UAbyssalSaveSubsystem* GetSaveSubsystem(const UObject* WorldContextObject);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Subsystems", meta = (WorldContext = "WorldContextObject"))
    static UWorldFlowSubsystem* GetWorldFlowSubsystem(const UObject* WorldContextObject);
};
