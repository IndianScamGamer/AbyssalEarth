# Milestones

## Milestone 0 - Project Foundation

Status: in progress.

- Create UE project skeleton.
- Define game vision and first biome.
- Add C++ foundation classes.
- Add config for Enhanced Input and default maps.
- Create hourly continuation workflow.

## Milestone 1 - First Playable Traversal Slice

Goal: playable first-person exploration loop in a blockout Luminous Rift map matching the core concept reference.

Deliverables:

- Player can move, sprint, crouch, and look around.
- Scanner pulse highlights placeholder discoveries.
- Three scan discoveries can be logged.
- Beacon actor can be placed as a navigation marker.
- Basic objective chain guides player from elevator start to overlook end. C++ subsystem and trigger actor foundation are in place; Blueprint HUD and map trigger placement remain.
- Map has readable landmark composition even with placeholder meshes: first overlook, abyssal approach, crystal galleries, collector array, ancient gate, and second sky overlook.

## Milestone 2 - Beauty Pass 1

Goal: make the first cavern visually compelling even before custom art.

Deliverables:

- Lumen lighting setup with cyan/amber contrast.
- Volumetric fog and mist layers.
- Central blue-white orb light source.
- Warm gold beam network with hex collector panels.
- Emissive blue crystal material prototypes.
- Ancient dark machine material prototypes.
- Cinematic overlook composition matching `Content/ArtDirection/References/luminous_rift_core_reference.png`.
- Screenshot pass at desktop resolution.

## Milestone 3 - Discovery Systems

Goal: exploration starts to feel meaningful.

Deliverables:

- Discovery data assets or data table.
- Journal UI shell.
- Scanning categories: geology, biology, anomaly, human-made.
- Audio/visual feedback for new vs repeated scans.
- Save/load for discovered entries.

## Milestone 4 - Vertical Slice

Goal: 10-15 minute playable cavern experience.

Deliverables:

- Complete route through Abyssal Approach, Crystal Galleries, Collector Array, Ancient Gate, and Second Sky Overlook.
- Environmental hazard prototype.
- Finished soundscape pass.
- Polished start and end beats.
- Packaged build if Unreal is installed.
