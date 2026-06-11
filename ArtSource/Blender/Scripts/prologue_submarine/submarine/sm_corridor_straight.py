"""
SM_Sub_CorridorSection_Straight_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Prologue')

def build():
    clear_scene()
    ob, me = new_mesh("SM_Sub_CorridorSection_Straight_A")
    bm = bmesh.new()

    W, H, L = 1.5, 1.25, 3.0   # half-width, half-height, full length
    SEGS = 10                   # arch segments per side

    def profile_verts(bm_ref, z_off):
        """Generate cross-section verts at z_off: arch top + flat walls + flat floor."""
        verts = []
        # Left wall bottom
        verts.append(bm_ref.verts.new((-W, z_off, 0.0)))
        # Left arch
        for i in range(SEGS + 1):
            t = i / SEGS
            ang = math.radians(180 + t * 180)
            vx = math.cos(ang) * W
            vy = H + math.sin(ang) * H * 0.35
            verts.append(bm_ref.verts.new((vx, z_off, vy)))
        # Right wall bottom
        verts.append(bm_ref.verts.new((W, z_off, 0.0)))
        return verts

    front = profile_verts(bm, 0.0)
    back  = profile_verts(bm, L)
    bm.verts.ensure_lookup_table()

    n = len(front)
    # Side walls
    for i in range(n - 1):
        bm.faces.new([front[i], front[i + 1], back[i + 1], back[i]])
    # End caps
    bm.faces.new(front)
    bm.faces.new(list(reversed(back)))
    # Floor
    bm.faces.new([front[0], back[0], back[-1], front[-1]])

    # Bolt rings at 0.5 m intervals
    for ring_z in [0.5, 1.0, 1.5, 2.0, 2.5]:
        for i, v in enumerate(front):
            lv = bm.verts.new(v.co + Vector((0, ring_z, 0)))
            rv = bm.verts.new(v.co + Vector((0.015 * (1 if v.co.x > 0 else -1),
                                              ring_z, 0.015)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, PROLOGUE_DIR, "SM_Sub_CorridorSection_Straight_A")


# ---------------------------------------------------------------------------
# SM_Sub_CorridorSection_Corner_A
#   90° L-bend corridor. Two 2 m arms meeting at rounded interior corner.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Sub_CorridorSection_Straight_A")
