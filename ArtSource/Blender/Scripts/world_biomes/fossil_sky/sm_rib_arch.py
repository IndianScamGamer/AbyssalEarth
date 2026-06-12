"""
SM_RIB_ARCH — AbyssalEarth procedural mesh.
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

def build_variant(name, span, height, rib_w, seed=1):
    """Giant fossil rib bone arching over a tunnel.
    Organic elongated parabola with bone texture striations.
    Matches: fossil_sky_concept.png — ribs arching over the entire tunnel ceiling."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs  = 20
    arc   = 0.92       # fraction of circle
    half  = span * 0.5

    rings = []
    for seg in range(int(segs * arc) + 1):
        t     = seg / segs
        angle = t * TAU * arc
        cx    = math.cos(angle) * half
        cz    = math.sin(angle) * height
        # organic bone cross-section (flattened oval)
        tw = rib_w * (0.7 + 0.5 * math.sin(t * PI))  # thicker in middle
        th = tw * 0.55                                  # flatter = bone
        ring = [bm.verts.new((
                    cx + math.cos(a*TAU/8)*tw,
                    math.sin(a*TAU/8)*th + rng.uniform(-0.02, 0.02),
                    cz + rng.uniform(-0.05*height, 0.05*height)))
                for a in range(8)]
        rings.append(ring)
        # bone striation grooves along length
        if seg % 3 == 0:
            for j in (0, 4):
                gv = bm.verts.new((cx + math.cos(j*TAU/8)*tw*1.02,
                                   math.sin(j*TAU/8)*th*1.02,
                                   cz))

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(8):
            nj=(j+1)%8
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    if rings:
        try: bm.faces.new(list(reversed(rings[0])))
        except: pass
        try: bm.faces.new(rings[-1])
        except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_fossil_bone"])
    set_origin_to_base(obj)
    return obj

VARIANTS = [
    ('SM_FossilSky_RibArch_A', 22, 14, 2.2, 1),
    ('SM_FossilSky_RibArch_B', 32, 20, 3.0, 5),
    ('SM_FossilSky_RibArch_C', 15, 10, 1.6, 9),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_RIB_ARCH")
