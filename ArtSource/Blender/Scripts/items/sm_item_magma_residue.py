"""
SM_Item_MagmaResidue_A — AbyssalEarth procedural mesh.
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
    """ITEM_MINERAL_MAGMA_RESIDUE — lumpy cooled magma nugget, glowing cracks."""
    random.seed(103)
    obj, bm = new_mesh("SM_Item_MagmaResidue_A")
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.09,
        matrix=Matrix.Translation((0, 0, 0.08)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.85, 1.25)
        v.co.y *= random.uniform(0.85, 1.25)
        if v.co.z < 0.05:
            v.co.z = 0.05 - (0.05 - v.co.z) * 0.3   # flatten base
    # crack ridge verts (heat glow strip)
    for i in range(6):
        a = i * TAU / 6
        bm.verts.new((math.cos(a)*0.095, math.sin(a)*0.095, 0.08))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_obsidian", "mat_heat_crack"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_MagmaResidue_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_MagmaResidue_A")
