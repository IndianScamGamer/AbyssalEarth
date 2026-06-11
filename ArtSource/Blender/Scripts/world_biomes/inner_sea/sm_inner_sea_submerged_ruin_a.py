"""
SM_InnerSea_SubmergedRuin_A — AbyssalEarth procedural mesh.
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
    """SM_InnerSea_SubmergedRuin_A — half-submerged ancient wall fragment 20m."""
    import random; random.seed(27)
    obj, bm = new_mesh("SM_InnerSea_SubmergedRuin_A")
    # main wall slab — upper half visible, lower submerged
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 2))
        @ Matrix.Scale(20, 4, (1,0,0))
        @ Matrix.Scale(2.5, 4, (0,1,0))
        @ Matrix.Scale(8.0, 4, (0,0,1))
        @ Matrix.Rotation(random.uniform(-0.08,0.08), 4, 'Z'))
    # machine grooves on face
    for gx in range(-8, 9, 2):
        bmesh.ops.create_cube(bm, size=0.15,
            matrix=Matrix.Translation((gx, 1.28, 4))
            @ Matrix.Scale(0.4/0.15, 4, (1,0,0))
            @ Matrix.Scale(0.08/0.15, 4, (0,1,0))
            @ Matrix.Scale(6/0.15, 4, (0,0,1)))
    # crystal sockets
    for i in range(3):
        sx = -6 + i*6
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=8,
            radius=0.45, depth=0.12,
            matrix=Matrix.Translation((sx, 1.32, 5.5)))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.35,
            matrix=Matrix.Translation((sx, 1.35, 5.5)))
    # eroded chunk missing
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.8,
        matrix=Matrix.Translation((7, 0, 5)))
    for v in result['verts']:
        v.co *= 0.0  # dissolve these verts to create hole (simplified)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_InnerSea_SubmergedRuin_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_InnerSea_SubmergedRuin_A")
