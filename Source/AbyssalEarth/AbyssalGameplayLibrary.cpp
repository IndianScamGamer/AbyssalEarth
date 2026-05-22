#include "AbyssalGameplayLibrary.h"
#include "BeaconSubsystem.h"
#include "DiscoverySubsystem.h"
#include "ObjectiveSubsystem.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"

namespace
{
    UGameInstance* ResolveGameInstance(const UObject* WorldContextObject)
    {
        if (!GEngine || !WorldContextObject)
        {
            return nullptr;
        }

        const UWorld* World = GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::ReturnNull);
        return World ? World->GetGameInstance() : nullptr;
    }
}

UDiscoverySubsystem* UAbyssalGameplayLibrary::GetDiscoverySubsystem(const UObject* WorldContextObject)
{
    UGameInstance* GameInstance = ResolveGameInstance(WorldContextObject);
    return GameInstance ? GameInstance->GetSubsystem<UDiscoverySubsystem>() : nullptr;
}

UObjectiveSubsystem* UAbyssalGameplayLibrary::GetObjectiveSubsystem(const UObject* WorldContextObject)
{
    UGameInstance* GameInstance = ResolveGameInstance(WorldContextObject);
    return GameInstance ? GameInstance->GetSubsystem<UObjectiveSubsystem>() : nullptr;
}

UBeaconSubsystem* UAbyssalGameplayLibrary::GetBeaconSubsystem(const UObject* WorldContextObject)
{
    UGameInstance* GameInstance = ResolveGameInstance(WorldContextObject);
    return GameInstance ? GameInstance->GetSubsystem<UBeaconSubsystem>() : nullptr;
}
