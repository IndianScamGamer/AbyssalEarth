"""
SM_Item_FossilShard_A — AbyssalEarth procedural mesh.
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
    """ITEM_MINERAL_FOSSIL_SHARD — curved fragment of fossilized bone."""
    random.seed(102)
    obj, bm = new_mesh("SM_Item_FossilShard_A")
    # curved shard: arc of tapered segments
    SEGS = 8
    rings = []
    for i in range(SEGS + 1):
        t = i / SEGS
        cx = math.sin(t * PI * 0.6) * 0.16
        cz = t * 0.22
        r = 0.030 * (1 - t * 0.7) + 0.008
        ring = [bm.verts.new((cx + math.cos(j*TAU/6)*r,
                               math.sin(j*TAU/6)*r * 0.55,
                               cz)) for j in range(6)]
        rings.append(ring)
    for ri in range(SEGS):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(6):
            bm.faces.new([lo[j], lo[(j+1)%6], hi[(j+1)%6], hi[j]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_FossilShard_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_FossilShard_A")
