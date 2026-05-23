# Abyssal Earth

**Abyssal Earth** is an Unreal Engine 5 first-person exploration adventure set inside planet Earth, where immense subterranean caverns contain impossible alien landscapes, ancient buried megastructures, luminous crystals, and unknown physical systems.

The project prioritizes awe, atmosphere, traversal, discovery, and visual fidelity over combat. The player is not conquering the underworld. They are documenting it, navigating it, surviving it, and slowly understanding why Earth contains spaces that should not exist.

![Luminous Rift core reference](Content/ArtDirection/References/luminous_rift_core_reference.png)

## Current Focus

The first playable map is **The Luminous Rift**: a colossal vertical cavern built around the core reference image above.

The target composition is a dark subterranean rift where carved rock and ancient machine architecture frame a suspended blue-white energy sphere. Gold beam networks connect the orb to hexagonal collector panels. Blue crystals grow from black basalt and buried machinery. Suspended bridges, ledges, distant towers, hanging slabs, and a monumental gate wall sell the sense that the player is tiny inside an ancient system far larger than the visible map.

This reference is treated as the source of truth for the first map:

`Content/ArtDirection/References/luminous_rift_core_reference.png`

## Design Pillars

1. **Beauty first**: every major space should be screenshot-worthy.
2. **Exploration over combat**: tension comes from scale, terrain, darkness, unknown systems, and environmental hazards.
3. **Discovery has weight**: scanning, naming, mapping, journaling, and revisiting findings should matter.
4. **Human smallness**: the player is capable, but visibly tiny against the cavern worlds.
5. **Natural mystery**: alien spaces should still feel geologic, ancient, and physically grounded.

## First Playable Route

The current vertical slice route is:

1. **Descent Elevator**: a recent human survey platform forced into black basalt.
2. **First Overlook**: the initial concept-art reveal of the Luminous Rift.
3. **Abyssal Approach**: broken rock ledges and ancient bridge spans descending into the void.
4. **Crystal Galleries**: blue crystals growing through carved wall panels.
5. **Collector Array**: the central energy orb, gold beams, hex collectors, and radial hub.
6. **Ancient Gate**: a monumental wall with circular blue-lit mechanisms.
7. **Second Sky Overlook**: the final reveal into an even deeper lower cavern.

The goal is a 10-15 minute playable slice with first-person traversal, scan/discovery interactions, deployable beacons, objective progression, atmospheric sound, and a strong visual payoff.

## Core Gameplay

- First-person movement with sprint, crouch, and future climb/mantle hooks.
- Scanner pulse that identifies discoveries and route-relevant anomalies.
- Discovery journal with entries for geology, structures, anomalies, biology, and human-made objects.
- Deployable navigation beacons with persistent save/load support.
- Objective chain guiding the player through the first Luminous Rift route.
- Environmental hazard foundations, currently including an Ember Vent actor prototype for future hazard zones.
- Blueprint-ready UI hooks for scanner readouts, journal views, objective HUD, damage feedback, and discovery toasts.

## Current Technical Foundation

The C++ foundation lives under `Source/AbyssalEarth/`.

Implemented or scaffolded systems include:

- `AAbyssalExplorerCharacter`: first-person exploration pawn.
- `UScannerComponent`: scan targeting, line-of-sight filtering, discovery feedback hooks.
- `ADiscoveryActor`: placeable scan target with journal metadata and optional objective completion.
- `UDiscoverySubsystem`: discovery registration, category queries, save/load support, and new-discovery delegates.
- `UAbyssalJournalWidget`: UMG base class for the discovery journal.
- `UAbyssalScannerReadoutWidget`: UMG base class for scan feedback.
- `UObjectiveSubsystem`: route progression through the revised Luminous Rift objective chain.
- `AObjectiveTriggerActor`: map trigger volumes for objective completion.
- `ABeaconActor` and `UBeaconSubsystem`: persistent player navigation beacons.
- `AEmberVentHazard`: cyclical environmental hazard prototype.
- `UAbyssalGameplayLibrary`: Blueprint accessors for project subsystems.

## Asset Pipeline

The current asset plan is built for Claude Code + Blender MCP collaboration. Unreal Editor and Blender work is expected to happen primarily on the Windows side, while repo/docs/code support can happen from Linux/OpenClaw.

Key documents:

- `Docs/CORE_REFERENCE_LUMINOUS_RIFT.md`: detailed visual analysis of the first-map reference.
- `Docs/BLENDER_ASSET_PIPELINE.md`: asset-generation contract for Claude/Blender workers.
- `Docs/ART_DIRECTION.md`: visual target, palette, lighting, shape language, and what to avoid.
- `Docs/LUMINOUS_RIFT_BLOCKOUT.md`: route, scale, zones, placement checklist, and screenshot targets.
- `Docs/MATERIAL_SPECS.md`: master material targets and material instances.
- `Content/Design/LuminousRiftAssetManifest.csv`: prioritized asset manifest.
- `ArtSource/Blender/LuminousRift/ASSET_NOTES.md`: notes file for Blender-created assets.

Highest-priority asset families:

- Dark basalt foreground ledges, arches, walls, and overhangs.
- Ancient bridge/platform kit.
- Central orb frame, hub, beam emitters, and energy orb Blueprint proxy.
- Hex collector panels and broken cluster variants.
- Blue crystal clusters in small, medium, large, and hero sizes.
- Monumental ancient gate wall.
- Distant towers, hanging slabs, and lower-abyss silhouettes.
- Small human survey kit for scale.

## Setup

The project targets **Unreal Engine 5.4+**.

For a fresh Windows checkout:

1. Install Git LFS.
2. Clone the repository.
3. Run `git lfs install` once for the Windows user account.
4. Open `AbyssalEarth.uproject` in Unreal Editor.
5. Let Unreal generate project files and compile the `AbyssalEarth` module when prompted.
6. Create Blueprint children from the C++ classes in `Source/AbyssalEarth`.
7. Follow `Docs/MILESTONES.md` and `Docs/NEXT_TASKS.md` for the current vertical-slice priorities.

Do not commit generated Unreal folders such as:

- `Binaries/`
- `DerivedDataCache/`
- `Intermediate/`
- `Saved/`

Binary Unreal assets such as `.uasset` and `.umap` files are configured for Git LFS.

## Collaboration Workflow

Before starting work:

1. Run `git fetch --prune`.
2. Inspect `git status`.
3. Pull safely, preferably with `git pull --ff-only` when there are no local changes.

When finishing a coherent change:

1. Run the smallest useful verification available.
2. Commit with a focused message.
3. Push so the Windows/Unreal/Blender side can pull the update.

Never overwrite or revert unrelated work from the Windows side, Claude, or another contributor.

## Project Structure

- `Docs/`: design, art direction, technical plans, milestones, asset pipeline docs, and hourly logs.
- `Source/AbyssalEarth/`: Unreal C++ gameplay foundation.
- `Content/Design/`: CSV design data and asset manifests.
- `Content/ArtDirection/`: reference images and visual direction material.
- `Content/Maps/`: target location for playable maps.
- `Content/Blueprints/`: Blueprint children and interactables.
- `Content/Materials/`: master materials and material instances.
- `ArtSource/Blender/`: source files and notes for Blender-created assets.
- `Content/ArtSourceExports/`: interchange exports from Blender before Unreal import.

## Development Status

The project is early but active. The immediate push is to turn the Luminous Rift reference into a playable, editor-built vertical slice with a coherent custom asset kit. The current foundation is strong enough to support map blockout, Blueprint wiring, scanner/discovery flow, objective progression, beacons, and first-pass visual development.
