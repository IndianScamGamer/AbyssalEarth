"""
SM_Elevator_Car_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Elevator_Car_A")
    bm = bmesh.new()

    W, D, H = 1.75, 1.75, 3.0

    # Floor
    bm.faces.new([bm.verts.new(c) for c in
                   [(-W, -D, 0), (W, -D, 0), (W, D, 0), (-W, D, 0)]])
    # Three solid walls
    for ax, ay, bx, by in [
        (-W, -D, W, -D),   # front (grate) — solid placeholder
        (W, -D,  W,  D),   # right
        (-W, D, -W, -D),   # left
    ]:
        v0 = bm.verts.new((ax, ay, 0))
        v1 = bm.verts.new((bx, by, 0))
        v2 = bm.verts.new((bx, by, H))
        v3 = bm.verts.new((ax, ay, H))
        bm.faces.new([v0, v1, v2, v3])
    # Back wall
    v0 = bm.verts.new((-W, D, 0))
    v1 = bm.verts.new(( W, D, 0))
    v2 = bm.verts.new(( W, D, H))
    v3 = bm.verts.new((-W, D, H))
    bm.faces.new([v0, v1, v2, v3])

    # Diamond plate rows on floor
    for row in range(6):
        for col in range(6):
            cx = -W + 0.28 + col * 0.50
            cy = -D + 0.28 + row * 0.55
            bmesh.ops.create_cube(bm, size=0.10,
                                   matrix=Matrix.Translation((cx, cy, 0.02))
                                   @ Matrix.Rotation(math.radians(45), 4, 'Z')
                                   @ Matrix.Scale(0.20, 4, (0, 0, 1)))

    # Grate front (4×3 grid of openings as bars)
    for gx in range(5):
        bmesh.ops.create_cube(bm, size=0.08,
                               matrix=Matrix.Translation((-W + 0.35 + gx * 0.70, -D, H * 0.5))
                               @ Matrix.Scale(0.25, 4, (1, 0, 0))
                               @ Matrix.Scale(H / 0.08, 4, (0, 0, 1)))

    # Speed indicator panel
    bmesh.ops.create_cube(bm, size=0.35,
                           matrix=Matrix.Translation((W - 0.18, D - 0.04, 1.5))
                           @ Matrix.Scale(0.5, 4, (1, 0, 0))
                           @ Matrix.Scale(0.10, 4, (0, 1, 0))
                           @ Matrix.Scale(1.2, 4, (0, 0, 1)))
    # LED depth counter strip
    bmesh.ops.create_cube(bm, size=0.12,
                           matrix=Matrix.Translation((W - 0.18, D - 0.08, 1.5))
                           @ Matrix.Scale(0.35, 4, (1, 0, 0))
                           @ Matrix.Scale(0.04, 4, (0, 1, 0))
                           @ Matrix.Scale(0.6, 4, (0, 0, 1)))

    finalise(ob, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_ancient_machine_dark", "mat_gold_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Elevator_Car_A")


# ---------------------------------------------------------------------------
# SM_Elevator_CrashedCar_A   (same cabin, crumpled lower half)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Elevator_Car_A")
