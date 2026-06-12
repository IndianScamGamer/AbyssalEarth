"""
SM_Elevator_WreckedPanel_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('ElevatorShaft')


def build():
    """Bent wall panel — 1.8×1.2m hull plate buckled along a diagonal crease,
    one corner peeled back, rivet rows intact. Lean against walls or scatter
    on the wreck floor."""
    random.seed(512)
    obj, bm = new_mesh("SM_Elevator_WreckedPanel_A")
    # panel as a 6x4 grid of verts, displaced along a diagonal crease
    NX, NZ = 7, 5
    W, H, T = 1.8, 1.2, 0.05
    front, back = [], []
    for iz in range(NZ):
        for ix in range(NX):
            x = -W / 2 + ix * W / (NX - 1)
            z = iz * H / (NZ - 1)
            # buckle: fold along diagonal x+z, plus peeled corner
            d = (x / W + z / H) - 0.2
            bend = max(0.0, d) ** 2 * 0.55
            if ix >= NX - 2 and iz >= NZ - 2:
                bend += 0.35   # peeled corner
            jitter = random.uniform(-0.02, 0.02)
            front.append(bm.verts.new((x, bend + jitter, z)))
            back.append(bm.verts.new((x, bend + jitter + T, z)))
    def vid(ix, iz):
        return iz * NX + ix
    for iz in range(NZ - 1):
        for ix in range(NX - 1):
            a, b = vid(ix, iz), vid(ix + 1, iz)
            c, d = vid(ix + 1, iz + 1), vid(ix, iz + 1)
            bm.faces.new([front[a], front[b], front[c], front[d]])
            bm.faces.new([back[d], back[c], back[b], back[a]])
    # edge walls
    for iz in range(NZ - 1):
        for ix_edge in [0, NX - 1]:
            a, d = vid(ix_edge, iz), vid(ix_edge, iz + 1)
            if ix_edge == 0:
                bm.faces.new([front[a], front[d], back[d], back[a]])
            else:
                bm.faces.new([back[a], back[d], front[d], front[a]])
    for ix in range(NX - 1):
        for iz_edge in [0, NZ - 1]:
            a, b = vid(ix, iz_edge), vid(ix + 1, iz_edge)
            if iz_edge == 0:
                bm.faces.new([back[a], back[b], front[b], front[a]])
            else:
                bm.faces.new([front[a], front[b], back[b], back[a]])
    # rivet rows along intact edge
    for iz in range(NZ):
        z = iz * H / (NZ - 1)
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.022,
            matrix=Matrix.Translation((-W / 2 + 0.06, -0.012, z)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_ancient_machine_edge_wear"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Elevator_WreckedPanel_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Elevator_WreckedPanel_A")
