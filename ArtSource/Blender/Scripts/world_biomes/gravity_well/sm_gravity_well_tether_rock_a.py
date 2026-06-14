"""
SM_GravityWell_TetherRock_A — AbyssalEarth procedural mesh.
Concept: GW-003, GW-004

A floating basalt shard (~4m across) with an iron tether ring and chain cable stub.
The tether rocks are the core traversal mechanic in the Gravity Well approach corridor —
basalt shards torn from the cave walls and held in place by chains bolted to anchor
points. Players fire their tether at the iron ring on the rock face to swing across gaps.

Run standalone:  blender --background --python <this_file>.py
"""
import sys, os, math, random
import bpy, bmesh
from mathutils import Matrix, Vector

_HERE         = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, TAU, PI)

EXPORT_DIR = get_export_dir('GravityWell')

ROCK_R       = 2.2     # bounding sphere radius of the main shard
ROCK_FLAT    = 0.55    # vertical flatten factor (shard is more disc-like than sphere)
RING_R       = 0.22    # tether ring outer radius
RING_TUBE    = 0.04    # ring tube cross-section radius
RING_BOSS_R  = 0.28    # mounting boss disc radius (the plate welded to rock face)
RING_BOSS_H  = 0.08    # boss disc height
CHAIN_LINKS  = 6       # number of chain links in the hanging stub
CHAIN_LINK_L = 0.24    # each chain link length
CHAIN_LINK_W = 0.08    # chain link width


def build():
    rng = random.Random(42)
    obj, bm = new_mesh("SM_GravityWell_TetherRock_A")

    # 1. Rock body — deformed icosphere
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=ROCK_R,
                                        matrix=Matrix.Identity(4))
    for v in result['verts']:
        # Random XY noise
        v.co.x += rng.uniform(-0.2 * ROCK_R, 0.2 * ROCK_R)
        v.co.y += rng.uniform(-0.2 * ROCK_R, 0.2 * ROCK_R)
        # Flatten bottom face: z < -0.3 → extra flatten
        if v.co.z < -0.3:
            v.co.z *= 0.4 * ROCK_FLAT
        else:
            v.co.z *= ROCK_FLAT

    # 2. Tether mounting boss — flat disc on the +X face
    boss_x = ROCK_R * 0.85
    boss_mat = Matrix.Translation(Vector((boss_x, 0.0, 0.3)))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
                          radius1=RING_BOSS_R, radius2=RING_BOSS_R,
                          depth=RING_BOSS_H, matrix=boss_mat)

    # 3. Tether ring — lofted torus on top of the boss
    ring_ox = boss_x
    ring_oy = 0.0
    ring_oz = 0.3 + RING_BOSS_H
    N_MAIN = 16
    N_TUBE = 8
    rings = []
    for i in range(N_MAIN):
        a = i * TAU / N_MAIN
        cx = ring_ox + math.cos(a) * RING_R
        cy = ring_oy + math.sin(a) * RING_R
        ring_verts = []
        for j in range(N_TUBE):
            angle2 = j * TAU / N_TUBE
            tube_x = cx + math.cos(a) * math.cos(angle2) * RING_TUBE
            tube_y = cy + math.sin(a) * math.cos(angle2) * RING_TUBE
            tube_z = ring_oz + math.sin(angle2) * RING_TUBE
            ring_verts.append(bm.verts.new((tube_x, tube_y, tube_z)))
        rings.append(ring_verts)
    for i in range(N_MAIN):
        lo = rings[i]
        hi = rings[(i + 1) % N_MAIN]
        for j in range(N_TUBE):
            nj = (j + 1) % N_TUBE
            try:
                bm.faces.new([lo[j], lo[nj], hi[nj], hi[j]])
            except Exception:
                pass

    # 4. Chain link stub — 6 links hanging below the rock
    chain_base_z = -ROCK_R * 0.8
    N_MAIN_C = 12
    N_TUBE_C = 6
    for link_i in range(CHAIN_LINKS):
        link_z = chain_base_z - link_i * CHAIN_LINK_L
        link_x = rng.uniform(-0.02, 0.02)
        # Alternate links rotate 90 degrees around Z
        angle_offset = (PI / 2) if (link_i % 2 == 1) else 0.0
        link_rings = []
        for i in range(N_MAIN_C):
            a = i * TAU / N_MAIN_C + angle_offset
            cx = link_x + math.cos(a) * CHAIN_LINK_W
            cy = math.sin(a) * CHAIN_LINK_W
            ring_verts = []
            for j in range(N_TUBE_C):
                angle2 = j * TAU / N_TUBE_C
                # Tube direction perpendicular to the major ring
                tube_x = cx + math.cos(a) * math.cos(angle2) * 0.025
                tube_y = cy + math.sin(a) * math.cos(angle2) * 0.025
                tube_z = link_z + math.sin(angle2) * 0.025
                ring_verts.append(bm.verts.new((tube_x, tube_y, tube_z)))
            link_rings.append(ring_verts)
        for i in range(N_MAIN_C):
            lo = link_rings[i]
            hi = link_rings[(i + 1) % N_MAIN_C]
            for j in range(N_TUBE_C):
                nj = (j + 1) % N_TUBE_C
                try:
                    bm.faces.new([lo[j], lo[nj], hi[nj], hi[j]])
                except Exception:
                    pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_dark_basalt", "mat_ancient_machine_dark", "mat_amber_stabilizer"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_TetherRock_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_GravityWell_TetherRock_A")
