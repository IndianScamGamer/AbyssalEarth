"""
SM_GravityWell_GuideCable_Span_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GravityWell')


def build():
    """Guide cable span — 12m sagging traversal cable with anchor posts at
    both ends and 3 marker flags. Strung between floating platforms in
    GW-002; the player's visual route line through zero-g jumps."""
    random.seed(630)
    obj, bm = new_mesh("SM_GravityWell_GuideCable_Span_A")
    L = 12.0
    # anchor posts (piton + eye ring)
    for px in [-L / 2, L / 2]:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
            radius1=0.07, radius2=0.07, depth=0.7,
            matrix=Matrix.Translation((px, 0, 0.35)))
        for s in range(6):
            sa = s * TAU / 6
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.030,
                matrix=Matrix.Translation((px, math.cos(sa) * 0.10,
                                            0.78 + math.sin(sa) * 0.10)))
    # main cable: catenary chain of spheres
    SEGS = 30
    for s in range(SEGS):
        t = (s + 0.5) / SEGS
        x = -L / 2 + t * L
        sag = math.sin(t * PI) * 1.1
        wobble = math.sin(t * TAU * 2.0) * 0.06
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.045,
            matrix=Matrix.Translation((x, wobble, 0.78 - sag)))
    # 3 marker flags clipped onto the cable
    for ft in [0.25, 0.5, 0.75]:
        fx = -L / 2 + ft * L
        fz = 0.78 - math.sin(ft * PI) * 1.1
        # clip
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
            radius1=0.05, radius2=0.05, depth=0.06,
            matrix=Matrix.Translation((fx, 0, fz)))
        # small triangular flag hanging below
        v0 = bm.verts.new((fx, 0.0, fz - 0.05))
        v1 = bm.verts.new((fx + 0.22, 0.0, fz - 0.12))
        v2 = bm.verts.new((fx, 0.0, fz - 0.28))
        bm.faces.new([v0, v1, v2])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_GuideCable_Span_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_GravityWell_GuideCable_Span_A")
