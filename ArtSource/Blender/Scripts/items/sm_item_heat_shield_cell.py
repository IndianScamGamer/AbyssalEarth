"""
SM_Item_HeatShieldCell_A — AbyssalEarth procedural mesh.
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
    """ITEM_TOOL_HEAT_SHIELD — hexagonal insulation cell cassette."""
    obj, bm = new_mesh("SM_Item_HeatShieldCell_A")
    # hex cassette body
    R, T = 0.07, 0.030
    lo = [bm.verts.new((math.cos(i*TAU/6)*R, math.sin(i*TAU/6)*R, 0))
          for i in range(6)]
    hi = [bm.verts.new((math.cos(i*TAU/6)*R, math.sin(i*TAU/6)*R, T))
          for i in range(6)]
    for i in range(6):
        ni = (i + 1) % 6
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # inner hex emissive core inset
    lo2 = [bm.verts.new((math.cos(i*TAU/6)*R*0.55,
                          math.sin(i*TAU/6)*R*0.55, T)) for i in range(6)]
    hi2 = [bm.verts.new((math.cos(i*TAU/6)*R*0.55,
                          math.sin(i*TAU/6)*R*0.55, T + 0.006)) for i in range(6)]
    for i in range(6):
        ni = (i + 1) % 6
        bm.faces.new([lo2[i], lo2[ni], hi2[ni], hi2[i]])
    bm.faces.new(hi2)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_heat_bloom"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_HeatShieldCell_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_HeatShieldCell_A")
