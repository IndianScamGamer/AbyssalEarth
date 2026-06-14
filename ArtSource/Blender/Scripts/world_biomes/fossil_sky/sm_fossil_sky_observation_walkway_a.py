"""
SM_FossilSky_ObservationWalkway_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('FossilSky')


def build():
    """SM_FossilSky_ObservationWalkway_A — 4×40m suspended walkway, bone planks."""
    obj, bm = new_mesh("SM_FossilSky_ObservationWalkway_A")
    W, L, THICK = 4.0, 40.0, 0.18
    # deck planks
    for i in range(20):
        px = -L/2 + i*2.1 + 0.5
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((px, 0, 0))
            @ Matrix.Scale(1.9, 4, (1,0,0))
            @ Matrix.Scale(W, 4, (0,1,0))
            @ Matrix.Scale(THICK, 4, (0,0,1)))
    # metal bracket supports every 4m
    for bx in range(-18, 20, 4):
        for side in [-1, 1]:
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
                radius1=0.05, radius2=0.05, depth=2.0,
                matrix=Matrix.Translation((bx, side*W*0.4, 0.9)))
            # anchor node
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.08,
                matrix=Matrix.Translation((bx, side*W*0.4, 1.9)))
    # side rails
    for side in [-1, 1]:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
            radius1=0.04, radius2=0.04, depth=L,
            matrix=Matrix.Translation((0, side*W*0.48, 1.0))
            @ Matrix.Rotation(TAU/4, 4, 'Y'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_ancient_machine_dark", "mat_ancient_machine_edge_wear"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_ObservationWalkway_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_FossilSky_ObservationWalkway_A")
