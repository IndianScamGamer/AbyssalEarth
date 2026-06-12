"""
SM_Human_CableCoil_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Human_CableCoil_A …")
    obj, bm = new_mesh("SM_Human_CableCoil_A")

    # ── stand frame ───────────────────────────────
    # 2 vertical posts
    for sx in (-0.28, 0.28):
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius=0.04, depth=0.55,
                                   matrix=Matrix.Translation(Vector((sx, 0, 0.275))))
    # horizontal axle
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius=0.035, depth=0.58,
                               matrix=Matrix.Translation(Vector((0, 0, 0.42))) @
                                      Matrix.Rotation(PI/2, 4, 'Y'))
    # base cross-bar
    box_from_corners(bm, (-0.32, -0.14, 0), (0.32, 0.14, 0.06))

    # ── drum ──────────────────────────────────────
    drum_r = 0.18
    for offset, r in [(0.0, drum_r), (0.0, drum_r * 1.25)]:
        disc = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                        segments=20, radius=r)
        for bv in (-0.26, 0.26):
            bmesh.ops.translate(bm, verts=disc['verts'],
                                vec=Vector((bv, 0, 0.42)))
            disc2 = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                             segments=20, radius=r)
            bmesh.ops.translate(bm, verts=disc2['verts'],
                                vec=Vector((bv + 0.04 if bv < 0 else bv - 0.04,
                                            0, 0.42)))

    # ── cable windings (helix tube) ────────────────
    n_coils = 8
    for t_i in range(n_coils * 12):
        t   = t_i / (n_coils * 12)
        angle = t * n_coils * TAU
        r_c = drum_r * 1.1
        cx  = r_c * math.cos(angle)
        cy  = r_c * math.sin(angle)
        cz  = 0.42 + (t - 0.5) * 0.45
        if abs(cz - 0.42) < 0.22:
            bm.verts.new((cx, cy, cz))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Human_CableCoil_A")
    return obj


# ══════════════════════════════════════════════
#  5. FIELD CONSOLE
# ══════════════════════════════════════════════
# Portable rugged field computer. 1.5×0.8m form factor on folding legs.
# Angled keyboard area, raised screen section, cyan status strip.
# Matches: expedition_crates_props_concept.png console item.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Human_CableCoil_A")
