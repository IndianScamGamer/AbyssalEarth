"""
SM_Sub_DecorPipes_Bundle_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Prologue')

def build():
    clear_scene()
    ob, me = new_mesh("SM_Sub_DecorPipes_Bundle_A")
    bm = bmesh.new()

    layout = [(-0.08, 0.00, 0.055), (0.08, 0.00, 0.055),
              (0.00, -0.08, 0.055), (0.00, 0.08, 0.055),
              (-0.04, -0.04, 0.035)]

    for px, py, pr in layout:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=pr, radius2=pr,
                                   depth=4.0,
                                   matrix=Matrix.Translation((px, py, 2.0))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Clamp bands every 1 m
    for cz in [0.5, 1.5, 2.5, 3.5]:
        bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False,
                                   segments=10, radius1=0.145, radius2=0.145,
                                   depth=0.06,
                                   matrix=Matrix.Translation((0, 0, cz)))

    finalise(ob, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Sub_DecorPipes_Bundle_A")


# ===========================================================================
# ELEVATOR SHAFT KIT
# ===========================================================================

# ---------------------------------------------------------------------------
# SM_Elevator_ShaftSection_A   (10 m shaft segment, square 4 × 4 m interior)
#   Guide rail channels on all 4 walls, cable run on back wall,
#   grating floor panel, bolt rings every 2 m.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Sub_DecorPipes_Bundle_A")
