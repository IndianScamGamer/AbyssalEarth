"""
SM_Later_BuriedMachineSlab_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('LaterRegions')

def build():
    """Half-buried angular machine wreck — tilted slab emerging from ash,
    cyan edge-light strip along one face. Concept: LT-001 foreground."""
    random.seed(402)
    obj, bm = new_mesh("SM_Later_BuriedMachineSlab_A")
    # main tilted slab
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.9))
        @ Matrix.Rotation(0.35, 4, 'Y')
        @ Matrix.Rotation(0.12, 4, 'X')
        @ Matrix.Scale(6.5, 4, (1,0,0))
        @ Matrix.Scale(3.0, 4, (0,1,0))
        @ Matrix.Scale(0.8, 4, (0,0,1)))
    # second smaller slab leaning on it
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((3.2, 1.2, 0.5))
        @ Matrix.Rotation(-0.5, 4, 'Y')
        @ Matrix.Rotation(0.3, 4, 'Z')
        @ Matrix.Scale(3.0, 4, (1,0,0))
        @ Matrix.Scale(1.8, 4, (0,1,0))
        @ Matrix.Scale(0.5, 4, (0,0,1)))
    # cyan edge-light strip along the exposed long edge
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((-0.5, -1.45, 1.85))
        @ Matrix.Rotation(0.35, 4, 'Y')
        @ Matrix.Scale(5.8, 4, (1,0,0))
        @ Matrix.Scale(0.08, 4, (0,1,0))
        @ Matrix.Scale(0.08, 4, (0,0,1)))
    # panel seams
    for sx in [-2.0, 0.0, 2.0]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((sx, 0, 1.45 + sx * 0.35))
            @ Matrix.Rotation(0.35, 4, 'Y')
            @ Matrix.Scale(0.06, 4, (1,0,0))
            @ Matrix.Scale(3.05, 4, (0,1,0))
            @ Matrix.Scale(0.06, 4, (0,0,1)))
    # ash drift piled against the base
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=2.4,
        matrix=Matrix.Translation((-2.0, 0.5, 0)))
    for v in result['verts']:
        if v.co.z > 0:
            v.co.z *= 0.25
        else:
            v.co.z = 0
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_pearl_stone"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Later_BuriedMachineSlab_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Later_BuriedMachineSlab_A")
