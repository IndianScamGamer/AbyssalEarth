#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "AbyssalAudioSubsystem.generated.h"

UENUM(BlueprintType)
enum class EAbyssalAudioLayer : uint8
{
    BiomeAmbient   UMETA(DisplayName = "Biome Ambient"),
    Tension        UMETA(DisplayName = "Tension"),
    VitalWarning   UMETA(DisplayName = "Vital Warning"),
    Narrative      UMETA(DisplayName = "Narrative"),
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalAudioLayerChangedSignature, EAbyssalAudioLayer, Layer, float, NewVolume);

/**
 * Ambient audio layer manager (roadmap O1). Tracks per-layer target volumes
 * (0..1) for the four game audio layers and exposes a single API for gameplay
 * systems to drive music/ambience state:
 *
 *   - SetBiomeAmbient(BiomeId): crossfade biome ambience on map travel
 *   - SetTensionLevel(0..1): creature aggression / hazard proximity
 *   - SetVitalWarningLevel(0..1): driven by UAbyssalHUDSubsystem readouts
 *   - DuckForNarrative(bDucked): lower other layers while a beat plays
 *
 * This subsystem is intentionally audio-asset-agnostic: it stores state and
 * broadcasts OnLayerVolumeChanged; the Blueprint audio manager (or MetaSound
 * graph) listens and performs the actual mixing. This keeps C++ free of
 * asset references and lets audio designers iterate without code changes.
 */
UCLASS()
class ABYSSALEARTH_API UAbyssalAudioSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    /** Switch the ambient biome track. Broadcasts a BiomeAmbient layer change. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Audio")
    void SetBiomeAmbient(FName BiomeId);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Audio")
    FName GetCurrentBiome() const { return CurrentBiomeId; }

    /** 0 = calm, 1 = full combat/danger tension. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Audio")
    void SetTensionLevel(float Level);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Audio")
    float GetTensionLevel() const { return TensionLevel; }

    /** 0 = all vitals fine, 1 = critical (drives heartbeat/alarm layer). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Audio")
    void SetVitalWarningLevel(float Level);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Audio")
    float GetVitalWarningLevel() const { return VitalWarningLevel; }

    /** Duck ambient/tension layers while narrative VO plays. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Audio")
    void DuckForNarrative(bool bDucked);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Audio")
    bool IsDuckedForNarrative() const { return bNarrativeDucked; }

    /** Volume the listener should apply to a layer right now, accounting for ducking. */
    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Audio")
    float GetEffectiveLayerVolume(EAbyssalAudioLayer Layer) const;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Audio")
    FAbyssalAudioLayerChangedSignature OnLayerVolumeChanged;

    /** Multiplier applied to BiomeAmbient + Tension while narrative ducking is active. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Audio", meta=(ClampMin="0.0", ClampMax="1.0"))
    float NarrativeDuckMultiplier = 0.35f;

private:
    void BroadcastLayer(EAbyssalAudioLayer Layer);

    UPROPERTY()
    FName CurrentBiomeId;

    UPROPERTY()
    float TensionLevel = 0.0f;

    UPROPERTY()
    float VitalWarningLevel = 0.0f;

    UPROPERTY()
    bool bNarrativeDucked = false;
};
