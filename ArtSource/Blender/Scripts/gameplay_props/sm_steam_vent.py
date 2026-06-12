"""
SM_SteamVent_A — AbyssalEarth procedural mesh.
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
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, mat_color, extrude_region,
                           add_subdivision, TAU, PI)

EXPORT_DIR = get_export_dir('Slice')

def build():
    print("Building SM_SteamVent_A …")
    obj, bm = new_mesh("SM_SteamVent_A")

    # ── outer octagonal grate ring ────────────────
    outer = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=8, radius=0.42)
    bmesh.ops.translate(bm, verts=outer['verts'], vec=Vector((0, 0, 0.04)))
    of = [f for f in bm.faces if f.calc_center_median().length < 0.43
          and abs(f.calc_center_median().z - 0.04) < 0.01]
    if of:
        extrude_region(bm, of, 0.04, Vector((0, 0, -1)))

    # ── 4×4 square grate openings ─────────────────
    for gx in range(-1, 2):
        for gy in range(-1, 2):
            if abs(gx) + abs(gy) > 2:
                continue
            cx, cy = gx * 0.20, gy * 0.20
            hw = 0.065
            gv = [bm.verts.new((cx+dx*hw, cy+dy*hw, 0.04))
                  for dx, dy in ((-1,-1),(1,-1),(1,1),(-1,1))]
            bm.faces.new(gv)
            extrude_region(bm, [bm.faces[-1]], 0.05, Vector((0, 0, -1)))

    # ── central pipe stub ─────────────────────────
    pipe = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                      segments=10, radius=0.09, depth=0.20)
    bmesh.ops.translate(bm, verts=pipe['verts'], vec=Vector((0, 0, -0.20)))

    # ── bolted flange lip ─────────────────────────
    flange = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                      segments=8, radius=0.14)
    bmesh.ops.translate(bm, verts=flange['verts'], vec=Vector((0, 0, 0.0)))
    ff = [f for f in bm.faces
          if all(abs(v.co.z) < 0.01 for v in f.verts)
          and f.calc_center_median().length < 0.15]
    if ff:
        extrude_region(bm, ff, 0.025)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_SteamVent_A")
    return obj


# ══════════════════════════════════════════════
#  7. MAGMA GEYSER
# ══════════════════════════════════════════════
# Rocky cone ~180cm tall, split fissures on sides that glow lava-orange.
# VFX handles the eruption column.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_SteamVent_A")
