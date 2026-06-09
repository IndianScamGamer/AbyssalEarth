#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "AbyssalItemDefinition.h"
#include "AbyssalItemTableRow.generated.h"

/**
 * DataTable row for designer-friendly item definitions (roadmap H4).
 * Row name = ItemId (FName). Parallel to UAbyssalItemDefinition PrimaryDataAsset;
 * use whichever pipeline suits the content: DataTable for spreadsheet-authored
 * bulk items, DataAsset for rich items that need an icon texture reference.
 *
 * UInventorySubsystem and UFabricationSubsystem accept both — they look up
 * UAbyssalItemDefinition via AssetManager first; if not found they fall back
 * to a UAbyssalItemDatabase lookup (see UAbyssalItemDatabase).
 */
USTRUCT(BlueprintType)
struct ABYSSALEARTH_API FAbyssalItemTableRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FText Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EAbyssalItemCategory Category = EAbyssalItemCategory::Material;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="1"))
    int32 MaxStackSize = 99;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsConsumable = false;

    /** Fabrication station tier required to craft items of this type. 0 = no station. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, meta=(ClampMin="0"))
    int32 RequiredStationTier = 0;

    /** Optional: icon texture path (soft ref, resolved at runtime). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TSoftObjectPtr<class UTexture2D> Icon;
};
