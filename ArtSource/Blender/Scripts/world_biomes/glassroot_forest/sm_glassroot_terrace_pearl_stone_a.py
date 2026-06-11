"""
SM_Glassroot_Terrace_PearlStone_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GlassrootForest')


def build():
    """SM_Glassroot_Terrace_PearlStone_A — 12m irregular pearl-white terrace."""
    import random; random.seed(33)
    obj, bm = new_mesh("SM_Glassroot_Terrace_PearlStone_A")
    VERTS = 14
    outer = []
    for i in range(VERTS):
        a = i * TAU / VERTS
        r = 6.0 * random.uniform(0.75, 1.25)
        outer.append(bm.verts.new((math.cos(a)*r, math.sin(a)*r, 0)))
    centre = bm.verts.new((0,0,0))
    for i in range(VERTS):
        bm.faces.new([outer[i], outer[(i+1)%VERTS], centre])
    extrude_region(bm, list(bm.faces), 0.35, Vector((0,0,-1)))
    # rounded top edge bevels
    for v in bm.verts:
        if v.co.z > -0.05:
            dist = (v.co.x**2 + v.co.y**2)**0.5
            v.co.z += max(0, 0.12 * (1 - dist/6))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_pearl_stone", "mat_wet_edge"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_Terrace_PearlStone_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Glassroot_Terrace_PearlStone_A")
