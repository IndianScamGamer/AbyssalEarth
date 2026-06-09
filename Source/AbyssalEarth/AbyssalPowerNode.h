#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AbyssalInteractable.h"
#include "AbyssalPowerNode.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAbyssalPowerChangedSignature, class AAbyssalPowerNode*, Node, float, NewPower);

UENUM(BlueprintType)
enum class EAbyssalPowerNodeType : uint8
{
    Source  UMETA(DisplayName = "Source"),    // Generates power when activated
    Relay   UMETA(DisplayName = "Relay"),     // Passes power from inputs to outputs, can split or boost
    Sink    UMETA(DisplayName = "Sink"),      // Receives power; drives AAbyssalInterfaceTerminal etc.
};

/**
 * Power routing node actor (roadmap K1 — Act 3 terminal puzzle system).
 * Nodes are placed in the world and connected via the ConnectedNodes array.
 * A Source node generates power when activated (IAbyssalInteractable);
 * that power propagates through Relay nodes to Sink nodes which call
 * SetPowerLevel on connected AAbyssalInterfaceTerminals.
 *
 * Power level is 0..1 normalised. Relay nodes can reduce power by
 * RelayLoss (default 0 — lossless) to require multiple sources for
 * distant terminals. Blueprint subclasses handle visuals and audio.
 */
UCLASS(Blueprintable)
class ABYSSALEARTH_API AAbyssalPowerNode : public AActor, public IAbyssalInteractable
{
    GENERATED_BODY()

public:
    AAbyssalPowerNode();

    /** Set the power level on this node and propagate to all connected nodes. */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Power")
    void SetPowerLevel(float NewPower);

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Power")
    float GetPowerLevel() const { return CurrentPower; }

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Power")
    EAbyssalPowerNodeType GetNodeType() const { return NodeType; }

    /** Activate this source node (sets power to SourceOutput). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Power")
    void Activate();

    /** Deactivate this source node (sets power to 0). */
    UFUNCTION(BlueprintCallable, Category = "Abyssal Earth|Power")
    void Deactivate();

    UFUNCTION(BlueprintPure, Category = "Abyssal Earth|Power")
    bool IsActive() const { return bIsActive; }

    // IAbyssalInteractable (Source nodes are player-interactable; Relay/Sink are not)
    virtual bool CanInteract_Implementation(AActor* Interactor) const override;
    virtual void OnInteract_Implementation(AActor* Interactor) override;
    virtual FText GetInteractPrompt_Implementation() const override;
    virtual void OnFocusBegin_Implementation(AActor* Interactor) override;
    virtual void OnFocusEnd_Implementation(AActor* Interactor) override;

    UPROPERTY(BlueprintAssignable, Category = "Abyssal Earth|Power")
    FAbyssalPowerChangedSignature OnPowerChanged;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Power")
    EAbyssalPowerNodeType NodeType = EAbyssalPowerNodeType::Source;

    /** Nodes this node propagates power to when its level changes. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Power")
    TArray<TObjectPtr<AAbyssalPowerNode>> ConnectedNodes;

    /** Also propagate to any AAbyssalInterfaceTerminal actors listed here. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Power")
    TArray<TObjectPtr<class AAbyssalInterfaceTerminal>> ConnectedTerminals;

    /** Power output when this Source is active (0..1). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Power",
        meta=(ClampMin="0.0", ClampMax="1.0", EditCondition="NodeType == EAbyssalPowerNodeType::Source"))
    float SourceOutput = 1.0f;

    /** Power lost per relay hop (0 = lossless). */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Power",
        meta=(ClampMin="0.0", ClampMax="1.0", EditCondition="NodeType == EAbyssalPowerNodeType::Relay"))
    float RelayLoss = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Abyssal Earth|Power")
    FText NodeLabel = NSLOCTEXT("AbyssalEarth", "PowerNodeDefaultLabel", "Power Node");

protected:
    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Power")
    void BP_OnPowerChanged(float NewPower);

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Power")
    void BP_OnActivated();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Power")
    void BP_OnDeactivated();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Power")
    void BP_OnFocusBegin();

    UFUNCTION(BlueprintImplementableEvent, Category = "Abyssal Earth|Power")
    void BP_OnFocusEnd();

private:
    void PropagatePower(float Power, int32 Depth);

    UPROPERTY()
    float CurrentPower = 0.0f;

    UPROPERTY()
    bool bIsActive = false;

    // Visited guard to prevent infinite loops in cyclic graphs
    bool bPropagating = false;
};
