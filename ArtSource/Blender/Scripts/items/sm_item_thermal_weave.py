"""
SM_Item_ThermalWeave_A — AbyssalEarth procedural mesh.
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
    """ITEM_UPGRADE_THERMAL_WEAVE — rolled insulating fabric bolt."""
    random.seed(109)
    obj, bm = new_mesh("SM_Item_ThermalWeave_A")
    # rolled cylinder (lying on side)
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=14,
        radius=0.045, depth=0.16,
        matrix=Matrix.Translation((0, 0, 0.045))
        @ Matrix.Rotation(TAU/4, 4, 'X'))
    # spiral edge detail: outer wrap lip
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=14,
        radius=0.048, depth=0.02,
        matrix=Matrix.Translation((0, 0.06, 0.045))
        @ Matrix.Rotation(TAU/4, 4, 'X'))
    # binding straps
    for sy in [-0.05, 0.05]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=10,
            radius=0.049, depth=0.012,
            matrix=Matrix.Translation((0, sy, 0.045))
            @ Matrix.Rotation(TAU/4, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_heat_bloom"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_ThermalWeave_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_ThermalWeave_A")
