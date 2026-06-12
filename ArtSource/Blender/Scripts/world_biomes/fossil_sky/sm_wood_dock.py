"""
SM_FossilSky_WoodDock_A — AbyssalEarth procedural mesh.
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


def box(bm, mn, mx):
    x0,y0,z0 = mn; x1,y1,z1 = mx
    vv = [bm.verts.new((x0,y0,z0)), bm.verts.new((x1,y0,z0)),
          bm.verts.new((x1,y1,z0)), bm.verts.new((x0,y1,z0)),
          bm.verts.new((x0,y0,z1)), bm.verts.new((x1,y0,z1)),
          bm.verts.new((x1,y1,z1)), bm.verts.new((x0,y1,z1))]
    for fi in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:
        try: bm.faces.new([vv[i] for i in fi])
        except: pass


# ════════════════════════════════════════════════════════
#  FOSSIL SKY
# ════════════════════════════════════════════════════════

def build_variant(length=8.0, seed=4):
    """Weathered wooden dock section. 2m wide plank-top walkway,
    support posts, cross-braces."""
    print("Building SM_FossilSky_WoodDock_A …")
    obj, bm = new_mesh("SM_FossilSky_WoodDock_A")
    rng = random.Random(seed)

    w = 2.0
    plank_h = 0.05
    n_planks = int(length / 0.25)

    for p in range(n_planks):
        y0 = (p / n_planks - 0.5) * length + rng.uniform(-0.005, 0.005)
        y1 = ((p+1)/n_planks - 0.5) * length + rng.uniform(-0.005, 0.005)
        dip = rng.uniform(-0.01, 0.008)
        box(bm, (-w/2 + 0.01, y0, dip), (w/2 - 0.01, y1, plank_h + dip))

    # support posts
    for py in [i/(4) * length - length/2 for i in range(5)]:
        for px in (-w/2 + 0.12, w/2 - 0.12):
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=6, radius=0.055, depth=0.85,
                                       matrix=Matrix.Translation(Vector((px, py, -0.42))))

    # cross-braces
    for py in [i/3*length - length/2 for i in range(4)]:
        for dx in (-1, 1):
            bv = [bm.verts.new((-w/2*dx, py - length*0.12, -0.05)),
                  bm.verts.new(( w/2*dx, py + length*0.12, -0.70))]

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])  # wood-like
    set_origin_to_base(obj)
    return obj


# ════════════════════════════════════════════════════════
#  GLASSROOT FOREST
# ════════════════════════════════════════════════════════

def build():
    clear_scene()
    obj = build_variant(8.0, 4)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_WoodDock_A")


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_FossilSky_WoodDock_A")
