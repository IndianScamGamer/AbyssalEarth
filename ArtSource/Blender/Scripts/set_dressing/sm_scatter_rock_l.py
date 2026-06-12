"""
SM_Scatter_Rock_L_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('SetDressing')

def build():
    """Scatter rock L — generic deformed boulder for set dressing."""
    random.seed(203)
    obj, bm = new_mesh("SM_Scatter_Rock_L_A")
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.6,
        matrix=Matrix.Translation((0, 0, 1.6 * 0.8)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.75, 1.30)
        v.co.y *= random.uniform(0.75, 1.30)
        zc = 1.6 * 0.8
        if v.co.z < zc:
            v.co.z = zc - (zc - v.co.z) * 0.45   # flatten underside
        else:
            v.co.z = zc + (v.co.z - zc) * random.uniform(0.7, 1.1)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Scatter_Rock_L_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Scatter_Rock_L_A")
