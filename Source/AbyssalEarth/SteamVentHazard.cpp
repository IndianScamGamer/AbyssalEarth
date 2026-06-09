#include "SteamVentHazard.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"

ASteamVentHazard::ASteamVentHazard()
{
    DamageMode = EHazardDamageMode::Overlap;
    DamagePerSecond = 8.0f;
    IdleDuration = 5.0f;
    WarningDuration = 1.5f;
    ActiveDuration = 3.0f;
    CooldownDuration = 2.0f;
    bStartActive = true;

    SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
    SetRootComponent(SceneRoot);

    SteamColumn = CreateDefaultSubobject<UCapsuleComponent>(TEXT("SteamColumn"));
    SteamColumn->SetupAttachment(RootComponent);
    SteamColumn->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    SteamColumn->SetCollisionResponseToAllChannels(ECR_Overlap);
    SteamColumn->OnComponentBeginOverlap.AddDynamic(this, &ASteamVentHazard::OnSteamOverlapBegin);
}

void ASteamVentHazard::BeginPlay()
{
    SteamColumn->SetCapsuleSize(ColumnRadius, ColumnHeight * 0.5f);
    // Centre the capsule so its base sits at the vent mouth
    SteamColumn->SetRelativeLocation(FVector(0.0f, 0.0f, ColumnHeight * 0.5f));
    // Base class applies overlap damage to actors inside registered primitives
    RegisterDamagePrimitive(SteamColumn);

    Super::BeginPlay();
}

void ASteamVentHazard::OnPhaseChanged(EHazardPhase NewPhase)
{
    Super::OnPhaseChanged(NewPhase);
    // Column only collides while erupting
    SteamColumn->SetCollisionEnabled(
        NewPhase == EHazardPhase::Active ? ECollisionEnabled::QueryOnly : ECollisionEnabled::NoCollision);
}

void ASteamVentHazard::OnSteamOverlapBegin(UPrimitiveComponent* /*OverlappedComp*/, AActor* OtherActor,
    UPrimitiveComponent* /*OtherComp*/, int32 /*OtherBodyIndex*/, bool /*bFromSweep*/, const FHitResult& /*SweepResult*/)
{
    if (!OtherActor || OtherActor == this)
    {
        return;
    }

    // Instant upward launch on entry
    if (ACharacter* Char = Cast<ACharacter>(OtherActor))
    {
        if (UCharacterMovementComponent* MoveComp = Char->GetCharacterMovement())
        {
            MoveComp->AddImpulse(FVector(0.0f, 0.0f, LaunchImpulse), true);
        }
    }
}
