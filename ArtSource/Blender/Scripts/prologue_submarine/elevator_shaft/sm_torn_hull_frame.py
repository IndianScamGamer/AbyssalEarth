"""
SM_Elevator_TornHullFrame_A — AbyssalEarth procedural mesh.
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
    """Torn-open hull aperture — 4×3.5m ripped breach frame with jagged
    petal-bent plating around the opening. This is the wreck's exit that
    frames the first view of the Luminous Rift (crashed elevator interior
    concept). Player walks through the hole."""
    random.seed(511)
    obj, bm = new_mesh("SM_Elevator_TornHullFrame_A")
    # surrounding wall panel (5×4.5m with a rough oval hole left open)
    # built as a ring of wall segments around the breach
    W, H = 2.5, 2.25       # half extents of wall
    HOLE_RX, HOLE_RZ = 1.5, 1.3
    SEGS = 14
    outer = []
    inner = []
    for i in range(SEGS):
        a = i * TAU / SEGS
        # outer rectangle-ish boundary
        ox = max(-W, min(W, math.cos(a) * W * 1.5))
        oz = max(0.0, min(2 * H, H + math.sin(a) * H * 1.5))
        outer.append((ox, oz))
        # inner jagged hole boundary
        jag = random.uniform(0.75, 1.2)
        ix = math.cos(a) * HOLE_RX * jag
        iz = H + math.sin(a) * HOLE_RZ * jag
        iz = max(0.05, min(2 * H - 0.05, iz))
        inner.append((ix, iz))
    o_lo = [bm.verts.new((x, 0.0, z)) for x, z in outer]
    o_hi = [bm.verts.new((x, 0.15, z)) for x, z in outer]
    i_lo = [bm.verts.new((x, 0.0, z)) for x, z in inner]
    i_hi = [bm.verts.new((x, 0.15, z)) for x, z in inner]
    for i in range(SEGS):
        ni = (i + 1) % SEGS
        bm.faces.new([o_lo[i], o_lo[ni], i_lo[ni], i_lo[i]])    # front ring
        bm.faces.new([i_hi[i], i_hi[ni], o_hi[ni], o_hi[i]])    # back ring
        bm.faces.new([i_lo[i], i_lo[ni], i_hi[ni], i_hi[i]])    # hole rim
        bm.faces.new([o_hi[i], o_hi[ni], o_lo[ni], o_lo[i]])    # outer rim
    # petal-bent plating: jagged triangular shards bent outward around hole
    for i in range(0, SEGS, 2):
        a = i * TAU / SEGS + random.uniform(-0.1, 0.1)
        bx = math.cos(a) * HOLE_RX * 0.95
        bz = H + math.sin(a) * HOLE_RZ * 0.95
        bz = max(0.1, min(2 * H - 0.1, bz))
        bend = random.uniform(0.5, 1.0)
        # shard: tapered quad bent away from wall (+y)
        root_w = random.uniform(0.25, 0.45)
        tip = bm.verts.new((bx + math.cos(a) * 0.2, -bend,
                             bz + math.sin(a) * 0.3))
        r0 = bm.verts.new((bx - math.sin(a) * root_w, 0.0,
                            bz + math.cos(a) * root_w))
        r1 = bm.verts.new((bx + math.sin(a) * root_w, 0.0,
                            bz - math.cos(a) * root_w))
        bm.faces.new([r0, r1, tip])
    # structural ribs on the intact wall
    for rx in [-2.0, 2.0]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((rx * 1.6, 0.20, H))
            @ Matrix.Scale(0.18, 4, (1, 0, 0))
            @ Matrix.Scale(0.12, 4, (0, 1, 0))
            @ Matrix.Scale(2 * H, 4, (0, 0, 1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_ancient_machine_dark",
                        "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Elevator_TornHullFrame_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Elevator_TornHullFrame_A")
