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
    IdleDuration = 6.5f;
    WarningDuration = 2.0f;
    ActiveDuration = 1.5f;
    CooldownDuration = 1.5f;
    bStartActive = true;
}

void AMagmaGeyserHazard::OnPhaseChanged(EHazardPhase NewPhase)
{
    Super::OnPhaseChanged(NewPhase);

    if (NewPhase != EHazardPhase::Active)
    {
        return;
    }

    const FVector ApexOrigin = GetActorLocation() + FVector(0.0f, 0.0f, ApexHeight);

    // One-off burst damage at the apex on eruption (the base damage tick covers lingering)
    TArray<AActor*> IgnoredActors;
    IgnoredActors.Add(this);
    UGameplayStatics::ApplyRadialDamage(this, DamagePerSecond, ApexOrigin,
        EruptionRadius, HazardDamageType, IgnoredActors, this, nullptr, true);

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
    IdleDuration = 3.5f;
    WarningDuration = 0.2f; // Barely-there glow flash before the pulse
    ActiveDuration = 0.3f;
    CooldownDuration = 0.0f;
    bStartActive = true;
}

void AMagmaPulseHazard::OnPhaseChanged(EHazardPhase NewPhase)
{
    Super::OnPhaseChanged(NewPhase);

    if (NewPhase != EHazardPhase::Active)
    {
        return;
    }

    TArray<AActor*> IgnoredActors;
    IgnoredActors.Add(this);
    UGameplayStatics::ApplyRadialDamage(this, DamagePerSecond, GetActorLocation(),
        PulseRadius, HazardDamageType, IgnoredActors, this, nullptr, true);
}
