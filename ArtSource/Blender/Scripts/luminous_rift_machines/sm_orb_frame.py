"""
SM_Rift_OrbFrame_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Rift_OrbFrame_A …")
    obj, bm = new_mesh("SM_Rift_OrbFrame_A")

    ring_r = 15.0        # frame ring radius
    tube_r = 0.85        # frame cross-section
    segs   = 28          # ring segments (we leave a gap)
    arc    = 0.82        # fraction of full circle (leaves ~65° gap)

    rng = random.Random(7)
    rings_verts = []
    for seg in range(int(segs * arc) + 1):
        t     = seg / segs
        angle = t * TAU * arc - PI/2
        cx    = math.cos(angle) * ring_r
        cz    = math.sin(angle) * ring_r
        tr    = tube_r + rng.uniform(-0.08, 0.12)

        ring = [bm.verts.new((
                    cx + math.cos(a*TAU/10) * tr,
                    math.sin(a*TAU/10) * tr,
                    cz + math.cos(a*TAU/10) * tr * 0.3))
                for a in range(10)]
        rings_verts.append((cx, cz, ring))

    for ri in range(len(rings_verts)-1):
        _, _, lo = rings_verts[ri]
        _, _, hi = rings_verts[ri+1]
        for j in range(10):
            nj=(j+1)%10
            try:
                bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except Exception:
                pass
    # end caps
    if rings_verts:
        bm.faces.new(list(reversed(rings_verts[0][2])))
        bm.faces.new(rings_verts[-1][2])

    # ── 8 beam arm attachment sockets ─────────────
    for i in range(8):
        angle = i * TAU/8
        arm_x = math.cos(angle) * ring_r * 0.85
        arm_z = math.sin(angle) * ring_r * 0.85
        sock  = bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=False, segments=8,
            radius1=0.60, radius2=0.60, depth=1.2,
            matrix=Matrix.Translation(Vector((arm_x, 0, arm_z))) @
                   Matrix.Rotation(PI/2, 4, 'X'))

    # ── structural cross-brace at 120° intervals ──
    for i in range(3):
        angle = i * TAU/3
        for sign in (-1, 1):
            x0 = math.cos(angle) * 1.5
            z0 = math.sin(angle) * 1.5
            x1 = math.cos(angle) * (ring_r - 1.0)
            z1 = math.sin(angle) * (ring_r - 1.0)
            bv = [bm.verts.new((x0 + math.cos(a*TAU/6)*0.22 * sign,
                                math.sin(a*TAU/6)*0.22,
                                z0 + math.sin(a*TAU/6)*0.22 * sign))
                  for a in range(6)]
            ev = [bm.verts.new((x1 + math.cos(a*TAU/6)*0.22 * sign,
                                math.sin(a*TAU/6)*0.22,
                                z1 + math.sin(a*TAU/6)*0.22 * sign))
                  for a in range(6)]
            for j in range(6):
                nj=(j+1)%6
                try:
                    bm.faces.new([bv[j],bv[nj],ev[nj],ev[j]])
                except Exception:
                    pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark",
                        "mat_ancient_machine_edge_wear",
                        "mat_gold_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_OrbFrame_A")
    return obj


# ══════════════════════════════════════════════
#  ORB HUB
# ══════════════════════════════════════════════
# Central hub with 8 radial beam arms. The orb itself is a VFX sphere
# in-engine; this is only the mechanical hub structure.
# Matches: AD-001 top-down view.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Rift_OrbFrame_A")
