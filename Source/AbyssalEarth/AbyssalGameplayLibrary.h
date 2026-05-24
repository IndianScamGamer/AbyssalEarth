#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "AbyssalGameplayLibrary.generated.h"

class UDiscoverySubsystem;
class UObjectiveSubsystem;
class UBeaconSubsystem;
class UAbyssalAudioCueSubsystem;

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
};
