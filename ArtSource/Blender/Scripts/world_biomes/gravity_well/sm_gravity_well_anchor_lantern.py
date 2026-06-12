"""
SM_GravityWell_AnchorLantern_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GravityWell')


def build():
    """Anchor lantern — 60cm expedition platform marker: spiked stake, caged
    amber lamp, ground hook. The warm waypoint lights dotting the floating
    platforms in GW-002."""
    obj, bm = new_mesh("SM_GravityWell_AnchorLantern_A")
    # spiked stake
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
        radius=0.020, depth=0.40,
        matrix=Matrix.Translation((0, 0, 0.20)))
    tip_ring = [bm.verts.new((math.cos(i * TAU / 6) * 0.018,
                               math.sin(i * TAU / 6) * 0.018, 0.02))
                for i in range(6)]
    tip = bm.verts.new((0, 0, -0.06))
    for i in range(6):
        bm.faces.new([tip_ring[i], tip_ring[(i + 1) % 6], tip])
    # lamp housing: short cylinder with cage bars
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=10,
        radius=0.075, depth=0.13,
        matrix=Matrix.Translation((0, 0, 0.47)))
    for i in range(4):
        a = i * TAU / 4
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=4,
            radius=0.006, depth=0.15,
            matrix=Matrix.Translation((math.cos(a) * 0.078,
                                        math.sin(a) * 0.078, 0.47)))
    # lamp cap + hanging hook
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.085, depth=0.025,
        matrix=Matrix.Translation((0, 0, 0.545)))
    for s in range(4):
        sa = PI * s / 3
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.015,
            matrix=Matrix.Translation((math.cos(sa) * 0.04, 0,
                                        0.56 + math.sin(sa) * 0.04)))
    # ground hook fin (keeps it anchored in low-g)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0.06, 0, 0.06))
        @ Matrix.Rotation(0.6, 4, 'Y')
        @ Matrix.Scale(0.10, 4, (1, 0, 0))
        @ Matrix.Scale(0.015, 4, (0, 1, 0))
        @ Matrix.Scale(0.05, 4, (0, 0, 1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_AnchorLantern_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_GravityWell_AnchorLantern_A")
