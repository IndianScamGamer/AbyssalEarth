"""
SM_MantleGarden_LavaBridge_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('MantleGarden')

def build():
    """Natural cooled-lava rock arch bridge. Player walks across this
    over a lava river. Matches: mantle_garden_concept.png foreground bridge arch."""
    print("Building SM_MantleGarden_LavaBridge_A …")
    obj, bm = new_mesh("SM_MantleGarden_LavaBridge_A")
    rng = random.Random(33)

    # arch params
    span  = 20.0
    rise  = 6.0
    w     = 5.0   # walkway width
    segs  = 16
    cover = 0.55  # fraction of circle

    rings_L = []  # left edge of walkway
    rings_R = []  # right edge

    for seg in range(int(segs * cover) + 1):
        t  = seg / segs
        a  = (t - 0.5) * TAU * cover
        ax = math.sin(a) * span * 0.5
        az = rise * (math.cos(a * 0.9) - math.cos(TAU*cover*0.9*0.5))
        az = max(az, 0)

        thick = 1.5 + rng.uniform(-0.1, 0.2)
        lv = bm.verts.new((ax - w/2 + rng.uniform(-0.2,0.2),
                            rng.uniform(-0.1,0.1), az + thick))
        rv = bm.verts.new((ax + w/2 + rng.uniform(-0.2,0.2),
                            rng.uniform(-0.1,0.1), az + thick))
        lb = bm.verts.new((ax - w/2 + rng.uniform(-0.15,0.15),
                            rng.uniform(-0.15,0.15)*3, az - 0.2))
        rb = bm.verts.new((ax + w/2 + rng.uniform(-0.15,0.15),
                            rng.uniform(-0.15,0.15)*3, az - 0.2))
        rings_L.append((lv, lb))
        rings_R.append((rv, rb))

    for ri in range(len(rings_L)-1):
        lt, lb = rings_L[ri];  lt2, lb2 = rings_L[ri+1]
        rt, rb = rings_R[ri];  rt2, rb2 = rings_R[ri+1]
        try:
            bm.faces.new([lt, lt2, rt2, rt])   # walkway top
            bm.faces.new([lb, lb2, lt2, lt])    # left side
            bm.faces.new([rb, rt, rt2, rb2])    # right side
        except: pass

    # ── lava fissure on underside ──────────────────
    for seg in range(4):
        t   = (seg + 0.5) / 4
        ax  = math.sin((t-0.5)*TAU*cover) * span * 0.5
        az  = rise * max(0, math.cos((t-0.5)*TAU*cover*0.9) - 0.3)
        fv  = [bm.verts.new((ax + dx*0.08, dy*0.5, az - 0.15))
               for dx, dy in ((-1,0),(1,0),(0,-1),(0,1))]
        try: bm.faces.new(fv)
        except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_lava_emissive"])
    set_origin_bottom(obj)
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_MantleGarden_LavaBridge_A")
