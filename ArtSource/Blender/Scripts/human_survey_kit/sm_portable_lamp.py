"""
SM_Human_PortableLamp_A — AbyssalEarth procedural mesh.
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


def box_from_corners(bm, min_pt, max_pt):
    x0,y0,z0 = min_pt
    x1,y1,z1 = max_pt
    verts = [
        bm.verts.new((x0,y0,z0)), bm.verts.new((x1,y0,z0)),
        bm.verts.new((x1,y1,z0)), bm.verts.new((x0,y1,z0)),
        bm.verts.new((x0,y0,z1)), bm.verts.new((x1,y0,z1)),
        bm.verts.new((x1,y1,z1)), bm.verts.new((x0,y1,z1)),
    ]
    faces = [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    for f in faces:
        try:
            bm.faces.new([verts[i] for i in f])
        except Exception:
            pass
    return verts


# ══════════════════════════════════════════════
#  1. SURVEY PLATFORM
# ══════════════════════════════════════════════
# 10×10m modular elevated platform. Grid of square deck panels,
# perimeter safety rail channel, 4 support legs with cross-braces.
# Matches: expedition atmosphere of HE-001 through HE-005.

def build():
    print("Building SM_Human_PortableLamp_A …")
    obj, bm = new_mesh("SM_Human_PortableLamp_A")

    segs = 16

    # ── main cylinder body ────────────────────────
    body = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                      segments=segs, radius=0.10, depth=0.28,
                                      matrix=Matrix.Translation(Vector((0,0,0.14))))

    # ── weighted base disc ─────────────────────────
    base = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                      segments=segs, radius=0.13, depth=0.04,
                                      matrix=Matrix.Translation(Vector((0,0,0.02))))

    # ── amber glow ring band ──────────────────────
    ring_lo = [bm.verts.new((math.cos(i*TAU/segs)*0.105,
                             math.sin(i*TAU/segs)*0.105, 0.18))
               for i in range(segs)]
    ring_hi = [bm.verts.new((math.cos(i*TAU/segs)*0.105,
                             math.sin(i*TAU/segs)*0.105, 0.22))
               for i in range(segs)]
    for i in range(segs):
        ni=(i+1)%segs
        try:
            bm.faces.new([ring_lo[i], ring_lo[ni], ring_hi[ni], ring_hi[i]])
        except Exception:
            pass

    # ── top diffuser cap ──────────────────────────
    top_cap = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                         segments=segs, radius=0.08, depth=0.06,
                                         matrix=Matrix.Translation(Vector((0,0,0.31))))

    # ── side panel emboss ──────────────────────────
    box_from_corners(bm, (-0.055, 0.10, 0.08), (0.055, 0.104, 0.16))
    box_from_corners(bm, (-0.020, 0.10, 0.23), (0.020, 0.104, 0.27))

    # ── cable stub ────────────────────────────────
    cable_segs = 6
    cable_dir  = [bm.verts.new((0.10 + t*0.12,
                                -0.02 + math.sin(t*PI)*0.04,
                                0.10)) for t in [i/5 for i in range(6)]]

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Human_PortableLamp_A")
    return obj


# ══════════════════════════════════════════════
#  4. CABLE COIL
# ══════════════════════════════════════════════
# Drum reel on a stand, partially unwound cable visible.
# Matches: expedition_crates_props_concept.png (cable reel item).

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Human_PortableLamp_A")
