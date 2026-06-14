"""
SM_Rift_MachineCliff_Facade_A — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-005, LR-017
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
    """Machine cliff facade — 30×40m canyon wall of stacked ancient machinery:
    stepped strata blocks, recessed panel bays, pipe galleries, vent rows,
    and a cantilevered ledge. The cliff faces flanking the chasm in LR-005.
    Tile side-by-side and mirror for canyon walls."""
    random.seed(730)
    obj, bm = new_mesh("SM_Rift_MachineCliff_Facade_A")
    W, H, D = 30.0, 40.0, 6.0
    # stepped strata: 6 stacked slabs, each set back or forward irregularly
    z = 0.0
    for layer in range(6):
        lh = random.uniform(4.5, 8.5)
        lh = min(lh, H - z)
        setback = random.uniform(-1.2, 1.2)
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, setback, z + lh / 2))
            @ Matrix.Scale(W, 4, (1, 0, 0))
            @ Matrix.Scale(D, 4, (0, 1, 0))
            @ Matrix.Scale(lh, 4, (0, 0, 1)))
        # recessed panel bays on this layer's face
        n_bays = random.randint(3, 5)
        for b in range(n_bays):
            bx = -W / 2 + (b + 0.5) * W / n_bays + random.uniform(-1, 1)
            bw = W / n_bays * random.uniform(0.5, 0.75)
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((bx, setback - D / 2 - 0.15,
                                            z + lh / 2))
                @ Matrix.Scale(bw, 4, (1, 0, 0))
                @ Matrix.Scale(0.5, 4, (0, 1, 0))
                @ Matrix.Scale(lh * 0.6, 4, (0, 0, 1)))
        # seam strip between layers with blue emissive groove
        if layer > 0:
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((0, setback - D / 2 - 0.05, z))
                @ Matrix.Scale(W * 0.96, 4, (1, 0, 0))
                @ Matrix.Scale(0.10, 4, (0, 1, 0))
                @ Matrix.Scale(0.10, 4, (0, 0, 1)))
        z += lh
        if z >= H:
            break
    # pipe gallery: 4 fat horizontal pipes running across mid-face
    for k in range(4):
        pz = 14.0 + k * 1.3
        pr = random.uniform(0.30, 0.55)
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=10,
            radius1=pr, radius2=pr, depth=W * 0.9,
            matrix=Matrix.Translation((0, -D / 2 - 0.9, pz))
            @ Matrix.Rotation(TAU / 4, 4, 'Y'))
        # pipe saddle clamps
        for cx in [-10, 0, 10]:
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((cx, -D / 2 - 0.9, pz))
                @ Matrix.Scale(0.5, 4, (1, 0, 0))
                @ Matrix.Scale(pr * 2.6, 4, (0, 1, 0))
                @ Matrix.Scale(pr * 2.6, 4, (0, 0, 1)))
    # vent row: dark slots near the top
    for v in range(6):
        vx = -W / 2 + 3 + v * 4.8
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((vx, -D / 2 - 0.2, 34.0))
            @ Matrix.Scale(2.2, 4, (1, 0, 0))
            @ Matrix.Scale(0.5, 4, (0, 1, 0))
            @ Matrix.Scale(1.0, 4, (0, 0, 1)))
    # cantilevered ledge walkable shelf at 20m
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((2.0, -D / 2 - 1.6, 20.0))
        @ Matrix.Scale(14.0, 4, (1, 0, 0))
        @ Matrix.Scale(3.2, 4, (0, 1, 0))
        @ Matrix.Scale(0.6, 4, (0, 0, 1)))
    # ledge support knees
    for kx in [-3.5, 2.0, 7.5]:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=5,
            radius1=0.35, radius2=0.35, depth=2.6,
            matrix=Matrix.Translation((kx, -D / 2 - 1.2, 18.6))
            @ Matrix.Rotation(0.6, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_MachineCliff_Facade_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Rift_MachineCliff_Facade_A")
