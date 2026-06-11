"""
SM_Glassroot_RootColumn_M — AbyssalEarth procedural mesh.
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
    """SM_Glassroot_RootColumn_M — 10m translucent root column."""
    import random; random.seed(22)
    obj, bm = new_mesh("SM_Glassroot_RootColumn_M")
    levels = [(0,0.55),(0.8,0.50),(2.5,0.44),(5.0,0.36),(8.0,0.22),(10.0,0.09)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/8)*r*(1+random.uniform(-0.05,0.05)),
                               math.sin(i*TAU/8)*r*(1+random.uniform(-0.05,0.05)), z))
                for i in range(8)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(8):
            bm.faces.new([lo[i], lo[(i+1)%8], hi[(i+1)%8], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # root flanges at base
    for i in range(4):
        a = i * TAU/4 + TAU/8
        fx, fy = math.cos(a)*0.90, math.sin(a)*0.90
        for z in [0.0, 0.5, 1.2]:
            t = z/1.2
            bm.verts.new((fx*(1-t), fy*(1-t), z))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_red_sap", "mat_pearl_stone"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootColumn_M")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Glassroot_RootColumn_M")
