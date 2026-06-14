"""
SM_Elevator_EmergencyStrip_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('ElevatorShaft')


def build():
    """Red emergency light strip — 2m wall-mount channel with 5 lit segments
    and end caps; one segment dark (failed). The red practical lighting of
    the crashed elevator interior concept."""
    obj, bm = new_mesh("SM_Elevator_EmergencyStrip_A")
    L = 2.0
    # mounting channel
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.02, 0.06))
        @ Matrix.Scale(L, 4, (1, 0, 0))
        @ Matrix.Scale(0.04, 4, (0, 1, 0))
        @ Matrix.Scale(0.12, 4, (0, 0, 1)))
    # 5 light segments (slot 3 is the dead one — same geometry, second
    # material slot lets the editor assign it unlit)
    for s in range(5):
        sx = -L / 2 + 0.2 + s * 0.4
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((sx, -0.005, 0.06))
            @ Matrix.Scale(0.30, 4, (1, 0, 0))
            @ Matrix.Scale(0.015, 4, (0, 1, 0))
            @ Matrix.Scale(0.07, 4, (0, 0, 1)))
    # end caps
    for ex in [-L / 2, L / 2]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((ex, 0.01, 0.06))
            @ Matrix.Scale(0.05, 4, (1, 0, 0))
            @ Matrix.Scale(0.06, 4, (0, 1, 0))
            @ Matrix.Scale(0.14, 4, (0, 0, 1)))
    # conduit stub from one end
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
        radius1=0.015, radius2=0.015, depth=0.30,
        matrix=Matrix.Translation((L / 2 + 0.15, 0.02, 0.06))
        @ Matrix.Rotation(TAU / 4, 4, 'Y'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_red_emissive_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Elevator_EmergencyStrip_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Elevator_EmergencyStrip_A")
