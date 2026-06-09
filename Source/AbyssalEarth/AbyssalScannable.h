#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "AbyssalScannable.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UAbyssalScannable : public UInterface
{
    GENERATED_BODY()
};

/**
 * Interface for actors that can be discovered by UAbyssalScanComponent.
 * Implement on creatures, structures, and collectibles that should register
 * with UDiscoverySubsystem when the player scans them.
 */
class ABYSSALEARTH_API IAbyssalScannable
{
    GENERATED_BODY()

public:
    /** Unique discovery ID to register. Must match a row in the discovery dataset. */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Scan")
    FName GetScanId() const;

    /** Display name shown in the scan-hit UI flash. */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Scan")
    FText GetScanDisplayName() const;

    /** Called when the player successfully scans this actor. */
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Abyssal Earth|Scan")
    void OnScanned(AActor* Scanner);
};
