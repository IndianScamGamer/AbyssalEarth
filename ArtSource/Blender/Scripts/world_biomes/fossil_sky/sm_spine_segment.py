"""
SM_SPINE_SEGMENT — AbyssalEarth procedural mesh.
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

def build(name, length, width, seed=5):
    """Giant vertebra-style spine segment.
    Oval body with 4 transverse processes (bone wings)."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    # ── vertebra body ─────────────────────────────
    segs = 12
    levels = [(0, width*0.55), (length*0.2, width*0.60),
              (length*0.5, width*0.65), (length*0.8, width*0.60),
              (length, width*0.55)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*r + rng.uniform(-0.05,0.05)*r,
                    math.sin(i*TAU/segs)*r*0.65 + rng.uniform(-0.03,0.03)*r,
                    z))
                for i in range(segs)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    for r in (rings[0], rings[-1]):
        try: bm.faces.new(list(reversed(r)))
        except: pass

    # ── 4 transverse bone wings ────────────────────
    for z_frac in (0.25, 0.75):
        for side in (-1, 1):
            wing_len = width * 1.4
            wx0, wx1 = width*0.62*side, wing_len*side
            wz = z_frac * length
            wv = [bm.verts.new((wx0, rng.uniform(-0.08,0.08)*width, wz-0.08)),
                  bm.verts.new((wx0, rng.uniform(-0.08,0.08)*width, wz+0.08)),
                  bm.verts.new((wx1, rng.uniform(-0.25,0.25)*width*0.3, wz+0.06+wing_len*0.12)),
                  bm.verts.new((wx1, rng.uniform(-0.25,0.25)*width*0.3, wz-0.06+wing_len*0.12))]
            try: bm.faces.new(wv)
            except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_fossil_bone"])
    set_origin_bottom(obj)
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_SPINE_SEGMENT")
