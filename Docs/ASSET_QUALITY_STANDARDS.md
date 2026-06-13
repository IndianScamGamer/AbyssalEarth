# Asset Quality Standards

The single governing rule: **every Blender asset script must produce geometry that matches the
corresponding concept art image well enough that an observer who sees both can recognize the
connection immediately.** Concept images are the ground truth. When a written spec and the
concept image disagree, the image wins.

---

## Visual Approval Gate

Assets are not "done" after they pass CI. They are done when:

1. CI passes (all 16 checks green, render artifacts uploaded)
2. A `*_vs_concept.png` composite has been reviewed
3. The user has given explicit go/no-go on that asset

The loop does not advance to the next batch until every asset in the current batch has user
approval. Re-iteration rounds are normal and expected; they stop when approval is given.

---

## Scale Reference Table

All dimensions are in **Blender metres** (1 Blender metre = 1 Unreal centimetre after
`global_scale=100.0` FBX export).

| Asset family | Width / span | Height / depth | Notes |
|---|---|---|---|
| Player reference | — | 1.8 m | Human scale marker |
| Player path width | 3–8 m | — | Minimum clearance |
| Small prop | 0.2–1.5 m | — | Beacons, crystals S, survey items |
| Crystal S | 0.5–1.5 m tall | — | |
| Crystal M | 2–4 m tall | — | |
| Crystal L | 5–9 m tall | — | |
| Crystal Hero | 10–18 m tall | — | |
| Bridge span | 8–16 m wide | — | 20–80 m long |
| Platform node | 6–12 m | — | Circular traversal disc |
| Hex collector tile | 4–7 m (face-to-face) | — | |
| Hex collector cluster | 20–35 m span | — | 3–7 tiles grouped |
| Ancient gate/wall | 40–60 m wide | 80–140 m tall | |
| Central orb | 18–28 m diameter | — | Sphere only |
| Orb apparatus (full) | 80–140 m span | — | Ring + arms + orb |
| Tower segment | 6–14 m | 25–50 m | Modular, stackable |
| Hanging slab | 10–30 m | 3–8 m thick | Ceiling-mounted |
| Root column hero | 6–10 m diameter | 50–80 m | Glassroot Forest |
| Buttress root spread | 10–18 m radius | — | From trunk base |
| Submerged ruin tower | 4–8 m | 20–40 m | Inner Sea, half-submerged |
| Fossil whale | 80–130 m long | — | Fossil Sky ceiling |
| Portal/gate arch | 20–35 m opening | 35–50 m tall | Gravity Well |
| Mineral flower cluster | 1–3 m | 0.5–3 m tall | Mantle Garden |

---

## Per-Biome Silhouette Language

### Luminous Rift
- **Shape vocabulary**: circles, rings, radial symmetry, hexagons, rectilinear plates
- **Key reads**: the orb is the brightest point; gold beams are thin warm lines; hex panels read
  as flat facets; the cavern frame is jagged, wet, dark
- **Avoid**: ovoid blobs, cubes without machine detail, generic cave rocks

### Glassroot Forest
- **Shape vocabulary**: massive organic columns with sweeping buttress roots; oval canopy
  clusters; shallow pool terraces; red sap lines running up trunks
- **Key reads**: columns must be dramatically wider at base (buttress flare is the hero shape);
  translucent/pale green surface; red veins are visible line details
- **Avoid**: uniform-width tubes, sharp edges, mechanical detail

### Inner Sea
- **Shape vocabulary**: flat water plane (implied by script placement), stone dock edges,
  pier pilings, ruined tower columns with gothic arches, broken masonry
- **Key reads**: ruins are ancient stone, not machine; gold plankton trails are the navigational
  accent; low horizontal composition
- **Avoid**: angular sci-fi shapes, machine panels on ruins

### Fossil Sky
- **Shape vocabulary**: elongated skeletal arcs (ribs), flattened cranium, tapered tail, bone
  surfaces with irregular texture; ceiling-dominant composition
- **Key reads**: fossils must read as actual anatomical bones (tube limbs, arced ribs, skull with
  rostrum), not abstract blobs; bone-white with amber warmth and cyan vein highlights
- **Avoid**: overlapping icosphere chains (they merge into undifferentiated blobs), smooth orbs

### Gravity Well
- **Shape vocabulary**: massive rectangular archway pillars, amber rune-light panels at equal
  vertical intervals; severe verticals; floating irregular basalt chunks
- **Key reads**: the gate arch is the dominant shape — two pillars + lintel, not a round ring;
  amber glow is the colour accent against dark basalt
