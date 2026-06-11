"""
SM_GravityWell_CurvedTower_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GravityWell')


def build():
    """SM_GravityWell_CurvedTower_A — 60m curved ancient stabilizer tower."""
    import random; random.seed(88)
    obj, bm = new_mesh("SM_GravityWell_CurvedTower_A")
    SEGS = 20
    H = 60.0
    rings = []
    for i in range(SEGS + 1):
        t = i/SEGS
        # curve: leans over by 8m at top
        x = math.sin(t*math.pi*0.5)*8.0
        z = t * H
        r = 3.5 - t*2.2
        ring = [bm.verts.new((x + math.cos(j*TAU/10)*r,
                               math.sin(j*TAU/10)*r, z))
                for j in range(10)]
        rings.append(ring)
    for ri in range(SEGS):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(10):
            bm.faces.new([lo[j], lo[(j+1)%10], hi[(j+1)%10], hi[j]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # vertical groove details
    for groove in range(5):
        ga = groove*TAU/5
        for gz in range(0, 60, 4):
            t = gz/60
            gx = math.sin(t*math.pi*0.5)*8.0 + math.cos(ga)*(3.5-t*2.2+0.1)
            gy = math.sin(ga)*(3.5-t*2.2+0.1)
            bm.verts.new((gx, gy, gz))
    # amber emissive bands
    for bz in [10, 25, 42, 55]:
        t = bz/60
        br = 3.5 - t*2.2 + 0.12
        bx = math.sin(t*math.pi*0.5)*8.0
        for j in range(16):
            bm.verts.new((bx + math.cos(j*TAU/16)*br,
                           math.sin(j*TAU/16)*br, bz))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_amber_stabilizer"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_CurvedTower_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_GravityWell_CurvedTower_A")
