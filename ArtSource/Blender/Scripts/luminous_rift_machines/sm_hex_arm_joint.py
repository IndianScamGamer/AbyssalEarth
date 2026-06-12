"""
SM_Rift_HexCollector_ArmJoint_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('LuminousRift')


def build():
    """Articulated arm joint connecting hex collector tiles — twin-cylinder
    elbow with piston rod and gold clamp heads. Concept: AD-002 detail sheet.
    Placed at tile corners where clusters articulate."""
    obj, bm = new_mesh("SM_Rift_HexCollector_ArmJoint_A")
    # elbow hub: twin coaxial cylinders
    for off in [-0.09, 0.09]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=12,
            radius=0.14, depth=0.10,
            matrix=Matrix.Translation((off, 0, 0.30))
            @ Matrix.Rotation(TAU/4, 4, 'Y'))
    # central pivot pin
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.05, depth=0.34,
        matrix=Matrix.Translation((0, 0, 0.30))
        @ Matrix.Rotation(TAU/4, 4, 'Y'))
    # upper arm strut (angled up to tile A)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.28, 0.46))
        @ Matrix.Rotation(0.55, 4, 'X')
        @ Matrix.Scale(0.10, 4, (1, 0, 0))
        @ Matrix.Scale(0.62, 4, (0, 1, 0))
        @ Matrix.Scale(0.07, 4, (0, 0, 1)))
    # lower arm strut (angled down to tile B)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, -0.28, 0.16))
        @ Matrix.Rotation(-0.45, 4, 'X')
        @ Matrix.Scale(0.10, 4, (1, 0, 0))
        @ Matrix.Scale(0.60, 4, (0, 1, 0))
        @ Matrix.Scale(0.07, 4, (0, 0, 1)))
    # piston rod alongside upper strut
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.025, depth=0.50,
        matrix=Matrix.Translation((0.10, 0.24, 0.44))
        @ Matrix.Rotation(0.55, 4, 'X'))
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.04, depth=0.22,
        matrix=Matrix.Translation((0.10, 0.10, 0.34))
        @ Matrix.Rotation(0.55, 4, 'X'))
    # clamp heads at both strut ends (grip the tile frames)
    for end_y, end_z, rot in [(0.55, 0.66, 0.55), (-0.55, 0.02, -0.45)]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, end_y, end_z))
            @ Matrix.Rotation(rot, 4, 'X')
            @ Matrix.Scale(0.16, 4, (1, 0, 0))
            @ Matrix.Scale(0.10, 4, (0, 1, 0))
            @ Matrix.Scale(0.14, 4, (0, 0, 1)))
        # clamp jaw teeth
        for tooth in [-1, 1]:
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((tooth * 0.06, end_y, end_z + 0.09))
                @ Matrix.Rotation(rot, 4, 'X')
                @ Matrix.Scale(0.035, 4, (1, 0, 0))
                @ Matrix.Scale(0.09, 4, (0, 1, 0))
                @ Matrix.Scale(0.05, 4, (0, 0, 1)))
    # detail bolts on hub faces
    for off in [-0.155, 0.155]:
        for i in range(4):
            a = i * TAU / 4
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.018,
                matrix=Matrix.Translation((off, math.cos(a) * 0.09,
                                            0.30 + math.sin(a) * 0.09)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_gold_emissive", "mat_ancient_machine_dark",
                        "mat_ancient_machine_edge_wear"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_HexCollector_ArmJoint_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Rift_HexCollector_ArmJoint_A")
