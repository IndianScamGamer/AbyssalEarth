"""
SM_Beacon_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Beacon_A …")
    obj, bm = new_mesh("SM_Beacon_A")

    # ── main stake body ───────────────────────────
    stake = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=12, radius=0.025, depth=0.46)
    bmesh.ops.translate(bm, verts=stake['verts'], vec=Vector((0, 0, 0.23)))

    # ── pointed bottom spike ──────────────────────
    spike_base = [bm.verts.new((math.cos(a*TAU/8)*0.022,
                                math.sin(a*TAU/8)*0.022, 0.02))
                  for a in range(8)]
    spike_tip  = bm.verts.new((0, 0, -0.055))
    bm.faces.new(list(reversed(spike_base)))
    for i in range(8):
        bm.faces.new([spike_base[i], spike_base[(i+1)%8], spike_tip])

    # ── emissive light ring band ──────────────────
    ring_segs = 20
    for r_mult, z_off in [(1.0, 0.28), (1.0, 0.30)]:
        rv = [bm.verts.new((math.cos(a*TAU/ring_segs)*0.038*r_mult,
                            math.sin(a*TAU/ring_segs)*0.038*r_mult,
                            z_off))
              for a in range(ring_segs)]
        for i in range(ring_segs):
            pass   # ring verts exist; face bridging below

    ring_lo = [bm.verts.new((math.cos(a*TAU/16)*0.038,
                             math.sin(a*TAU/16)*0.038, 0.27))
               for a in range(16)]
    ring_hi = [bm.verts.new((math.cos(a*TAU/16)*0.038,
                             math.sin(a*TAU/16)*0.038, 0.31))
               for a in range(16)]
    for i in range(16):
        ni = (i+1)%16
        bm.faces.new([ring_lo[i], ring_lo[ni], ring_hi[ni], ring_hi[i]])

    # ── top emitter dome cap ──────────────────────
    cap = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035,
                                      matrix=Matrix.Translation(
                                          Vector((0, 0, 0.50))))
    # flatten bottom half of dome
    for v in cap['verts']:
        if v.co.z < 0.50:
            v.co.z = 0.50

    # ── base disc with grip notches ───────────────
    base_disc = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                         segments=8, radius=0.06)
    bmesh.ops.translate(bm, verts=base_disc['verts'],
                        vec=Vector((0, 0, 0.01)))
    base_f = [f for f in bm.faces
              if all(v.co.z < 0.02 for v in f.verts)
              and f.calc_center_median().length < 0.07]
    if base_f:
        extrude_region(bm, base_f, 0.015, Vector((0, 0, -1)))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Beacon_A")
    return obj


# ══════════════════════════════════════════════
#  5. CHECKPOINT PYLON
# ══════════════════════════════════════════════
# 150cm exploration waypoint marker. Tapered octagonal pylon, wide at
# base, emissive ring band at 80cm, glowing disc top cap.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Beacon_A")
