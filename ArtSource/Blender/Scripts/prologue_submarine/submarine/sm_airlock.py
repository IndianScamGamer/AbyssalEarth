"""
SM_Sub_AirlockChamber_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_Sub_AirlockChamber_A")
    bm = bmesh.new()

    R = 2.0   # inscribed radius
    H = 3.0
    SEGS = 8

    for z in [0.0, H]:
        for i in range(SEGS):
            ang = math.radians(i * 360 / SEGS + 22.5)
            bm.verts.new((math.cos(ang) * R, math.sin(ang) * R, z))

    bm.verts.ensure_lookup_table()
    v = bm.verts
    # Walls
    for i in range(SEGS):
        ni = (i + 1) % SEGS
        bm.faces.new([v[i], v[ni], v[SEGS + ni], v[SEGS + i]])
    # Ceiling
    ceil_verts = [v[SEGS + i] for i in range(SEGS)]
    bm.faces.new(ceil_verts)

    # Outer hatch ring
    bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                               segments=20, radius1=0.82, radius2=0.82,
                               depth=0.12,
                               matrix=Matrix.Translation((0, -R + 0.05, 0.80)))
    # Hatch dogs (locking lugs)
    for i in range(6):
        ang = math.radians(i * 60)
        bmesh.ops.create_cube(bm, size=0.08,
                               matrix=Matrix.Translation(
                                   (math.cos(ang) * 0.90, -R + 0.05 + math.sin(ang) * 0.90, 0.80))
                               @ Matrix.Scale(0.5, 4, (0, 0, 1)))

    # Warning stripe ring on floor
    bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                               segments=20, radius1=1.65, radius2=1.65,
                               depth=0.02,
                               matrix=Matrix.Translation((0, 0, 0.01)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_Sub_AirlockChamber_A")


# ---------------------------------------------------------------------------
# SM_Sub_DecorPipes_Bundle_A   (4 m straight pipe bundle)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Sub_AirlockChamber_A")
