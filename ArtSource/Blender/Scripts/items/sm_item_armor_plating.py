"""
SM_Item_ArmorPlating_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Items')

def build():
    """ITEM_UPGRADE_ARMOR_PLATING — angular stacked hull plates."""
    obj, bm = new_mesh("SM_Item_ArmorPlating_A")
    # 3 stacked offset angular plates
    for i in range(3):
        z = i * 0.018
        off = i * 0.012
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((off, off * 0.5, z + 0.008))
            @ Matrix.Rotation(i * 0.12, 4, 'Z')
            @ Matrix.Scale(0.13 - i*0.015, 4, (1,0,0))
            @ Matrix.Scale(0.10 - i*0.012, 4, (0,1,0))
            @ Matrix.Scale(0.014, 4, (0,0,1)))
    # corner bolts on top plate
    for cx, cy in [(-0.04, -0.03), (0.06, -0.02), (0.05, 0.05), (-0.03, 0.045)]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.007,
            matrix=Matrix.Translation((cx + 0.024, cy + 0.012, 0.062)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_ArmorPlating_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_ArmorPlating_A")
