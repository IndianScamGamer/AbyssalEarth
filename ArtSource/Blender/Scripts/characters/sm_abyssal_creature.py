"""
SM_AbyssalCreature_Patrol_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Characters')

def build():
    clear_scene()
    ob, me = new_mesh("SM_AbyssalCreature_Patrol_A")
    bm = bmesh.new()

    # Carapace — scaled icosphere
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.40,
                                         matrix=Matrix.Translation((0, 0, 0.25)))
    for v in result['verts']:
        v.co.x *= 1.35
        v.co.y *= 0.90
        v.co.z *= 0.58

    # Segmented abdomen plates (3 bands)
    for i in range(3):
        az = 0.12 + i * 0.06
        bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False,
                                   segments=12, radius1=0.36 - i * 0.04,
                                   radius2=0.36 - i * 0.04,
                                   depth=0.03,
                                   matrix=Matrix.Translation((0, -0.20 - i * 0.12, az)))

    # 6 legs (3 per side)
    for side in [-1, 1]:
        for j in range(3):
            lx = side * 0.42
            ly = (j - 1) * 0.22
            # Upper segment
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                       segments=6, radius1=0.035, radius2=0.028,
                                       depth=0.28,
                                       matrix=Matrix.Translation(
                                           (lx + side * 0.12, ly, 0.22))
                                       @ Matrix.Rotation(math.radians(30 * side), 4, 'Z'))
            # Lower segment
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                       segments=5, radius1=0.025, radius2=0.015,
                                       depth=0.28,
                                       matrix=Matrix.Translation(
                                           (lx + side * 0.30, ly, 0.08))
                                       @ Matrix.Rotation(math.radians(-10 * side), 4, 'Z'))

    # Two pincer arms
    for side in [-1, 1]:
        # Arm
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=7, radius1=0.055, radius2=0.042,
                                   depth=0.45,
                                   matrix=Matrix.Translation(
                                       (side * 0.38, 0.32, 0.30))
                                   @ Matrix.Rotation(math.radians(20), 4, 'X'))
        # Pincer outer
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=4, radius1=0.04, radius2=0.008,
                                   depth=0.25,
                                   matrix=Matrix.Translation(
                                       (side * 0.40 + side * 0.05, 0.65, 0.38)))
        # Pincer inner (smaller)
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=4, radius1=0.030, radius2=0.005,
                                   depth=0.18,
                                   matrix=Matrix.Translation(
                                       (side * 0.40 - side * 0.04, 0.62, 0.35)))

    # Head stalks with sensor orbs
    for side in [-1, 1]:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius1=0.018, radius2=0.015,
                                   depth=0.22,
                                   matrix=Matrix.Translation(
                                       (side * 0.12, 0.44, 0.42)))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.04,
                                    matrix=Matrix.Translation(
                                        (side * 0.12, 0.44, 0.58)))

    finalise(ob, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_wet_basalt", "mat_blue_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_AbyssalCreature_Patrol_A")


# ---------------------------------------------------------------------------
# 7. Collectible item meshes — small props spawned as world pickups
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_AbyssalCreature_Patrol_A")
