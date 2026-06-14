"""
SM_BRIDGE_SPAN — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-010, LR-011
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

def build_variant(name, length=24.0, broken=False, seed=3):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    w, l, h = 8.0, length, 0.9
    nx, ny = 6, 12

    # ── top walkable surface ───────────────────────
    top = []
    for ix in range(nx):
        row = []
        for iy in range(ny):
            x = (ix/(nx-1) - 0.5) * w + rng.uniform(-0.08, 0.08)
            y = (iy/(ny-1) - 0.5) * l + rng.uniform(-0.05, 0.05)
            z = rng.uniform(-0.04, 0.04)
            if broken and iy > ny*0.65 and ix > nx*0.5:
                z -= (iy - ny*0.65) * 0.25 * (ix - nx*0.5) * 0.3
            row.append(bm.verts.new((x, y, z)))
        top.append(row)

    for ix in range(nx-1):
        for iy in range(ny-1):
            try:
                bm.faces.new([top[ix][iy], top[ix+1][iy],
                               top[ix+1][iy+1], top[ix][iy+1]])
            except Exception:
                pass

    # ── underside (thicker slabs) ─────────────────
    bot = []
    for ix in range(nx):
        row = []
        for iy in range(ny):
            tv = top[ix][iy]
            depth = h + rng.uniform(-0.05, 0.15)
            row.append(bm.verts.new((tv.co.x + rng.uniform(-0.05, 0.05),
                                     tv.co.y + rng.uniform(-0.05, 0.05),
                                     tv.co.z - depth)))
        bot.append(row)

    for ix in range(nx-1):
        for iy in range(ny-1):
            try:
                bm.faces.new([bot[ix][iy], bot[ix][iy+1],
                               bot[ix+1][iy+1], bot[ix+1][iy]])
            except Exception:
                pass

    # side walls
    for iy in range(ny-1):
        try:
            bm.faces.new([top[0][iy], top[0][iy+1],
                          bot[0][iy+1], bot[0][iy]])
            bm.faces.new([top[nx-1][iy], top[nx-1][iy+1],
                          bot[nx-1][iy+1], bot[nx-1][iy]])
        except Exception:
            pass
    for ix in range(nx-1):
        try:
            bm.faces.new([top[ix][0], top[ix+1][0],
                          bot[ix+1][0], bot[ix][0]])
            bm.faces.new([top[ix][ny-1], top[ix+1][ny-1],
                          bot[ix+1][ny-1], bot[ix][ny-1]])
        except Exception:
            pass

    # ── circular inset details ─────────────────────
    for iy in range(2, ny-2, 3):
        cy = (iy/(ny-1) - 0.5) * l
        for cx_off in (-w*0.25, w*0.25):
            rv = [bm.verts.new((cx_off + math.cos(a*TAU/12)*0.55,
                                cy + math.sin(a*TAU/12)*0.55,
                                0.02))
                  for a in range(12)]
            try:
                bm.faces.new(rv)
            except Exception:
                pass

    # ── blue emissive channel strips ──────────────
    for side in (-1, 1):
        sv = [bm.verts.new((side * (w*0.5 - 0.20), (iy/(ny-1)-0.5)*l, 0.01))
              for iy in range(ny)]
        for i in range(len(sv)-1):
            bv = [bm.verts.new((sv[i].co.x, sv[i].co.y, -0.04)),
                  bm.verts.new((sv[i+1].co.x, sv[i+1].co.y, -0.04))]
            try:
                bm.faces.new([sv[i], sv[i+1], bv[1], bv[0]])
            except Exception:
                pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_blue_emissive",
                        "mat_ancient_machine_edge_wear", "mat_wet_basalt"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  PLATFORM NODE
# ══════════════════════════════════════════════
# Floating circular platform ~18m diameter, layered slab underside,
# ancient machine surface detail.

VARIANTS = [
    ('SM_Rift_BridgeSpan_A', 24, False, 3),
    ('SM_Rift_BridgeSpan_B_Broken', 24, True, 6),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_BRIDGE_SPAN")
