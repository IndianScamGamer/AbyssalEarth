"""
SM_GravityWell_PortalRing_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GravityWell')

def build():
    """Outer ring structure of the Gravity Well vortex opening.
    Partially destroyed, floating rock shards incorporated.
    Matches: gravity_well_concept.png — the central glowing void."""
    print("Building SM_GravityWell_PortalRing_A …")
    obj, bm = new_mesh("SM_GravityWell_PortalRing_A")
    rng = random.Random(7)

    ring_r  = 22.0
    tube_r  = 1.2
    segs    = 32
    cover   = 0.78    # partial ring

    rings_all = []
    for seg in range(int(segs * cover) + 1):
        t     = seg / segs
        angle = t * TAU * cover
        cx    = math.cos(angle) * ring_r
        cz    = math.sin(angle) * ring_r
        tr    = tube_r + rng.uniform(-0.1, 0.15)
        ring  = [bm.verts.new((
                     cx + math.cos(a*TAU/10)*tr,
                     math.sin(a*TAU/10)*tr,
                     cz + math.sin(a*TAU/10)*tr*0.35))
                 for a in range(10)]
        rings_all.append(ring)

    for ri in range(len(rings_all)-1):
        lo, hi = rings_all[ri], rings_all[ri+1]
        for j in range(10):
            nj=(j+1)%10
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    if rings_all:
        try: bm.faces.new(list(reversed(rings_all[0])))
        except: pass
        try: bm.faces.new(rings_all[-1])
        except: pass

    # ── ancient machine details on ring ───────────
    for i in range(8):
        angle = i * TAU/8
        rx = math.cos(angle) * ring_r
        rz = math.sin(angle) * ring_r
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=tube_r*1.4,
                                    matrix=Matrix.Translation(Vector((rx, 0, rz))))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_blue_emissive",
                        "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_PortalRing_A")
    return obj


# ════════════════════════════════════════════════════════
#  INNER SEA
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_GravityWell_PortalRing_A")
