"""
SM_FossilSky_CeilingSkeleton_Hero_A — AbyssalEarth procedural mesh.
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


def build():
    """SM_FossilSky_CeilingSkeleton_Hero_A — 120m hero ceiling fossil."""
    import random; random.seed(13)
    obj, bm = new_mesh("SM_FossilSky_CeilingSkeleton_Hero_A")
    # spine chain
    SPINE_LEN = 120.0
    SPINE_SEGS = 30
    for i in range(SPINE_SEGS):
        t = i / (SPINE_SEGS-1)
        sx = (t - 0.5) * SPINE_LEN
        sz = random.uniform(-1.5, 1.5)
        r = 1.2 - t * 0.6
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r,
            matrix=Matrix.Translation((sx, 0, sz)))
    # 6 large ribs
    for ri in range(6):
        t = (ri + 1) / 7
        rx = (t - 0.5) * SPINE_LEN * 0.85
        for side in [-1, 1]:
            RIB_SPAN = random.uniform(8, 16)
            RIB_H = random.uniform(6, 12)
            SEGS = 10
            for si in range(SEGS + 1):
                rt = si / SEGS
                x = rx + side * math.sin(rt * math.pi) * RIB_SPAN
                z = -RIB_H * math.sin(rt * math.pi) + random.uniform(-0.3, 0.3)
                bmesh.ops.create_icosphere(bm, subdivisions=1,
                    radius=0.35 * (1-rt*0.7),
                    matrix=Matrix.Translation((x, side*0.4, z)))
    # skull mass at one end
    skull_x = -SPINE_LEN * 0.45
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=4.5,
        matrix=Matrix.Translation((skull_x, 0, 0)))
    for eye_side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.2,
            matrix=Matrix.Translation((skull_x - 1.5, eye_side*2.5, 1.0)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_CeilingSkeleton_Hero_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_FossilSky_CeilingSkeleton_Hero_A")
