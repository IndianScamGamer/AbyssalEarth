"""
SM_GravityWell_FloatingPlatform_A — AbyssalEarth procedural mesh.
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
    """SM_GravityWell_FloatingPlatform_A — 15m irregular floating rock platform."""
    import random; random.seed(66)
    obj, bm = new_mesh("SM_GravityWell_FloatingPlatform_A")
    result = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=7.5,
        matrix=Matrix.Translation((0,0,1.5)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.85, 1.15)
        v.co.y *= random.uniform(0.85, 1.15)
        if v.co.z < 1.5:
            v.co.z = 1.5 - (1.5 - v.co.z) * 0.35
        else:
            v.co.z = 1.5 + (v.co.z - 1.5) * 0.22
    # anchor cable stubs
    for i in range(4):
        a = i*TAU/4
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
            radius=0.15, depth=2.5,
            matrix=Matrix.Translation((math.cos(a)*4, math.sin(a)*4, -0.5)))
    # Tether mount posts — iron ring anchors at platform edges for player tether attachment
    MOUNT_R   = 0.065   # post radius
    MOUNT_H   = 0.30    # post height above platform surface
    MOUNT_RING_R = 0.09 # ring radius
    MOUNT_RING_T = 0.018 # ring tube radius
    platform_top_z = 1.5 + 7.5 * 0.22   # approx top of platform
    mount_positions = [
        (3.5, 0.0), (-3.5, 0.0), (0.0, 3.5), (0.0, -3.5)
    ]
    for (mx, my) in mount_positions:
        # Post cylinder
        mpost_mat = Matrix.Translation(Vector((mx, my, platform_top_z + MOUNT_H/2)))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
            radius1=MOUNT_R, radius2=MOUNT_R * 0.85, depth=MOUNT_H, matrix=mpost_mat)
        # Tether ring — simple lofted torus at post top
        ring_z = platform_top_z + MOUNT_H + MOUNT_RING_R
        N_RING = 10; N_TUBE = 6
        rings_m = []
        for ri in range(N_RING):
            a = ri * TAU / N_RING
            cx = mx + math.cos(a) * MOUNT_RING_R
            cy = my + math.sin(a) * MOUNT_RING_R
            ring_m = [bm.verts.new((
                cx + math.cos(a) * math.cos(j * TAU / N_TUBE) * MOUNT_RING_T,
                cy + math.sin(a) * math.cos(j * TAU / N_TUBE) * MOUNT_RING_T,
                ring_z + math.sin(j * TAU / N_TUBE) * MOUNT_RING_T,
            )) for j in range(N_TUBE)]
            rings_m.append(ring_m)
        for ri in range(N_RING):
            lo_m = rings_m[ri]; hi_m = rings_m[(ri+1) % N_RING]
            for j in range(N_TUBE):
                nj = (j+1) % N_TUBE
                try:
                    bm.faces.new([lo_m[j], lo_m[nj], hi_m[nj], hi_m[j]])
                except Exception:
                    pass
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_dark_basalt", "mat_blue_emissive", "mat_ancient_machine_dark"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_FloatingPlatform_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_GravityWell_FloatingPlatform_A")
