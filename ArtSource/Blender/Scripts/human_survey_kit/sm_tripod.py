"""
SM_Human_TripodScanner_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Human_TripodScanner_A …")
    obj, bm = new_mesh("SM_Human_TripodScanner_A")

    leg_h = 1.30
    # ── 3 legs ────────────────────────────────────
    for i in range(3):
        angle = i * TAU/3
        tx = math.cos(angle) * 0.45
        ty = math.sin(angle) * 0.45
        # leg as thin box
        bv = [bm.verts.new((0, 0, leg_h)),
              bm.verts.new((tx, ty, 0.04))]
        # thin cylinder leg
        leg_dir = Vector((tx, ty, 0.04 - leg_h)).normalized()
        for j in range(8):
            pass  # simplified: just thin cylinder
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius=0.018, depth=leg_h,
                                   matrix=(Matrix.Translation(Vector((tx/2, ty/2, leg_h/2))) @
                                           Matrix.Rotation(-math.atan2(math.sqrt(tx**2+ty**2),
                                                                         leg_h-0.04), 4, 'X') @
                                           Matrix.Rotation(angle, 4, 'Z')))
        # foot
        box_from_corners(bm, (tx-0.06, ty-0.06, 0), (tx+0.06, ty+0.06, 0.04))

    # ── centre column ─────────────────────────────
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=6, radius=0.025, depth=0.40,
                               matrix=Matrix.Translation(Vector((0, 0, leg_h + 0.20))))

    # ── scanner head box ──────────────────────────
    box_from_corners(bm, (-0.14, -0.09, leg_h+0.38), (0.14, 0.09, leg_h+0.58))
    # optic lens
    bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                             segments=12, radius=0.06)
    for v in bm.verts:
        if abs(v.co.z) < 0.01 and v.co.length < 0.07:
            v.co.z = leg_h + 0.48
            v.co.y = 0.10

    # ── cyan status ring ──────────────────────────
    for status_z in (leg_h+0.40, leg_h+0.56):
        sv = [bm.verts.new((math.cos(a*TAU/12)*0.15,
                            math.sin(a*TAU/12)*0.09,
                            status_z))
              for a in range(12)]
        try:
            bm.faces.new(sv)
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Human_TripodScanner_A")
    return obj


# ══════════════════════════════════════════════
#  8. BEDROLL BUNDLE
# ══════════════════════════════════════════════
# Rolled sleeping mat + bag strapped with webbing.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Human_TripodScanner_A")
