"""
SM_OVERHANG — AbyssalEarth procedural mesh.
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

def build(name, width, depth, seed=15):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    n = 10
    # ── bottom face profile (irregular) ──────────
    bot_pts = []
    for i in range(n):
        t = i / (n - 1)
        bx = (t - 0.5) * width + rng.uniform(-0.5, 0.5)
        by = rng.uniform(-depth * 0.15, depth * 0.15)
        bot_pts.append(bm.verts.new((bx, by, 0.0)))

    top_pts = []
    for i, bv in enumerate(bot_pts):
        t = i / (n - 1)
        thk = rng.uniform(1.5, 4.0)
        ovh = depth * (0.5 + 0.5 * abs(1 - 2*t))  # deeper at edges
        top_pts.append(bm.verts.new((bv.co.x + rng.uniform(-0.3, 0.3),
                                     bv.co.y + ovh,
                                     thk + rng.uniform(-0.3, 0.3))))

    # faces
    try:
        bm.faces.new(list(reversed(bot_pts)))
        bm.faces.new(top_pts)
    except Exception:
        pass
    for i in range(n-1):
        try:
            bm.faces.new([bot_pts[i], bot_pts[i+1],
                          top_pts[i+1], top_pts[i]])
        except Exception:
            pass
    # side caps
    try:
        bm.faces.new([bot_pts[0], top_pts[0],
                      bm.verts.new((bot_pts[0].co.x - 0.3, top_pts[0].co.y, 0))])
        bm.faces.new([bot_pts[-1], top_pts[-1],
                      bm.verts.new((bot_pts[-1].co.x + 0.3, top_pts[-1].co.y, 0))])
    except Exception:
        pass

    # ── stalactite-style crystal drips ────────────
    for _ in range(rng.randint(3, 6)):
        cx = rng.uniform(-width*0.35, width*0.35)
        cy = rng.uniform(0, depth * 0.3)
        ch = rng.uniform(0.3, 0.8)
        cv = [bm.verts.new((cx + math.cos(a*TAU/4)*0.08,
                            cy + math.sin(a*TAU/4)*0.08,
                            rng.uniform(-0.2, 0.2)))
              for a in range(4)]
        ctip = bm.verts.new((cx, cy, -ch))
        try:
            bm.faces.new(list(reversed(cv)))
            for i in range(4):
                bm.faces.new([cv[i], cv[(i+1)%4], ctip])
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  HANGING SLAB
# ══════════════════════════════════════════════
# Large fractured rock slab suspended from the ceiling. Crystal clusters
# embedded on underside. Convincing fracture geometry at anchor.
# Matches: AD-006 (Hanging Slab — Ceiling Detail).

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_OVERHANG")
