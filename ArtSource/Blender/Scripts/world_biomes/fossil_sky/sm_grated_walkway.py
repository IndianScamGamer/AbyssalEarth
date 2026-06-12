"""
SM_FossilSky_GratedWalkway_A — AbyssalEarth procedural mesh.
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
    """Expedition grated walkway — 6m modular metal span: open-mesh deck,
    twin thin handrails on slender balusters, kick plates, under-truss.
    The human-built route through FS-002's cathedral; deliberately spindly
    so the fossils dwarf it."""
    obj, bm = new_mesh("SM_FossilSky_GratedWalkway_A")
    L, W = 6.0, 1.6
    # deck frame rails
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, side * W / 2, 0.06))
            @ Matrix.Scale(L, 4, (1, 0, 0))
            @ Matrix.Scale(0.08, 4, (0, 1, 0))
            @ Matrix.Scale(0.12, 4, (0, 0, 1)))
    # grate: longitudinal bars + cross bars (open mesh)
    for k in range(7):
        gy = -W / 2 + 0.2 + k * 0.2
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, gy, 0.10))
            @ Matrix.Scale(L * 0.98, 4, (1, 0, 0))
            @ Matrix.Scale(0.025, 4, (0, 1, 0))
            @ Matrix.Scale(0.04, 4, (0, 0, 1)))
    for k in range(13):
        gx = -L / 2 + 0.25 + k * 0.46
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((gx, 0, 0.085))
            @ Matrix.Scale(0.025, 4, (1, 0, 0))
            @ Matrix.Scale(W * 0.92, 4, (0, 1, 0))
            @ Matrix.Scale(0.03, 4, (0, 0, 1)))
    # kick plates along both edges
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, side * (W / 2 - 0.01), 0.18))
            @ Matrix.Scale(L, 4, (1, 0, 0))
            @ Matrix.Scale(0.02, 4, (0, 1, 0))
            @ Matrix.Scale(0.10, 4, (0, 0, 1)))
    # slender balusters + twin rails
    for side in [-1, 1]:
        for k in range(5):
            bx = -L / 2 + 0.3 + k * 1.35
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
                radius=0.022, depth=1.05,
                matrix=Matrix.Translation((bx, side * W / 2, 0.64)))
        for rz in [0.70, 1.12]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
                radius=0.020, depth=L,
                matrix=Matrix.Translation((0, side * W / 2, rz))
                @ Matrix.Rotation(TAU / 4, 4, 'Y'))
    # under-truss: shallow V struts beneath the deck
    for k in range(4):
        tx = -L / 2 + 0.75 + k * 1.5
        for sx in [-1, 1]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=5,
                radius=0.030, depth=0.85,
                matrix=Matrix.Translation((tx + sx * 0.30, 0, -0.30))
                @ Matrix.Rotation(sx * 0.75, 4, 'Y'))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.06,
            matrix=Matrix.Translation((tx, 0, -0.66)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_ancient_machine_edge_wear"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_GratedWalkway_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_FossilSky_GratedWalkway_A")
