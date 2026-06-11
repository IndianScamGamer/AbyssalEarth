#include "NarrativeTriggerComponent.h"
#include "NarrativeSubsystem.h"
#include "Components/PrimitiveComponent.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"

UNarrativeTriggerComponent::UNarrativeTriggerComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UNarrativeTriggerComponent::BeginPlay()
{
    Super::BeginPlay();

    if (bTriggerOnOverlap)
    {
        if (AActor* Owner = GetOwner())
        {
            if (UPrimitiveComponent* Root = Cast<UPrimitiveComponent>(Owner->GetRootComponent()))
            {
                Root->OnComponentBeginOverlap.AddDynamic(this, &UNarrativeTriggerComponent::HandleOwnerOverlap);
            }
        }
    }
}

void UNarrativeTriggerComponent::HandleOwnerOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp,
    int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    if (!OtherActor || OtherActor == GetOwner())
    {
        return;
    }

    if (bPawnOnly && !OtherActor->IsA(APawn::StaticClass()))
    {
        return;
    }

    Trigger();
}

bool UNarrativeTriggerComponent::Trigger()
{
    if (BeatId.IsNone())
    {
        return false;
    }

    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UNarrativeSubsystem* Narrative = GI->GetSubsystem<UNarrativeSubsystem>())
        {
            return Narrative->PlayBeat(BeatId);
        }
    }
    return false;
}
