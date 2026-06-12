"""
SM_Later_AshDune_A — AbyssalEarth procedural mesh.
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
    """Soft ash dune — 12m wind-formed mound with crest ridge, used to bury
    the cathedral floor. Concept: LT-001 ground plane."""
    random.seed(403)
    obj, bm = new_mesh("SM_Later_AshDune_A")
    # dune: stretched, flattened icosphere with leeward steepening
    result = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=6.0,
        matrix=Matrix.Translation((0, 0, 0)))
    for v in result['verts']:
        v.co.y *= 1.6
        if v.co.z < 0:
            v.co.z = 0
        else:
            v.co.z *= 0.30
            # windward side (x<0) gentle, leeward steeper
            if v.co.x > 0:
                v.co.x *= 0.72
        v.co.z += random.uniform(-0.04, 0.04)
    # crest ripple bumps
    for i in range(6):
        t = i / 5
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.5,
            matrix=Matrix.Translation((random.uniform(-0.5, 0.5),
                                        -7 + t * 14,
                                        1.55 + random.uniform(-0.15, 0.15))))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_pearl_stone"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Later_AshDune_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Later_AshDune_A")
