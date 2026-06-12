"""
SM_Crystal_Scatter_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('SetDressing')

def build():
    """Tiny crystal scatter clump — 30cm breadcrumb accent, cheap tri count."""
    random.seed(206)
    obj, bm = new_mesh("SM_Crystal_Scatter_A")
    for i in range(5):
        a = i * TAU / 5 + random.uniform(-0.3, 0.3)
        cx = math.cos(a) * random.uniform(0.02, 0.10)
        cy = math.sin(a) * random.uniform(0.02, 0.10)
        h = random.uniform(0.08, 0.28)
        w = h * random.uniform(0.18, 0.28)
        tilt_x = random.uniform(-0.2, 0.2)
        tip = bm.verts.new((cx + tilt_x * h, cy, h))
        ring = [bm.verts.new((cx + math.cos(j*TAU/4)*w,
                               cy + math.sin(j*TAU/4)*w, 0)) for j in range(4)]
        for j in range(4):
            bm.faces.new([ring[j], ring[(j+1)%4], tip])
        bm.faces.new(list(reversed(ring)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Crystal_Scatter_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Crystal_Scatter_A")
