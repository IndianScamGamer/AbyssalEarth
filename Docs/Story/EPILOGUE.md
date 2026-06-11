# AbyssalEarth — Epilogue & Ending Design

## The Ending Sequence

### Beat 1 — The Rift Opens (gameplay)
`AAbyssalRiftActor` completes its charge. The amber light of the chamber reaches full intensity. The two Confluence Watchers drift to the chamber edges — the only time in the game they react to anything. They are giving the player room. (No explanation. Players who notice will wonder forever; that's the point.)

### Beat 2 — The Threshold (player-controlled)
The rift is a vertical seam of surface-blue light — the first cold-spectrum light since the submarine. The player walks in under their own control. No cutscene takeover. `RIFT_ENTER_01` fires at the threshold:

> *"Whatever this place is — whatever you are — I'll be back. I have to be."*

### Beat 3 — Fade to white
The only hard cut in the game. Hold white for 3 seconds. Silence.

### Beat 4 — The Surface (epilogue scene)
Fade in: the ocean surface, dawn. The same establishing shot as PRO_001 — reversed. The expedition submarine on the horizon, search lights still running after all this time. The player character floats in the foreground in their battered suit. They turn — the camera follows — and look down at the water.

One narrative beat, the last line of the game:

> **EPILOGUE_01** — Player: *"Six thousand metres straight down... and a door."*

Cut to black. Title card. Credits.

### Beat 5 — Post-credits (sequel hook)
After credits: 10 seconds of black, then the HELIOS anomaly sensor readout from the prologue — except now it's *two* rhythmic pulses, slightly out of phase. The Confluence's idle signature... and an answer to it, from somewhere else. Hard cut. End.

*(Canon note per STORY_BIBLE: this does not show or name the third stratum. It is a sensor reading. Interpretation is the player's job.)*

---

## Ending Rules
- The player walks into the rift; the game never takes control during the final act.
- No NPC, terminal, or creature comments on the player leaving. The Confluence does not say goodbye. Indifference, maintained to the last frame.
- The epilogue contains exactly one line of dialogue. Resist all temptation to add more.
- Credits music: the biome ambient themes from all five acts, layered in sequence, resolving into the submarine interior hum from the first playable minute. The game ends on the sound it began with.

## Epilogue Beat Data
See `Content/Design/EpilogueNarrativeBeats.csv`:
- `EPILOGUE_01` — the final line (surface scene)
- `POSTCREDIT_01` — silent beat ID reserved for the sensor-readout scene trigger (no caption; drives the sequence via `UNarrativeSubsystem::OnBeatStarted` listeners)
