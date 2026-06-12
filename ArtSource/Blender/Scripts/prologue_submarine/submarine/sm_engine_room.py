"""
SM_Sub_EngineRoom_Shell_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Sub_EngineRoom_Shell_A")
    bm = bmesh.new()

    W, D, H = 3.0, 6.0, 3.5

    # Room shell
    for corner, is_top in [
        ((-W, 0, 0), False), ((W, 0, 0), False),
        ((W, D, 0), False), ((-W, D, 0), False),
        ((-W, 0, H), True), ((W, 0, H), True),
        ((W, D, H), True), ((-W, D, H), True),
    ]:
        bm.verts.new(corner)

    bm.verts.ensure_lookup_table()
    v = bm.verts
    bm.faces.new([v[0], v[1], v[2], v[3]])   # floor
    bm.faces.new([v[4], v[5], v[6], v[7]])   # ceiling
    bm.faces.new([v[0], v[1], v[5], v[4]])   # front
    bm.faces.new([v[2], v[3], v[7], v[6]])   # back
    bm.faces.new([v[0], v[3], v[7], v[4]])   # left
    bm.faces.new([v[1], v[2], v[6], v[5]])   # right

    # Engine turbines
    for side in [-0.9, 0.9]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=16, radius1=0.55, radius2=0.55,
                                   depth=2.0,
                                   matrix=Matrix.Translation((side, D * 0.45, 1.0))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))
        # Turbine front intake cowl
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=16, radius1=0.65, radius2=0.45,
                                   depth=0.35,
                                   matrix=Matrix.Translation((side, D * 0.45 - 1.17, 1.0))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))
        # Turbine exhaust port
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=12, radius1=0.40, radius2=0.55,
                                   depth=0.28,
                                   matrix=Matrix.Translation((side, D * 0.45 + 1.14, 1.0))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Central drive shaft
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius1=0.12, radius2=0.12,
                               depth=D * 0.7,
                               matrix=Matrix.Translation((0, D * 0.45, 0.65))
                               @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Conduit bundle ceiling
    for cx in [-1.5, -0.5, 0.5, 1.5]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius1=0.06, radius2=0.06,
                                   depth=D,
                                   matrix=Matrix.Translation((cx, D * 0.5, H - 0.20))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Pressure gauge array panel
    bmesh.ops.create_cube(bm, size=1.0,
                           matrix=Matrix.Translation((0, 0.06, 1.8))
                           @ Matrix.Scale(2.4, 4, (1, 0, 0))
                           @ Matrix.Scale(0.06, 4, (0, 1, 0))
                           @ Matrix.Scale(1.2, 4, (0, 0, 1)))
    for gx in [-0.80, -0.26, 0.26, 0.80]:
        for gz in [1.3, 1.85]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=12, radius1=0.10, radius2=0.10,
                                       depth=0.05,
                                       matrix=Matrix.Translation((gx, 0.10, gz)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt", "mat_gold_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Sub_EngineRoom_Shell_A")


# ---------------------------------------------------------------------------
# SM_Sub_AirlockChamber_A
#   4 × 4 × 3 m octagonal room with outer hatch (open bottom for water entry).
#   Inner door frame + outer circular hatch ring. Warning stripes on floor.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Sub_EngineRoom_Shell_A")
