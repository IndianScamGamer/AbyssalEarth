"""
SM_Diver_Protagonist_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Diver_Protagonist_A")
    bm = bmesh.new()

    def add_cyl(r, h, segs, mat_i, z_offset=0.0, cap=True):
        bmesh.ops.create_cone(
            bm,
            cap_ends=cap,
            cap_tris=False,
            segments=segs,
            radius1=r,
            radius2=r * 0.85,
            depth=h,
            matrix=Matrix.Translation((0, 0, z_offset + h * 0.5)),
        )
        top = sorted(bm.verts, key=lambda v: v.co.z, reverse=True)[:segs * 2]
        return top

    def add_sphere(r, segs, z_off):
        result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r,
                                            matrix=Matrix.Translation((0, 0, z_off)))
        for v in result['verts']:
            v.co.z += 0
        return result['verts']

    # Legs (two cylinders offset laterally)
    for side in [-1, 1]:
        mat = Matrix.Translation((side * 0.14, 0, 0))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=10, radius1=0.085, radius2=0.07,
                                   depth=0.55, matrix=mat @ Matrix.Translation((0, 0, 0.275)))
        # Fin boot
        boot_mat = mat @ Matrix.Translation((0, 0.05, 0.10))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.10, radius2=0.08,
                                   depth=0.20, matrix=boot_mat)

    # Torso
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                               segments=12, radius1=0.175, radius2=0.16,
                               depth=0.52, matrix=Matrix.Translation((0, 0, 0.83)))

    # Shoulder tank pair
    for side in [-1, 1]:
        tank_mat = Matrix.Translation((side * 0.22, -0.08, 0.95))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.055, radius2=0.055,
                                   depth=0.36, matrix=tank_mat)

    # Arms
    for side in [-1, 1]:
        arm_mat = Matrix.Translation((side * 0.26, 0, 0.95))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.065, radius2=0.055,
                                   depth=0.42, matrix=arm_mat)
        # Glove
        glove_mat = Matrix.Translation((side * 0.26, 0, 0.72))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.06,
                                    matrix=glove_mat)

    # Neck
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius1=0.065, radius2=0.065,
                               depth=0.10, matrix=Matrix.Translation((0, 0, 1.12)))

    # Helmet (large sphere, visor notch)
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.165,
                                matrix=Matrix.Translation((0, 0, 1.31)))

    # Visor plate (flat disc forward)
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                               segments=12, radius1=0.10, radius2=0.10,
                               depth=0.03,
                               matrix=Matrix.Translation((0, 0.155, 1.31)))

    # Utility belt detail
    bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False,
                               segments=14, radius1=0.18, radius2=0.18,
                               depth=0.06,
                               matrix=Matrix.Translation((0, 0, 0.73)))

    # Belt pouches
    for ang in [0, 60, -60, 180]:
        rad = math.radians(ang)
        px = 0.185 * math.sin(rad)
        py = 0.185 * math.cos(rad)
        bmesh.ops.create_cube(bm, size=0.07,
                               matrix=Matrix.Translation((px, py, 0.73)))

    finalise(ob, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_glass_bark"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Diver_Protagonist_A")


# ---------------------------------------------------------------------------
# 2. Helios Robot — detailed  —  SM_HeliosRobot_Detailed_A
#    Humanoid AI ~1.85 m. Smooth-panelled form, oval glowing faceplate,
#    segmented limbs. Based on Figure 03 concept (sleek, non-threatening).
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Diver_Protagonist_A")
