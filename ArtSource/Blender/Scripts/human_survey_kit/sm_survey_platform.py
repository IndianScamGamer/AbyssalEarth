"""
SM_Human_SurveyPlatform_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Human_SurveyPlatform_A …")
    obj, bm = new_mesh("SM_Human_SurveyPlatform_A")
    rng = random.Random(3)

    plat_w = 10.0
    deck_h = 0.18
    leg_h  = 1.8

    # ── deck panels (3×3 grid) ─────────────────────
    panel_w = plat_w / 3
    for gx in range(3):
        for gy in range(3):
            x0 = (gx * panel_w - plat_w/2) + 0.02
            x1 = x0 + panel_w - 0.04
            y0 = (gy * panel_w - plat_w/2) + 0.02
            y1 = y0 + panel_w - 0.04
            box_from_corners(bm, (x0, y0, 0), (x1, y1, deck_h))
            # anti-slip groove lines on top
            for sl in range(4):
                sx = x0 + (sl+1) * panel_w/5
                sv = [bm.verts.new((sx, y0 + 0.02, deck_h)),
                      bm.verts.new((sx, y1 - 0.02, deck_h))]
                gv = [bm.verts.new((sx, y0 + 0.02, deck_h - 0.012)),
                      bm.verts.new((sx, y1 - 0.02, deck_h - 0.012))]
                try:
                    bm.faces.new([sv[0], sv[1], gv[1], gv[0]])
                except Exception:
                    pass

    # ── perimeter rail channel ─────────────────────
    half = plat_w * 0.5
    for sx, sy, ex, ey in [(-half, -half, half, -half),
                            (half,  -half, half, half),
                            (half,   half,-half,  half),
                            (-half,  half,-half, -half)]:
        rv = [bm.verts.new((sx - 0.06 * (1 if ey != -half else 0),
                            sy, deck_h + 0.02)),
              bm.verts.new((ex, ey, deck_h + 0.02)),
              bm.verts.new((ex, ey, deck_h + 1.05)),
              bm.verts.new((sx - 0.06 * (1 if ey != -half else 0),
                            sy, deck_h + 1.05))]
        # top rail bar
        for z_off in (deck_h + 0.02, deck_h + 1.05):
            bm.verts.new((sx, sy, z_off))

    # ── 4 support legs ─────────────────────────────
    for lx, ly in [(-4.2,-4.2),(4.2,-4.2),(4.2,4.2),(-4.2,4.2)]:
        leg_verts = bmesh.ops.create_cylinder(
            bm, cap_ends=True, cap_tris=False, segments=6,
            radius=0.14, depth=leg_h,
            matrix=Matrix.Translation(Vector((lx, ly, -leg_h/2))))
        # cross-braces to adjacent legs
        for sign in (-1, 1):
            brace_pts = [
                bm.verts.new((lx, ly, -leg_h * 0.3)),
                bm.verts.new((lx + sign * 8.4 * 0.5, ly, -leg_h * 0.7)),
            ]

    # ── anchor feet ────────────────────────────────
    for lx, ly in [(-4.2,-4.2),(4.2,-4.2),(4.2,4.2),(-4.2,4.2)]:
        foot = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                        segments=8, radius=0.28)
        bmesh.ops.translate(bm, verts=foot['verts'],
                            vec=Vector((lx, ly, -leg_h - 0.02)))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  2. SURVEY CRATE
# ══════════════════════════════════════════════
# Weathered metal storage crate with corner reinforcements,
# latch detail, and stencil emboss. Matches: expedition_crates_props_concept.png

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Human_SurveyPlatform_A")
