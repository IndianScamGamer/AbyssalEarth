"""
SM_Human_FieldConsole_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Human_FieldConsole_A …")
    obj, bm = new_mesh("SM_Human_FieldConsole_A")

    # ── main chassis ──────────────────────────────
    box_from_corners(bm, (-0.70, -0.38, 0.68), (0.70, 0.38, 1.05))

    # ── angled keyboard tray ──────────────────────
    kbd_pts = [
        bm.verts.new((-0.65, -0.36, 0.68)),
        bm.verts.new(( 0.65, -0.36, 0.68)),
        bm.verts.new(( 0.65, -0.36, 0.72)),
        bm.verts.new((-0.65, -0.36, 0.72)),
        bm.verts.new((-0.65, 0.05, 0.84)),
        bm.verts.new(( 0.65, 0.05, 0.84)),
        bm.verts.new(( 0.65, 0.05, 0.88)),
        bm.verts.new((-0.65, 0.05, 0.88)),
    ]
    for fi in [(0,1,2,3),(4,5,6,7),(0,4,7,3),(1,5,4,0),(2,6,5,1),(3,7,6,2)]:
        try:
            bm.faces.new([kbd_pts[i] for i in fi])
        except Exception:
            pass

    # ── raised screen panel ───────────────────────
    box_from_corners(bm, (-0.62, 0.08, 0.88), (0.62, 0.10, 1.46))
    # screen face
    box_from_corners(bm, (-0.56, 0.09, 0.92), (0.56, 0.11, 1.42))

    # ── status LED strip ──────────────────────────
    box_from_corners(bm, (-0.60, -0.39, 0.70), (0.60, -0.38, 0.72))

    # ── 4 folding legs ────────────────────────────
    for lx, ly in [(-0.55, -0.30), (0.55, -0.30),
                   (0.55,  0.30),  (-0.55, 0.30)]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius=0.025, depth=0.68,
                                   matrix=Matrix.Translation(Vector((lx, ly, 0.34))))

    # ── rubber foot pads ──────────────────────────
    for lx, ly in [(-0.55,-0.30),(0.55,-0.30),(0.55,0.30),(-0.55,0.30)]:
        box_from_corners(bm, (lx-0.04, ly-0.04, 0), (lx+0.04, ly+0.04, 0.04))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  6. TEMPORARY RAILING
# ══════════════════════════════════════════════
# 3m modular safety railing segment. Two horizontal rails,
# vertical balusters every 60cm, end snap-connectors.
# Snaps end-to-end for arbitrary path lengths.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Human_FieldConsole_A")
