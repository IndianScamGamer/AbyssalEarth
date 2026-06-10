#include "AbyssalPlayerController.h"
#include "AbyssalPlayerCharacter.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputActionValue.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"

AAbyssalPlayerController::AAbyssalPlayerController()
{
}

void AAbyssalPlayerController::BeginPlay()
{
    Super::BeginPlay();

    if (DefaultMappingContext)
    {
        if (UEnhancedInputLocalPlayerSubsystem* Subsystem =
            ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(GetLocalPlayer()))
        {
            Subsystem->AddMappingContext(DefaultMappingContext, 0);
        }
    }
}

void AAbyssalPlayerController::SetupInputComponent()
{
    Super::SetupInputComponent();

    UEnhancedInputComponent* EIC = CastChecked<UEnhancedInputComponent>(InputComponent);

    if (MoveAction)
    {
        EIC->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AAbyssalPlayerController::HandleMove);
    }
    if (LookAction)
    {
        EIC->BindAction(LookAction, ETriggerEvent::Triggered, this, &AAbyssalPlayerController::HandleLook);
    }
    if (SprintAction)
    {
        EIC->BindAction(SprintAction, ETriggerEvent::Started,   this, &AAbyssalPlayerController::HandleSprintStart);
        EIC->BindAction(SprintAction, ETriggerEvent::Completed, this, &AAbyssalPlayerController::HandleSprintStop);
    }
    if (CrouchAction)
    {
        EIC->BindAction(CrouchAction, ETriggerEvent::Started,   this, &AAbyssalPlayerController::HandleCrouchStart);
        EIC->BindAction(CrouchAction, ETriggerEvent::Completed, this, &AAbyssalPlayerController::HandleCrouchStop);
    }
    if (InteractAction)
    {
        EIC->BindAction(InteractAction, ETriggerEvent::Started, this, &AAbyssalPlayerController::HandleInteract);
    }
    if (ScanPulseAction)
    {
        EIC->BindAction(ScanPulseAction, ETriggerEvent::Started, this, &AAbyssalPlayerController::HandleScanPulse);
    }
    if (ObservationModeAction)
    {
        EIC->BindAction(ObservationModeAction, ETriggerEvent::Started, this, &AAbyssalPlayerController::HandleObservationMode);
    }
}

AAbyssalPlayerCharacter* AAbyssalPlayerController::GetAbyssalCharacter() const
{
    return Cast<AAbyssalPlayerCharacter>(GetPawn());
}

void AAbyssalPlayerController::HandleMove(const FInputActionValue& Value)
{
    ACharacter* Char = GetCharacter();
    if (!Char)
    {
        return;
    }
    const FVector2D MoveVec = Value.Get<FVector2D>();
    Char->AddMovementInput(Char->GetActorForwardVector(), MoveVec.Y);
    Char->AddMovementInput(Char->GetActorRightVector(),   MoveVec.X);
}

void AAbyssalPlayerController::HandleLook(const FInputActionValue& Value)
{
    const FVector2D LookVec = Value.Get<FVector2D>();
    AddYawInput(LookVec.X);
    AddPitchInput(LookVec.Y);
}

void AAbyssalPlayerController::HandleSprintStart()
{
    if (AAbyssalPlayerCharacter* PC = GetAbyssalCharacter())
    {
        PC->Input_SprintStart();
    }
}

void AAbyssalPlayerController::HandleSprintStop()
{
    if (AAbyssalPlayerCharacter* PC = GetAbyssalCharacter())
    {
        PC->Input_SprintStop();
    }
}

void AAbyssalPlayerController::HandleCrouchStart()
{
    if (ACharacter* Char = GetCharacter())
    {
        Char->Crouch();
    }
}

void AAbyssalPlayerController::HandleCrouchStop()
{
    if (ACharacter* Char = GetCharacter())
    {
        Char->UnCrouch();
    }
}

void AAbyssalPlayerController::HandleInteract()
{
    if (AAbyssalPlayerCharacter* PC = GetAbyssalCharacter())
    {
        PC->Input_Interact();
    }
}

void AAbyssalPlayerController::HandleScanPulse()
{
    if (AAbyssalPlayerCharacter* PC = GetAbyssalCharacter())
    {
        PC->Input_ScanPulse();
    }
}

void AAbyssalPlayerController::HandleObservationMode()
{
    if (AAbyssalPlayerCharacter* PC = GetAbyssalCharacter())
    {
        PC->Input_ToggleObservationMode();
    }
}
