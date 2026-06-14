"""
SM_Kelp_Strand_A — AbyssalEarth procedural mesh.
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
    """Bioluminescent kelp strand — 2.5m swaying flora for Inner Sea / Rift."""
    random.seed(204)
    obj, bm = new_mesh("SM_Kelp_Strand_A")
    # main stem: chain of segments with slight S-curve
    SEGS = 12
    for i in range(SEGS):
        t = i / (SEGS - 1)
        sx = math.sin(t * PI * 1.5) * 0.12
        sz = t * 2.5
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=5,
            radius1=0.025 * (1 - t * 0.6), radius2=0.025 * (1 - t * 0.6), depth=0.24,
            matrix=Matrix.Translation((sx, 0, sz + 0.12)))
    # leaf blades alternating sides
    for i in range(8):
        t = (i + 1) / 9
        sx = math.sin(t * PI * 1.5) * 0.12
        sz = t * 2.5
        side = 1 if i % 2 == 0 else -1
        # blade: flat tapered quad strip
        blade_pts = []
        for b in range(4):
            bt = b / 3
            blade_pts.append(bm.verts.new((
                sx + side * bt * 0.30,
                side * bt * 0.08,
                sz + bt * 0.15 + math.sin(bt * PI) * 0.05)))
        for b in range(3):
            w = 0.04 * (1 - b/3 * 0.7)
            v0 = blade_pts[b]
            v1 = blade_pts[b+1]
            v2 = bm.verts.new(v1.co + Vector((0, 0, w)))
            v3 = bm.verts.new(v0.co + Vector((0, 0, w)))
            bm.faces.new([v0, v1, v2, v3])
    # glow bulb at tip
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.045,
        matrix=Matrix.Translation((math.sin(PI*1.5)*0.12, 0, 2.55)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_water_bioluminescent", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Kelp_Strand_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Kelp_Strand_A")
