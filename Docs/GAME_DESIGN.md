# Abyssal Earth - Game Design

## High Concept

The player begins as a human verification diver on the first major exploration expedition of Earth's abyssal plains. After a Helios robot-built descent elevator fails catastrophically, the player is stranded in impossible cavern systems deep inside Earth: luminous rifts, alien ecosystems, ancient machine structures, hostile climates, monsters, and technology that should not exist.

The game is about awe, survival, curiosity, and practical scientific discovery. The player is not conquering the underworld; they are trying to live long enough to understand alien technology, use it, build with it, and eventually create a rift back to the surface.

## Pillars

1. Beauty first: every major space should feel like a screenshot worth keeping.
2. Survival through exploration: tension comes from scale, monsters, navigation, alien climates, weather, and environmental hazards rather than shooter-first combat.
3. Discovery becomes technology: scanning, naming, sketching, mapping, and revisiting discoveries should unlock understanding, fabrication, and escape tools.
4. Human smallness: the player should feel competent but tiny against the cavern worlds.
5. Natural mystery: alien landscapes should still feel geologic, ancient, and physically grounded.
6. Story becomes environment: after the Luminous Rift reveal, normal storytelling stops and the player learns through survival, scanning, building, and environmental discovery.

## Core Loop

1. Enter a new cavern pocket.
2. Survey from a dramatic overlook.
3. Pick routes using light, sound, landmarks, scanner hints, and survival pressure.
4. Traverse hazards, alien terrain, monsters, and climate threats.
5. Discover organisms, minerals, structures, artifacts, or machine principles.
6. Scan, log, and test findings until they become practical knowledge.
7. Use discovered technology to build tools, open routes, survive hostile conditions, and move closer to creating a return rift.

## Player Fantasy

The player is a verification diver/explorer sent to inspect Helios robot construction in the abyssal plains. After the elevator crash, they become a stranded survivor. They carry a scanner, diving/exploration suit, deployable beacons, rugged digital tablet journal, and whatever alien technology they learn to repair or fabricate. Their strength is observation, persistence, experimentation, and careful route-finding.

## Initial Mechanics

- First-person movement with sprint, crouch, and mantle/climb hooks.
- Scanner pulse that highlights nearby discoveries, alien tech, route hints, and survival-relevant anomalies.
- Discovery log with entries for biomes, minerals, lifeforms, structures, alien tech, fabrication clues, and survival rules.
- Deployable navigation beacons with colored light.
- Environmental hazards: heat, toxic spores, unstable crystal growth, flooding, darkness, monsters, pressure, gravity anomalies, and alien climates.
- Later add-on: Abyssal Interface terminal, a diegetic LLM-powered ancient/alien interface for short cryptic hints, lore fragments, warnings, and fabrication guidance once the core game is mature.
- Alien tech fabrication arc: discoveries eventually let the player build devices and a return rift.
- Photo mode or observation mode as an early priority because visuals are central.

## Story Structure

Full details live in Docs/NARRATIVE_FOUNDATION.md.

Authored story exists only at the beginning:

1. Submarine alone on a flat, empty ocean.
2. Camera pushes into the submarine window.
3. Player stands inside wearing the diving/exploration suit.
4. Wall display reads FIRST MAJOR EXPLORATION EXPEDITION OF EARTH'S ABYSSAL PLAINS.
5. Player walks around the room while sunlight fades and sub lights activate.
6. Submarine docks with the Helios-built elevator shaft.
7. Player exits through a short passage with humanoid Helios robots.
8. Helios warns of unresolved anomalies but the player enters the elevator.
9. Calm descent, then catastrophic elevator failure.
10. Player wakes in the crushed elevator, pries open the doors, and sees the Luminous Rift.

Final authored player line before the real game begins:

Oh... shit.

After that, the objective changes to SURVIVE and normal story delivery ends.

## Main Objective Arc

1. Verify the AI Robot Fleet HELIOS's work.
2. SURVIVE.
3. DISCOVER WHAT THIS PLACE IS.
4. MAKE THE MACHINE ANSWER.
5. BUILD A WAY OUT.
6. OPEN THE RIFT.

The ending is the player-created rift back to the surface. End credits show still images of survival, public discovery, and future scientific progress rather than a long explanatory scene.

## Abyssal Interface

Full details live in Docs/ABYSSAL_INTERFACE_AI_SYSTEM.md.

