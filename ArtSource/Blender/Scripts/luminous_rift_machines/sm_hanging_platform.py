"""
SM_Rift_HangingPlatform_A — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-010, LR-011
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

EXPORT_DIR = get_export_dir('LuminousRift')

def build():
    """Chain-suspended platform — 8m deck hanging from 4 chain runs with
    anchor ring above. Concept: ancient_bridge_platform_kit."""
    random.seed(420)
    obj, bm = new_mesh("SM_Rift_HangingPlatform_A")
    # deck (octagonal slab)
    R, T = 4.0, 0.5
    lo = [bm.verts.new((math.cos(i*TAU/8)*R, math.sin(i*TAU/8)*R, 0))
          for i in range(8)]
    hi = [bm.verts.new((math.cos(i*TAU/8)*R, math.sin(i*TAU/8)*R, T))
          for i in range(8)]
    for i in range(8):
        ni = (i + 1) % 8
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # circular inset detail on deck
    bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False, segments=16,
        radius1=2.2, radius2=2.2, depth=0.06,
        matrix=Matrix.Translation((0, 0, T + 0.02)))
    # 4 chain runs to anchor ring (chain = stacks of small tori approximated
    # by alternating-rotation rings of spheres)
    CHAIN_H = 6.0
    for i in range(4):
        a = i * TAU / 4 + TAU / 8
        bx, by = math.cos(a) * R * 0.8, math.sin(a) * R * 0.8
        LINKS = 9
        for l in range(LINKS):
            t = (l + 0.5) / LINKS
            cx = bx * (1 - t * 0.85)
            cy = by * (1 - t * 0.85)
            cz = T + t * CHAIN_H
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.13,
                matrix=Matrix.Translation((cx, cy, cz)))
    # anchor ring at top
    SEGS = 12
    for s in range(SEGS):
        a = s * TAU / SEGS
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.18,
            matrix=Matrix.Translation((math.cos(a)*0.8, math.sin(a)*0.8,
                                        T + CHAIN_H + 0.3)))
    # corner anchor lugs on deck
    for i in range(4):
        a = i * TAU / 4 + TAU / 8
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
            radius1=0.18, radius2=0.18, depth=0.35,
            matrix=Matrix.Translation((math.cos(a)*R*0.8,
                                        math.sin(a)*R*0.8, T + 0.17)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_HangingPlatform_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Rift_HangingPlatform_A")
