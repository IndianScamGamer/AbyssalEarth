"""
SM_FossilSky_WhaleSkeleton_Wall_A — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
"""
import sys
import os
import math
import random
import bpy
import bmesh
from mathutils import Matrix, Vector

_HERE        = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, mat_color, extrude_region,
                           add_subdivision, TAU, PI)

EXPORT_DIR = get_export_dir('FossilSky')


def build():
    """Whale skeleton half-embedded in the cavern wall — 18m arcing spine
    with tapering vertebrae, sweeping rib cage open to the room, long-jawed
    skull, and one trailing flipper-bone fan. Mount flush against a wall;
    the back half reads as buried (FS-002 left wall)."""
    random.seed(710)
    obj, bm = new_mesh("SM_FossilSky_WhaleSkeleton_Wall_A")
    L = 18.0
    # spine: arc of vertebra discs diving toward the wall (+y) at both ends
    N_VERT = 22
    spine = []
    for i in range(N_VERT):
        t = i / (N_VERT - 1)
        x = -L / 2 + t * L
        z = 5.0 + math.sin(t * PI) * 3.2
        y = 0.55 - math.sin(t * PI) * 0.55      # ends sink into the wall
        r = 0.42 * (1.0 - abs(t - 0.35) * 0.9) + 0.12
        spine.append((x, y, z, r))
        # vertebra body
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
            radius1=r, radius2=r, depth=r * 1.1,
            matrix=Matrix.Translation((x, y, z))
            @ Matrix.Rotation(TAU / 4, 4, 'Y'))
        # dorsal process
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=5,
            radius1=r * 0.22, radius2=r * 0.22, depth=r * 1.8,
            matrix=Matrix.Translation((x, y, z + r * 1.2)))
    # rib cage: 9 ribs sweeping down-out from the forward spine
    for k in range(9):
        t = 0.18 + k * 0.055
        sx = -L / 2 + t * L
        sz = 5.0 + math.sin(t * PI) * 3.2
        sy = 0.55 - math.sin(t * PI) * 0.55
        rib_len = 4.2 * (1.0 - abs(k - 4) * 0.12)
        SEG = 9
        for s in range(SEG):
            st = s / (SEG - 1)
            # rib curls out (-y) and down, then tucks back in
            ry = sy - math.sin(st * PI * 0.85) * rib_len * 0.55
            rz = sz - st * rib_len
            rx = sx + math.sin(st * PI) * 0.3
            rr = 0.16 * (1 - st * 0.55)
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=rr,
                matrix=Matrix.Translation((rx, ry, rz)))
    # skull: long tapered jaw box + cranium dome at the front end
    skull_x = -L / 2 + 0.06 * L
    skull_z = 5.0 + math.sin(0.06 * PI) * 3.2
    cr = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.15,
        matrix=Matrix.Translation((skull_x, 0.3, skull_z)))
    for v in cr['verts']:
        v.co.y = 0.3 + (v.co.y - 0.3) * 0.6     # flatten against wall
    # upper + lower jaw beams
    for jz, jlen in [(skull_z - 0.25, 3.4), (skull_z - 0.75, 3.0)]:
        rings = []
        for s in range(6):
            st = s / 5
            jx = skull_x - 0.8 - st * jlen
            jr = 0.30 * (1 - st * 0.7)
            ring = [bm.verts.new((jx,
                                   0.3 + math.cos(i * TAU / 6) * jr * 0.5,
                                   jz + math.sin(i * TAU / 6) * jr))
                    for i in range(6)]
            rings.append(ring)
        for ri in range(len(rings) - 1):
            lo, hi = rings[ri], rings[ri + 1]
            for i in range(6):
                bm.faces.new([lo[i], lo[(i + 1) % 6],
                               hi[(i + 1) % 6], hi[i]])
    # flipper-bone fan trailing from below the cage
    fx = -L / 2 + 0.30 * L
    for k in range(4):
        fa = -0.9 - k * 0.22
        flen = 1.8 - k * 0.25
        v0 = bm.verts.new((fx, -1.6, 2.2))
        v1 = bm.verts.new((fx + math.cos(fa) * flen, -1.9,
                            2.2 + math.sin(fa) * flen))
        v2 = bm.verts.new((fx + math.cos(fa) * flen * 0.6, -1.7,
                            2.2 + math.sin(fa) * flen * 0.6 - 0.15))
        bm.faces.new([v0, v1, v2])
    # cyan vein beads tracing the spine arc
    for i in range(0, N_VERT, 2):
        x, y, z, r = spine[i]
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.06,
            matrix=Matrix.Translation((x, y - r * 0.8, z + r * 0.4)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein",
                        "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_WhaleSkeleton_Wall_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_FossilSky_WhaleSkeleton_Wall_A")