Priority note: this is a later add-on, not an immediate production priority. Current work should focus on assets, maps, survival, discovery, fabrication, and playable game development.

The Abyssal Interface is an in-game LLM-powered system presented through ancient terminals, alien devices, or a mysterious interface presence. Unreal owns UI, input, world state, objectives, inventory, discoveries, scanned artifacts, and visuals. A backend/agent system generates short responses from relevant context.

It should feel:

- Eerie.
- Intelligent.
- Lore-aware.
- Ancient or alien.
- Useful but incomplete.
- Part of the world, not a normal chatbot.

It can provide:

- Cryptic hints.
- Lore fragments.
- Environmental warnings.
- Fabrication guidance.
- Possible quest/event trigger suggestions, always validated by Unreal.

It must not provide:

- Casual chatbot conversation.
- Long exposition dumps.
- Meta AI language.
- Exact solutions that remove exploration.
- Normal NPC-style companion banter.

## First Biome: The Luminous Rift

The Luminous Rift is anchored to the core concept reference at Content/ArtDirection/References/luminous_rift_core_reference.png.

A vast vertical cavern opens around an ancient machine complex buried inside Earth. Black basalt, blue crystals, suspended platforms, and monumental carved structures surround a radiant blue-white energy sphere. Warm gold beams connect the sphere to hexagonal collector panels, implying that the cavern is not only geologic but also part of an enormous dormant mechanism.

Initial post-crash route:

- Crushed Elevator: recover, pry doors open, step into the impossible cavern.
- First Overlook: see the Luminous Rift and understand the scale of the survival problem.
- Abyssal Approach: find a safe path through broken ledges and ancient machine spans.
- Crystal Galleries: discover scanner-reactive crystals and first alien tech principles.
- Collector Array: discover the central orb, hex collectors, and first alien-tech operating principles.
- Ancient Gate: learn the machine can be operated.
- Second Sky Overlook: realize the visible structure is only one layer of a much larger underworld.

Earlier marsh, fungus, and geothermal ideas are preserved as future biome candidates, but they should not define the first map's visual identity.

## Tone

Quiet wonder with moments of danger. More Subnautica, Journey, Outer Wilds, and Avatar bioluminescence than shooter or horror. Darkness should frame beauty rather than swallow it. Survival should matter, but the heart of the game is still discovery.

## World Roadmap

The first map proves the core loop, but Abyssal Earth should feel like a descent through multiple impossible layers. The broader world roadmap is documented in Docs/WORLD_ATLAS.md and supported by generated reference images under Content/ArtDirection/WorldMaps/.

### Map Sequence Intent

1. Luminous Rift: ancient machine + crystal abyss. Teaches the base game.
2. Glassroot Forest: living mineral ecosystem. Teaches biological scanning and softer route reading.
3. Inner Sea: underground ocean. Expands route scale, navigation, and beacon value.
4. Fossil Sky: deep-time fossil archive. Shifts awe upward and emphasizes scientific reconstruction.
5. Gravity Well: local physics anomaly. Introduces parkour-based descent, tethered floating rock traversal, altered gravity, and orientation risk. Feels unlike any other map — active kinetic movement through a zone that wants to pull you in.
6. Mantle Garden: geothermal edge. Pushes environmental hazards without turning the game into combat.

### Long-Term Mechanical Arc

- Luminous Rift: scanner, journal, beacons, alien tech discovery, first survival hazards, and later optional Abyssal Interface terminal.
- Glassroot Forest: scanner timing, biological responses, spore interference, living gates.
- Inner Sea: route marking over water, floating beacons/buoys, possible skiff traversal.
- Fossil Sky: scanner reconstruction, brittle walkways, fossil pattern matching.
- Gravity Well: parkour-based descent with tethered drifting rocks, reorientation volumes, tether anchors, chain-swing traversal, spatial route planning.
- Mantle Garden: heat management, timed safe windows, low-visibility steam, pressure vents.

### Discovery Philosophy

Discoveries should not be collectible trivia. Each discovery should do at least one of these:

- Explain how the map works.
- Reveal a safe route or hazard rule.
- Deepen the ancient-machine mystery.
- Show how human survey teams adapted before contact was lost.
- Give the journal a meaningful field-science tone.
- Unlock or foreshadow alien tech fabrication.
- Move the player closer to creating the return rift.
