#include "AbyssalAudioSubsystem.h"

void UAbyssalAudioSubsystem::SetBiomeAmbient(FName BiomeId)
{
    if (CurrentBiomeId == BiomeId)
    {
        return;
    }
    CurrentBiomeId = BiomeId;
    BroadcastLayer(EAbyssalAudioLayer::BiomeAmbient);
}

void UAbyssalAudioSubsystem::SetTensionLevel(float Level)
{
    const float Clamped = FMath::Clamp(Level, 0.0f, 1.0f);
    if (FMath::IsNearlyEqual(Clamped, TensionLevel))
    {
        return;
    }
    TensionLevel = Clamped;
    BroadcastLayer(EAbyssalAudioLayer::Tension);
}

void UAbyssalAudioSubsystem::SetVitalWarningLevel(float Level)
{
    const float Clamped = FMath::Clamp(Level, 0.0f, 1.0f);
    if (FMath::IsNearlyEqual(Clamped, VitalWarningLevel))
    {
        return;
    }
    VitalWarningLevel = Clamped;
    BroadcastLayer(EAbyssalAudioLayer::VitalWarning);
}

void UAbyssalAudioSubsystem::DuckForNarrative(bool bDucked)
{
    if (bNarrativeDucked == bDucked)
    {
        return;
    }
    bNarrativeDucked = bDucked;
    // Ducking changes the effective volume of ambient + tension layers
    BroadcastLayer(EAbyssalAudioLayer::BiomeAmbient);
    BroadcastLayer(EAbyssalAudioLayer::Tension);
    BroadcastLayer(EAbyssalAudioLayer::Narrative);
}

float UAbyssalAudioSubsystem::GetEffectiveLayerVolume(EAbyssalAudioLayer Layer) const
{
    const float Duck = bNarrativeDucked ? NarrativeDuckMultiplier : 1.0f;

    switch (Layer)
    {
        case EAbyssalAudioLayer::BiomeAmbient:
            return 1.0f * Duck;
        case EAbyssalAudioLayer::Tension:
            return TensionLevel * Duck;
        case EAbyssalAudioLayer::VitalWarning:
            return VitalWarningLevel; // Never ducked — safety information
        case EAbyssalAudioLayer::Narrative:
            return bNarrativeDucked ? 1.0f : 0.0f;
    }
    return 0.0f;
}

void UAbyssalAudioSubsystem::BroadcastLayer(EAbyssalAudioLayer Layer)
{
    OnLayerVolumeChanged.Broadcast(Layer, GetEffectiveLayerVolume(Layer));
}
