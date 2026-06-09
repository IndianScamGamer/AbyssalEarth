#include "AbyssalCreature.h"
#include "Perception/AIPerceptionComponent.h"
#include "Perception/AISenseConfig_Sight.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "AIController.h"

AAbyssalCreature::AAbyssalCreature()
{
    PrimaryActorTick.bCanEverTick = false;

    PerceptionComponent = CreateDefaultSubobject<UAIPerceptionComponent>(TEXT("PerceptionComponent"));

    UAISenseConfig_Sight* SightConfig = CreateDefaultSubobject<UAISenseConfig_Sight>(TEXT("SightConfig"));
    SightConfig->SightRadius = 1200.0f;
    SightConfig->LoseSightRadius = 1600.0f;
    SightConfig->PeripheralVisionAngleDegrees = 75.0f;
    SightConfig->SetMaxAge(5.0f);
    SightConfig->DetectionByAffiliation.bDetectEnemies = true;
    SightConfig->DetectionByAffiliation.bDetectNeutrals = true;
    SightConfig->DetectionByAffiliation.bDetectFriendlies = false;
    PerceptionComponent->ConfigureSense(*SightConfig);
    PerceptionComponent->SetDominantSense(SightConfig->GetSenseImplementation());

    UCharacterMovementComponent* MoveComp = GetCharacterMovement();
    MoveComp->bUseRVOAvoidance = true;
    MoveComp->AvoidanceConsiderationRadius = 200.0f;
    MoveComp->MaxWalkSpeed = PassiveSpeed;
    MoveComp->bOrientRotationToMovement = true;
    bUseControllerRotationYaw = false;
}

void AAbyssalCreature::BeginPlay()
{
    Super::BeginPlay();
    CurrentHealth = MaxHealth;
    PerceptionComponent->OnPerceptionUpdated.AddDynamic(this, &AAbyssalCreature::OnPerceptionUpdated);
    ApplySpeedForState(CurrentState);
}

float AAbyssalCreature::TakeDamage(float DamageAmount, const FDamageEvent& DamageEvent,
    AController* EventInstigator, AActor* DamageCauser)
{
    if (IsDead() || DamageAmount <= 0.0f)
    {
        return 0.0f;
    }

    const float Applied = Super::TakeDamage(DamageAmount, DamageEvent, EventInstigator, DamageCauser);
    CurrentHealth = FMath::Max(0.0f, CurrentHealth - Applied);

    if (CurrentHealth <= 0.0f)
    {
        SetCreatureState(EAbyssalCreatureState::Dead);
        return Applied;
    }

    // Being hit always triggers flight-or-fight if not already reactive
    if (CurrentState == EAbyssalCreatureState::Passive || CurrentState == EAbyssalCreatureState::Curious)
    {
        if (DamageCauser)
        {
            ThreatTarget = DamageCauser;
        }
        const bool bLowHealth = (CurrentHealth / MaxHealth) <= FleeHealthThreshold;
        SetCreatureState(bIsAggressive && !bLowHealth ? EAbyssalCreatureState::Aggressive : EAbyssalCreatureState::Fleeing);
    }

    return Applied;
}

void AAbyssalCreature::SetCreatureState(EAbyssalCreatureState NewState)
{
    if (CurrentState == NewState)
    {
        return;
    }
    if (CurrentState == EAbyssalCreatureState::Dead)
    {
        return;
    }

    CurrentState = NewState;
    ApplySpeedForState(NewState);

    if (NewState == EAbyssalCreatureState::Dead)
    {
        // Disable collision and movement so the corpse settles
        if (UCharacterMovementComponent* MoveComp = GetCharacterMovement())
        {
            MoveComp->StopMovementImmediately();
            MoveComp->DisableMovement();
        }
        SetActorEnableCollision(false);
        BP_OnDeath();
    }

    OnCreatureStateChanged.Broadcast(this, NewState);
    BP_OnStateChanged(NewState);
}

void AAbyssalCreature::OnPerceptionUpdated(const TArray<AActor*>& UpdatedActors)
{
    if (IsDead())
    {
        return;
    }

    for (AActor* Actor : UpdatedActors)
    {
        if (!Actor || Actor == this)
        {
            continue;
        }

        FActorPerceptionBlueprintInfo PerceptionInfo;
        PerceptionComponent->GetActorsPerception(Actor, PerceptionInfo);

        bool bCurrentlySeen = false;
        for (const FAIStimulus& Stimulus : PerceptionInfo.LastSensedStimuli)
        {
            if (Stimulus.IsValid() && Stimulus.IsActive())
            {
                bCurrentlySeen = true;
                break;
            }
        }

        if (!bCurrentlySeen)
        {
            continue;
        }

        // New threat sighted
        ThreatTarget = Actor;
        OnThreatPerceived.Broadcast(this, Actor);
        BP_OnThreatPerceived(Actor);

        if (CurrentState == EAbyssalCreatureState::Passive)
        {
            const bool bLowHealth = (CurrentHealth / MaxHealth) <= FleeHealthThreshold;
            if (bIsAggressive && !bLowHealth)
            {
                SetCreatureState(EAbyssalCreatureState::Aggressive);
            }
            else
            {
                SetCreatureState(EAbyssalCreatureState::Curious);
            }
        }
    }
}

void AAbyssalCreature::ApplySpeedForState(EAbyssalCreatureState State)
{
    UCharacterMovementComponent* MoveComp = GetCharacterMovement();
    if (!MoveComp)
    {
        return;
    }

    switch (State)
    {
        case EAbyssalCreatureState::Passive:    MoveComp->MaxWalkSpeed = PassiveSpeed;    break;
        case EAbyssalCreatureState::Curious:    MoveComp->MaxWalkSpeed = CuriousSpeed;    break;
        case EAbyssalCreatureState::Fleeing:    MoveComp->MaxWalkSpeed = FleeSpeed;       break;
        case EAbyssalCreatureState::Aggressive: MoveComp->MaxWalkSpeed = AggressiveSpeed; break;
        case EAbyssalCreatureState::Dead:       MoveComp->MaxWalkSpeed = 0.0f;            break;
    }
}
