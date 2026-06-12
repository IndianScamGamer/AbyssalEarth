"""
SM_WorkLight_Post_A — AbyssalEarth procedural mesh.
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
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, mat_color, extrude_region,
                           add_subdivision, TAU, PI)

EXPORT_DIR = get_export_dir('Prologue')

def build():
    """Standalone seafloor work light — weighted tripod base, 3m mast,
    twin amber flood heads. Scatter around the shaft rim."""
    obj, bm = new_mesh("SM_WorkLight_Post_A")
    # weighted base disc
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=10,
        radius=0.45, depth=0.15,
        matrix=Matrix.Translation((0, 0, 0.075)))
    # mast
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.06, depth=3.0,
        matrix=Matrix.Translation((0, 0, 1.65)))
    # crossbar
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 3.15))
        @ Matrix.Scale(1.1, 4, (1,0,0))
        @ Matrix.Scale(0.08, 4, (0,1,0))
        @ Matrix.Scale(0.08, 4, (0,0,1)))
    # twin flood heads, angled down
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side*0.48, -0.06, 3.12))
            @ Matrix.Rotation(-0.5, 4, 'X')
            @ Matrix.Scale(0.30, 4, (1,0,0))
            @ Matrix.Scale(0.12, 4, (0,1,0))
            @ Matrix.Scale(0.22, 4, (0,0,1)))
    # cable drape stub
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=5,
        radius=0.02, depth=0.8,
        matrix=Matrix.Translation((0.3, 0.2, 0.4))
        @ Matrix.Rotation(0.9, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_WorkLight_Post_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_WorkLight_Post_A")
