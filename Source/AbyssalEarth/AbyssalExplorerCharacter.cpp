#include "AbyssalExplorerCharacter.h"
#include "AbyssalAudioCueSubsystem.h"
#include "BeaconActor.h"
#include "BeaconSubsystem.h"
#include "AbyssalHealthComponent.h"
#include "DiscoveryActor.h"
#include "DiscoverySubsystem.h"
#include "ObjectiveSubsystem.h"
#include "ScannerComponent.h"
#include "Camera/CameraComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/GameInstance.h"
#include "Engine/LocalPlayer.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "InputActionValue.h"

AAbyssalExplorerCharacter::AAbyssalExplorerCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    FirstPersonCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonCamera"));
    // Attach to the capsule root rather than the skeletal mesh socket.
    // The character mesh is assigned per-Blueprint; attaching to "head" here
    // fires GetSocketInfoByName warnings when no SkeletalMesh is set.
    FirstPersonCamera->SetupAttachment(GetRootComponent());
    FirstPersonCamera->SetRelativeLocation(FVector(0.0f, 0.0f, 64.0f));
    FirstPersonCamera->bUsePawnControlRotation = true;

    ScannerComponent = CreateDefaultSubobject<UScannerComponent>(TEXT("ScannerComponent"));
    HealthComponent = CreateDefaultSubobject<UAbyssalHealthComponent>(TEXT("HealthComponent"));

    UCharacterMovementComponent* Movement = GetCharacterMovement();
    Movement->MaxWalkSpeed = WalkSpeed;
    Movement->bOrientRotationToMovement = false;
    Movement->NavAgentProps.bCanCrouch = true;
    Movement->SetCrouchedHalfHeight(CrouchedHalfHeight);
    bUseControllerRotationYaw = true;
}

UScannerComponent* AAbyssalExplorerCharacter::GetScannerComponent() const
{
    return ScannerComponent;
}

UAbyssalHealthComponent* AAbyssalExplorerCharacter::GetHealthComponent() const
{
    return HealthComponent;
}

void AAbyssalExplorerCharacter::BeginPlay()
{
    Super::BeginPlay();

    if (APlayerController* PlayerController = Cast<APlayerController>(Controller))
    {
        if (UEnhancedInputLocalPlayerSubsystem* Subsystem =
            ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer()))
        {
            if (DefaultMappingContext)
            {
                Subsystem->AddMappingContext(DefaultMappingContext, 0);
            }
        }
    }

    if (BeaconClass && GetGameInstance())
    {
        if (UBeaconSubsystem* BeaconSubsystem = GetGameInstance()->GetSubsystem<UBeaconSubsystem>())
        {
            BeaconSubsystem->RestoreSavedBeacons(this, BeaconClass);
        }
    }

    if (GetGameInstance())
    {
        if (UAbyssalAudioCueSubsystem* AudioCueSubsystem = GetGameInstance()->GetSubsystem<UAbyssalAudioCueSubsystem>())
        {
            AudioCueSubsystem->RegisterScannerComponent(ScannerComponent);
        }
    }

    if (HealthComponent)
    {
        HealthComponent->OnDamaged.AddDynamic(this, &AAbyssalExplorerCharacter::HandleHealthDamaged);
    }
}

void AAbyssalExplorerCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (HealthComponent)
    {
        HealthComponent->OnDamaged.RemoveDynamic(this, &AAbyssalExplorerCharacter::HandleHealthDamaged);
    }

    if (GetGameInstance())
    {
        if (UAbyssalAudioCueSubsystem* AudioCueSubsystem = GetGameInstance()->GetSubsystem<UAbyssalAudioCueSubsystem>())
        {
            AudioCueSubsystem->UnregisterScannerComponent(ScannerComponent);
        }
    }

    Super::EndPlay(EndPlayReason);
}

void AAbyssalExplorerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    UEnhancedInputComponent* EnhancedInput = CastChecked<UEnhancedInputComponent>(PlayerInputComponent);
    if (MoveAction)
    {
        EnhancedInput->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AAbyssalExplorerCharacter::Move);
    }
    if (LookAction)
    {
        EnhancedInput->BindAction(LookAction, ETriggerEvent::Triggered, this, &AAbyssalExplorerCharacter::Look);
    }
    if (SprintAction)
    {
        EnhancedInput->BindAction(SprintAction, ETriggerEvent::Started, this, &AAbyssalExplorerCharacter::StartSprint);
        EnhancedInput->BindAction(SprintAction, ETriggerEvent::Completed, this, &AAbyssalExplorerCharacter::StopSprint);
    }
    if (CrouchAction)
    {
        EnhancedInput->BindAction(CrouchAction, ETriggerEvent::Started, this, &AAbyssalExplorerCharacter::StartCrouch);
        EnhancedInput->BindAction(CrouchAction, ETriggerEvent::Completed, this, &AAbyssalExplorerCharacter::StopCrouch);
    }
    if (ScanAction)
    {
        EnhancedInput->BindAction(ScanAction, ETriggerEvent::Started, this, &AAbyssalExplorerCharacter::TriggerScan);
    }
    if (PlaceBeaconAction)
    {
        EnhancedInput->BindAction(PlaceBeaconAction, ETriggerEvent::Started, this, &AAbyssalExplorerCharacter::PlaceBeacon);
    }
    if (JournalAction)
    {
        EnhancedInput->BindAction(JournalAction, ETriggerEvent::Started, this, &AAbyssalExplorerCharacter::ToggleJournal);
    }
}

void AAbyssalExplorerCharacter::Move(const FInputActionValue& Value)
{
    const FVector2D MovementVector = Value.Get<FVector2D>();
    AddMovementInput(GetActorForwardVector(), MovementVector.Y);
    AddMovementInput(GetActorRightVector(), MovementVector.X);
}

