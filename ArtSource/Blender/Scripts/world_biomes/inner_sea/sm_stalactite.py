"""
SM_STALACTITE — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('InnerSea')

def build(name, r_base, height, seed=50):
    """Hanging cave stalactite. Natural tapered form with occasional
    bioluminescent tip. Matches: inner_sea_concept.png."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs  = 8
    levels = [(0, r_base), (height*0.25, r_base*0.78),
              (height*0.55, r_base*0.50), (height*0.80, r_base*0.26),
              (height*0.95, r_base*0.09), (height, r_base*0.02)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*(r + rng.uniform(-0.05,0.05)*r),
                    math.sin(i*TAU/segs)*(r + rng.uniform(-0.05,0.05)*r),
                    -(z + rng.uniform(-0.02,0.02)*height)))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    tip = bm.verts.new((rng.uniform(-0.02,0.02)*r_base,
                        rng.uniform(-0.02,0.02)*r_base,
                        -(height + r_base*0.05)))
    for j in range(segs):
        try: bm.faces.new([rings[-1][j], rings[-1][(j+1)%segs], tip])
        except: pass

    # top mount cap
    try: bm.faces.new(rings[0])
    except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_water_bioluminescent"])
    set_origin_bottom(obj)
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_STALACTITE")
