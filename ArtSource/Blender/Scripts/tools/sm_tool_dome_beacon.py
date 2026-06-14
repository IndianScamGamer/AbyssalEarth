"""
SM_Tool_DomeBeacon_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Tools')

def build():
    """Deployable dome beacon — squat ribbed dome with caged lamp on top.
    Matches the domed device in the toolkit sheet; alt beacon style."""
    obj, bm = new_mesh("SM_Tool_DomeBeacon_A")
    # dome body (hemisphere)
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.12,
        matrix=Matrix.Translation((0, 0, 0.04)))
    for v in result['verts']:
        if v.co.z < 0.04:
            v.co.z = 0.04
    # base skirt
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12,
        radius1=0.135, radius2=0.135, depth=0.045,
        matrix=Matrix.Translation((0, 0, 0.0225)))
    # rib bands over dome
    for band_a in [0, TAU/4]:
        SEGS = 8
        for s in range(SEGS + 1):
            t = s / SEGS
            arc = -PI/2 + t * PI
            rx = math.cos(arc) * 0.125
            rz = 0.045 + math.sin(arc) * 0.115 + 0.115
            if rz < 0.045:
                continue
            bmesh.ops.create_cube(bm, size=0.018,
                matrix=Matrix.Translation((math.cos(band_a)*rx,
                                            math.sin(band_a)*rx, rz)))
    # caged lamp on top
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
        radius1=0.030, radius2=0.030, depth=0.045,
        matrix=Matrix.Translation((0, 0, 0.185)))
    for i in range(4):
        a = i * TAU / 4
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=4,
            radius1=0.004, radius2=0.004, depth=0.05,
            matrix=Matrix.Translation((math.cos(a)*0.032,
                                        math.sin(a)*0.032, 0.185)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_DomeBeacon_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Tool_DomeBeacon_A")
