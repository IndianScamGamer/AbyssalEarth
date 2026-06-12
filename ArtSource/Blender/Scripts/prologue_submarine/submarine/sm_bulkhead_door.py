"""
SM_Sub_BulkheadDoor_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Sub_BulkheadDoor_A")
    bm = bmesh.new()

    # Frame wall panel
    for corner in [(-1.2, 0), (1.2, 0), (1.2, 2.8), (-1.2, 2.8)]:
        bm.verts.new((corner[0], 0.0, corner[1]))
        bm.verts.new((corner[0], 0.06, corner[1]))
    bm.verts.ensure_lookup_table()
    v = bm.verts
    bm.faces.new([v[0], v[2], v[4], v[6]])   # front face
    bm.faces.new([v[1], v[3], v[5], v[7]])   # back face
    bm.faces.new([v[0], v[1], v[3], v[2]])   # bottom
    bm.faces.new([v[4], v[5], v[7], v[6]])   # top
    bm.faces.new([v[0], v[1], v[5], v[4]])   # left
    bm.faces.new([v[2], v[3], v[7], v[6]])   # right

    # Door oval (12 segs)
    SEGS = 14
    for i in range(SEGS):
        ang = math.radians(i * 360 / SEGS)
        x = math.cos(ang) * 0.52
        z = math.sin(ang) * 0.90 + 1.10  # centred at z=1.1
        bm.verts.new((x, -0.04, z))
        bm.verts.new((x, -0.10, z))
    bm.verts.ensure_lookup_table()
    # Door faces
    base = 16
    for i in range(SEGS):
        ni = (i + 1) % SEGS
        bm.faces.new([v[base + i*2], v[base + i*2 + 1],
                       v[base + ni*2 + 1], v[base + ni*2]])

    # Wheel handle
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=12, radius1=0.28, radius2=0.28,
                               depth=0.04,
                               matrix=Matrix.Translation((0, -0.14, 1.10)))
    # Spokes
    for i in range(4):
        ang = math.radians(i * 45)
        sx = math.cos(ang) * 0.22
        sz = math.sin(ang) * 0.22
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=4, radius1=0.018, radius2=0.018,
                                   depth=0.44,
                                   matrix=Matrix.Translation((0, -0.16, 1.10))
                                   @ Matrix.Rotation(ang, 4, 'Y'))

    # Hinge bolts
    for bz in [0.35, 1.10, 1.85]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.04,
                                    matrix=Matrix.Translation((-0.56, -0.10, bz)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Sub_BulkheadDoor_A")


# ---------------------------------------------------------------------------
# SM_Sub_BunkRoom_Shell_A
#   Room shell: 5 × 4 × 2.5 m box, no floor (sits on ground).
#   Interior bunk alcoves each side (2 per side, stacked).
#   Riveted panel detail on walls.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Sub_BulkheadDoor_A")
