"""
SM_Elevator_CrashedCar_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Elevator_CrashedCar_A")
    bm = bmesh.new()

    W, D, H = 1.75, 1.75, 3.0

    # Intact upper half
    for ax, ay, bx, by in [
        (-W, -D, W, -D),
        (W, -D,  W,  D),
        (-W, D, -W, -D),
    ]:
        v0 = bm.verts.new((ax, ay, H * 0.5))
        v1 = bm.verts.new((bx, by, H * 0.5))
        v2 = bm.verts.new((bx, by, H))
        v3 = bm.verts.new((ax, ay, H))
        bm.faces.new([v0, v1, v2, v3])

    # Crumpled lower half — irregular verts

    random.seed(42)
    for ax, ay, bx, by in [
        (-W, -D, W, -D),
        (W, -D,  W,  D),
        (-W, D, -W, -D),
    ]:
        for step in range(5):
            t = step / 4.0
            t2 = (step + 1) / 4.0
            rx1 = random.uniform(-0.15, 0.15)
            rz1 = random.uniform(-0.08, 0.08)
            rx2 = random.uniform(-0.15, 0.15)
            rz2 = random.uniform(-0.08, 0.08)
            v0 = bm.verts.new((ax + (bx - ax) * t + rx1, ay + (by - ay) * t + rx1, H * 0.5 * t + rz1))
            v1 = bm.verts.new((ax + (bx - ax) * t2 + rx2, ay + (by - ay) * t2 + rx2, H * 0.5 * t2 + rz2))
            v2 = bm.verts.new((ax + (bx - ax) * t2 + rx2, ay + (by - ay) * t2 + rx2, H * 0.5 * (t2 - 0.25) + rz2))
            v3 = bm.verts.new((ax + (bx - ax) * t + rx1, ay + (by - ay) * t + rx1, H * 0.5 * (t - 0.25) + rz1))
            try:
                bm.faces.new([v0, v1, v2, v3])
            except Exception:
                pass

    # Debris slab (floor panel broken, tilted)
    bmesh.ops.create_cube(bm, size=1.0,
                           matrix=Matrix.Translation((0.3, 0.2, 0.15))
                           @ Matrix.Rotation(math.radians(22), 4, 'X')
                           @ Matrix.Rotation(math.radians(15), 4, 'Z')
                           @ Matrix.Scale(W * 1.4, 4, (1, 0, 0))
                           @ Matrix.Scale(D * 1.4, 4, (0, 1, 0))
                           @ Matrix.Scale(0.08, 4, (0, 0, 1)))

    finalise(ob, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Elevator_CrashedCar_A")


# ---------------------------------------------------------------------------
# SM_Elevator_Mechanism_A
#   Large counterweight + pulley block at top of shaft, 6 × 6 × 4 m.
#   Ancient machine aesthetic: arched frame, huge gear wheels, chain loops.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Elevator_CrashedCar_A")
