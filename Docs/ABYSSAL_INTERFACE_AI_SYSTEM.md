# Abyssal Interface AI System

## Goal

Abyssal Earth should include an in-game AI system that lets the player talk or text with an LLM through an ancient terminal, companion device, or mysterious alien machine presence called the Abyssal Interface.

The system must not feel like a normal chatbot. It should feel like part of the world: eerie, intelligent, context-aware, partial, and ancient. The player should wonder whether it is a machine, a translation layer, a surviving intelligence, a simulation, or the voice of the buried structure itself.

## Narrative Boundary

The game has no normal story delivery after the Luminous Rift reveal. The Abyssal Interface is not an exception in the usual NPC sense. It is a tool, artifact, and mystery. It should not behave like a friendly companion or mission-control assistant.

Allowed behavior:

- Short cryptic hints.
- Lore fragments grounded in scanned artifacts.
- Warnings about environmental conditions.
- Translations of alien terminal states.
- Possible quest/event triggers.
- Fabrication guidance after the player has discovered enough components.

Disallowed behavior:

- Long conversational roleplay.
- Casual chatbot tone.
- Meta references to being an AI model.
- Modern internet humor.
- Overexplaining the plot.
- Telling the player exactly what to do every time.
- Replacing exploration and observation.

## First Version

Build the first version as a simple text-based terminal in Unreal.

Player flow:

1. Player discovers an ancient terminal/interface node in the Luminous Rift.
2. Player activates it.
3. Terminal UI opens with a small text input and response panel.
4. Unreal sends a compact context payload to a backend/agent system.
5. Backend returns a short in-world response.
6. Unreal displays the response diegetically on the terminal.

First version should be text only. Voice, TTS, embodied companions, and AI director behavior come later.

## System Architecture

### Unreal Responsibilities

Unreal owns:

- Terminal UI.
- Player input.
- World state collection.
- Current map/location.
- Current objective.
- Inventory/resources.
- Discovered lore/artifacts.
- Scanned objects.
- Recent player actions.
- Quest/event trigger validation.
- Visual and audio presentation.
- Rate limiting and safety around gameplay effects.

Unreal should never blindly execute arbitrary LLM instructions. It should parse only a constrained response schema.

### Backend/Agent Responsibilities

Backend/agent system owns:

- LLM response generation.
- Tone/persona of the Abyssal Interface.
- Context summarization.
- Lore-aware hint phrasing.
- Optional candidate event suggestions.
- Refusal or uncertainty when context is insufficient.

The backend can be Shinrou or another local/remote agent service, but the interface contract should remain stable so the model can change without rewriting Unreal UI.

## Context Payload

Unreal should send only relevant compact context. Avoid dumping full logs.

Suggested request shape:

```json
{
  "sessionId": "run-local-guid",
  "playerInput": "What is this machine doing?",
  "mapId": "MAP_LuminousRift",
  "zoneId": "CollectorArray",
  "currentObjective": "MAKE_THE_MACHINE_ANSWER",
  "playerState": {
    "health": 72,
    "suitIntegrity": 81,
    "oxygenOrPower": 64,
    "hazardsNearby": ["unstable_energy_pulse"]
  },
  "inventory": ["scanner", "beacon_pack", "crystal_resonator_fragment"],
  "discoveries": [
    "D_Anomaly_RiftEnergyOrb",
    "D_Structure_HexCollector",
    "D_Geo_BlueRiftCrystal"
  ],
  "recentScans": [
    { "id": "D_Structure_HexCollector", "ageSeconds": 18 },
    { "id": "D_Anomaly_RiftEnergyOrb", "ageSeconds": 44 }
  ],
  "recentActions": [
    "placed_beacon_at_collector_platform",
    "rerouted_power_node_A_to_node_C"
  ],
  "knownLoreFacts": [
    "Hex collectors receive gold beam energy from the central hub.",
    "Blue crystals resonate when the scanner pulses."
  ],
  "allowedResponseModes": ["dialogue", "hint", "lore", "warning", "eventSuggestion"]
}
```

## Response Schema

The backend should return constrained JSON so Unreal can safely render and optionally act.

Suggested response shape:

```json
{
  "mode": "hint",
  "speaker": "Abyssal Interface",
  "text": "The ring does not open. It remembers alignment. Feed the blue lattice before waking the gold path.",
  "confidence": 0.72,
  "suggestedEvents": [
    {
      "eventId": "EVT_MARK_BLUE_LATTICE_NODE",
      "type": "soft_hint_marker",
      "requiresUnrealValidation": true
    }
  ],
  "memoryTags": ["collector_array", "blue_lattice", "gold_path"]
}
```

Rules:

