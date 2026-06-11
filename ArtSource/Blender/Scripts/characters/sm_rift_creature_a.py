"""
SM_RiftCreature_Silhouette_A — AbyssalEarth procedural mesh.
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
    ob, me = new_mesh("SM_RiftCreature_Silhouette_A")
    bm = bmesh.new()

    # Central body — elongated ellipsoid via scaled icosphere
    result = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=0.35,
                                         matrix=Matrix.Translation((0, 0, 0)))
    for v in result['verts']:
        v.co.z *= 2.2   # elongate vertically
        v.co.x *= 0.65
        v.co.y *= 0.65

    # Bioluminescent core orb (inner — will be separate slot)
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.12,
                                matrix=Matrix.Translation((0, 0, 0.05)))

    # 4 radial tentacle arms at 90° intervals
    for i in range(4):
        ang = math.radians(i * 90)
        cx = math.cos(ang) * 0.30
        cy = math.sin(ang) * 0.30
        # Arm root segment
        arm_mat = Matrix.Translation((cx * 0.6, cy * 0.6, 0.0))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius1=0.07, radius2=0.045,
                                   depth=0.40,
                                   matrix=arm_mat @ Matrix.Rotation(
                                       math.atan2(cy, cx), 4, 'Z')
                                   @ Matrix.Rotation(math.radians(90), 4, 'Y'))
        # Arm mid segment (angled down)
        mid_mat = Matrix.Translation((cx * 1.25, cy * 1.25, -0.15))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius1=0.042, radius2=0.025,
                                   depth=0.38,
                                   matrix=mid_mat @ Matrix.Rotation(
                                       math.atan2(cy, cx), 4, 'Z')
                                   @ Matrix.Rotation(math.radians(80), 4, 'Y'))
        # Tip fingers (2 tapered)
        for j in [-1, 1]:
            tip_offset = Vector((cx * 1.95 + j * cy * 0.08,
                                  cy * 1.95 + j * cx * 0.08,
                                  -0.38))
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=4, radius1=0.020, radius2=0.004,
                                       depth=0.28,
                                       matrix=Matrix.Translation(tip_offset))

    # Head crest — fan of flat spines
    for i in range(5):
        ang = math.radians(-40 + i * 20)
        spine_x = math.sin(ang) * 0.22
        spine_z_top = 0.72 + 0.06 * math.cos(ang * 2)
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=3, radius1=0.012, radius2=0.002,
                                   depth=0.24,
                                   matrix=Matrix.Translation((spine_x, 0, spine_z_top))
                                   @ Matrix.Rotation(ang * 0.5, 4, 'Y'))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_water_bioluminescent", "mat_blue_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, EXPORT_DIR, "SM_RiftCreature_Silhouette_A")


# ---------------------------------------------------------------------------
# 4. Rift Creature — Silhouette B  —  SM_RiftCreature_Silhouette_B
#    Manta-like: broad flat mantle, twin trailing tails, upper ridge spines.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_RiftCreature_Silhouette_A")
