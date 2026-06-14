"""
SM_Tool_DataTablet_A — AbyssalEarth procedural mesh.
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
    """Ruggedised data tablet — narrative pickup prop for journal/terminal
    beats (NarrativeSubsystem). Corner bumpers, screen inset, side clasps."""
    obj, bm = new_mesh("SM_Tool_DataTablet_A")
    # slab
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.012))
        @ Matrix.Scale(0.16, 4, (1,0,0))
        @ Matrix.Scale(0.22, 4, (0,1,0))
        @ Matrix.Scale(0.022, 4, (0,0,1)))
    # screen inset (raised lip frame)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.026))
        @ Matrix.Scale(0.13, 4, (1,0,0))
        @ Matrix.Scale(0.18, 4, (0,1,0))
        @ Matrix.Scale(0.004, 4, (0,0,1)))
    # corner bumpers
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
                radius1=0.022, radius2=0.022, depth=0.030,
                matrix=Matrix.Translation((sx*0.075, sy*0.105, 0.015)))
    # side clasps
    for sy in [-0.06, 0.06]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0.085, sy, 0.012))
            @ Matrix.Scale(0.015, 4, (1,0,0))
            @ Matrix.Scale(0.030, 4, (0,1,0))
            @ Matrix.Scale(0.018, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_DataTablet_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Tool_DataTablet_A")