- `text` should usually be 1-4 short sentences.
- `suggestedEvents` are suggestions only; Unreal validates and decides.
- No arbitrary code, commands, file paths, or engine calls in model output.
- If unsure, the Interface should speak with uncertainty instead of inventing facts.

## Voice And Tone

The Abyssal Interface should sound:

- Ancient but not medieval.
- Intelligent but incomplete.
- Eerie but useful.
- Alien but understandable.
- Calm under danger.
- More like a buried machine-consciousness than a person.

Example response styles:

- `Your suit asks for air. The chamber answers with pressure. Leave before the stone exhales again.`
- `The blue lattice is not decoration. It is memory under compression.`
- `You carry three fragments of a tool and call them debris.`
- `Helios touched the door. It did not understand the lock.`
- `A path exists, but not for your weight. Wake the anchors first.`

Avoid:

- `Hi! How can I help you today?`
- `As an AI language model...`
- `Quest updated: go to the blue marker!`
- Long encyclopedia answers.

## Gameplay Uses

### Cryptic Hints

The player asks for help and receives a clue that still requires observation.

Example:

Player: `How do I cross this?`

Interface: `The bridge is missing only in stone. The gold line still knows the shape.`

### Lore Explanations

The player asks about a scanned artifact. The Interface explains only what the player has earned through discoveries.

Example:

Player: `What are the hex panels?`

Interface: `Collectors. Petals for a star that was never meant to burn. Broken, but not dead.`

### Environmental Warnings

The player is near danger.

Example:

`Pressure is collecting beneath you. Three breaths, then the vent opens.`

### Fabrication Guidance

The player has enough discoveries/components to craft something.

Example:

`The fragment is not a key. It is a tooth. Build the jaw around it.`

### Quest/Event Suggestions

The model can suggest possible triggers, but Unreal must validate.

Examples:

- Reveal a hint marker.
- Unlock a terminal translation.
- Suggest a new fabrication recipe.
- Trigger a scanner resonance event.
- Add a journal annotation.

## Progression

### Version 0 - Static Terminal

- Hand-authored terminal UI.
- Backend request with current zone/objective/discoveries.
- Short text response.
- No event triggers.
- No voice.

### Version 1 - Context-Aware Terminal

- Sends inventory, discoveries, recent scans, and recent actions.
- Returns hint/lore/warning modes.
- Can suggest journal annotations.

### Version 2 - Fabrication And Quest Hints

- Interface can suggest tech recipes after discovery prerequisites.
- Unreal validates component requirements.
- Interface can hint toward alien tech construction.

### Version 3 - Voice And Diegetic Audio

- TTS for terminal or suit audio.
- Voice should be low, processed, eerie, and restrained.
- Text remains available for accessibility.

### Version 4 - AI Companion Or Device

- A portable shard/device lets the player access the Interface outside terminals.
- The system remains sparse; it does not chatter.

### Version 5 - AI Director

- The backend can help choose atmospheric events, hints, or environmental pressure based on player state.
- Unreal still validates and executes all gameplay changes.

## Backend Endpoint Sketch

Initial local endpoint:

- `POST /abyssal-interface/respond`

Request:

- JSON context payload from Unreal.

Response:

- JSON response schema with mode, text, confidence, suggested events, and memory tags.

Timeout:

- Target 2-5 seconds for terminal responses.
- If backend times out, terminal should show a diegetic failure such as `signal incomplete`.

Privacy/security:

- Send only game state.
- Do not send player personal data.
- Do not allow model output to execute code.
- Log enough for debugging but avoid giant transcripts.

## Unreal Implementation Notes

Suggested classes/Blueprints:

- `UAbyssalInterfaceComponent`: attach to terminal actors, gathers local context and opens UI.
- `AAbyssalInterfaceTerminal`: interactable world actor.
- `UAbyssalInterfaceSubsystem`: tracks conversation/session state and request throttling.
- `WBP_AbyssalInterfaceTerminal`: text input and response display.
- `FAbyssalInterfaceContext`: serializable request context struct.
- `FAbyssalInterfaceResponse`: constrained response struct.
- `BP_AbyssalInterfaceTerminal`: Blueprint child for placement and visuals.

Initial implementation can be Blueprint-heavy if C++ HTTP plumbing is deferred. The docs should still preserve the schema so the backend and Unreal sides agree.

## Failure States

Failure should feel in-world:

- `signal incomplete`
- `translation failed`
- `the lattice refuses the query`
- `context insufficient`
- `interface dormant`

Do not show raw HTTP errors to the player.

## Relationship To Shinrou

Shinrou or a similar backend agent can power responses, but the in-game fiction should never call the Interface `Shinrou`. Shinrou is the development/helper identity; the Abyssal Interface is the world object.

## Design Constraint

The Interface should make the world feel deeper, not smaller. If it explains too much, talks too casually, or solves the game for the player, it weakens Abyssal Earth.
