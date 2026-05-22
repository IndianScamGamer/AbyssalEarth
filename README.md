# Abyssal Earth

An Unreal Engine exploration adventure set inside planet Earth, where immense caverns contain impossible alien landscapes. The project prioritizes awe, atmosphere, traversal, discovery, and visual fidelity over combat.

## Current Direction

- Engine target: Unreal Engine 5.4+.
- Genre: first-person exploration adventure.
- Core fantasy: descend into Earth and discover beautiful, impossible subterranean worlds.
- First playable target: one polished vertical slice cavern with traversal, scan/discovery interactions, atmospheric sound, and a short objective path.

## Setup

The project targets Unreal Engine 5.4 or later. For a fresh Windows checkout:

1. Install Git LFS, then clone the repository and run `git lfs install` once for the Windows user account.
2. Open `AbyssalEarth.uproject` in Unreal Editor.
3. Let Unreal generate project files and compile the `AbyssalEarth` module when prompted.
4. Create Blueprint children from the C++ classes in `Source/AbyssalEarth`.
5. Follow `Docs/MILESTONES.md` for the first playable slice.

Do not commit generated Unreal folders such as `Binaries/`, `DerivedDataCache/`, `Intermediate/`, or `Saved/`. Binary Unreal assets such as `.uasset` and `.umap` files are configured for Git LFS.

## Project Structure

- `Docs/`: design, art direction, milestone plans, and hourly work logs.
- `Source/AbyssalEarth/`: UE C++ gameplay foundation.
- `Content/Design/`: in-editor design notes and data tables.
- `Content/ArtDirection/`: visual references and style notes.
- `Content/Maps/`: target location for playable maps.
- `Content/Blueprints/`: Blueprint children and interactables.
- `Content/Materials/`: master materials and material instances.
