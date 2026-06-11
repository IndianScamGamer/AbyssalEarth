"""
SM_MantleGarden_SteamColumn_A — AbyssalEarth procedural mesh.
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
    """Rock base column for steam vent VFX attachment.
    Cracked basalt pillar with lava glow at base crack."""
    print("Building SM_MantleGarden_SteamColumn_A …")
    obj, bm = new_mesh("SM_MantleGarden_SteamColumn_A")
    rng = random.Random(44)

    segs = 8
    h    = 2.5
    levels = [(0, 0.8), (0.3, 0.72), (0.9, 0.62), (1.6, 0.55),
              (2.1, 0.50), (h, 0.44)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*(r + rng.uniform(-0.04,0.04)*r),
                    math.sin(i*TAU/segs)*(r + rng.uniform(-0.04,0.04)*r),
                    z))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    try: bm.faces.new(list(reversed(rings[0])))
    except: pass

    # vent opening at top
    top_r = [bm.verts.new((math.cos(i*TAU/8)*0.30,
                           math.sin(i*TAU/8)*0.30, h))
             for i in range(8)]
    try: bm.faces.new(top_r)
    except: pass

    # lava glow cracks at base
    for crack_a in range(3):
        angle = crack_a * TAU/3
        for step in range(4):
            t = step/3
            cv = bm.verts.new((math.cos(angle)*0.78*(1-t*0.2),
                               math.sin(angle)*0.78*(1-t*0.2),
                               t*0.35))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_lava_emissive"])
    set_origin_bottom(obj)
    return obj


# ════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_MantleGarden_SteamColumn_A")
