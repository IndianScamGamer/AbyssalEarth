"""
SM_HeliosRobot_Detailed_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_HeliosRobot_Detailed_A")
    bm = bmesh.new()

    # Legs
    for side in [-1, 1]:
        for seg_z, seg_r, seg_h in [(0.0, 0.09, 0.30), (0.32, 0.085, 0.28)]:
            mat = Matrix.Translation((side * 0.135, 0, seg_z + seg_h * 0.5))
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=10, radius1=seg_r, radius2=seg_r * 0.92,
                                       depth=seg_h, matrix=mat)
        # Foot block
        foot_mat = Matrix.Translation((side * 0.135, 0.03, 0.10))
        bmesh.ops.create_cube(bm, size=0.10,
                               matrix=foot_mat @ Matrix.Scale(1.0, 4, (1, 0, 0))
                               @ Matrix.Scale(0.55, 4, (0, 0, 1)))

    # Hip junction sphere
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.13,
                                matrix=Matrix.Translation((0, 0, 0.65)))

    # Torso — two tapered sections
    for z_off, r1, r2, h in [(0.65, 0.155, 0.18, 0.26), (0.91, 0.18, 0.155, 0.24)]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=12, radius1=r1, radius2=r2,
                                   depth=h, matrix=Matrix.Translation((0, 0, z_off + h * 0.5)))

    # Chest emissive panel
    bmesh.ops.create_cube(bm, size=0.12,
                           matrix=Matrix.Translation((0, 0.175, 1.0))
                           @ Matrix.Scale(1.4, 4, (1, 0, 0))
                           @ Matrix.Scale(0.18, 4, (0, 0, 1)))

    # Shoulder spheres
    for side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.075,
                                    matrix=Matrix.Translation((side * 0.245, 0, 1.13)))

    # Upper arms
    for side in [-1, 1]:
        for seg_z, seg_r, seg_h in [(0.78, 0.065, 0.25), (1.04, 0.058, 0.22)]:
            mat = Matrix.Translation((side * 0.295, 0, seg_z + seg_h * 0.5))
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=8, radius1=seg_r, radius2=seg_r * 0.90,
                                       depth=seg_h, matrix=mat)
        # Hand disc
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.06, radius2=0.06,
                                   depth=0.04,
                                   matrix=Matrix.Translation((side * 0.295, 0, 0.73)))

    # Neck cylinder
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius1=0.055, radius2=0.055,
                               depth=0.10, matrix=Matrix.Translation((0, 0, 1.19)))

    # Head — slightly flattened sphere
    head_r = 0.145
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=head_r,
                                         matrix=Matrix.Translation((0, 0, 1.365)))
    for v in result['verts']:
        if (v.co - Vector((0, 0, 1.365))).length < head_r + 0.001:
            v.co.y *= 0.78  # flatten front-back

    # Oval faceplate (forward)
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=14, radius1=0.09, radius2=0.09,
                               depth=0.025,
                               matrix=Matrix.Translation((0, 0.155, 1.365))
                               @ Matrix.Scale(0.7, 4, (1, 0, 0))
                               @ Matrix.Scale(1.15, 4, (0, 0, 1)))

    # Head side vents
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=0.05,
                               matrix=Matrix.Translation((side * 0.15, 0, 1.36))
                               @ Matrix.Scale(0.25, 4, (1, 0, 0))
                               @ Matrix.Scale(0.5, 4, (0, 0, 1)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_ancient_machine_dark", "mat_gold_emissive", "mat_blue_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_HeliosRobot_Detailed_A")


# ---------------------------------------------------------------------------
# 3. Rift Creature — Silhouette A  —  SM_RiftCreature_Silhouette_A
#    Long-bodied, 4 radial tentacle arms, central bioluminescent core.
#    Inspired by concept "rift_creature_silhouettes": fluid, deep-sea-like.
#    ~1.4 m long body + arm spans.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_HeliosRobot_Detailed_A")
