"""
SM_RiftCreature_Silhouette_C — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_RiftCreature_Silhouette_C")
    bm = bmesh.new()

    # Spine helix — stack of spheres along sinusoidal path
    segments = 18
    for i in range(segments):
        t = i / (segments - 1)
        z = t * 2.8
        x = math.sin(t * math.pi * 2.5) * 0.18
        y = math.cos(t * math.pi * 2.5) * 0.12
        r = 0.14 - t * 0.06  # taper toward tail
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r,
                                    matrix=Matrix.Translation((x, y, z)))

    # Neck frill — ring of flat petals at z≈2.4
    frill_z = 2.40
    for i in range(8):
        ang = math.radians(i * 45)
        fx = math.cos(ang) * 0.28
        fy = math.sin(ang) * 0.28
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=4, radius1=0.03, radius2=0.005,
                                   depth=0.32,
                                   matrix=Matrix.Translation((fx, fy, frill_z + 0.16))
                                   @ Matrix.Rotation(ang, 4, 'Z')
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Head — elongated snout
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.18,
                                matrix=Matrix.Translation((0, 0, 2.95)))
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius1=0.06, radius2=0.03,
                               depth=0.30,
                               matrix=Matrix.Translation((0, 0.28, 2.95)))

    # Eye lights
    for side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.03,
                                    matrix=Matrix.Translation((side * 0.09, 0.16, 3.04)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_water_bioluminescent", "mat_blue_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_RiftCreature_Silhouette_C")


# ---------------------------------------------------------------------------
# 6. AbyssalCreature (patrol enemy)  —  SM_AbyssalCreature_Patrol_A
#    Crab/isopod hybrid: wide armoured carapace, 6 legs, two pincer arms,
#    head stalks with sensor orbs. Low to ground, ~1 m wide.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_RiftCreature_Silhouette_C")
