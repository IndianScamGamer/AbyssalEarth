# Editor Guide: BP_PlayerCharacter

Blueprint subclass of `AAbyssalPlayerCharacter`. All 9 gameplay components are created in C++ and auto-assigned — the Blueprint's job is camera setup, mesh binding, and wiring the death animation.

## 1. Create the Blueprint

1. Content Browser → `Content/Blueprints/` → **Blueprint Class**
2. Parent: **AbyssalPlayerCharacter**
3. Name: `BP_PlayerCharacter`

## 2. Camera Setup

In the **Components** panel:

1. Select **CapsuleComponent** (root)
2. Add child → **Spring Arm** (`USpringArmComponent`)
   - Target Arm Length: `300`
   - Enable Camera Lag: `true`, Camera Lag Speed: `8`
   - Socket Offset: `(0, 0, 60)` (eye height)
3. Attach **Camera** (`UCameraComponent`) to the spring arm
   - Field of View: `90`
   - No lag of its own — the spring arm handles it

## 3. Skeletal Mesh

1. Select the **Mesh** component (inherited from ACharacter)
2. Skeletal Mesh: `SK_Diver`
3. Animation Blueprint: `ABP_Diver`
4. Relative Location: `(0, 0, -88)`, Relative Rotation: `(0, -90, 0)` (standard UE character offset)

## 4. Collision

Capsule (inherited from ACharacter):
- Capsule Radius: `34`
- Capsule Half-Height: `88`

## 5. Configure Class Defaults

| Property | Value |
|---|---|
| Sea Level Z | `0.0` (adjust per map — positive = sea level is above origin) |
| Depth Scale | `0.01` (1 cm → 0.01 m) |
| Sprint Speed Multiplier | `1.6` |
| Respawn Delay | `2.0` (seconds after death before respawn) |

## 6. Wire BP_OnDeath

In the Event Graph:

```
Event BP_OnDeath
  → Play Anim Montage (Death_Montage)
  [The C++ timer handles calling RespawnAtCheckpoint after RespawnDelay seconds.
   No further Blueprint action needed for respawn.]
```

Optional — fade out camera before respawn:
```
Event BP_OnDeath
  → Play Anim Montage (Death_Montage)
  → Delay (1.8s)
  → Camera Fade (0→1, 0.2s, black)
```

## 7. Wire BP_OnRespawned

```
Event BP_OnRespawned
  → Camera Fade (1→0, 0.3s, black)
  → Play Anim Montage (Respawn_Montage) [optional]
```

## 8. Verify All Components

In **Details** panel → **Components**, confirm these are present (auto-created by C++ constructor):
- HealthComponent, OxygenComponent, StaminaComponent
- TemperatureComponent, PressureComponent
- InteractionComponent, ScanComponent
- TraversalComponent, ObservationComponent

None of these need Blueprint configuration — their defaults are set in C++ and tuned via UPROPERTY EditAnywhere fields.
