"""
SM_Item_AirCanister_A — AbyssalEarth procedural mesh.
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
    """ITEM_TOOL_AIR_CANISTER — compressed oxygen cylinder with valve."""
    obj, bm = new_mesh("SM_Item_AirCanister_A")
    # tank body
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=12,
        radius=0.045, depth=0.20,
        matrix=Matrix.Translation((0, 0, 0.10)))
    # dome top
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.045,
        matrix=Matrix.Translation((0, 0, 0.20)))
    for v in result['verts']:
        if v.co.z < 0.20:
            v.co.z = 0.20
    # valve stem + knob
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.012, depth=0.035,
        matrix=Matrix.Translation((0, 0, 0.262)))
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
        radius=0.022, depth=0.012,
        matrix=Matrix.Translation((0, 0, 0.286)))
    # gauge band
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=14,
        radius=0.048, depth=0.018,
        matrix=Matrix.Translation((0, 0, 0.155)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_AirCanister_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_AirCanister_A")
