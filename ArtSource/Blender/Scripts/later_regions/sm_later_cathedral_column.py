"""
SM_Later_CathedralColumn_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('LaterRegions')

def build():
    """Ash cathedral column — eroded natural gothic column 45m tall that
    flares into pointed-arch buttresses at the top. Concept: LT-001."""
    random.seed(401)
    obj, bm = new_mesh("SM_Later_CathedralColumn_A")
    SEGS = 10
    H = 45.0
    # main shaft with entasis (slight swell) and erosion jitter
    stations = [(0, 3.2), (5, 2.9), (15, 2.5), (28, 2.3), (38, 2.6), (45, 3.4)]
    rings = []
    for z, r in stations:
        ring = [bm.verts.new((math.cos(i*TAU/SEGS)*r*random.uniform(0.92, 1.08),
                               math.sin(i*TAU/SEGS)*r*random.uniform(0.92, 1.08),
                               z + random.uniform(-0.4, 0.4)))
                for i in range(SEGS)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i+1)%SEGS], hi[(i+1)%SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # 4 arch buttresses flaring from the crown (pointed-arch ribs)
    for i in range(4):
        a = i * TAU / 4
        ARC_SEGS = 7
        for s in range(ARC_SEGS):
            t = s / (ARC_SEGS - 1)
            # quarter arch sweeping out and down from crown
            reach = math.sin(t * PI / 2) * 9.0
            drop = (1 - math.cos(t * PI / 2)) * 12.0
            px = math.cos(a) * (3.0 + reach)
            py = math.sin(a) * (3.0 + reach)
            pz = 44.0 - drop
            r = 1.1 * (1 - t * 0.5)
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r,
                matrix=Matrix.Translation((px, py, pz)))
    # vertical erosion flutes
    for i in range(5):
        a = i * TAU / 5 + 0.3
        for z in range(4, 40, 5):
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((math.cos(a)*2.55, math.sin(a)*2.55, z))
                @ Matrix.Rotation(a, 4, 'Z')
                @ Matrix.Scale(0.25, 4, (1,0,0))
                @ Matrix.Scale(0.5, 4, (0,1,0))
                @ Matrix.Scale(3.5, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_pearl_stone", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Later_CathedralColumn_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Later_CathedralColumn_A")