void AAbyssalExplorerCharacter::Look(const FInputActionValue& Value)
{
    const FVector2D LookAxisVector = Value.Get<FVector2D>();
    AddControllerYawInput(LookAxisVector.X);
    AddControllerPitchInput(LookAxisVector.Y);
}

void AAbyssalExplorerCharacter::StartSprint()
{
    GetCharacterMovement()->MaxWalkSpeed = SprintSpeed;
}

void AAbyssalExplorerCharacter::StopSprint()
{
    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
}

void AAbyssalExplorerCharacter::StartCrouch()
{
    Crouch();
}

void AAbyssalExplorerCharacter::StopCrouch()
{
    UnCrouch();
}

void AAbyssalExplorerCharacter::TriggerScan()
{
    if (ScannerComponent)
    {
        ScannerComponent->Scan();
    }
}

void AAbyssalExplorerCharacter::ToggleJournal()
{
    BP_ToggleJournal();
}

void AAbyssalExplorerCharacter::HandleHealthDamaged(float DamageAmount, AActor* DamageCauser, float CurrentHealth)
{
    BP_OnTookDamage(DamageAmount, DamageCauser);
}

void AAbyssalExplorerCharacter::AbyssalDebugDiscoverAll()
{
#if !UE_BUILD_SHIPPING
    UWorld* World = GetWorld();
    UGameInstance* GameInstance = GetGameInstance();
    UDiscoverySubsystem* DiscoverySubsystem = GameInstance ? GameInstance->GetSubsystem<UDiscoverySubsystem>() : nullptr;
    if (!World || !DiscoverySubsystem)
    {
        return;
    }

    int32 Registered = 0;
    for (TActorIterator<ADiscoveryActor> It(World); It; ++It)
    {
        ADiscoveryActor* Discovery = *It;
        if (!Discovery)
        {
            continue;
        }

        FAbyssalDiscoveryEntry Entry;
        Entry.DiscoveryId = Discovery->DiscoveryId.IsNone() ? FName(*Discovery->GetName()) : Discovery->DiscoveryId;
        Entry.DisplayName = Discovery->DisplayName.IsEmpty() ? FText::FromName(Entry.DiscoveryId) : Discovery->DisplayName;
        Entry.JournalText = Discovery->JournalText;
        Entry.Category = Discovery->Category;
        if (DiscoverySubsystem->RegisterDiscoveryEntry(Entry))
        {
            ++Registered;
        }
    }

    UE_LOG(LogTemp, Display, TEXT("[AbyssalDebug] Registered %d new discoveries."), Registered);
#endif // !UE_BUILD_SHIPPING
}

void AAbyssalExplorerCharacter::AbyssalDebugResetDiscoveries()
{
#if !UE_BUILD_SHIPPING
    UGameInstance* GameInstance = GetGameInstance();
    if (!GameInstance)
    {
        return;
    }

    if (UDiscoverySubsystem* DiscoverySubsystem = GameInstance->GetSubsystem<UDiscoverySubsystem>())
    {
        DiscoverySubsystem->ClearAllDiscoveries();
    }

    if (UObjectiveSubsystem* ObjectiveSubsystem = GameInstance->GetSubsystem<UObjectiveSubsystem>())
    {
        ObjectiveSubsystem->ResetRoute();
    }

    UE_LOG(LogTemp, Display, TEXT("[AbyssalDebug] Discoveries cleared from save, objective route reset."));
#endif // !UE_BUILD_SHIPPING
}

void AAbyssalExplorerCharacter::AbyssalDebugAdvanceObjective()
{
#if !UE_BUILD_SHIPPING
    UGameInstance* GameInstance = GetGameInstance();
    if (!GameInstance)
    {
        return;
    }

    if (UObjectiveSubsystem* ObjectiveSubsystem = GameInstance->GetSubsystem<UObjectiveSubsystem>())
    {
        const bool bAdvanced = ObjectiveSubsystem->CompleteCurrentObjective();
        UE_LOG(LogTemp, Display, TEXT("[AbyssalDebug] AdvanceObjective -> %s"), bAdvanced ? TEXT("advanced") : TEXT("no-op (route complete?)"));
    }
#endif // !UE_BUILD_SHIPPING
}

void AAbyssalExplorerCharacter::PlaceBeacon()
{
    if (!BeaconClass || !FirstPersonCamera || !GetWorld())
    {
        return;
    }

    const FVector Start = FirstPersonCamera->GetComponentLocation();
    const FVector End = Start + FirstPersonCamera->GetForwardVector() * MaxBeaconPlacementDistance;

    FHitResult Hit;
    FCollisionQueryParams Params(SCENE_QUERY_STAT(PlaceBeacon), false, this);

    if (!GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
    {
        return;
    }

    UBeaconSubsystem* BeaconSubsystem = GetGameInstance() ? GetGameInstance()->GetSubsystem<UBeaconSubsystem>() : nullptr;

    if (ABeaconActor* ExistingBeacon = Cast<ABeaconActor>(Hit.GetActor()))
    {
        if (BeaconSubsystem)
        {
            BeaconSubsystem->RemoveBeacon(ExistingBeacon);
        }
        else
        {
            ExistingBeacon->Destroy();
        }
        return;
    }

    const FVector SpawnLocation = Hit.ImpactPoint + Hit.ImpactNormal * 12.0f;
    const FRotator SpawnRotation = Hit.ImpactNormal.Rotation();
    ABeaconActor* Beacon = GetWorld()->SpawnActor<ABeaconActor>(BeaconClass, SpawnLocation, SpawnRotation);
    if (Beacon && BeaconSubsystem)
    {
        BeaconSubsystem->RegisterBeacon(Beacon);
    }
}
