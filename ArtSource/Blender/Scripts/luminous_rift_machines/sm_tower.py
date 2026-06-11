"""
SM_TOWER — AbyssalEarth procedural mesh.
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
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, mat_color, extrude_region,
                           add_subdivision, TAU, PI)

EXPORT_DIR = get_export_dir('LuminousRift')

def build(name, width, height, seed=2):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs = 8
    levels_r = [(0, width*0.6), (height*0.15, width*0.55),
                (height*0.40, width*0.50), (height*0.65, width*0.46),
                (height*0.85, width*0.44), (height*0.95, width*0.40)]

    # ── tapered tower body ─────────────────────────
    rings = []
    for z, r in levels_r:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*(r + rng.uniform(-0.05,0.05)*width),
                    math.sin(i*TAU/segs)*(r + rng.uniform(-0.05,0.05)*width),
                    z + rng.uniform(-0.08, 0.08)*height*0.01))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try:
                bm.faces.new([lo[j], lo[nj], hi[nj], hi[j]])
            except Exception:
                pass
    bm.faces.new(list(reversed(rings[0])))

    # ── broken top (ragged edge) ──────────────────
    top_ring = rings[-1]
    for j in range(segs):
        top_h = height + rng.uniform(-height*0.08, height*0.04)
        bm.verts.new((top_ring[j].co.x, top_ring[j].co.y, top_h))

    # ── vertical groove cutouts ───────────────────
    for j in range(segs):
        angle = j * TAU/segs
        gx = math.cos(angle) * (width * 0.52)
        gy = math.sin(angle) * (width * 0.52)
        for seg_i in range(5):
            z0 = height * 0.15 + seg_i * height * 0.15
            z1 = z0 + height * 0.08
            gv = [bm.verts.new((gx + math.cos(angle+da)*0.04,
                                gy + math.sin(angle+da)*0.04,
                                z))
                  for da, z in [(-0.25,z0),(0.25,z0),(0.25,z1),(-0.25,z1)]]
            try:
                bm.faces.new(list(reversed(gv)))
            except Exception:
                pass

    # ── cyan emissive vertical strip ──────────────
    for _ in range(2):
        angle = rng.uniform(0, TAU)
        sx = math.cos(angle) * width * 0.51
        sy = math.sin(angle) * width * 0.51
        sv = [bm.verts.new((sx + math.cos(angle)*da, sy + math.sin(angle)*da,
                            z * height))
              for da, z in [(-0.04, 0.12), (0.04, 0.12),
                             (0.04, 0.88), (-0.04, 0.88)]]
        try:
            bm.faces.new(sv)
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_wet_basalt",
                        "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_TOWER")
