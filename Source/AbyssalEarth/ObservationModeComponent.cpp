#include "ObservationModeComponent.h"
#include "Camera/CameraActor.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "DiscoverySubsystem.h"

UObservationModeComponent::UObservationModeComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.bStartWithTickEnabled = false;
    CurrentFOV = DefaultFOV;
}

void UObservationModeComponent::BeginPlay()
{
    Super::BeginPlay();
    CurrentFOV = DefaultFOV;
}

void UObservationModeComponent::EndPlay(EEndPlayReason::Type EndPlayReason)
{
    if (bIsObserving)
    {
        ExitObservationMode();
    }
    Super::EndPlay(EndPlayReason);
}

void UObservationModeComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    ClampCameraToRadius();
}

void UObservationModeComponent::EnterObservationMode()
{
    if (bIsObserving)
    {
        return;
    }

    ACharacter* Owner = Cast<ACharacter>(GetOwner());
    if (!Owner)
    {
        return;
    }

    bIsObserving = true;
    OwnerEnterLocation = Owner->GetActorLocation();
    CameraLocation = OwnerEnterLocation;
    CameraRotation = Owner->GetControlRotation();
    CurrentFOV = DefaultFOV;

    SpawnObservationCamera();
    SetComponentTickEnabled(true);

    // Disable pawn movement input via the controller
    if (APlayerController* PC = Cast<APlayerController>(Owner->GetController()))
    {
        PC->SetIgnoreMoveInput(true);
    }

    OnObservationModeEntered.Broadcast();
    BP_OnEnterObservationMode();
}

void UObservationModeComponent::ExitObservationMode()
{
    if (!bIsObserving)
    {
        return;
    }

    bIsObserving = false;
    SetComponentTickEnabled(false);
    DestroyObservationCamera();

    ACharacter* Owner = Cast<ACharacter>(GetOwner());
    if (Owner)
    {
        if (APlayerController* PC = Cast<APlayerController>(Owner->GetController()))
        {
            PC->SetIgnoreMoveInput(false);
            // Restore view to pawn
            PC->SetViewTargetWithBlend(Owner, 0.25f);
        }
    }

    OnObservationModeExited.Broadcast();
    BP_OnExitObservationMode();
}

void UObservationModeComponent::ToggleObservationMode()
{
    bIsObserving ? ExitObservationMode() : EnterObservationMode();
}

void UObservationModeComponent::MoveCamera(FVector WorldDelta)
{
    if (!bIsObserving)
    {
        return;
    }
    CameraLocation += WorldDelta;
    ClampCameraToRadius();
    if (ObservationCamera)
    {
        ObservationCamera->SetActorLocation(CameraLocation);
    }
}

void UObservationModeComponent::RotateCamera(float DeltaPitch, float DeltaYaw)
{
    if (!bIsObserving)
    {
        return;
    }
    CameraRotation.Pitch = FMath::Clamp(CameraRotation.Pitch + DeltaPitch, -MaxPitchAngle, MaxPitchAngle);
    CameraRotation.Yaw += DeltaYaw;
    CameraRotation.Yaw = FRotator::NormalizeAxis(CameraRotation.Yaw);
    if (ObservationCamera)
    {
        ObservationCamera->SetActorRotation(CameraRotation);
    }
}

void UObservationModeComponent::RollCamera(float DeltaRoll)
{
    if (!bIsObserving)
    {
        return;
    }
    CameraRotation.Roll = FMath::Clamp(CameraRotation.Roll + DeltaRoll, -MaxRollAngle, MaxRollAngle);
    if (ObservationCamera)
    {
        ObservationCamera->SetActorRotation(CameraRotation);
    }
}

void UObservationModeComponent::AdjustZoom(float DeltaFOV)
{
    if (!bIsObserving)
    {
        return;
    }
    CurrentFOV = FMath::Clamp(CurrentFOV + DeltaFOV, MinFOV, MaxFOV);
    if (ObservationCamera)
    {
        if (UCameraComponent* CamComp = ObservationCamera->GetCameraComponent())
        {
            CamComp->FieldOfView = CurrentFOV;
        }
    }
}

void UObservationModeComponent::ScanForward()
{
    if (!bIsObserving || !ObservationCamera)
    {
        return;
    }

    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    const FVector Start = CameraLocation;
    const FVector End = Start + CameraRotation.Vector() * ScanDistance;

    FHitResult Hit;
    FCollisionQueryParams Params;
    Params.AddIgnoredActor(GetOwner());
    Params.AddIgnoredActor(ObservationCamera);

    if (!World->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
    {
        return;
    }

    AActor* HitActor = Hit.GetActor();
    if (!HitActor)
    {
        return;
    }

    // Resolve discovery ID: actor tag takes priority, then actor name as fallback
    FName DiscoveryId = NAME_None;
    for (const FName& Tag : HitActor->Tags)
    {
        if (!Tag.IsNone())
        {
            DiscoveryId = Tag;
            break;
        }
    }
    if (DiscoveryId.IsNone())
    {
        return;
    }

    if (UGameInstance* GI = UGameplayStatics::GetGameInstance(this))
    {
        if (UDiscoverySubsystem* Discovery = GI->GetSubsystem<UDiscoverySubsystem>())
        {
            Discovery->RegisterDiscovery(DiscoveryId);
        }
    }

    OnScanComplete.Broadcast(DiscoveryId);
    BP_OnScanHit(HitActor, DiscoveryId);
}

FVector UObservationModeComponent::GetCameraLocation() const
{
    return ObservationCamera ? ObservationCamera->GetActorLocation() : FVector::ZeroVector;
}

FRotator UObservationModeComponent::GetCameraRotation() const
{
    return ObservationCamera ? ObservationCamera->GetActorRotation() : FRotator::ZeroRotator;
}

void UObservationModeComponent::SpawnObservationCamera()
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    FActorSpawnParameters Params;
    Params.Owner = GetOwner();
    ObservationCamera = World->SpawnActor<ACameraActor>(CameraLocation, CameraRotation, Params);

    if (ObservationCamera)
    {
        if (UCameraComponent* CamComp = ObservationCamera->GetCameraComponent())
        {
            CamComp->FieldOfView = CurrentFOV;
        }

        // Blend the player view to the observation camera
        ACharacter* Owner = Cast<ACharacter>(GetOwner());
        if (Owner)
        {
            if (APlayerController* PC = Cast<APlayerController>(Owner->GetController()))
            {
                PC->SetViewTargetWithBlend(ObservationCamera, 0.25f);
            }
        }
    }
}

void UObservationModeComponent::DestroyObservationCamera()
{
    if (ObservationCamera)
    {
        ObservationCamera->Destroy();
        ObservationCamera = nullptr;
    }
}

void UObservationModeComponent::ClampCameraToRadius()
{
    if (!bIsObserving)
    {
        return;
    }
    const FVector Delta = CameraLocation - OwnerEnterLocation;
    if (Delta.SizeSquared() > FMath::Square(MaxRoamRadius))
    {
        CameraLocation = OwnerEnterLocation + Delta.GetSafeNormal() * MaxRoamRadius;
        if (ObservationCamera)
        {
            ObservationCamera->SetActorLocation(CameraLocation);
        }
    }
}
