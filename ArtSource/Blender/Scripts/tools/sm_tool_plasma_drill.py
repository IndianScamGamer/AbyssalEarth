"""
SM_Tool_PlasmaDrill_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Tools')

def build():
    """Compact harvest drill — body with side grip, tapered bit, heat fins.
    In-hand visual for harvesting interactions."""
    obj, bm = new_mesh("SM_Tool_PlasmaDrill_A")
    # body
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=10,
        radius=0.055, depth=0.20,
        matrix=Matrix.Translation((0, 0, 0.14))
        @ Matrix.Rotation(TAU/4, 4, 'X'))
    # drill bit (tapered, fluted)
    bit_levels = [(0, 0.030), (0.06, 0.022), (0.12, 0.010), (0.16, 0.002)]
    rings = []
    for d, r in bit_levels:
        ring = [bm.verts.new((math.cos(i*TAU/6)*r,
                               -0.10 - d,
                               0.14 + math.sin(i*TAU/6)*r)) for i in range(6)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(6):
            bm.faces.new([lo[i], lo[(i+1)%6], hi[(i+1)%6], hi[i]])
    # heat fins
    for fy in [0.04, 0.08, 0.12]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, fy, 0.205))
            @ Matrix.Scale(0.13, 4, (1,0,0))
            @ Matrix.Scale(0.012, 4, (0,1,0))
            @ Matrix.Scale(0.035, 4, (0,0,1)))
    # grip handle below
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.07, 0.045))
        @ Matrix.Rotation(0.25, 4, 'X')
        @ Matrix.Scale(0.040, 4, (1,0,0))
        @ Matrix.Scale(0.050, 4, (0,1,0))
        @ Matrix.Scale(0.10, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_heat_bloom"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_PlasmaDrill_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Tool_PlasmaDrill_A")
