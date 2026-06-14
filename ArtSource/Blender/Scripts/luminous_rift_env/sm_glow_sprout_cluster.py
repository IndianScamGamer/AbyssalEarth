"""
SM_Rift_GlowSprout_Cluster_A — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-016
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

EXPORT_DIR = get_export_dir('LuminousRift')


def build():
    """Glow sprout cluster — 40cm tuft of curling cyan fern-sprouts with
    bulb tips, the small foreground plants on the overlook ledge in NR-002
    ('first sight of the orb'). Scatter along routes as living breadcrumbs."""
    random.seed(810)
    obj, bm = new_mesh("SM_Rift_GlowSprout_Cluster_A")
    N_SPROUTS = 7
    for sp in range(N_SPROUTS):
        sa = sp * TAU / N_SPROUTS + random.uniform(-0.3, 0.3)
        sx = math.cos(sa) * random.uniform(0.02, 0.12)
        sy = math.sin(sa) * random.uniform(0.02, 0.12)
        h = random.uniform(0.18, 0.42)
        curl = random.uniform(0.6, 1.4)
        lean_x = math.cos(sa) * 0.4
        lean_y = math.sin(sa) * 0.4
        # stem: bead chain curling outward then over (fiddlehead)
        SEG = 9
        for s in range(SEG):
            t = s / (SEG - 1)
            # fiddlehead curve: rises, leans out, tip curls back in
            cx = sx + lean_x * t * h + math.sin(t * PI * curl) * 0.04
            cy = sy + lean_y * t * h
            cz = t * h + math.sin(t * PI * 0.5) * 0.02
            if t > 0.75:    # curl the tip over
                over = (t - 0.75) * 4
                cx -= lean_x * over * 0.08
                cz -= over * over * 0.04
            bmesh.ops.create_icosphere(bm, subdivisions=1,
                radius=0.016 * (1 - t * 0.55) + 0.004,
                matrix=Matrix.Translation((cx, cy, cz)))
        # glow bulb at the curled tip
        tip_x = sx + lean_x * h - lean_x * 0.08
        tip_y = sy + lean_y * h
        bmesh.ops.create_icosphere(bm, subdivisions=1,
            radius=random.uniform(0.022, 0.038),
            matrix=Matrix.Translation((tip_x, tip_y, h - 0.04)))
        # tiny leaf barbs along the upper stem
        for b in range(3):
            bt = 0.45 + b * 0.15
            bx = sx + lean_x * bt * h
            by = sy + lean_y * bt * h
            bz = bt * h
            v0 = bm.verts.new((bx, by, bz))
            v1 = bm.verts.new((bx - lean_y * 0.06, by + lean_x * 0.06,
                                bz + 0.05))
            v2 = bm.verts.new((bx - lean_y * 0.025, by + lean_x * 0.025,
                                bz + 0.075))
            bm.faces.new([v0, v1, v2])
    # mossy base pad
    pad = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.16,
        matrix=Matrix.Translation((0, 0, 0)))
    for v in pad['verts']:
        if v.co.z > 0:
            v.co.z *= 0.22
        else:
            v.co.z = 0
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_water_bioluminescent", "mat_blue_emissive",
                        "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_GlowSprout_Cluster_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Rift_GlowSprout_Cluster_A")
