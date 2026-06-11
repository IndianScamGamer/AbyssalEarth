"""
SM_InnerSea_WoodDock_A — AbyssalEarth procedural mesh.
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
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, mat_color, extrude_region,
                           add_subdivision, TAU, PI)

EXPORT_DIR = get_export_dir('InnerSea')

def build():
    """Floating harbour dock section. Plank walkway, rusty metal cleats,
    rope loops. Matches atmosphere of inner_sea_concept.png."""
    print("Building SM_InnerSea_WoodDock_A …")
    obj, bm = new_mesh("SM_InnerSea_WoodDock_A")
    rng = random.Random(60)

    length, width = 12.0, 3.0

    # planks
    for p in range(int(length / 0.28)):
        y0 = p * 0.28 - length/2
        y1 = y0 + 0.26
        dip = rng.uniform(-0.02, 0.015)
        box(bm, (-width/2 + 0.015, y0, dip), (width/2 - 0.015, y1, 0.055 + dip))

    # gunwale rails
    for sx in (-width/2 - 0.05, width/2 + 0.05):
        box(bm, (sx, -length/2, 0.0), (sx + 0.08, length/2, 0.18))

    # dock posts (cleats)
    for py in [-length/2 + 1, 0, length/2 - 1]:
        for px in (-width/2 - 0.02, width/2 + 0.02):
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=6, radius=0.065, depth=0.45,
                                       matrix=Matrix.Translation(Vector((px, py, -0.22))))
            box(bm, (px - 0.09, py - 0.025, 0.12), (px + 0.09, py + 0.025, 0.22))

    # floats (barrel-like)
    for fy in (-length/3, length/3):
        for fx in (-width/2 + 0.15, width/2 - 0.15):
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=12, radius=0.22, depth=0.40,
                                       matrix=Matrix.Translation(Vector((fx, fy, -0.20))) @
                                              Matrix.Rotation(PI/2, 4, 'X'))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_bottom(obj)
    return obj


# ════════════════════════════════════════════════════════
#  MANTLE GARDEN
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_InnerSea_WoodDock_A")
