"""
SM_GravityWell_FloatingPlatform_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GravityWell')


def build():
    """SM_GravityWell_FloatingPlatform_A — 15m irregular floating rock platform."""
    import random; random.seed(66)
    obj, bm = new_mesh("SM_GravityWell_FloatingPlatform_A")
    result = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=7.5,
        matrix=Matrix.Translation((0,0,1.5)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.85, 1.15)
        v.co.y *= random.uniform(0.85, 1.15)
        if v.co.z < 1.5:
            v.co.z = 1.5 - (1.5 - v.co.z) * 0.35
        else:
            v.co.z = 1.5 + (v.co.z - 1.5) * 0.22
    # anchor cable stubs
    for i in range(4):
        a = i*TAU/4
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
            radius=0.15, depth=2.5,
            matrix=Matrix.Translation((math.cos(a)*4, math.sin(a)*4, -0.5)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_dark_basalt", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_FloatingPlatform_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_GravityWell_FloatingPlatform_A")
