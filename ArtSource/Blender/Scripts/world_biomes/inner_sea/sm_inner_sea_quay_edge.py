"""
SM_InnerSea_QuayEdge_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('InnerSea')


def build():
    """Fitted basalt quay edge — 6m modular waterfront lip of interlocking
    wet stone blocks, the foreground edge of IS-002. Tile along the shore
    where players stand over the plankton-trail water."""
    random.seed(620)
    obj, bm = new_mesh("SM_InnerSea_QuayEdge_A")
    L = 6.0
    # two courses of fitted blocks with irregular widths
    x = -L / 2
    course_z = [0.0, 0.42]
    while x < L / 2:
        w = random.uniform(0.55, 1.0)
        w = min(w, L / 2 - x)
        for ci, cz in enumerate(course_z):
            off = 0.3 if ci == 1 else 0.0   # running bond offset
            bx = x + off
            if bx + w > L / 2:
                bw = L / 2 - bx
            else:
                bw = w
            if bw < 0.1:
                continue
            d = random.uniform(0.75, 0.95)
            h = 0.40 * random.uniform(0.92, 1.0)
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((bx + bw / 2,
                                            -d / 2 + random.uniform(-0.03, 0.03),
                                            cz + h / 2))
                @ Matrix.Rotation(random.uniform(-0.02, 0.02), 4, 'Z')
                @ Matrix.Scale(bw * 0.97, 4, (1, 0, 0))
                @ Matrix.Scale(d, 4, (0, 1, 0))
                @ Matrix.Scale(h, 4, (0, 0, 1)))
        x += w
    # worn capstone lip overhanging the water side
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, -0.55, 0.92))
        @ Matrix.Scale(L, 4, (1, 0, 0))
        @ Matrix.Scale(0.45, 4, (0, 1, 0))
        @ Matrix.Scale(0.16, 4, (0, 0, 1)))
    # mooring ring posts every 2m
    for px in [-2.0, 0.0, 2.0]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
            radius=0.09, depth=0.35,
            matrix=Matrix.Translation((px, -0.4, 1.15)))
        # iron ring (sphere chain arc)
        for s in range(5):
            sa = PI * s / 4
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035,
                matrix=Matrix.Translation((px + math.cos(sa) * 0.12,
                                            -0.52,
                                            1.28 + math.sin(sa) * -0.10)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_InnerSea_QuayEdge_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_InnerSea_QuayEdge_A")
