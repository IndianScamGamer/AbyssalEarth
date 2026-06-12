"""
SM_Item_GravityCrystal_A — AbyssalEarth procedural mesh.
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
    """ITEM_MINERAL_GRAVITY_CRYSTAL — octahedral crystal that distorts gravity."""
    obj, bm = new_mesh("SM_Item_GravityCrystal_A")
    # octahedron: 6 verts
    R, H = 0.07, 0.12
    top = bm.verts.new((0, 0, 0.13 + H))
    bot = bm.verts.new((0, 0, 0.13 - H))
    mid = [bm.verts.new((math.cos(i*TAU/4)*R, math.sin(i*TAU/4)*R, 0.13))
           for i in range(4)]
    for i in range(4):
        ni = (i + 1) % 4
        bm.faces.new([mid[i], mid[ni], top])
        bm.faces.new([mid[ni], mid[i], bot])
    # small orbit ring (floats around crystal)
    ring = [bm.verts.new((math.cos(i*TAU/16)*0.11,
                           math.sin(i*TAU/16)*0.11, 0.13)) for i in range(16)]
    ring2 = [bm.verts.new((math.cos(i*TAU/16)*0.118,
                            math.sin(i*TAU/16)*0.118, 0.13)) for i in range(16)]
    for i in range(16):
        ni = (i + 1) % 16
        bm.faces.new([ring[i], ring[ni], ring2[ni], ring2[i]])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_purple_emissive", "mat_ancient_machine_dark"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_GravityCrystal_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_GravityCrystal_A")
