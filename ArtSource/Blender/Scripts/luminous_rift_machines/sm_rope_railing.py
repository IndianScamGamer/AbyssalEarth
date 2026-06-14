"""
SM_Rift_RopeRailing_A — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-010, LR-011
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

EXPORT_DIR = get_export_dir('LuminousRift')

def build():
    """Expedition rope railing strung between ancient posts — 4m modular run,
    2 posts, 2 sagging rope spans. Concept: bridge kit foreground railings."""
    obj, bm = new_mesh("SM_Rift_RopeRailing_A")
    L = 4.0
    # 2 posts
    for px in [-L/2, L/2]:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=7,
            radius1=0.07, radius2=0.07, depth=1.1,
            matrix=Matrix.Translation((px, 0, 0.55)))
        # post cap
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.085,
            matrix=Matrix.Translation((px, 0, 1.12)))
    # 2 sagging rope spans (catenary approximated by sphere chains)
    for rope_z in [0.55, 1.0]:
        SEGS = 11
        for s in range(SEGS):
            t = (s + 0.5) / SEGS
            x = -L/2 + t * L
            sag = math.sin(t * PI) * 0.12
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035,
                matrix=Matrix.Translation((x, 0, rope_z - sag)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_ancient_machine_dark"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_RopeRailing_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Rift_RopeRailing_A")
