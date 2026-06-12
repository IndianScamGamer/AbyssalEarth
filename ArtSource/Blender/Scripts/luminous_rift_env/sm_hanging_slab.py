"""
SM_HANGING_SLAB — AbyssalEarth procedural mesh.
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

def build_variant(name, w, l, thickness, seed=42):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    n_w, n_l = 5, 8
    # ── slab top surface ──────────────────────────
    top_grid = []
    for gx in range(n_w):
        row = []
        for gy in range(n_l):
            tx = (gx / (n_w-1) - 0.5) * w + rng.uniform(-0.15, 0.15)
            ty = (gy / (n_l-1) - 0.5) * l + rng.uniform(-0.15, 0.15)
            tz = 0.0 + rng.uniform(-0.08, 0.08)
            row.append(bm.verts.new((tx, ty, tz)))
        top_grid.append(row)

    # ── slab bottom (slightly varied) ─────────────
    bot_grid = []
    for gx in range(n_w):
        row = []
        for gy in range(n_l):
            tv = top_grid[gx][gy]
            thk = thickness + rng.uniform(-0.2, 0.3)
            row.append(bm.verts.new((tv.co.x + rng.uniform(-0.12, 0.12),
                                     tv.co.y + rng.uniform(-0.12, 0.12),
                                     tv.co.z - thk)))
        bot_grid.append(row)

    # top faces
    for gx in range(n_w-1):
        for gy in range(n_l-1):
            try:
                bm.faces.new([top_grid[gx][gy],   top_grid[gx+1][gy],
                               top_grid[gx+1][gy+1], top_grid[gx][gy+1]])
            except Exception:
                pass

    # bottom faces
    for gx in range(n_w-1):
        for gy in range(n_l-1):
            try:
                bm.faces.new([bot_grid[gx][gy],   bot_grid[gx][gy+1],
                               bot_grid[gx+1][gy+1], bot_grid[gx+1][gy]])
            except Exception:
                pass

    # side edges
    for gy in range(n_l-1):
        for gx, gx2 in [(0,0), (n_w-1, n_w-1)]:
            try:
                bm.faces.new([top_grid[gx][gy],   top_grid[gx][gy+1],
                               bot_grid[gx2][gy+1], bot_grid[gx2][gy]])
            except Exception:
                pass
    for gx in range(n_w-1):
        for gy, gy2 in [(0,0), (n_l-1, n_l-1)]:
            try:
                bm.faces.new([top_grid[gx][gy],   top_grid[gx+1][gy],
                               bot_grid[gx+1][gy2], bot_grid[gx][gy2]])
            except Exception:
                pass

    # ── crystal clusters on underside ─────────────
    for cx, cy in [(0,0), (rng.uniform(-w*0.25, w*0.25),
                            rng.uniform(-l*0.25, l*0.25))]:
        cz_base = -thickness - 0.05
        for s in range(rng.randint(2, 4)):
            h = rng.uniform(0.25, 0.55)
            angle = s * TAU / 4 + rng.uniform(-0.3, 0.3)
            spx = cx + math.cos(angle) * rng.uniform(0.1, 0.25)
            spy = cy + math.sin(angle) * rng.uniform(0.1, 0.25)
            cv = [bm.verts.new((spx + math.cos(a*TAU/5)*0.06,
                                spy + math.sin(a*TAU/5)*0.06,
                                cz_base))
                  for a in range(5)]
            ctip = bm.verts.new((spx, spy, cz_base - h))
            try:
                bm.faces.new(list(reversed(cv)))
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
#  CAVERN WALL
# ══════════════════════════════════════════════
# Large background wall tile ~50m wide.  World-aligned UV friendly,
# vertical striations, occasional crystal socket.

VARIANTS = [
    ('SM_Rift_HangingSlab_A', 12, 25, 2.5, 42),
    ('SM_Rift_HangingSlab_B', 8, 18, 3.5, 55),
    ('SM_Rift_HangingSlab_C', 20, 40, 4.0, 68),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_HANGING_SLAB")
