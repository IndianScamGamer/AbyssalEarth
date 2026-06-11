"""
SM_ROCK_ARCH — AbyssalEarth procedural mesh.
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

def build(name, span, height, thickness, seed=3):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs = 16  # arch segments
    half = span * 0.5

    # ── left pillar ───────────────────────────────
    for side, sx in [("left", -half), ("right", half)]:
        pillar_w = thickness * rng.uniform(0.8, 1.2)
        pillar_d = thickness * rng.uniform(0.9, 1.1)
        base_h   = height * rng.uniform(0.35, 0.50)

        # tapered pillar: wider at base
        for i, (fz, fw, fd) in enumerate([
                (0.0,     pillar_w*1.3, pillar_d*1.3),
                (base_h*0.3, pillar_w*1.1, pillar_d*1.1),
                (base_h,  pillar_w,     pillar_d)]):
            ring = [bm.verts.new((sx + math.cos(a*TAU/8)*fw + rng.uniform(-0.2,0.2),
                                  math.sin(a*TAU/8)*fd + rng.uniform(-0.2,0.2),
                                  fz))
                    for a in range(8)]
            if i > 0:
                prev = list(bm.verts)[-8 - 8 : -8]
                for j in range(8):
                    nj = (j+1)%8
                    try:
                        bm.faces.new([prev[j], prev[nj], ring[nj], ring[j]])
                    except Exception:
                        pass
            if i == 0:
                try:
                    bm.faces.new(list(reversed(ring)))
                except Exception:
                    pass

    # ── arch curve (tube following parabolic path) ─
    arch_verts_rings = []
    for seg in range(segs + 1):
        t = seg / segs
        ax = half * (1 - 2 * t)                   # -half to +half
        az = height * (1 - (2*t-1)**2) * 0.85     # parabola
        az += rng.uniform(-0.3, 0.3)
        ring_r = thickness * (0.7 + rng.uniform(0, 0.25))
        ring_pts = [bm.verts.new((ax + math.cos(a*TAU/8)*ring_r,
                                  math.sin(a*TAU/8)*ring_r,
                                  az))
                    for a in range(8)]
        arch_verts_rings.append(ring_pts)

    for ri in range(len(arch_verts_rings)-1):
        lo, hi = arch_verts_rings[ri], arch_verts_rings[ri+1]
        for j in range(8):
            nj = (j+1)%8
            try:
                bm.faces.new([lo[j], lo[nj], hi[nj], hi[j]])
            except Exception:
                pass
    # cap ends
    try:
        bm.faces.new(list(reversed(arch_verts_rings[0])))
        bm.faces.new(arch_verts_rings[-1])
    except Exception:
        pass

    # ── crystal clusters embedded in arch ─────────
    for cx, cz, ch in [(0, height*0.9, 0.35), (-half*0.5, height*0.7, 0.28),
                        (half*0.5, height*0.7, 0.28)]:
        cv = [bm.verts.new((cx + math.cos(a*TAU/5)*0.14,
                            rng.uniform(-0.10, 0.10),
                            cz + math.sin(a*TAU/5)*0.14))
              for a in range(5)]
        ctip = bm.verts.new((cx, 0, cz + ch))
        try:
            bm.faces.new(cv)
            for i in range(5):
                bm.faces.new([cv[i], cv[(i+1)%5], ctip])
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  CEILING OVERHANG
# ══════════════════════════════════════════════
# Dark rock overhangs that frame the top of the First Overlook composition.
# Matches: AD-004, LR-004, LR-009.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_ROCK_ARCH")
