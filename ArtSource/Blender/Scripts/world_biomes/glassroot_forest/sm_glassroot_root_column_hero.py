"""
SM_Glassroot_RootColumn_Hero — AbyssalEarth procedural mesh.
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
    """SM_Glassroot_RootColumn_Hero — 50m cathedral hero root column."""
    import random; random.seed(77)
    obj, bm = new_mesh("SM_Glassroot_RootColumn_Hero")
    levels = [(0,2.2),(2,2.0),(8,1.75),(18,1.40),(30,1.0),(42,0.55),(50,0.20)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/12)*r*(1+random.uniform(-0.04,0.04)),
                               math.sin(i*TAU/12)*r*(1+random.uniform(-0.04,0.04)), z))
                for i in range(12)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(12):
            bm.faces.new([lo[i], lo[(i+1)%12], hi[(i+1)%12], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # massive root flanges
    for i in range(6):
        a = i*TAU/6
        for z, ext, w in [(0,3.5,0.6),(1.5,2.5,0.5),(4.0,1.2,0.35)]:
            bm.verts.new((math.cos(a)*(2.2+ext), math.sin(a)*(2.2+ext), z+w*0.5))
    # red vein ridges
    for i in range(5):
        a = i*TAU/5
        for lz in range(0, 50, 3):
            bm.verts.new((math.cos(a)*2.25, math.sin(a)*2.25, lz))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_red_sap", "mat_pearl_stone"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootColumn_Hero")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Glassroot_RootColumn_Hero")
