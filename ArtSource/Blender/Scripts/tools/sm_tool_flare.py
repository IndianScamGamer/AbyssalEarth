"""
SM_Tool_Flare_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Tools')

def build():
    """Emergency flare stick — grip tube with cap and red glow tip."""
    obj, bm = new_mesh("SM_Tool_Flare_A")
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.016, depth=0.18,
        matrix=Matrix.Translation((0, 0, 0.09)))
    # grip rings
    for gz in [0.04, 0.08, 0.12]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=8,
            radius=0.018, depth=0.010,
            matrix=Matrix.Translation((0, 0, gz)))
    # glow tip
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.014, depth=0.035,
        matrix=Matrix.Translation((0, 0, 0.198)))
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.015,
        matrix=Matrix.Translation((0, 0, 0.216)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_red_emissive_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_Flare_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Tool_Flare_A")
