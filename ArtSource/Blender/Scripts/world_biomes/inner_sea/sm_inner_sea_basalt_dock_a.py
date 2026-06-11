"""
SM_InnerSea_BasaltDock_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('InnerSea')


def build():
    """SM_InnerSea_BasaltDock_A — wet stone dock 10×30m with dock posts."""
    obj, bm = new_mesh("SM_InnerSea_BasaltDock_A")
    # main deck
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Scale(30.0, 4, (1,0,0))
        @ Matrix.Scale(10.0, 4, (0,1,0))
        @ Matrix.Scale(0.5, 4, (0,0,1))
        @ Matrix.Translation((0, 0, 0.25)))
    # dock posts
    for px in [-12, -6, 0, 6, 12]:
        for py in [-4, 4]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
                radius=0.22, depth=2.5,
                matrix=Matrix.Translation((px, py, 1.5)))
            # mooring ring
            bmesh.ops.create_cylinder(bm, cap_ends=False, segments=12,
                radius=0.30, depth=0.08,
                matrix=Matrix.Translation((px, py, 2.2)))
    # edge lip detail
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=0.12,
            matrix=Matrix.Translation((0, side*5.06, 0.3))
            @ Matrix.Scale(30.5/0.12, 4, (1,0,0))
            @ Matrix.Scale(0.5/0.12, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_InnerSea_BasaltDock_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_InnerSea_BasaltDock_A")
