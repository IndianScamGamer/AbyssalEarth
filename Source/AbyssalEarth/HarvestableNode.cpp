#include "HarvestableNode.h"
#include "AbyssalItemDefinition.h"
#include "InventorySubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Kismet/GameplayStatics.h"

AHarvestableNode::AHarvestableNode()
{
    PrimaryActorTick.bCanEverTick = false;

    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    RootComponent = MeshComponent;
}

void AHarvestableNode::BeginPlay()
{
    Super::BeginPlay();
}

bool AHarvestableNode::CanInteract_Implementation(AActor* Interactor)
{
    return !bHarvested && ItemDefinition != nullptr;
}

FText AHarvestableNode::GetInteractionPrompt_Implementation()
{
    if (ItemDefinition)
    {
        return FText::Format(
            NSLOCTEXT("HarvestableNode", "HarvestPrompt", "Harvest {0}"),
            ItemDefinition->DisplayName);
    }
    return NSLOCTEXT("HarvestableNode", "HarvestFallback", "Harvest");
}

void AHarvestableNode::OnInteract_Implementation(AActor* Interactor)
{
    if (!CanInteract_Implementation(Interactor))
    {
        return;
    }

    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UInventorySubsystem* Inventory = GI->GetSubsystem<UInventorySubsystem>())
        {
            Inventory->AddItem(ItemDefinition->ItemId, HarvestCount);
        }
    }

    bHarvested = true;
    BP_OnHarvestBegin();

    if (RespawnTime > 0.0f)
    {
        GetWorldTimerManager().SetTimer(
            RespawnTimerHandle, this, &AHarvestableNode::Respawn, RespawnTime, false);
    }
}

void AHarvestableNode::OnBeginFocus_Implementation(AActor* Interactor)
{
    BP_OnFocusBegin();
}

void AHarvestableNode::OnEndFocus_Implementation(AActor* Interactor)
{
    BP_OnFocusEnd();
}

void AHarvestableNode::Respawn()
{
    bHarvested = false;
    BP_OnHarvestRespawn();
}
