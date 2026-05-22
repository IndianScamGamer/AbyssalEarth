#include "ObjectiveTriggerActor.h"
#include "ObjectiveSubsystem.h"
#include "Components/BoxComponent.h"
#include "Engine/GameInstance.h"
#include "GameFramework/Pawn.h"

AObjectiveTriggerActor::AObjectiveTriggerActor()
{
    PrimaryActorTick.bCanEverTick = false;

    TriggerVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerVolume"));
    SetRootComponent(TriggerVolume);
    TriggerVolume->SetBoxExtent(FVector(250.0f, 250.0f, 160.0f));
    TriggerVolume->SetCollisionProfileName(TEXT("Trigger"));
}

void AObjectiveTriggerActor::BeginPlay()
{
    Super::BeginPlay();

    if (TriggerVolume)
    {
        TriggerVolume->OnComponentBeginOverlap.AddDynamic(this, &AObjectiveTriggerActor::HandleTriggerOverlap);
    }
}

void AObjectiveTriggerActor::HandleTriggerOverlap(
    UPrimitiveComponent* OverlappedComponent,
    AActor* OtherActor,
    UPrimitiveComponent* OtherComp,
    int32 OtherBodyIndex,
    bool bFromSweep,
    const FHitResult& SweepResult)
{
    if (ObjectiveIdToComplete.IsNone())
    {
        OnObjectiveTriggerActivated(false);
        return;
    }

    if (bOnlyPlayerControlledPawn)
    {
        const APawn* Pawn = Cast<APawn>(OtherActor);
        if (!Pawn || !Pawn->IsPlayerControlled())
        {
            return;
        }
    }

    UObjectiveSubsystem* ObjectiveSubsystem = nullptr;
    if (UGameInstance* GameInstance = GetGameInstance())
    {
        ObjectiveSubsystem = GameInstance->GetSubsystem<UObjectiveSubsystem>();
    }

    if (!ObjectiveSubsystem)
    {
        OnObjectiveTriggerActivated(false);
        return;
    }

    if (bRequireCurrentObjective && !ObjectiveSubsystem->IsObjectiveActive(ObjectiveIdToComplete))
    {
        OnObjectiveTriggerActivated(false);
        return;
    }

    const bool bAdvanced = ObjectiveSubsystem->CompleteObjective(ObjectiveIdToComplete);
    OnObjectiveTriggerActivated(bAdvanced);

    if (bAdvanced && bTriggerOnce && TriggerVolume)
    {
        TriggerVolume->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    }
}
