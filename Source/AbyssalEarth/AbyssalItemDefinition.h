#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "AbyssalItemDefinition.generated.h"

UENUM(BlueprintType)
enum class EAbyssalItemCategory : uint8
{
    Resource   UMETA(DisplayName = "Resource"),
    Crafting   UMETA(DisplayName = "Crafting"),
    Equipment  UMETA(DisplayName = "Equipment"),
    Consumable UMETA(DisplayName = "Consumable"),
};

/**
 * DataAsset defining a single item type.
 * Create instances in the Content Browser and set ItemId to a unique FName.
 * Reference via UAssetManager using primary asset type "AbyssalItem".
 */
UCLASS(BlueprintType)
class ABYSSALEARTH_API UAbyssalItemDefinition : public UPrimaryDataAsset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item")
    FName ItemId;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item")
    FText DisplayName;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item", meta = (MultiLine = true))
    FText Description;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item")
    EAbyssalItemCategory Category = EAbyssalItemCategory::Resource;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item", meta = (ClampMin = 1))
    int32 MaxStackSize = 99;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item")
    TSoftObjectPtr<UTexture2D> Icon;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item")
    bool bIsConsumable = false;

    virtual FPrimaryAssetId GetPrimaryAssetId() const override
    {
        return FPrimaryAssetId(TEXT("AbyssalItem"), ItemId);
    }
};
