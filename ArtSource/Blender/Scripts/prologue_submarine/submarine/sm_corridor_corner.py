"""
SM_Sub_CorridorSection_Corner_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Sub_CorridorSection_Corner_A")
    bm = bmesh.new()

    W, H = 1.4, 1.2
    ARM = 2.0  # arm length

    # Arm along +Y (forward)
    for z in [0.0, ARM]:
        for (x, y) in [(-W, z), (W, z)]:
            bm.verts.new((x, y, 0))
            bm.verts.new((x, y, H))

    # Arm along +X (right)
    for x in [ARM, ARM + ARM]:
        for (xi, y) in [(x, 0), (x, W)]:
            bm.verts.new((xi, y, 0))
            bm.verts.new((xi, y, H))

    # Connect with simple quads (simplified box corridors)
    bm.verts.ensure_lookup_table()
    v = bm.verts

    # Y-arm floor & ceiling quad
    bm.faces.new([v[0], v[2], v[6], v[4]])   # floor
    bm.faces.new([v[1], v[3], v[7], v[5]])   # ceiling
    # Left wall
    bm.faces.new([v[0], v[1], v[5], v[4]])
    # Right wall segment
    bm.faces.new([v[2], v[3], v[7], v[6]])

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Sub_CorridorSection_Corner_A")


# ---------------------------------------------------------------------------
# SM_Sub_BulkheadDoor_A
#   Oval pressure door in frame.  Frame is 2.4 × 2.8 m wall segment.
#   Door oval: 1.0 × 1.8 m. Locking wheel handle. Hinge bolts.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Sub_CorridorSection_Corner_A")