- **Avoid**: tube-ring geometry for the gate, circular profile, blue as primary accent

### Mantle Garden
- **Shape vocabulary**: sharp pointed crystal spires (hexagonal or octahedral), very narrow
  aspect ratio (height/width ≥ 15:1 at tip), irregular outward tilts; dark cracked obsidian base
- **Key reads**: spires must be pointy and faceted, not rounded; magenta is punchy against
  black obsidian; steam columns are large vertical blobs (implied by material/VFX, not mesh)
- **Avoid**: fat hex prisms with blunt tops, uniform height, symmetric arrangement

---

## Geometry Anti-Patterns (CI checks + human review)

| Anti-pattern | CI check | Why it fails |
|---|---|---|
| `bm.verts.new(...)` with no connected faces | Check 14 (warning) | Invisible floating point cloud |
| `bmesh.ops.create_icosphere()` in a loop with no join | Check 14 (heuristic) | Overlapping blobs don't auto-merge; become undifferentiated mass |
| No module-level UPPER_CASE scale constants | Check 15 (warning) | Scale can't be audited or adjusted without hunting magic numbers |
| Missing `Concept: IMAGE-ID` in docstring | Check 13 (warning→error) | Breaks render harness auto-match; breaks visual audit trail |
| `bpy.ops.render.render()` in asset script | Check 16 (error) | Must use `Tools/render_asset_preview.py` instead |
| Setting vertex coords to 0 to "erase" geometry | Human review | Collapses all faces to origin; destroys mesh; creates degenerate faces |
| Razor-thin planes (0 thickness) | Human review | Z-fighting in UE5 renderer |
| Applied transforms not reset | Human review | Origin drift; breaks UE5 placement |

---

## UE5 Handoff Checklist (per asset)

Complete before marking an asset `Exported` in the import checklist CSV:

- [ ] `finalise()` called → mesh has correct normals and no loose geometry
- [ ] `smart_uv()` called → UV0 island packing is reasonable (check in UV editor)
- [ ] `set_origin_to_base()` called → pivot at base Z-minimum
- [ ] All transforms applied (no scale/rotation on the object)
- [ ] Material slots match the canonical `mat_*` names from `shared/utils.py` palette
- [ ] FBX exported to `Content/ArtSourceExports/<Category>/SM_<Name>.fbx`
- [ ] Asset notes entry created or updated in `ArtSource/Blender/LuminousRift/ASSET_NOTES.md`
- [ ] Vertex count is within reason (env assets: <500K; props: <100K; hero landmarks: <1M)

### Nanite decision
| Use Nanite | Do NOT use Nanite |
|---|---|
| Basalt walls, ledges, gate walls, tower segments, bridge slabs, machine frames, collector frames | Transparent/glass panes, energy orb, VFX card meshes, crystal clusters (use LOD instead) |

### Collision standard
| Asset type | Collision method |
|---|---|
| Player-walkable ledge / bridge | Simple UCX convex box(es) |
| Large decorative cliff | No collision, or blocking volume in UE5 |
| Interactive props | Simple convex |
| Gate / wall | Blocking volume in UE5 (not per-poly) |
| Crystals near route | No collision or simple convex if blocking path |

---

## CI Validation Checks Reference

| Check | Severity | Description |
|---|---|---|
| 1 | ERROR | Valid Python syntax |
| 2 | ERROR | `build()` function defined |
| 3 | ERROR | `new_mesh()` called with `SM_`-prefixed name |
| 4 | ERROR | `export_fbx()` called with matching filename |
| 5 | ERROR | All `add_mat_slots()` material names in canonical palette |
| 6 | ERROR | Imports from `shared.utils` (waived for STANDALONE) |
| 7 | ERROR | `_SCRIPTS_ROOT` path depth matches file depth |
| 8 | ERROR | `finalise()`, `smart_uv()`, `set_origin_to_base()` called |
| 9 | ERROR | All `sm_*.py` siblings imported in `run_all.py` |
| 10 | ERROR | `SM_` asset names globally unique across all scripts |
| 11 | ERROR | All category folders covered by root `run_all_assets.py` |
| 12 | ERROR | `shared/utils.py` palette is superset of all used materials |
| 13 | WARNING | `Concept: IMAGE-ID` line present in docstring |
| 14 | WARNING | No blatant floating-vert anti-pattern detected |
| 15 | WARNING | At least one module-level UPPER_CASE scale constant present |
| 16 | ERROR | Script does not call `bpy.ops.render.render()` directly |
