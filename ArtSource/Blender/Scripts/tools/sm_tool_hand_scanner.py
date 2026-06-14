"""
SM_Tool_HandScanner_A — AbyssalEarth procedural mesh.
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
    """Handheld survey scanner — pistol grip, boxy head with screen and
    sensor snout. Physical prop for UAbyssalScanComponent in-hand visual."""
    obj, bm = new_mesh("SM_Tool_HandScanner_A")
    # head box
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.16))
        @ Matrix.Scale(0.10, 4, (1,0,0))
        @ Matrix.Scale(0.16, 4, (0,1,0))
        @ Matrix.Scale(0.11, 4, (0,0,1)))
    # screen plate (angled back face)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.085, 0.18))
        @ Matrix.Rotation(-0.25, 4, 'X')
        @ Matrix.Scale(0.085, 4, (1,0,0))
        @ Matrix.Scale(0.012, 4, (0,1,0))
        @ Matrix.Scale(0.075, 4, (0,0,1)))
    # sensor snout
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
        radius1=0.030, radius2=0.030, depth=0.06,
        matrix=Matrix.Translation((0, -0.11, 0.17))
        @ Matrix.Rotation(TAU/4, 4, 'X'))
    # pistol grip
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.03, 0.055))
        @ Matrix.Rotation(0.30, 4, 'X')
        @ Matrix.Scale(0.045, 4, (1,0,0))
        @ Matrix.Scale(0.055, 4, (0,1,0))
        @ Matrix.Scale(0.11, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_HandScanner_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Tool_HandScanner_A")
