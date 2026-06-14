"""
SM_Elevator_Mechanism_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Elevator_Mechanism_A")
    bm = bmesh.new()

    # Structural arch frame (two vertical pillars + cross beam)
    for sx in [-2.2, 2.2]:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.22, radius2=0.22,
                                   depth=4.0,
                                   matrix=Matrix.Translation((sx, 0, 2.0)))
    # Cross beam
    bmesh.ops.create_cube(bm, size=0.40,
                           matrix=Matrix.Translation((0, 0, 4.20))
                           @ Matrix.Scale(4.4 / 0.40, 4, (1, 0, 0))
                           @ Matrix.Scale(0.8, 4, (0, 1, 0)))

    # Two large gear wheels
    for gx in [-1.2, 1.2]:
        GEAR_SEGS = 16
        for i in range(GEAR_SEGS):
            ang = math.radians(i * 360 / GEAR_SEGS)
            next_ang = math.radians((i + 1) * 360 / GEAR_SEGS)
            bmesh.ops.create_cube(bm, size=0.18,
                                   matrix=Matrix.Translation(
                                       (gx + math.cos(ang) * 0.72,
                                        math.sin(ang) * 0.12,
                                        3.50 + math.sin(ang) * 0.72))
                                   @ Matrix.Rotation(ang, 4, 'X')
                                   @ Matrix.Scale(0.5, 4, (0, 1, 0))
                                   @ Matrix.Scale(2.0, 4, (0, 0, 1)))
        # Gear hub
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=16, radius1=0.60, radius2=0.60,
                                   depth=0.18,
                                   matrix=Matrix.Translation((gx, 0, 3.50))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.18, radius2=0.18,
                                   depth=0.24,
                                   matrix=Matrix.Translation((gx, 0, 3.50))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Counterweight block
    bmesh.ops.create_cube(bm, size=1.0,
                           matrix=Matrix.Translation((0, -1.60, 1.80))
                           @ Matrix.Scale(1.4, 4, (1, 0, 0))
                           @ Matrix.Scale(0.80, 4, (0, 1, 0))
                           @ Matrix.Scale(2.2, 4, (0, 0, 1)))
    # Weight detail bands
    for wz in [0.70, 1.20, 1.70, 2.20, 2.70]:
        bmesh.ops.create_cube(bm, size=0.05,
                               matrix=Matrix.Translation((0, -1.60, wz))
                               @ Matrix.Scale(1.5 / 0.05, 4, (1, 0, 0))
                               @ Matrix.Scale(0.85 / 0.05, 4, (0, 1, 0)))

    # Cable (twin cylinders from counterweight to gears)
    for cx in [-0.30, 0.30]:
        bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False,
                                   segments=5, radius1=0.025, radius2=0.025,
                                   depth=2.60,
                                   matrix=Matrix.Translation((cx, -1.60, 3.10)))

    # Ancient machine emissive nodes on beam
    for nx in [-1.8, -0.6, 0.6, 1.8]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.09,
                                    matrix=Matrix.Translation((nx, 0, 4.28)))

    finalise(ob, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_ancient_machine_dark", "mat_gold_emissive", "mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Elevator_Mechanism_A")


# ---------------------------------------------------------------------------
# SM_Elevator_ShaftDebris_A   (rubble pile + bent rail section)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Elevator_Mechanism_A")
