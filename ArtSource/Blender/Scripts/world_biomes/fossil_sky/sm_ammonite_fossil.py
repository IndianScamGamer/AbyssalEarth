"""
SM_FossilSky_Ammonite_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('FossilSky')


def build():
    """Ammonite fossil — 1.5m logarithmic-spiral shell with ribbed whorls,
    half-proud of its rock matrix slab. Wall and floor accent for Fossil Sky
    (the coiled fossils in FS-002's ceiling)."""
    random.seed(720)
    obj, bm = new_mesh("SM_FossilSky_Ammonite_A")
    # rock matrix slab behind the shell
    slab = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.95,
        matrix=Matrix.Translation((0, 0.18, 0.85)))
    for v in slab['verts']:
        v.co.y = 0.18 + (v.co.y - 0.18) * 0.30
        v.co.x *= 1.15
        v.co += Vector((random.uniform(-0.04, 0.04), 0,
                        random.uniform(-0.04, 0.04)))
    # logarithmic spiral shell: tube of shrinking radius sweeping ~2.5 turns
    TURNS = 2.5
    STEPS = 60
    centre_z = 0.85
    prev_ring = None
    for s in range(STEPS):
        t = s / (STEPS - 1)
        ang = t * TURNS * TAU
        spiral_r = 0.62 * math.exp(-1.05 * t)          # shrinking orbit
        tube_r = 0.155 * math.exp(-0.9 * t) + 0.012    # shrinking tube
        cx = math.cos(ang) * spiral_r
        cz = centre_z + math.sin(ang) * spiral_r
        ring = []
        SEG = 8
        for i in range(SEG):
            a = i * TAU / SEG
            # tube cross-section in the plane facing out of the wall
            rx = cx + math.cos(ang) * math.cos(a) * tube_r
            ry = -0.05 + math.sin(a) * tube_r * 0.9
            rz = cz + math.sin(ang) * math.cos(a) * tube_r
            ring.append(bm.verts.new((rx, ry, rz)))
        if prev_ring:
            for i in range(SEG):
                bm.faces.new([prev_ring[i], prev_ring[(i + 1) % SEG],
                               ring[(i + 1) % SEG], ring[i]])
        prev_ring = ring
        # rib ridges every few steps: small bead row across the whorl
        if s % 6 == 0 and s > 4:
            bmesh.ops.create_icosphere(bm, subdivisions=1,
                radius=tube_r * 0.35,
                matrix=Matrix.Translation((cx + math.cos(ang) * tube_r,
                                            -0.05 - tube_r * 0.55,
                                            cz + math.sin(ang) * tube_r)))
    # flared aperture lip at the outer end
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=10,
        radius=0.19, depth=0.10,
        matrix=Matrix.Translation((0.62, -0.05, centre_z))
        @ Matrix.Rotation(TAU / 4, 4, 'Y'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein",
                        "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_Ammonite_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_FossilSky_Ammonite_A")
