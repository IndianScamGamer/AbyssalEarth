"""
SM_Human_BedrollBundle_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Human_BedrollBundle_A …")
    obj, bm = new_mesh("SM_Human_BedrollBundle_A")

    # ── outer roll cylinder ────────────────────────
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=20, radius=0.16, depth=0.62,
                               matrix=Matrix.Translation(Vector((0, 0, 0.31))) @
                                      Matrix.Rotation(PI/2, 4, 'X'))

    # ── 3 webbing straps ───────────────────────────
    for sy in (-0.18, 0, 0.18):
        strap = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                         segments=20, radius=0.165)
        bmesh.ops.translate(bm, verts=strap['verts'], vec=Vector((0, sy, 0.31)))
        for sv in strap['verts']:
            sv.co.x *= 0.15   # flatten strap

    # ── compression bag attached on back ──────────
    box_from_corners(bm, (-0.08, 0.14, 0.14), (0.08, 0.28, 0.48))
    # buckle
    box_from_corners(bm, (-0.03, 0.27, 0.28), (0.03, 0.30, 0.34))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Human_BedrollBundle_A")
    return obj


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Human_BedrollBundle_A")
