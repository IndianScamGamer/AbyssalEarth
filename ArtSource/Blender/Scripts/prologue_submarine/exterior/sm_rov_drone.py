"""
SM_ROV_Drone_A — AbyssalEarth procedural mesh.
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
    """Small support ROV drone — 80cm boxy body, 4 thruster pods, light bar.
    Concept: small lit drones around the submarine in intro_submarine_wide."""
    obj, bm = new_mesh("SM_ROV_Drone_A")
    # body
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.30))
        @ Matrix.Scale(0.55, 4, (1,0,0))
        @ Matrix.Scale(0.80, 4, (0,1,0))
        @ Matrix.Scale(0.35, 4, (0,0,1)))
    # 4 thruster pods at corners
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False, segments=10,
                radius1=0.10, radius2=0.10, depth=0.16,
                matrix=Matrix.Translation((sx*0.34, sy*0.46, 0.30))
                @ Matrix.Rotation(TAU/4, 4, 'X'))
    # front light bar
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, -0.42, 0.34))
        @ Matrix.Scale(0.42, 4, (1,0,0))
        @ Matrix.Scale(0.06, 4, (0,1,0))
        @ Matrix.Scale(0.08, 4, (0,0,1)))
    # top antenna + sensor dome
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.09,
        matrix=Matrix.Translation((0, 0.1, 0.52)))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=5,
        radius1=0.012, radius2=0.012, depth=0.22,
        matrix=Matrix.Translation((0.15, 0.3, 0.58)))
    # belly manipulator stub
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
        radius1=0.035, radius2=0.035, depth=0.18,
        matrix=Matrix.Translation((0, -0.25, 0.08)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_ROV_Drone_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_ROV_Drone_A")
