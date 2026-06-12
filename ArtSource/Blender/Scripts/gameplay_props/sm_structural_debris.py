"""
SM_StructuralDebris_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Slice')

def build():
    """StructuralHazards falling debris — jagged rock slab cluster used by
    the falling-debris hazard, 1.5m chunk."""
    random.seed(122)
    obj, bm = new_mesh("SM_StructuralDebris_A")
    # primary jagged chunk
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.7,
        matrix=Matrix.Translation((0, 0, 0.7)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.7, 1.3)
        v.co.y *= random.uniform(0.7, 1.3)
        v.co.z = 0.7 + (v.co.z - 0.7) * random.uniform(0.6, 1.2)
    # 2 satellite shards
    for sx, sy, sr in [(0.75, 0.3, 0.28), (-0.6, -0.4, 0.22)]:
        result = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=sr,
            matrix=Matrix.Translation((sx, sy, sr)))
        for v in result['verts']:
            v.co.x = sx + (v.co.x - sx) * random.uniform(0.6, 1.4)
            v.co.y = sy + (v.co.y - sy) * random.uniform(0.6, 1.4)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_StructuralDebris_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_StructuralDebris_A")
