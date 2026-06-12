"""
SM_Item_PressureLiner_A — AbyssalEarth procedural mesh.
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
    """ITEM_UPGRADE_PRESSURE_LINER — curved suit plate segment."""
    obj, bm = new_mesh("SM_Item_PressureLiner_A")
    # curved plate: arc strip
    SEGS = 10
    W = 0.10
    lo_out, lo_in, hi_out, hi_in = [], [], [], []
    for i in range(SEGS + 1):
        a = -TAU/8 + (i / SEGS) * TAU/4
        R_OUT, R_IN = 0.16, 0.145
        for lst, r, z in [(lo_out, R_OUT, 0), (lo_in, R_IN, 0),
                           (hi_out, R_OUT, W), (hi_in, R_IN, W)]:
            lst.append(bm.verts.new((math.cos(a)*r, math.sin(a)*r, z)))
    for i in range(SEGS):
        bm.faces.new([lo_out[i], lo_out[i+1], hi_out[i+1], hi_out[i]])
        bm.faces.new([lo_in[i+1], lo_in[i], hi_in[i], hi_in[i+1]])
        bm.faces.new([lo_in[i], lo_in[i+1], lo_out[i+1], lo_out[i]])
        bm.faces.new([hi_out[i], hi_out[i+1], hi_in[i+1], hi_in[i]])
    for cap in [(lo_out[0], lo_in[0], hi_in[0], hi_out[0]),
                (lo_in[-1], lo_out[-1], hi_out[-1], hi_in[-1])]:
        bm.faces.new(cap)
    # rivet studs
    for i in range(3):
        a = -TAU/10 + i * TAU/10
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.008,
            matrix=Matrix.Translation((math.cos(a)*0.162, math.sin(a)*0.162, W/2)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_PressureLiner_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_PressureLiner_A")
