"""
SM_Rift_HangingHose_Bundle_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('LuminousRift')


def build():
    """Hanging hose bundle — 5 thick ancient conduits drooping 8m off a
    structure edge with a collar manifold at the anchor and frayed lower
    ends. The heavy cable drapery on the machine structures in LR-005."""
    random.seed(731)
    obj, bm = new_mesh("SM_Rift_HangingHose_Bundle_A")
    # anchor manifold collar at the top
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 8.0))
        @ Matrix.Scale(2.0, 4, (1, 0, 0))
        @ Matrix.Scale(1.0, 4, (0, 1, 0))
        @ Matrix.Scale(0.7, 4, (0, 0, 1)))
    for px in [-0.7, 0.0, 0.7]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=8,
            radius=0.28, depth=0.45,
            matrix=Matrix.Translation((px, 0, 7.55)))
    # 5 drooping hoses: lofted tube along a hanging curve
    for h in range(5):
        x0 = -0.8 + h * 0.4
        sway = random.uniform(-0.8, 0.8)
        drop = random.uniform(5.5, 7.8)
        hr = random.uniform(0.14, 0.24)
        SEGS = 14
        prev_ring = None
        for s in range(SEGS):
            t = s / (SEGS - 1)
            # curve: starts vertical, bows outward then hangs
            cx = x0 + math.sin(t * PI * 0.8) * sway
            cy = -t * t * 1.6
            cz = 7.6 - t * drop
            ring = []
            for i in range(7):
                a = i * TAU / 7
                ring.append(bm.verts.new((cx + math.cos(a) * hr,
                                           cy + math.sin(a) * hr * 0.8,
                                           cz)))
            if prev_ring:
                for i in range(7):
                    bm.faces.new([prev_ring[i], prev_ring[(i + 1) % 7],
                                   ring[(i + 1) % 7], ring[i]])
            prev_ring = ring
            # segment collar every 4th step
            if s % 4 == 2:
                bmesh.ops.create_cylinder(bm, cap_ends=False, segments=8,
                    radius=hr * 1.25, depth=0.12,
                    matrix=Matrix.Translation((cx, cy, cz)))
        # frayed end: connector stub or torn strands
        end_x = x0 + math.sin(PI * 0.8) * sway
        end_y = -1.6
        end_z = 7.6 - drop
        if h % 2 == 0:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
                radius=hr * 1.1, depth=0.30,
                matrix=Matrix.Translation((end_x, end_y, end_z - 0.15)))
        else:
            for f in range(3):
                bmesh.ops.create_cylinder(bm, cap_ends=True, segments=4,
                    radius=0.025, depth=0.4,
                    matrix=Matrix.Translation((end_x + random.uniform(-0.1, 0.1),
                                                end_y + random.uniform(-0.1, 0.1),
                                                end_z - 0.2))
                    @ Matrix.Rotation(random.uniform(-0.4, 0.4), 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_HangingHose_Bundle_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Rift_HangingHose_Bundle_A")
