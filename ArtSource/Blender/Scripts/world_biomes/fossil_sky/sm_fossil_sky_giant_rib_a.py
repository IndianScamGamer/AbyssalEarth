"""
SM_FossilSky_GiantRib_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('FossilSky')


def build():
    """SM_FossilSky_GiantRib_A — single 25m parabolic rib arch, bone cross-section."""
    import random; random.seed(55)
    obj, bm = new_mesh("SM_FossilSky_GiantRib_A")
    SEGS = 22
    SPAN = 25.0
    HEIGHT = 22.0
    for i in range(SEGS + 1):
        t = i / SEGS
        x = (t - 0.5) * SPAN
        z = HEIGHT * math.sin(t * math.pi)
        # oval cross-section: 0.7 wide x 1.0 tall
        for ci in range(8):
            a = ci * TAU / 8
            cx = x + math.cos(a) * 0.35 * random.uniform(0.92, 1.08)
            cz = z + math.sin(a) * 0.50 * random.uniform(0.92, 1.08)
            bm.verts.new((cx, math.sin(a) * 0.20, cz))
    bm.verts.ensure_lookup_table()
    v = bm.verts
    n = 8
    for ring in range(SEGS):
        base = ring * n
        for i in range(n):
            ni = (i + 1) % n
            bm.faces.new([v[base+i], v[base+ni],
                           v[base+n+ni], v[base+n+i]])
    for cap_base in [0, SEGS*n]:
        bm.faces.new([v[cap_base + i] for i in range(n)])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_GiantRib_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_FossilSky_GiantRib_A")
