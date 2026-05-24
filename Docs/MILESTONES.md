# Milestones

## Milestone 0 - Project Foundation

Status: in progress.

- Create UE project skeleton.
- Define game vision, story premise, first biome, and world atlas.
- Add C++ foundation classes.
- Add config for Enhanced Input and default maps.
- Create hourly continuation workflow.
- Establish Git fetch-before-work and push-after-completion workflow.

## Milestone 1 - Prologue And Crash

Goal: playable opening sequence from submarine to Luminous Rift reveal.

Deliverables:

- Ocean-surface establishing shot or placeholder cinematic.
- Submarine room where the player can walk and inspect the expedition briefing.
- Briefing display with the headline FIRST MAJOR EXPLORATION EXPEDITION OF EARTH'S ABYSSAL PLAINS.
- Docking sequence into the Helios-built elevator shaft.
- Short Helios robot passage with final normal text-bubble/dialogue interaction.
- Elevator descent with calm period, warning failure, cable cut, fall, and blackout.
- Crushed elevator wakeup and door-pry interaction.
- Luminous Rift reveal and objective change to SURVIVE.
- No normal story/dialogue after the reveal.

## Milestone 2 - First Playable Traversal Slice

Goal: playable first-person exploration loop in a blockout Luminous Rift map matching the core concept reference.

Deliverables:

- Player can move, sprint, crouch, and look around.
- Scanner pulse highlights placeholder discoveries.
- Three or more scan discoveries can be logged.
- Beacon actor can be placed as a navigation marker.
- Objective chain guides player from crash survival into alien-tech discovery.
- Map has readable landmark composition even with placeholder meshes: first overlook, abyssal approach, crystal galleries, collector array, ancient gate, and second sky overlook.

## Milestone 3 - Abyssal Interface V0

Goal: first text-based LLM-backed ancient terminal.

Deliverables:

- `WBP_AbyssalInterfaceTerminal` or Blueprint equivalent.
- Interactable terminal actor placed in the Luminous Rift.
- Context payload includes location, objective, inventory, discoveries, recent scans, and recent actions.
- Backend/agent endpoint returns constrained JSON response.
- Unreal displays short diegetic response text.
- Failure states are in-world, not raw network errors.
- LLM-suggested events are ignored or validated; never blindly executed.

## Milestone 4 - Beauty Pass 1

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

## Milestone 5 - Discovery, Fabrication, And Survival Systems

Goal: exploration starts to become practical survival progress.

Deliverables:

- Discovery data assets or data table.
- Journal UI shell.
- Scanning categories: geology, biology, anomaly, human-made, structure, alien tech.
- Audio/visual feedback for new vs repeated scans.
- Save/load for discovered entries.
- First alien-tech fabrication prototype.
- First survival pressure prototype beyond navigation: health, suit integrity, environmental hazard, or monster avoidance.

## Milestone 6 - Vertical Slice

Goal: 10-15 minute playable cavern experience.

Deliverables:

- Prologue-to-crash opening.
- Complete route through Abyssal Approach, Crystal Galleries, Collector Array, Ancient Gate, and Second Sky Overlook.
- Abyssal Interface V0 terminal.
- Environmental hazard prototype.
- Discovery-to-technology progression hook.
- Finished soundscape pass.
- Polished start and end beats.
- Packaged build if Unreal is installed.

## Long-Term Ending Target

Goal: complete game arc.

Deliverables:

- Player learns alien technology across multiple maps.
- Player fabricates increasingly advanced devices.
- Player creates a rift/portal back to the surface.
- End credits show survival, public announcement of discoveries, and future scientific progress.
