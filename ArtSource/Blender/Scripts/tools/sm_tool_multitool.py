"""
SM_Tool_Multitool_A — AbyssalEarth procedural mesh.
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
    """Folding multitool — open scissor-pose with two handle slabs and
    plier head."""
    obj, bm = new_mesh("SM_Tool_Multitool_A")
    # two handle slabs in shallow V
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side*0.030, -0.035, 0.012))
            @ Matrix.Rotation(side*0.35, 4, 'Z')
            @ Matrix.Scale(0.022, 4, (1,0,0))
            @ Matrix.Scale(0.115, 4, (0,1,0))
            @ Matrix.Scale(0.020, 4, (0,0,1)))
    # pivot boss
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.014, depth=0.026,
        matrix=Matrix.Translation((0, 0.030, 0.012)))
    # plier jaws
    for side in [-1, 1]:
        jaw_levels = [(0, 0.010), (0.030, 0.007), (0.055, 0.003)]
        rings = []
        for d, r in jaw_levels:
            ring = [bm.verts.new((side*0.006 + math.cos(i*TAU/4)*r,
                                   0.045 + d,
                                   0.012 + math.sin(i*TAU/4)*r))
                    for i in range(4)]
            rings.append(ring)
        for ri in range(len(rings)-1):
            lo, hi = rings[ri], rings[ri+1]
            for i in range(4):
                bm.faces.new([lo[i], lo[(i+1)%4], hi[(i+1)%4], hi[i]])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_Multitool_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Tool_Multitool_A")
