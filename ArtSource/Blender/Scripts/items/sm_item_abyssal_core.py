"""
SM_Item_AbyssalCore_A — AbyssalEarth procedural mesh.
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
    """ITEM_MINERAL_ABYSSAL_CORE — dense crystalline mineral chunk."""
    random.seed(101)
    obj, bm = new_mesh("SM_Item_AbyssalCore_A")
    # core chunk: deformed icosphere
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.10,
        matrix=Matrix.Translation((0, 0, 0.10)))
    for v in result['verts']:
        v.co += Vector((random.uniform(-0.015, 0.015),
                        random.uniform(-0.015, 0.015),
                        random.uniform(-0.012, 0.012)))
    # 3 small crystal facets protruding
    for i in range(3):
        a = i * TAU / 3 + 0.4
        cx, cy = math.cos(a) * 0.07, math.sin(a) * 0.07
        tip = bm.verts.new((cx * 1.9, cy * 1.9, 0.14 + i * 0.02))
        ring = [bm.verts.new((cx + math.cos(j*TAU/4)*0.025,
                               cy + math.sin(j*TAU/4)*0.025,
                               0.08 + i * 0.02)) for j in range(4)]
        for j in range(4):
            bm.faces.new([ring[j], ring[(j+1)%4], tip])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_AbyssalCore_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_AbyssalCore_A")
