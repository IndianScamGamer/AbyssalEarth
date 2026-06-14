"""
SM_RiftCreature_Silhouette_B — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Characters')

def build():
    clear_scene()
    ob, me = new_mesh("SM_RiftCreature_Silhouette_B")
    bm = bmesh.new()

    # Flat mantle — wide subdivided plane, extruded to give volume
    verts_raw = []
    for i in range(9):
        ang = math.radians(i * 40 - 160)  # 320° sweep leaving trailing gap
        r = 1.10 + 0.18 * math.cos(math.radians(i * 80))
        verts_raw.append(bm.verts.new((math.cos(ang) * r,
                                        math.sin(ang) * r * 0.42,
                                        0.0)))
    bm.verts.ensure_lookup_table()
    # Centre
    cv = bm.verts.new((0, 0, 0))
    for i in range(len(verts_raw) - 1):
        bm.faces.new([verts_raw[i], verts_raw[i + 1], cv])
    # Thicken via extrude
    for v in bm.verts:
        dup = bm.verts.new(v.co + Vector((0, 0, 0.12)))

    # Body ridge (dorsal spine row)
    for i in range(7):
        t = i / 6.0
        px = (t - 0.5) * 1.6
        pz = 0.18 + 0.12 * math.sin(math.pi * t)
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                   segments=3, radius1=0.025, radius2=0.005,
                                   depth=0.20,
                                   matrix=Matrix.Translation((px, 0, pz)))

    # Twin trailing tails
    for side in [-1, 1]:
        for seg, (tz, tr, tlen) in enumerate([(0, 0.055, 0.60), (-0.20, 0.040, 0.50), (-0.42, 0.020, 0.35)]):
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                       segments=6, radius1=tr, radius2=tr * 0.75,
                                       depth=tlen,
                                       matrix=Matrix.Translation(
                                           (side * 0.22, -1.05 - seg * 0.5, tz + tlen * 0.5 - 0.3)))

    # Cephalic lobes (head end)
    for side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.16,
                                    matrix=Matrix.Translation((side * 0.30, 0.85, 0.05)))

    finalise(ob, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_water_bioluminescent", "mat_purple_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_RiftCreature_Silhouette_B")


# ---------------------------------------------------------------------------
# 5. Rift Creature — Silhouette C  —  SM_RiftCreature_Silhouette_C
#    Vertical serpentine: coiled body column ~3 m tall, frilled neck collar.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_RiftCreature_Silhouette_B")
