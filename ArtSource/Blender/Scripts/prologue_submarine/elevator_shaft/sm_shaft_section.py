"""
SM_Elevator_ShaftSection_A — AbyssalEarth procedural mesh.
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
    clear_scene()
    ob, me = new_mesh("SM_Elevator_ShaftSection_A")
    bm = bmesh.new()

    W = 2.0   # half-width
    H = 10.0

    # Four walls
    walls = [
        ((-W, -W), (W, -W)),   # front
        ((W, -W),  (W,  W)),   # right
        ((W,  W),  (-W, W)),   # back
        ((-W, W),  (-W, -W)),  # left
    ]
    for (ax, ay), (bx, by) in walls:
        v0 = bm.verts.new((ax, ay, 0))
        v1 = bm.verts.new((bx, by, 0))
        v2 = bm.verts.new((bx, by, H))
        v3 = bm.verts.new((ax, ay, H))
        bm.faces.new([v0, v1, v2, v3])

    # Guide rail channels (front-left and front-right)
    for rx in [-W + 0.15, W - 0.15]:
        bmesh.ops.create_cube(bm, size=0.10,
                               matrix=Matrix.Translation((rx, -W, H * 0.5))
                               @ Matrix.Scale(0.6, 4, (1, 0, 0))
                               @ Matrix.Scale(H / 0.10, 4, (0, 0, 1)))

    # Cable run — back wall
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=6, radius1=0.045, radius2=0.045,
                               depth=H,
                               matrix=Matrix.Translation((0, W - 0.12, H * 0.5)))

    # Bolt rings
    for bz in [0.0, 2.5, 5.0, 7.5, 10.0]:
        for (ax, ay), (bx, by) in walls:
            v0 = bm.verts.new((ax * 1.015, ay * 1.015, bz))
            v1 = bm.verts.new((bx * 1.015, by * 1.015, bz))
            v2 = bm.verts.new((bx * 1.015, by * 1.015, bz + 0.06))
            v3 = bm.verts.new((ax * 1.015, ay * 1.015, bz + 0.06))
            bm.faces.new([v0, v1, v2, v3])

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_ancient_machine_dark", "mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, ELEVATOR_DIR, "SM_Elevator_ShaftSection_A")


# ---------------------------------------------------------------------------
# SM_Elevator_Car_A  (the elevator cabin, 3.5 × 3.5 × 3 m)
#   Open top, three solid walls, one grate front.
#   Floor: diamond-plate pattern. Speed indicator panel.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Elevator_ShaftSection_A")
