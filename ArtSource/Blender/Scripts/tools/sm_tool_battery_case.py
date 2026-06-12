"""
SM_Tool_BatteryCase_A — AbyssalEarth procedural mesh.
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
    """Battery cell case — hinged box with 6 visible cells in foam."""
    obj, bm = new_mesh("SM_Tool_BatteryCase_A")
    # case base
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.030))
        @ Matrix.Scale(0.20, 4, (1,0,0))
        @ Matrix.Scale(0.13, 4, (0,1,0))
        @ Matrix.Scale(0.055, 4, (0,0,1)))
    # open lid (tilted back)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.085, 0.095))
        @ Matrix.Rotation(1.15, 4, 'X')
        @ Matrix.Scale(0.20, 4, (1,0,0))
        @ Matrix.Scale(0.12, 4, (0,1,0))
        @ Matrix.Scale(0.015, 4, (0,0,1)))
    # 6 cells in 2x3 grid
    for cx in [-0.06, 0.0, 0.06]:
        for cy in [-0.028, 0.028]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
                radius=0.020, depth=0.045,
                matrix=Matrix.Translation((cx, cy, 0.068)))
    # latch
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, -0.068, 0.035))
        @ Matrix.Scale(0.035, 4, (1,0,0))
        @ Matrix.Scale(0.010, 4, (0,1,0))
        @ Matrix.Scale(0.030, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_BatteryCase_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Tool_BatteryCase_A")
