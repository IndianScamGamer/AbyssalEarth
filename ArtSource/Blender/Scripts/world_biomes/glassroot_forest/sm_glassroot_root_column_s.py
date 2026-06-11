"""
SM_Glassroot_RootColumn_S — AbyssalEarth procedural mesh.
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
    """SM_Glassroot_RootColumn_S — 3m translucent root column, hex tapered."""
    obj, bm = new_mesh("SM_Glassroot_RootColumn_S")
    levels = [(0, 0.28), (0.5, 0.24), (1.2, 0.20), (2.0, 0.15), (3.0, 0.06)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/6)*r, math.sin(i*TAU/6)*r, z))
                for i in range(6)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(6):
            bm.faces.new([lo[i], lo[(i+1)%6], hi[(i+1)%6], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_red_sap"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootColumn_S")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Glassroot_RootColumn_S")
