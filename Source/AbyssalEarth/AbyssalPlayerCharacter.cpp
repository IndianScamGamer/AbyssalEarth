#include "AbyssalPlayerCharacter.h"
#include "AbyssalGameMode.h"
#include "AbyssalHealthComponent.h"
#include "OxygenComponent.h"
#include "StaminaComponent.h"
#include "TemperatureComponent.h"
#include "PressureComponent.h"
#include "AbyssalInteractionComponent.h"
#include "AbyssalScanComponent.h"
#include "AbyssalTraversalComponent.h"
#include "ObservationModeComponent.h"
#include "AbyssalHUDSubsystem.h"
#include "AbyssalUpgradeSubsystem.h"
#include "CheckpointSubsystem.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"

AAbyssalPlayerCharacter::AAbyssalPlayerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    HealthComponent      = CreateDefaultSubobject<UAbyssalHealthComponent>(TEXT("HealthComponent"));
    OxygenComponent      = CreateDefaultSubobject<UOxygenComponent>(TEXT("OxygenComponent"));
    StaminaComponent     = CreateDefaultSubobject<UStaminaComponent>(TEXT("StaminaComponent"));
    TemperatureComponent = CreateDefaultSubobject<UTemperatureComponent>(TEXT("TemperatureComponent"));
    PressureComponent    = CreateDefaultSubobject<UPressureComponent>(TEXT("PressureComponent"));
    InteractionComponent = CreateDefaultSubobject<UAbyssalInteractionComponent>(TEXT("InteractionComponent"));
    ScanComponent        = CreateDefaultSubobject<UAbyssalScanComponent>(TEXT("ScanComponent"));
    TraversalComponent   = CreateDefaultSubobject<UAbyssalTraversalComponent>(TEXT("TraversalComponent"));
    ObservationComponent = CreateDefaultSubobject<UObservationModeComponent>(TEXT("ObservationComponent"));
}

void AAbyssalPlayerCharacter::BeginPlay()
{
    Super::BeginPlay();

    BaseWalkSpeed = GetCharacterMovement()->MaxWalkSpeed;

    HealthComponent->OnDeath.AddDynamic(this, &AAbyssalPlayerCharacter::HandleDeath);

    if (UGameInstance* GI = GetGameInstance())
    {
        if (UAbyssalHUDSubsystem* HUD = GI->GetSubsystem<UAbyssalHUDSubsystem>())
        {
            HUD->RegisterPlayerPawn(this);
        }
        if (UAbyssalUpgradeSubsystem* Upgrades = GI->GetSubsystem<UAbyssalUpgradeSubsystem>())
        {
            Upgrades->RegisterPlayerPawn(this);
        }
    }
}

void AAbyssalPlayerCharacter::EndPlay(EEndPlayReason::Type EndPlayReason)
{
    if (HealthComponent)
    {
        HealthComponent->OnDeath.RemoveDynamic(this, &AAbyssalPlayerCharacter::HandleDeath);
    }
    Super::EndPlay(EndPlayReason);
}

void AAbyssalPlayerCharacter::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    UpdateDepth();

    // Sprint gate: stop sprinting when stamina runs out
    if (bWantsSprint && !StaminaComponent->CanExert())
    {
        ApplySprintState(false);
    }
}

void AAbyssalPlayerCharacter::Input_Interact()
{
    InteractionComponent->TryInteract();
}

void AAbyssalPlayerCharacter::Input_ScanPulse()
{
    ScanComponent->ScanPulse();
}

void AAbyssalPlayerCharacter::Input_ToggleObservationMode()
{
    ObservationComponent->ToggleObservationMode();
}

void AAbyssalPlayerCharacter::Input_SprintStart()
{
    bWantsSprint = true;
    if (StaminaComponent->CanExert())
    {
        ApplySprintState(true);
    }
}

void AAbyssalPlayerCharacter::Input_SprintStop()
{
    bWantsSprint = false;
    ApplySprintState(false);
}

void AAbyssalPlayerCharacter::HandleDeath(UAbyssalHealthComponent* /*HealthComp*/)
{
    // Stop all exertion and movement; schedule respawn via GameMode after RespawnDelay
    ApplySprintState(false);
    GetCharacterMovement()->StopMovementImmediately();
    GetCharacterMovement()->DisableMovement();
    BP_OnDeath();

    GetWorldTimerManager().SetTimer(
        RespawnTimerHandle,
        this,
        &AAbyssalPlayerCharacter::TriggerRespawnFromGameMode,
        RespawnDelay,
        false);
}

void AAbyssalPlayerCharacter::TriggerRespawnFromGameMode()
{
    if (AAbyssalGameMode* GM = GetWorld()->GetAuthGameMode<AAbyssalGameMode>())
    {
        GM->RespawnPlayer();
    }
}

void AAbyssalPlayerCharacter::RespawnAtCheckpoint()
{
    UGameInstance* GI = GetGameInstance();
    if (!GI)
    {
        return;
    }

    if (UCheckpointSubsystem* Checkpoints = GI->GetSubsystem<UCheckpointSubsystem>())
    {
        if (Checkpoints->HasActiveCheckpoint())
        {
            SetActorLocation(Checkpoints->GetRespawnLocation());
        }
    }

    HealthComponent->Respawn();
    OxygenComponent->RefillOxygen();
    StaminaComponent->RestoreStamina();
    TemperatureComponent->ResetTemperature();
    PressureComponent->ResetPressure();
    GetCharacterMovement()->SetMovementMode(MOVE_Walking);

    // Re-apply upgrades and HUD binding for the restored pawn
    if (UAbyssalUpgradeSubsystem* Upgrades = GI->GetSubsystem<UAbyssalUpgradeSubsystem>())
    {
        Upgrades->RegisterPlayerPawn(this);
    }
    if (UAbyssalHUDSubsystem* HUD = GI->GetSubsystem<UAbyssalHUDSubsystem>())
    {
        HUD->RegisterPlayerPawn(this);
    }

    BP_OnRespawned();
}

void AAbyssalPlayerCharacter::UpdateDepth()
{
    const float DepthMetres = FMath::Max(0.0f, (SeaLevelZ - GetActorLocation().Z) * DepthScale);
    PressureComponent->SetCurrentDepth(DepthMetres);
}

void AAbyssalPlayerCharacter::ApplySprintState(bool bSprinting)
{
    GetCharacterMovement()->MaxWalkSpeed = bSprinting ? BaseWalkSpeed * SprintSpeedMultiplier : BaseWalkSpeed;
    StaminaComponent->SetExerting(bSprinting);
}
