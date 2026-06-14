"""
SM_ShaftRim_Segment_A — AbyssalEarth procedural mesh.
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
    """Modular rim segment of the great shaft pit — 30° arc of the ring lip
    with terraced inner wall and 3 work-light posts. Tiles 12x for full ring.
    Concept: ringed pit in intro_submarine_wide."""
    random.seed(310)
    obj, bm = new_mesh("SM_ShaftRim_Segment_A")
    ARC = TAU / 12
    R_OUT, R_IN = 30.0, 22.0
    SEGS = 8
    # rim deck (flat annular sector)
    out_lo, in_lo = [], []
    for i in range(SEGS + 1):
        a = -ARC/2 + (i/SEGS) * ARC
        out_lo.append(bm.verts.new((math.cos(a)*R_OUT, math.sin(a)*R_OUT, 0)))
        in_lo.append(bm.verts.new((math.cos(a)*R_IN, math.sin(a)*R_IN, 0)))
    for i in range(SEGS):
        bm.faces.new([out_lo[i], out_lo[i+1], in_lo[i+1], in_lo[i]])
    # terraced inner wall: 3 steps down into the pit
    prev = in_lo
    for step, (dr, dz) in enumerate([(1.5, -4.0), (1.5, -4.0), (1.2, -4.0)]):
        r = R_IN - (step + 1) * dr
        z = (step + 1) * dz
        cur = []
        for i in range(SEGS + 1):
            a = -ARC/2 + (i/SEGS) * ARC
            cur.append(bm.verts.new((math.cos(a)*r, math.sin(a)*r, z)))
        for i in range(SEGS):
            bm.faces.new([prev[i], prev[i+1], cur[i+1], cur[i]])
        prev = cur
    # 3 work-light posts on the rim
    for t in [0.2, 0.5, 0.8]:
        a = -ARC/2 + t * ARC
        px, py = math.cos(a)*(R_IN + 1.0), math.sin(a)*(R_IN + 1.0)
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
            radius1=0.08, radius2=0.08, depth=2.5,
            matrix=Matrix.Translation((px, py, 1.25)))
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((px, py, 2.6))
            @ Matrix.Scale(0.45, 4, (1,0,0))
            @ Matrix.Scale(0.18, 4, (0,1,0))
            @ Matrix.Scale(0.18, 4, (0,0,1)))
    # rocky outer edge irregularity
    for i in range(6):
        a = -ARC/2 + random.uniform(0.05, 0.95) * ARC
        rr = R_OUT - random.uniform(0, 1.5)
        s = random.uniform(0.6, 1.8)
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=s,
            matrix=Matrix.Translation((math.cos(a)*rr, math.sin(a)*rr, s*0.3)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_human_equipment",
                        "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_ShaftRim_Segment_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_ShaftRim_Segment_A")
