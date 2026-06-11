"""
SM_Rift_OrbHub_A — AbyssalEarth procedural mesh.
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
    print("Building SM_Rift_OrbHub_A …")
    obj, bm = new_mesh("SM_Rift_OrbHub_A")

    # ── central sphere structure ──────────────────
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=2.8)

    # ── concentric ring bands ─────────────────────
    for r_off in [3.2, 3.8, 4.4]:
        rv = [bm.verts.new((math.cos(i*TAU/32)*r_off,
                            math.sin(i*TAU/32)*r_off,
                            0.0))
              for i in range(32)]
        for i in range(32):
            ni=(i+1)%32
            bv = [bm.verts.new((rv[i].co.x, rv[i].co.y, -0.35)),
                  bm.verts.new((rv[ni].co.x,rv[ni].co.y, -0.35))]
            try:
                bm.faces.new([rv[i], rv[ni], bv[1], bv[0]])
            except Exception:
                pass

    # ── 8 radial beam arms (tapered, ~10m each) ───
    n_arms = 8
    for i in range(n_arms):
        angle = i * TAU/n_arms
        for t in range(16):
            pct = t / 15
            cx  = math.cos(angle) * (3.0 + pct * 10.0)
            cz  = math.sin(angle) * (3.0 + pct * 10.0)
            arm_r = 0.38 * (1 - pct * 0.55)
            if t == 0:
                prev = [bm.verts.new((
                            cx + math.cos(a*TAU/8)*arm_r,
                            math.sin(a*TAU/8)*arm_r,
                            cz + math.sin(a*TAU/8)*arm_r*0.4))
                        for a in range(8)]
            else:
                curr = [bm.verts.new((
                            cx + math.cos(a*TAU/8)*arm_r,
                            math.sin(a*TAU/8)*arm_r,
                            cz + math.sin(a*TAU/8)*arm_r*0.4))
                        for a in range(8)]
                for j in range(8):
                    nj=(j+1)%8
                    try:
                        bm.faces.new([prev[j],prev[nj],curr[nj],curr[j]])
                    except Exception:
                        pass
                prev = curr

        # emitter node at tip
        tip_cx = math.cos(angle) * 13.5
        tip_cz = math.sin(angle) * 13.5
        bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.55,
            matrix=Matrix.Translation(Vector((tip_cx, 0, tip_cz))))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive",
                        "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  BEAM EMITTER NODE
# ══════════════════════════════════════════════
# End-device at collector array. 2–3m diameter disc with concave
# emitter face, mounting flange, gold emissive ring.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Rift_OrbHub_A")
