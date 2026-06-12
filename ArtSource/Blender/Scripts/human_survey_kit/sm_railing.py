"""
SM_Human_TemporaryRailing_A — AbyssalEarth procedural mesh.
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


def box_from_corners(bm, min_pt, max_pt):
    x0,y0,z0 = min_pt
    x1,y1,z1 = max_pt
    verts = [
        bm.verts.new((x0,y0,z0)), bm.verts.new((x1,y0,z0)),
        bm.verts.new((x1,y1,z0)), bm.verts.new((x0,y1,z0)),
        bm.verts.new((x0,y0,z1)), bm.verts.new((x1,y0,z1)),
        bm.verts.new((x1,y1,z1)), bm.verts.new((x0,y1,z1)),
    ]
    faces = [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    for f in faces:
        try:
            bm.faces.new([verts[i] for i in f])
        except Exception:
            pass
    return verts


# ══════════════════════════════════════════════
#  1. SURVEY PLATFORM
# ══════════════════════════════════════════════
# 10×10m modular elevated platform. Grid of square deck panels,
# perimeter safety rail channel, 4 support legs with cross-braces.
# Matches: expedition atmosphere of HE-001 through HE-005.

def build():
    print("Building SM_Human_TemporaryRailing_A …")
    obj, bm = new_mesh("SM_Human_TemporaryRailing_A")

    length = 3.0
    height = 1.05
    post_r = 0.022

    # ── 2 end posts ────────────────────────────────
    for px in (0, length):
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius=post_r*1.4, depth=height,
                                   matrix=Matrix.Translation(Vector((px, 0, height/2))))
        # snap connector
        box_from_corners(bm, (px-0.04, -0.03, -0.04), (px+0.04, 0.03, 0.04))
        box_from_corners(bm, (px-0.04, -0.03, height-0.04), (px+0.04, 0.03, height+0.04))

    # ── 4 intermediate balusters ────────────────────
    for bx in (0.60, 1.20, 1.80, 2.40):
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius=post_r, depth=height,
                                   matrix=Matrix.Translation(Vector((bx, 0, height/2))))

    # ── 2 horizontal rail bars ──────────────────────
    for rz in (0.35, height):
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius=post_r, depth=length,
                                   matrix=Matrix.Translation(Vector((length/2, 0, rz))) @
                                          Matrix.Rotation(PI/2, 4, 'Y'))

    # ── reflective warning strip on top rail ───────
    box_from_corners(bm, (-0.01, -0.025, height-0.01),
                          (length+0.01, 0.025, height+0.01))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Human_TemporaryRailing_A")
    return obj


# ══════════════════════════════════════════════
#  7. TRIPOD SCANNER
# ══════════════════════════════════════════════
# Survey tripod with box scanner head. Extended legs, cable tether.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Human_TemporaryRailing_A")
