"""
SM_Item_SuitPatch_A — AbyssalEarth procedural mesh.
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
    """ITEM_TOOL_SUIT_PATCH — rounded square emergency hull patch."""
    obj, bm = new_mesh("SM_Item_SuitPatch_A")
    # rounded square plate
    S, T = 0.09, 0.014
    SEGS = 4
    pts = []
    for corner in [(1,1),(-1,1),(-1,-1),(1,-1)]:
        cx, cy = corner[0]*S*0.7, corner[1]*S*0.7
        base_a = math.atan2(corner[1], corner[0]) - TAU/8
        for s in range(SEGS+1):
            a = base_a + s * (TAU/4) / SEGS
            pts.append((cx + math.cos(a)*S*0.3, cy + math.sin(a)*S*0.3))
    lo = [bm.verts.new((x, y, 0)) for x, y in pts]
    hi = [bm.verts.new((x, y, T)) for x, y in pts]
    n = len(pts)
    for i in range(n):
        ni = (i + 1) % n
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # cross seam detail on top
    for axis in range(2):
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, 0, T + 0.003))
            @ Matrix.Rotation(axis * TAU/4, 4, 'Z')
            @ Matrix.Scale(S*1.7, 4, (1,0,0))
            @ Matrix.Scale(0.012, 4, (0,1,0))
            @ Matrix.Scale(0.005, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_SuitPatch_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_SuitPatch_A")
