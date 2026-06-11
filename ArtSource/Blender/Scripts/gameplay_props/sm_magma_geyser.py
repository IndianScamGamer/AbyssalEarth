"""
SM_MagmaGeyser_A — AbyssalEarth procedural mesh.
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
    print("Building SM_MagmaGeyser_A …")
    obj, bm = new_mesh("SM_MagmaGeyser_A")

    # ── main cone body ────────────────────────────
    segs = 10
    levels = [(0, 0.55), (0.2, 0.52), (0.5, 0.46), (0.85, 0.38),
              (1.1, 0.28), (1.4, 0.18), (1.75, 0.08), (1.82, 0.04)]
    rings = []
    import random; random.seed(12)
    for z, r in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*r * random.uniform(0.88, 1.12),
                    math.sin(i*TAU/segs)*r * random.uniform(0.88, 1.12),
                    z + random.uniform(-0.03, 0.03)))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(segs):
            ni = (i+1)%segs
            bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(rings[0])))  # base cap

    # ── 3 fissure cracks (indented wedges) ────────
    for i in range(3):
        angle = i * TAU/3 + TAU/6
        for lvl_z, lvl_r in [(0.3, 0.50), (0.7, 0.42), (1.1, 0.30)]:
            crack_v = [
                bm.verts.new((
                    math.cos(angle + da) * (lvl_r - 0.04),
                    math.sin(angle + da) * (lvl_r - 0.04),
                    lvl_z + dz))
                for da, dz in ((-0.12, -0.05),(0.12, -0.05),(0.0, 0.08))
            ]
            bm.faces.new(crack_v)

    # ── vent opening at top ────────────────────────
    top_ring = [bm.verts.new((math.cos(i*TAU/8)*0.05,
                              math.sin(i*TAU/8)*0.05, 1.82))
                for i in range(8)]
    bm.faces.new(top_ring)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_lava_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  8. HELIOS ROBOT (STATIC MESH PLACEHOLDER)
# ══════════════════════════════════════════════
# Figure 03 inspired: smooth white humanoid, ~175cm. Oval black faceplate,
# black joints (shoulders/elbows/hips/knees), slim torso.
# Matches: helios_figure03_style_fullbody_concept.png

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_MagmaGeyser_A")
