"""
SM_Glassroot_FloatingPlatform_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GlassrootForest')

def build():
    """Rock platform overgrown with glass tree roots."""
    print("Building SM_Glassroot_FloatingPlatform_A …")
    obj, bm = new_mesh("SM_Glassroot_FloatingPlatform_A")
    rng = random.Random(22)

    # ── rock body ─────────────────────────────────
    res = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=3.5)
    for v in res['verts']:
        if v.co.z < -1.5: v.co.z = -1.5
        v.co.z *= 0.5
        v.co.x += rng.uniform(-0.2, 0.2)
        v.co.y += rng.uniform(-0.2, 0.2)

    # ── surface root tendrils ─────────────────────
    for ri in range(6):
        angle  = ri * TAU/6 + rng.uniform(-0.2, 0.2)
        length = rng.uniform(1.5, 3.5)
        for t in range(8):
            pct = t/7
            rx  = math.cos(angle) * (3.4 + pct * length)
            ry  = math.sin(angle) * (3.4 + pct * length)
            rz  = -pct * 0.8 + rng.uniform(-0.1, 0.1)
            rw  = 0.08 * (1 - pct * 0.6)
            bm.verts.new((rx + rng.uniform(-0.04,0.04),
                          ry + rng.uniform(-0.04,0.04),
                          rz))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_glass_bark"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_FloatingPlatform_A")
    return obj


# ════════════════════════════════════════════════════════
#  GRAVITY WELL
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Glassroot_FloatingPlatform_A")
