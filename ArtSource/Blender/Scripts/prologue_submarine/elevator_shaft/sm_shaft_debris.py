"""
SM_Elevator_ShaftDebris_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Elevator_ShaftDebris_A")
    bm = bmesh.new()

    random.seed(77)

    # Rock chunks
    for i in range(8):
        px = random.uniform(-1.2, 1.2)
        py = random.uniform(-1.2, 1.2)
        rs = random.uniform(0.15, 0.45)
        result = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=rs,
                                             matrix=Matrix.Translation((px, py, rs * 0.5)))
        for v in result['verts']:
            v.co += Vector((random.uniform(-0.05, 0.05),
                            random.uniform(-0.05, 0.05),
                            random.uniform(-0.04, 0.04)))

    # Bent rail section
    for i in range(8):
        t = i / 7.0
        seg_x = -1.0 + t * 2.0
        seg_z = math.sin(t * math.pi) * 0.4 + 0.05
        bmesh.ops.create_cube(bm, size=0.08,
                               matrix=Matrix.Translation((seg_x, 0, seg_z))
                               @ Matrix.Scale(0.35, 4, (1, 0, 0))
                               @ Matrix.Scale(0.5, 4, (0, 0, 1)))

    # Torn cable coil
    CABLE_SEGS = 12
    for i in range(CABLE_SEGS):
        t = i / (CABLE_SEGS - 1)
        ang = t * math.pi * 3
        cx = math.cos(ang) * (0.35 - t * 0.1)
        cy = math.sin(ang) * (0.35 - t * 0.1)
        cz = t * 0.5
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius1=0.022, radius2=0.022,
                                   depth=0.18,
                                   matrix=Matrix.Translation((cx, cy, cz)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_wet_basalt", "mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Elevator_ShaftDebris_A")


# ===========================================================================
# Main
# ===========================================================================

if __name__ == "__main__":
    print("=== gen_prologue_submarine.py ===")

    print("[Sub 1/6] SM_Sub_CorridorSection_Straight_A ...")
    build_corridor_straight()

    print("[Sub 2/6] SM_Sub_CorridorSection_Corner_A ...")
    build_corridor_corner()

    print("[Sub 3/6] SM_Sub_BulkheadDoor_A ...")
    build_bulkhead_door()

    print("[Sub 4/6] SM_Sub_BunkRoom_Shell_A ...")
    build_bunk_room()

    print("[Sub 5/6] SM_Sub_EngineRoom_Shell_A ...")
    build_engine_room()

    print("[Sub 6/6] SM_Sub_AirlockChamber_A ...")
    build_airlock()

    print("[Sub Decor] SM_Sub_DecorPipes_Bundle_A ...")
    build_pipe_bundle()

    print("[Elev 1/4] SM_Elevator_ShaftSection_A ...")
    build_shaft_section()

    print("[Elev 2/4] SM_Elevator_Car_A ...")
    build_elevator_car()

    print("[Elev 3/4] SM_Elevator_CrashedCar_A ...")
    build_crashed_car()

    print("[Elev 4/4] SM_Elevator_Mechanism_A ...")
    build_elevator_mechanism()

    print("[Elev Debris] SM_Elevator_ShaftDebris_A ...")
    build_shaft_debris()

    print("=== gen_prologue_submarine.py COMPLETE ===")
    print(f"Prologue → {EXPORT_DIR}")
    print(f"Elevator → {EXPORT_DIR}")

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Elevator_ShaftDebris_A")
