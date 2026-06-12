"""
SM_CheckpointActor_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Slice')

def build():
    print("Building SM_CheckpointActor_A …")
    obj, bm = new_mesh("SM_CheckpointActor_A")

    segs = 8
    # ── tapered pylon body (wider at base) ────────
    levels = [
        (0.00, 0.14),   # z, radius
        (0.05, 0.13),
        (0.10, 0.11),
        (0.80, 0.075),
        (1.40, 0.055),
        (1.48, 0.045),
    ]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/segs)*r,
                              math.sin(i*TAU/segs)*r, z))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(segs):
            ni = (i+1)%segs
            bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])

    # base cap
    bm.faces.new(list(reversed(rings[0])))

    # ── emissive ring at 80cm ─────────────────────
    ring_z0, ring_z1 = 0.76, 0.84
    band_r = 0.085
    blo = [bm.verts.new((math.cos(i*TAU/16)*band_r,
                         math.sin(i*TAU/16)*band_r, ring_z0))
           for i in range(16)]
    bhi = [bm.verts.new((math.cos(i*TAU/16)*band_r,
                         math.sin(i*TAU/16)*band_r, ring_z1))
           for i in range(16)]
    for i in range(16):
        ni = (i+1)%16
        bm.faces.new([blo[i], blo[ni], bhi[ni], bhi[i]])

    # ── top disc cap ──────────────────────────────
    top = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                   segments=16, radius=0.06)
    bmesh.ops.translate(bm, verts=top['verts'], vec=Vector((0, 0, 1.48)))
    top_f = [f for f in bm.faces
             if all(abs(v.co.z - 1.48) < 0.01 for v in f.verts)
             and f.calc_center_median().length < 0.07]
    if top_f:
        extrude_region(bm, top_f, 0.018)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_CheckpointActor_A")
    return obj


# ══════════════════════════════════════════════
#  6. STEAM VENT
# ══════════════════════════════════════════════
# Floor grate 80cm diameter with square openings, short 20cm pipe stub.
# VFX from the BP handles the steam column.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_CheckpointActor_A")
