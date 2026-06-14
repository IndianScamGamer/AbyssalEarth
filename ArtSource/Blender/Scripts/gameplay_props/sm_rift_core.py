"""
SM_RiftActor_Core_A — AbyssalEarth procedural mesh.
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
    """AAbyssalRiftActor — endgame rift anchor: 6m double-ring gate with
    central void sphere and 6 stabiliser sockets (for ITEM_KEY_RIFT_STABILISER)."""
    obj, bm = new_mesh("SM_RiftActor_Core_A")
    # twin vertical rings (gyroscope arrangement)
    for ring_rot in [0, TAU/4]:
        SEGS = 24
        for s in range(SEGS):
            a = s * TAU / SEGS
            x = math.cos(a) * 2.6
            z = 3.0 + math.sin(a) * 2.6
            pos = Vector((x * math.cos(ring_rot), x * math.sin(ring_rot), z))
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.16,
                matrix=Matrix.Translation(pos))
    # central void sphere
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0,
        matrix=Matrix.Translation((0, 0, 3.0)))
    # base pedestal
    lo = [bm.verts.new((math.cos(i*TAU/6)*1.6, math.sin(i*TAU/6)*1.6, 0))
          for i in range(6)]
    hi = [bm.verts.new((math.cos(i*TAU/6)*1.1, math.sin(i*TAU/6)*1.1, 0.6))
          for i in range(6)]
    for i in range(6):
        ni = (i + 1) % 6
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # 6 stabiliser sockets around pedestal rim
    for i in range(6):
        a = i * TAU / 6 + TAU/12
        sx, sy = math.cos(a)*1.35, math.sin(a)*1.35
        bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False, segments=8,
            radius1=0.14, radius2=0.14, depth=0.10,
            matrix=Matrix.Translation((sx, sy, 0.62)))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
            radius1=0.10, radius2=0.10, depth=0.04,
            matrix=Matrix.Translation((sx, sy, 0.60)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive",
                        "mat_orb_energy", "mat_purple_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_RiftActor_Core_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_RiftActor_Core_A")
