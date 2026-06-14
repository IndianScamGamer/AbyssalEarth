"""
SM_PowerNode_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Slice')

def build():
    """AAbyssalPowerNode — ancient power relay pylon, 2.2m. Emissive core
    sphere visible through 4 frame ribs; conduit ports at 4 compass points."""
    obj, bm = new_mesh("SM_PowerNode_A")
    # base plinth (octagon)
    lo = [bm.verts.new((math.cos(i*TAU/8)*0.45, math.sin(i*TAU/8)*0.45, 0))
          for i in range(8)]
    hi = [bm.verts.new((math.cos(i*TAU/8)*0.38, math.sin(i*TAU/8)*0.38, 0.25))
          for i in range(8)]
    for i in range(8):
        ni = (i + 1) % 8
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # central column
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
        radius1=0.10, radius2=0.10, depth=0.55,
        matrix=Matrix.Translation((0, 0, 0.52)))
    # core energy sphere
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.22,
        matrix=Matrix.Translation((0, 0, 1.15)))
    # 4 cage frame ribs around the core
    for i in range(4):
        a = i * TAU / 4
        SEGS = 8
        for s in range(SEGS + 1):
            t = s / SEGS
            ring_a = -PI/2 + t * PI
            rx = math.cos(ring_a) * 0.32
            rz = 1.15 + math.sin(ring_a) * 0.32
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.030,
                matrix=Matrix.Translation((math.cos(a)*rx, math.sin(a)*rx, rz)))
    # top cap antenna
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
        radius1=0.04, radius2=0.04, depth=0.45,
        matrix=Matrix.Translation((0, 0, 1.75)))
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.07,
        matrix=Matrix.Translation((0, 0, 2.05)))
    # 4 conduit ports on plinth
    for i in range(4):
        a = i * TAU / 4 + TAU/8
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
            radius1=0.07, radius2=0.07, depth=0.12,
            matrix=Matrix.Translation((math.cos(a)*0.44, math.sin(a)*0.44, 0.12))
            @ Matrix.Rotation(a + TAU/4, 4, 'Z')
            @ Matrix.Rotation(TAU/4, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_orb_energy"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_PowerNode_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_PowerNode_A")
