"""
SM_Rift_PlatformNode_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Rift_PlatformNode_A …")
    obj, bm = new_mesh("SM_Rift_PlatformNode_A")

    r = 9.0
    segs = 24

    # ── top surface (irregular circle) ───────────
    rng = random.Random(5)
    top_verts = [bm.verts.new((
                     math.cos(i*TAU/segs) * (r + rng.uniform(-0.5, 0.5)),
                     math.sin(i*TAU/segs) * (r + rng.uniform(-0.5, 0.5)),
                     rng.uniform(-0.12, 0.12)))
                 for i in range(segs)]
    try:
        bm.faces.new(top_verts)
    except Exception:
        pass

    # ── underslab steps (3 tiers) ─────────────────
    prev = top_verts
    for tier, (depth, squeeze) in enumerate([(0.5, 0.88), (1.4, 0.74), (2.8, 0.60)]):
        curr = [bm.verts.new((v.co.x * squeeze + rng.uniform(-0.15,0.15),
                              v.co.y * squeeze + rng.uniform(-0.15,0.15),
                              -depth))
                for v in prev]
        for j in range(segs):
            nj=(j+1)%segs
            try:
                bm.faces.new([prev[j], prev[nj], curr[nj], curr[j]])
            except Exception:
                pass
        prev = curr
    # bottom cap
    try:
        bm.faces.new(list(reversed(prev)))
    except Exception:
        pass

    # ── surface hex-grid inset detail ─────────────
    for hr in range(3):
        for hangle_i in range(6 if hr > 0 else 1):
            hangle = hangle_i * TAU/6
            hr_r   = hr * 3.5
            hcx    = math.cos(hangle) * hr_r
            hcy    = math.sin(hangle) * hr_r
            for s in range(6):
                a0 = s * TAU/6
                a1 = (s+1)*TAU/6
                pv = [bm.verts.new((hcx + math.cos(a)*1.6, hcy + math.sin(a)*1.6, 0.02))
                      for a in (a0, a1, a1, a0)]
                try:
                    bm.faces.new(pv)
                except Exception:
                    pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_blue_emissive",
                        "mat_ancient_machine_edge_wear"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  ANCIENT GATE WALL
# ══════════════════════════════════════════════
# Right-side gate wall structure. 50m wide × 100m tall.
# Two large circular sockets with blue emissive centres,
# nested rings, radial grooves, rock intrusions at base.
# Matches: concept art gate wall visible in Luminous Rift shots.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Rift_PlatformNode_A")
