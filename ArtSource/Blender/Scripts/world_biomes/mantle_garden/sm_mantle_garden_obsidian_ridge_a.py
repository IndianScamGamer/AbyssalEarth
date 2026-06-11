"""
SM_MantleGarden_ObsidianRidge_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('MantleGarden')


def build():
    """SM_MantleGarden_ObsidianRidge_A — 50m walkable obsidian ridge, heat cracks."""
    import random; random.seed(51)
    obj, bm = new_mesh("SM_MantleGarden_ObsidianRidge_A")
    SEGS = 20
    L = 50.0
    rings = []
    for i in range(SEGS + 1):
        t = i/SEGS
        cx = (t-0.5)*L
        cz = math.sin(t*math.pi)*1.5 + random.uniform(-0.3,0.3)
        # sharp diamond cross-section
        pts = [
            (cx, -2.0, cz),
            (cx, -0.5, cz + 1.2 + random.uniform(-0.1,0.1)),
            (cx,  0.5, cz + 1.2 + random.uniform(-0.1,0.1)),
            (cx,  2.0, cz),
        ]
        ring = [bm.verts.new(p) for p in pts]
        rings.append(ring)
    for ri in range(SEGS):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(3):
            bm.faces.new([lo[j], lo[j+1], hi[j+1], hi[j]])
    # heat crack fissures
    for i in range(8):
        t = i/7
        cx = (t-0.5)*L*0.9
        cz = math.sin(t*math.pi)*1.5
        for fi in range(4):
            ft = fi/3
            bm.verts.new((cx + random.uniform(-1,1),
                           random.uniform(-0.3,0.3),
                           cz + 0.5 + ft*0.8))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_obsidian", "mat_heat_crack"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_MantleGarden_ObsidianRidge_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_MantleGarden_ObsidianRidge_A")
