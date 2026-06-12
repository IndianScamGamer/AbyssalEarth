"""
SM_Glassroot_CanopyCluster_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GlassrootForest')


def build():
    """Glowing canopy bulb cluster — 6m mass of luminous pods on branching
    stems; the green background glow of GR-002. Hang from trunk crowns or
    cavern ceiling; emissive material drives the bloom."""
    random.seed(611)
    obj, bm = new_mesh("SM_Glassroot_CanopyCluster_A")
    # 3 branching stems from a common root
    for b in range(3):
        ba = b * TAU / 3 + random.uniform(-0.3, 0.3)
        SEGS = 6
        bx = by = 0.0
        bz = 0.0
        dx = math.cos(ba) * 0.7
        dy = math.sin(ba) * 0.7
        for s in range(SEGS):
            t = s / (SEGS - 1)
            bx += dx * (1 - t * 0.4)
            by += dy * (1 - t * 0.4)
            bz += 0.85
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=5,
                radius=0.10 * (1 - t * 0.6), depth=0.9,
                matrix=Matrix.Translation((bx, by, bz)))
            # pods budding off each stem segment
            for p in range(2):
                pa = random.uniform(0, TAU)
                pr = random.uniform(0.25, 0.55)
                pod = bmesh.ops.create_icosphere(bm, subdivisions=1,
                    radius=random.uniform(0.18, 0.42),
                    matrix=Matrix.Translation((bx + math.cos(pa) * pr,
                                                by + math.sin(pa) * pr,
                                                bz + random.uniform(-0.3, 0.3))))
                for v in pod['verts']:
                    v.co.z = bz + (v.co.z - bz) * 1.25   # teardrop stretch
    # dense crown mass of large pods at top
    for c in range(8):
        ca = c * TAU / 8 + random.uniform(-0.2, 0.2)
        cr = random.uniform(0.3, 1.1)
        bmesh.ops.create_icosphere(bm, subdivisions=1,
            radius=random.uniform(0.35, 0.65),
            matrix=Matrix.Translation((math.cos(ca) * cr,
                                        math.sin(ca) * cr,
                                        5.0 + random.uniform(-0.4, 0.5))))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_water_bioluminescent"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_CanopyCluster_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Glassroot_CanopyCluster_A")
