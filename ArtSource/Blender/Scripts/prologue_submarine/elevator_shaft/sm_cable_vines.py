"""
SM_Elevator_CableVines_A — AbyssalEarth procedural mesh.
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
    """Tangled cable-vine drape — torn cables hanging and snaking across a
    4m span, the dominant texture of the crashed elevator interior concept.
    Place along walls, ceiling, and floor of the wreck."""
    random.seed(510)
    obj, bm = new_mesh("SM_Elevator_CableVines_A")
    # 7 drooping ceiling-to-floor cable runs (catenary sphere chains)
    for c in range(7):
        x0 = random.uniform(-2.0, 2.0)
        x1 = x0 + random.uniform(-1.2, 1.2)
        z0 = random.uniform(2.2, 2.8)
        sag = random.uniform(0.8, 1.8)
        r = random.uniform(0.025, 0.055)
        SEGS = 14
        for s in range(SEGS):
            t = s / (SEGS - 1)
            x = x0 + (x1 - x0) * t
            y = random.uniform(-0.1, 0.1) + (c - 3) * 0.35
            z = z0 * (1 - t) + math.sin(t * PI) * -sag + 0.05 * t
            z = max(z, 0.03)
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r,
                matrix=Matrix.Translation((x, y, z)))
    # 4 floor-snaking cable runs
    for c in range(4):
        y0 = -1.2 + c * 0.8
        SEGS = 12
        for s in range(SEGS):
            t = s / (SEGS - 1)
            x = -2.0 + t * 4.0
            y = y0 + math.sin(t * TAU * 1.5 + c) * 0.3
            bmesh.ops.create_icosphere(bm, subdivisions=1,
                radius=random.uniform(0.03, 0.05),
                matrix=Matrix.Translation((x, y, 0.04)))
    # torn cable ends with frayed connector blocks
    for e in range(3):
        ex = random.uniform(-1.5, 1.5)
        ey = random.uniform(-1.0, 1.0)
        ez = random.uniform(0.8, 2.0)
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((ex, ey, ez))
            @ Matrix.Rotation(random.uniform(0, TAU), 4, 'Z')
            @ Matrix.Scale(0.10, 4, (1, 0, 0))
            @ Matrix.Scale(0.07, 4, (0, 1, 0))
            @ Matrix.Scale(0.06, 4, (0, 0, 1)))
        # frayed strands
        for f in range(3):
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=4,
                radius1=0.008, radius2=0.008, depth=0.15,
                matrix=Matrix.Translation((ex + random.uniform(-0.05, 0.05),
                                            ey + random.uniform(-0.05, 0.05),
                                            ez - 0.10))
                @ Matrix.Rotation(random.uniform(-0.5, 0.5), 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Elevator_CableVines_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Elevator_CableVines_A")
