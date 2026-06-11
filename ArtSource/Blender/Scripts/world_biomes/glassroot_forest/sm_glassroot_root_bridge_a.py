"""
SM_Glassroot_RootBridge_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GlassrootForest')


def build():
    """SM_Glassroot_RootBridge_A — 30m organic living root bridge."""
    import random; random.seed(44)
    obj, bm = new_mesh("SM_Glassroot_RootBridge_A")
    L, W = 30.0, 4.0
    # deck — organic path segments
    for i in range(15):
        t = i/14
        dx = random.uniform(-0.3, 0.3)
        bz = -math.sin(t*math.pi)*0.8
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((-L/2 + t*L + dx, 0, bz))
            @ Matrix.Scale(2.2, 4, (1,0,0))
            @ Matrix.Scale(W*(0.85+random.uniform(-0.1,0.1)), 4, (0,1,0))
            @ Matrix.Scale(0.22, 4, (0,0,1)))
    # 3 root ribs underneath spanning the bridge
    for ri in range(3):
        rx = -L/3 + ri*L/3
        for side in [-1, 1]:
            for si in range(8):
                st = si/7
                x = rx + side*math.sin(st*math.pi)*W*0.6
                z = -math.sin(st*math.pi)*2.5 - 0.3
                bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
                    radius=0.15*(1-st*0.5), depth=0.5,
                    matrix=Matrix.Translation((x, 0, z)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_red_sap"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootBridge_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Glassroot_RootBridge_A")
