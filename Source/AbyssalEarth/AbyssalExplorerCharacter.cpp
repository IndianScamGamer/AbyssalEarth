#include "AbyssalExplorerCharacter.h"
#include "BeaconActor.h"
#include "BeaconSubsystem.h"
#include "ScannerComponent.h"
#include "Camera/CameraComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/LocalPlayer.h"
#include "Engine/World.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "InputActionValue.h"

AAbyssalExplorerCharacter::AAbyssalExplorerCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    FirstPersonCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonCamera"));
    FirstPersonCamera->SetupAttachment(GetRootComponent());
    FirstPersonCamera->SetRelativeLocation(FVector(0.0f, 0.0f, 64.0f));
    FirstPersonCamera->bUsePawnControlRotation = true;

    ScannerComponent = CreateDefaultSubobject<UScannerComponent>(TEXT("ScannerComponent"));

    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
    GetCharacterMovement()->bOrientRotationToMovement = false;
    bUseControllerRotationYaw = true;
}

UScannerComponent* AAbyssalExplorerCharacter::GetScannerComponent() const
{
    return ScannerComponent;
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
    if (ScanAction)
    {
        EnhancedInput->BindAction(ScanAction, ETriggerEvent::Started, this, &AAbyssalExplorerCharacter::TriggerScan);
    }
    if (PlaceBeaconAction)
    {
        EnhancedInput->BindAction(PlaceBeaconAction, ETriggerEvent::Started, this, &AAbyssalExplorerCharacter::PlaceBeacon);
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

void AAbyssalExplorerCharacter::TriggerScan()
{
    if (ScannerComponent)
    {
        ScannerComponent->Scan();
    }
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

    const FVector SpawnLocation = Hit.ImpactPoint + Hit.ImpactNormal * 12.0f;
    const FRotator SpawnRotation = Hit.ImpactNormal.Rotation();
    ABeaconActor* Beacon = GetWorld()->SpawnActor<ABeaconActor>(BeaconClass, SpawnLocation, SpawnRotation);
    if (Beacon && GetGameInstance())
    {
        if (UBeaconSubsystem* BeaconSubsystem = GetGameInstance()->GetSubsystem<UBeaconSubsystem>())
        {
            BeaconSubsystem->RegisterBeacon(Beacon);
        }
    }
}
