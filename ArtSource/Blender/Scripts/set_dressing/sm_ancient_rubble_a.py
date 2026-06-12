"""
SM_Ancient_Rubble_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('SetDressing')

def build():
    """Ancient machine rubble pile — broken dark-metal fragments, 1.2m spread."""
    random.seed(205)
    obj, bm = new_mesh("SM_Ancient_Rubble_A")
    # angular machine fragments at random orientations
    for i in range(7):
        px = random.uniform(-0.5, 0.5)
        py = random.uniform(-0.5, 0.5)
        s = random.uniform(0.12, 0.35)
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((px, py, s * 0.4))
            @ Matrix.Rotation(random.uniform(0, TAU), 4, 'Z')
            @ Matrix.Rotation(random.uniform(-0.4, 0.4), 4, 'X')
            @ Matrix.Scale(s, 4, (1,0,0))
            @ Matrix.Scale(s * random.uniform(0.5, 1.2), 4, (0,1,0))
            @ Matrix.Scale(s * random.uniform(0.2, 0.5), 4, (0,0,1)))
    # one recognisable curved shell piece
    SEGS = 8
    for s in range(SEGS):
        a = s * (TAU / 4) / SEGS
        bmesh.ops.create_cube(bm, size=0.10,
            matrix=Matrix.Translation((0.1 + math.cos(a)*0.35,
                                        -0.15, 0.05 + math.sin(a)*0.35))
            @ Matrix.Rotation(a, 4, 'Y'))
    # faint emissive vein fragment
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((-0.2, 0.25, 0.05))
        @ Matrix.Scale(0.30, 4, (1,0,0))
        @ Matrix.Scale(0.02, 4, (0,1,0))
        @ Matrix.Scale(0.02, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Ancient_Rubble_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Ancient_Rubble_A")
