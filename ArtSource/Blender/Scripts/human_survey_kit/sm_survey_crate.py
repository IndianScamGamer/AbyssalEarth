"""
SM_Human_SurveyCrate_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Human_SurveyCrate_A …")
    obj, bm = new_mesh("SM_Human_SurveyCrate_A")
    rng = random.Random(7)

    # ── main body ─────────────────────────────────
    box_from_corners(bm, (-0.45, -0.30, 0), (0.45, 0.30, 0.32))

    # ── corner edge reinforcements ─────────────────
    corners = [(-0.45,-0.30),(0.45,-0.30),(0.45,0.30),(-0.45,0.30)]
    for cx, cy in corners:
        for z_range in [(0.0, 0.05), (0.27, 0.32)]:
            z0, z1 = z_range
            brace_w = 0.06
            # horizontal brace
            bx = cx + (brace_w if cx < 0 else -brace_w)
            by = cy + (brace_w if cy < 0 else -brace_w)
            box_from_corners(bm, (min(cx, bx), min(cy, by), z0),
                                 (max(cx, bx), max(cy, by), z1))

    # ── lid lip ───────────────────────────────────
    box_from_corners(bm, (-0.44,-0.29, 0.30), (0.44, 0.29, 0.34))

    # ── 2 latch details ───────────────────────────
    for lx in (-0.15, 0.15):
        box_from_corners(bm, (lx - 0.04, -0.32, 0.15),
                              (lx + 0.04, -0.31, 0.22))
        latch_arm = [bm.verts.new((lx - 0.025, -0.31, 0.15)),
                     bm.verts.new((lx + 0.025, -0.31, 0.15)),
                     bm.verts.new((lx + 0.025, -0.34, 0.17)),
                     bm.verts.new((lx - 0.025, -0.34, 0.17))]
        try:
            bm.faces.new(latch_arm)
        except Exception:
            pass

    # ── carry handle ──────────────────────────────
    for hx in (-0.18, 0.18):
        box_from_corners(bm, (hx - 0.02, -0.02, 0.34),
                              (hx + 0.02,  0.02, 0.40))
    box_from_corners(bm, (-0.18, -0.02, 0.38), (0.18, 0.02, 0.41))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  3. PORTABLE LAMP
# ══════════════════════════════════════════════
# Cylindrical survey lantern. 20cm dia × 30cm tall.
# Warm amber glow ring, weighted base, side cable connector.
# Matches: AD-005 (Human Survey Lamp — Close-Up).

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Human_SurveyCrate_A")
