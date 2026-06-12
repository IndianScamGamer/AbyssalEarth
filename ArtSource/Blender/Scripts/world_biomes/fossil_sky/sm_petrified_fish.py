"""
SM_FossilSky_PetrifiedFish (A/B) — AbyssalEarth procedural mesh.
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


def build_variant(name, length, girth, seed):
    """Petrified coelacanth — ancient fish preserved in stone, suspended
    mid-air in the Fossil Sky cavern (FS-002). Lofted body with dorsal and
    paired lobe fins, gill plates, cyan fossil-vein ridge lines."""
    random.seed(seed)
    obj, bm = new_mesh(name)
    SEGS = 12
    # body stations: (t along length, radius factor, z drift)
    stations = [(0.00, 0.06, 0.00), (0.08, 0.32, 0.02), (0.22, 0.66, 0.03),
                (0.38, 0.92, 0.02), (0.52, 1.00, 0.00), (0.66, 0.86, -0.02),
                (0.78, 0.58, -0.03), (0.88, 0.30, -0.02), (0.95, 0.16, 0.00),
                (1.00, 0.30, 0.04)]   # tail flare
    rings = []
    for t, rf, zd in stations:
        y = -length / 2 + t * length
        r = girth * rf
        ring = []
        for i in range(SEGS):
            a = i * TAU / SEGS
            # fish cross-section: taller than wide
            x = math.cos(a) * r * 0.62 * random.uniform(0.97, 1.03)
            z = girth + zd * length + math.sin(a) * r * random.uniform(0.97, 1.03)
            ring.append(bm.verts.new((x, y, z)))
        rings.append(ring)
    for ri in range(len(rings) - 1):
        lo, hi = rings[ri], rings[ri + 1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i + 1) % SEGS],
                           hi[(i + 1) % SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # tail fin: vertical fan of tapered blades
    tail_y = length / 2
    for k in range(5):
        ka = -0.7 + k * 0.35
        blade_l = girth * random.uniform(1.2, 1.7)
        v0 = bm.verts.new((0, tail_y - 0.05 * length, girth))
        v1 = bm.verts.new((0, tail_y + blade_l * 0.8,
                            girth + math.sin(ka) * blade_l))
        v2 = bm.verts.new((0, tail_y + blade_l * 0.5,
                            girth + math.sin(ka) * blade_l * 0.5 + 0.08 * girth))
        bm.faces.new([v0, v1, v2])
    # dorsal fin: serrated sail at 45-60% length
    for k in range(4):
        t = 0.42 + k * 0.06
        fy = -length / 2 + t * length
        fh = girth * random.uniform(0.5, 0.8)
        v0 = bm.verts.new((0, fy, girth * 1.9))
        v1 = bm.verts.new((0, fy + length * 0.04, girth * 1.9 + fh))
        v2 = bm.verts.new((0, fy + length * 0.07, girth * 1.9))
        bm.faces.new([v0, v1, v2])
    # paired pectoral lobe fins
    for side in [-1, 1]:
        fy = -length / 2 + 0.30 * length
        root = bm.verts.new((side * girth * 0.55, fy, girth * 0.7))
        tip = bm.verts.new((side * girth * 1.5, fy + length * 0.10,
                             girth * 0.35))
        trail = bm.verts.new((side * girth * 0.6, fy + length * 0.12,
                               girth * 0.6))
        bm.faces.new([root, tip, trail])
    # gill plate ring detail
    gy = -length / 2 + 0.16 * length
    for i in range(SEGS):
        a = i * TAU / SEGS
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=girth * 0.05,
            matrix=Matrix.Translation((math.cos(a) * girth * 0.40,
                                        gy,
                                        girth + math.sin(a) * girth * 0.62)))
    # eye socket boss
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=girth * 0.13,
        matrix=Matrix.Translation((girth * 0.30, -length / 2 + 0.09 * length,
                                    girth * 1.25)))
    # cyan fossil-vein ridge: bead line along the flank
    for s in range(10):
        t = 0.15 + s * 0.07
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=girth * 0.035,
            matrix=Matrix.Translation((girth * 0.55,
                                        -length / 2 + t * length,
                                        girth * 1.1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein"])
    set_origin_to_base(obj)
    return obj


VARIANTS = [
    ("SM_FossilSky_PetrifiedFish_A", 8.0, 1.1, 701),
    ("SM_FossilSky_PetrifiedFish_B", 5.0, 0.65, 702),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_FossilSky_PetrifiedFish_A/B")
