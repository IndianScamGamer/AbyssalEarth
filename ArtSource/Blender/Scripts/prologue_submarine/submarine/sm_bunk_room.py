"""
SM_Sub_BunkRoom_Shell_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Sub_BunkRoom_Shell_A")
    bm = bmesh.new()

    W, D, H = 2.5, 4.0, 2.5

    # Outer shell (open-top box for interior)
    verts_box = [
        bm.verts.new((-W, 0, 0)),    # 0
        bm.verts.new(( W, 0, 0)),    # 1
        bm.verts.new(( W, D, 0)),    # 2
        bm.verts.new((-W, D, 0)),    # 3
        bm.verts.new((-W, 0, H)),    # 4
        bm.verts.new(( W, 0, H)),    # 5
        bm.verts.new(( W, D, H)),    # 6
        bm.verts.new((-W, D, H)),    # 7
    ]
    bm.faces.new([verts_box[0], verts_box[1], verts_box[2], verts_box[3]])  # floor
    bm.faces.new([verts_box[4], verts_box[5], verts_box[6], verts_box[7]])  # ceiling
    bm.faces.new([verts_box[0], verts_box[1], verts_box[5], verts_box[4]])  # front
    bm.faces.new([verts_box[2], verts_box[3], verts_box[7], verts_box[6]])  # back
    bm.faces.new([verts_box[0], verts_box[3], verts_box[7], verts_box[4]])  # left
    bm.faces.new([verts_box[1], verts_box[2], verts_box[6], verts_box[5]])  # right

    # Bunk alcoves left wall
    for row in range(2):
        bz = 0.30 + row * 1.10
        bmesh.ops.create_cube(bm, size=0.8,
                               matrix=Matrix.Translation((-W + 0.45, D * 0.3 + row * 0.2, bz + 0.4))
                               @ Matrix.Scale(1.05, 4, (0, 1, 0))
                               @ Matrix.Scale(0.28, 4, (1, 0, 0))
                               @ Matrix.Scale(0.55, 4, (0, 0, 1)))
        bmesh.ops.create_cube(bm, size=0.8,
                               matrix=Matrix.Translation((-W + 0.45, D * 0.65 - row * 0.2, bz + 0.4))
                               @ Matrix.Scale(1.05, 4, (0, 1, 0))
                               @ Matrix.Scale(0.28, 4, (1, 0, 0))
                               @ Matrix.Scale(0.55, 4, (0, 0, 1)))

    # Riveted panel lines — horizontal strips
    for i in range(5):
        strip_z = 0.5 * (i + 1)
        bmesh.ops.create_cube(bm, size=0.04,
                               matrix=Matrix.Translation((0, D * 0.5, strip_z))
                               @ Matrix.Scale(W * 2 / 0.04, 4, (1, 0, 0))
                               @ Matrix.Scale(0.5, 4, (0, 0, 1)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Sub_BunkRoom_Shell_A")


# ---------------------------------------------------------------------------
# SM_Sub_EngineRoom_Shell_A
#   6 × 6 × 3.5 m.  Central engine block (2 turbine cylinders side by side).
#   Conduit bundles on ceiling. Pressure gauge array.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Sub_BunkRoom_Shell_A")
