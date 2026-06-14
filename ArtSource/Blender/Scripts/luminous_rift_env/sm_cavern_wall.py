"""
SM_CAVERN_WALL — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-001, LR-003
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

def build_variant(name, width, height, depth, seed=99):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    nx, nz = 8, 10
    verts = []
    for ix in range(nx):
        col = []
        for iz in range(nz):
            x = (ix / (nx-1) - 0.5) * width
            z = iz / (nz-1) * height
            # vertical striation noise (deeper in y = wall thickness)
            y_noise = math.sin(x * 0.8) * 0.8 + math.cos(x * 1.4) * 0.5
            y = -depth * 0.5 + y_noise + rng.uniform(-0.3, 0.3)
            z += rng.uniform(-0.15, 0.15)
            col.append(bm.verts.new((x, y, z)))
        verts.append(col)

    for ix in range(nx-1):
        for iz in range(nz-1):
            try:
                bm.faces.new([verts[ix][iz],   verts[ix+1][iz],
                               verts[ix+1][iz+1], verts[ix][iz+1]])
            except Exception:
                pass

    # ── crystal sockets ────────────────────────────
    for _ in range(rng.randint(2, 5)):
        cx = rng.uniform(-width*0.35, width*0.35)
        cz = rng.uniform(height*0.15, height*0.80)
        h  = rng.uniform(0.5, 1.5)
        cv = [bm.verts.new((cx + math.cos(a*TAU/5)*0.18,
                            rng.uniform(-depth*0.3, 0),
                            cz + math.sin(a*TAU/5)*0.18))
              for a in range(5)]
        ctip = bm.verts.new((cx, rng.uniform(0, depth*0.1), cz + h))
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
#  MAIN
# ══════════════════════════════════════════════

VARIANTS = [
    ('SM_Rift_CavernWall_Large_A', 40, 30, 5, 99),
    ('SM_Rift_CavernWall_Large_B', 60, 40, 8, 111),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_CAVERN_WALL")
