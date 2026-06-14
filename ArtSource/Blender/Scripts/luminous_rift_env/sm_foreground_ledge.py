"""
SM_FOREGROUND_LEDGE — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-002
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

def build_variant(name, broken=False, seed=7):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    # ── ledge top surface (irregular polygon) ─────
    # Base outline: roughly trapezoidal with organic bumps
    outline_pts = []
    n_pts = 14
    base_w = 5.0  # ~10m wide total (half = 5 in each direction)
    base_d = 8.0
    for i in range(n_pts):
        a = i * TAU / n_pts
        # trapezoid-ish base shape with noise
        bx = math.cos(a) * (base_w + rng.uniform(-0.8, 0.8))
        by = math.sin(a) * (base_d * 0.5 + rng.uniform(-1.0, 1.0))
        outline_pts.append((bx, by, rng.uniform(-0.15, 0.25)))

    # Create top surface
    top_verts = [bm.verts.new(p) for p in outline_pts]
    bm.faces.new(top_verts)

    # ── extrude down for thickness with layered striations ─
    depths = [0.6, 1.4, 2.8, 5.2]
    prev_ring = top_verts
    for depth in depths:
        new_ring = []
        for v in prev_ring:
            squeeze = 1.0 - depth * 0.04
            nx = v.co.x * squeeze + rng.uniform(-0.15, 0.15)
            ny = v.co.y * squeeze + rng.uniform(-0.15, 0.15)
            new_ring.append(bm.verts.new((nx, ny, -depth + rng.uniform(-0.1, 0.1))))
        for i in range(len(prev_ring)):
            ni = (i+1)%len(prev_ring)
            try:
                bm.faces.new([prev_ring[i], prev_ring[ni],
                               new_ring[ni], new_ring[i]])
            except Exception:
                pass
        prev_ring = new_ring

    # bottom cap
    try:
        bm.faces.new(list(reversed(prev_ring)))
    except Exception:
        pass

    # ── crystal sockets on underside/edges ────────
    crystal_positions = [(-2.5, -2.0, -1.5), (1.8, 1.5, -2.0),
                         (-0.5, 3.0, -1.2),   (3.0, -1.0, -3.0)]
    if not broken:
        for cx, cy, cz in crystal_positions:
            cv = [bm.verts.new((cx + math.cos(a*TAU/4)*0.12,
                                cy + math.sin(a*TAU/4)*0.12,
                                cz))
                  for a in range(4)]
            tip = bm.verts.new((cx, cy, cz + 0.45))
            try:
                bm.faces.new(cv)
                for i in range(4):
                    bm.faces.new([cv[i], cv[(i+1)%4], tip])
            except Exception:
                pass

    # ── broken variant: shear off one side ────────
    if broken:
        for v in bm.verts:
            if v.co.x > 2.0 and v.co.z > -1.5:
                v.co.z -= (v.co.x - 2.0) * 0.8
                v.co.x += rng.uniform(-0.3, 0.1)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  ROCK ARCH
# ══════════════════════════════════════════════
# Natural stone arch 30–60m span. Uneven sides, crystal sockets,
# strong silhouette for cavern framing. Matches: AD-004.

VARIANTS = [
    ('SM_Rift_ForegroundLedge_A', False, 7),
    ('SM_Rift_ForegroundLedge_B_Broken', True, 14),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_FOREGROUND_LEDGE")
