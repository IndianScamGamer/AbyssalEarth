"""
SM_InnerSea_BrokenPier_A — AbyssalEarth procedural mesh.
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
    """SM_InnerSea_BrokenPier_A — 5×40m pier, broken end."""
    import random; random.seed(19)
    obj, bm = new_mesh("SM_InnerSea_BrokenPier_A")
    # intact section (0-26m)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((-7, 0, 0.2))
        @ Matrix.Scale(26, 4, (1,0,0))
        @ Matrix.Scale(5, 4, (0,1,0))
        @ Matrix.Scale(0.45, 4, (0,0,1)))
    # support legs every 4m
    for lx in range(-18, 8, 4):
        for ly in [-1.8, 1.8]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
                radius=0.18, depth=3.5,
                matrix=Matrix.Translation((lx, ly, -1.5)))
    # broken end (angled, cracked)
    for i in range(5):
        t = i/4
        bx = 12 + t*10
        bz = -t*2.5
        brot = random.uniform(-0.2, 0.2)
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((bx, random.uniform(-0.4,0.4), bz))
            @ Matrix.Scale(2.2, 4, (1,0,0))
            @ Matrix.Scale(4.5, 4, (0,1,0))
            @ Matrix.Scale(0.45, 4, (0,0,1))
            @ Matrix.Rotation(brot, 4, 'Z'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_InnerSea_BrokenPier_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_InnerSea_BrokenPier_A")
