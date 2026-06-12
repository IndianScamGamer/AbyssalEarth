"""
SM_EmberVent_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Slice')

def build():
    """AEmberVentHazard — Mantle Garden ember vent: low rocky mound with
    8 small spit-holes and glowing throat, 1.2m diameter."""
    random.seed(121)
    obj, bm = new_mesh("SM_EmberVent_A")
    # mound
    SEGS = 12
    levels = [(0, 0.60), (0.12, 0.55), (0.28, 0.42), (0.42, 0.26), (0.50, 0.14)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/SEGS)*r*random.uniform(0.9, 1.1),
                               math.sin(i*TAU/SEGS)*r*random.uniform(0.9, 1.1),
                               z + random.uniform(-0.02, 0.02)))
                for i in range(SEGS)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i+1)%SEGS], hi[(i+1)%SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    # glowing throat (inner ring at top)
    throat = [bm.verts.new((math.cos(i*TAU/8)*0.10,
                             math.sin(i*TAU/8)*0.10, 0.46)) for i in range(8)]
    bm.faces.new(throat)
    # 8 ember spit-holes on the flanks
    for i in range(8):
        a = i * TAU / 8 + 0.2
        hr = random.uniform(0.30, 0.48)
        hz = random.uniform(0.10, 0.30)
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
            radius=0.035, depth=0.06,
            matrix=Matrix.Translation((math.cos(a)*hr, math.sin(a)*hr, hz))
            @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Rotation(TAU/4, 4, 'Y'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_obsidian", "mat_heat_crack", "mat_lava_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_EmberVent_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_EmberVent_A")
