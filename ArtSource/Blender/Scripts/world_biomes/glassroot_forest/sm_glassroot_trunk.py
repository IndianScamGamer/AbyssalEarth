"""
SM_GLASSROOT_TRUNK — AbyssalEarth procedural mesh.
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

def build_variant(name, r, seed=10):
    """Translucent glass-bark tree trunk with red vein channels.
    Smooth surface with occasional red emissive ridge.
    Matches: glassroot_forest_concept.png."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs = 16
    h_trunk = r * 4.0    # trunks are tall relative to radius

    # ── trunk levels (slight natural taper) ──────
    levels = [(0, r), (r*0.8, r*0.98), (r*1.8, r*0.95),
              (h_trunk*0.4, r*0.88), (h_trunk*0.65, r*0.82),
              (h_trunk*0.80, r*0.76), (h_trunk, r*0.70)]
    rings = []
    for z, lr in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*lr + rng.uniform(-0.02,0.02)*r,
                    math.sin(i*TAU/segs)*lr + rng.uniform(-0.02,0.02)*r,
                    z + rng.uniform(-0.01,0.01)*r))
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

    # ── root flange at base ───────────────────────
    flange_segs = 24
    for fi in range(flange_segs):
        angle = fi * TAU / flange_segs
        spread = r * (1.8 + 0.6 * abs(math.sin(angle * 3)))
        fv = [
            bm.verts.new((math.cos(angle)*r*1.02, math.sin(angle)*r*1.02, 0.0)),
            bm.verts.new((math.cos(angle)*spread,  math.sin(angle)*spread,  0.0)),
            bm.verts.new((math.cos(angle)*spread*0.95, math.sin(angle)*spread*0.95,
                          -rng.uniform(0.05,0.20)*r)),
        ]
        try: bm.faces.new(fv)
        except: pass

    # ── 3 red emissive vein ridges ─────────────────
    for vein_i in range(3):
        v_angle = vein_i * TAU/3 + rng.uniform(-0.3, 0.3)
        for zi in range(12):
            z = zi / 11 * h_trunk * 0.85
            v_angle += rng.uniform(-0.05, 0.05)  # gentle spiral
            vx = math.cos(v_angle) * (r + 0.035)
            vy = math.sin(v_angle) * (r + 0.035)
            bm.verts.new((vx, vy, z))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glass_bark", "mat_red_emissive_vein"])
    set_origin_to_base(obj)
    return obj

VARIANTS = [
    ('SM_Glassroot_TrunkBase_A', 2.2, 10),
    ('SM_Glassroot_TrunkBase_B', 3.5, 17),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_GLASSROOT_TRUNK")
