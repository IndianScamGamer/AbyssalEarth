"""
SM_Item_RiftStabiliser_A — AbyssalEarth procedural mesh.
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
    """ITEM_KEY_RIFT_STABILISER — alien fabricated key device: ring + core."""
    obj, bm = new_mesh("SM_Item_RiftStabiliser_A")
    # outer ring (torus approximation: ring of spheres)
    R = 0.085
    for i in range(14):
        a = i * TAU / 14
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.014,
            matrix=Matrix.Translation((math.cos(a)*R, math.sin(a)*R, 0.10)))
    # core octahedron
    top = bm.verts.new((0, 0, 0.10 + 0.05))
    bot = bm.verts.new((0, 0, 0.10 - 0.05))
    mid = [bm.verts.new((math.cos(i*TAU/4)*0.032,
                          math.sin(i*TAU/4)*0.032, 0.10)) for i in range(4)]
    for i in range(4):
        ni = (i + 1) % 4
        bm.faces.new([mid[i], mid[ni], top])
        bm.faces.new([mid[ni], mid[i], bot])
    # 3 anchor prongs from ring to core
    for i in range(3):
        a = i * TAU / 3
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=5,
            radius=0.006, depth=R - 0.035,
            matrix=Matrix.Translation((math.cos(a)*R*0.55,
                                        math.sin(a)*R*0.55, 0.10))
            @ Matrix.Rotation(a + TAU/4, 4, 'Z')
            @ Matrix.Rotation(TAU/4, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive", "mat_orb_energy"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_RiftStabiliser_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Item_RiftStabiliser_A")
