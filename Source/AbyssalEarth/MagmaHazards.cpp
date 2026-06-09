#include "MagmaHazards.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"

// ---------------------------------------------------------------------------
// AMagmaGeyserHazard
// ---------------------------------------------------------------------------

AMagmaGeyserHazard::AMagmaGeyserHazard()
{
    DamageMode = EHazardDamageMode::Radial;
    DamageRadius = 350.0f;
    DamagePerSecond = 30.0f;
    WarningDuration = 2.0f;
    ActiveDuration = 1.5f;
    CooldownDuration = 8.0f;
    bAutoActivate = true;
}

void AMagmaGeyserHazard::OnActivePhaseBegin_Implementation()
{
    Super::OnActivePhaseBegin_Implementation();

    const FVector ApexOrigin = GetActorLocation() + FVector(0.0f, 0.0f, ApexHeight);

    // Knockback all characters in blast radius
    TArray<AActor*> IgnoredActors;
    IgnoredActors.Add(this);
    UGameplayStatics::ApplyRadialDamage(this, DamagePerSecond, ApexOrigin,
        EruptionRadius, nullptr, IgnoredActors, this, nullptr, true);

    // Knockback pass (radial damage doesn't inherently push characters)
    TArray<AActor*> NearbyActors;
    UGameplayStatics::GetAllActorsOfClass(this, ACharacter::StaticClass(), NearbyActors);
    for (AActor* Actor : NearbyActors)
    {
        const float Dist = FVector::Dist(Actor->GetActorLocation(), ApexOrigin);
        if (Dist <= EruptionRadius)
        {
            ACharacter* Char = Cast<ACharacter>(Actor);
            if (Char && Char->GetCharacterMovement())
            {
                const FVector Dir = (Actor->GetActorLocation() - ApexOrigin).GetSafeNormal();
                Char->GetCharacterMovement()->AddImpulse(Dir * KnockbackImpulse, true);
            }
        }
    }
}

// ---------------------------------------------------------------------------
// AMagmaPulseHazard
// ---------------------------------------------------------------------------

AMagmaPulseHazard::AMagmaPulseHazard()
{
    DamageMode = EHazardDamageMode::Radial;
    DamageRadius = 180.0f;
    DamagePerSecond = 18.0f;
    WarningDuration = 0.0f; // No warning — instant pulse
    ActiveDuration = 0.3f;
    CooldownDuration = 3.5f;
    bAutoActivate = true;
}

void AMagmaPulseHazard::OnActivePhaseBegin_Implementation()
{
    Super::OnActivePhaseBegin_Implementation();

    TArray<AActor*> IgnoredActors;
    IgnoredActors.Add(this);
    UGameplayStatics::ApplyRadialDamage(this, DamagePerSecond, GetActorLocation(),
        PulseRadius, nullptr, IgnoredActors, this, nullptr, true);
}
