"""
SM_Rift_StairRamp_A — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-010, LR-014
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
    """Ancient stepped ramp — 8 broad stone-machine steps climbing 3m over
    8m, linking platform tiers. Concept: bridge kit connectors."""
    random.seed(421)
    obj, bm = new_mesh("SM_Rift_StairRamp_A")
    STEPS = 8
    W = 3.5
    RUN, RISE = 1.0, 0.375
    for s in range(STEPS):
        y = s * RUN
        z = s * RISE
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, y + RUN/2, z + RISE/2))
            @ Matrix.Scale(W, 4, (1,0,0))
            @ Matrix.Scale(RUN + 0.08, 4, (0,1,0))
            @ Matrix.Scale(RISE, 4, (0,0,1)))
        # worn edge chamfer detail (thin strip on nose)
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, y + 0.04, z + RISE - 0.03))
            @ Matrix.Scale(W*0.98, 4, (1,0,0))
            @ Matrix.Scale(0.10, 4, (0,1,0))
            @ Matrix.Scale(0.05, 4, (0,0,1)))
    # side stringer walls
    for side in [-1, 1]:
        for s in range(STEPS):
            y = s * RUN
            z = s * RISE
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((side*(W/2 + 0.12), y + RUN/2, z*0.5 + RISE))
                @ Matrix.Scale(0.24, 4, (1,0,0))
                @ Matrix.Scale(RUN, 4, (0,1,0))
                @ Matrix.Scale(z + RISE*2, 4, (0,0,1)))
    # blue guide strip up the centre
    for s in range(STEPS):
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, s*RUN + RUN/2, s*RISE + RISE + 0.005))
            @ Matrix.Scale(0.15, 4, (1,0,0))
            @ Matrix.Scale(RUN*0.8, 4, (0,1,0))
            @ Matrix.Scale(0.01, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_StairRamp_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Rift_StairRamp_A")
