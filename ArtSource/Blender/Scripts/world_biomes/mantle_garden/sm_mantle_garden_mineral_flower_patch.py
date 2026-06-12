"""
SM_MantleGarden_MineralFlower_Patch_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('MantleGarden')


def build():
    """Mineral flower patch — 3m drift of 7 starburst magenta blooms growing
    from a shared obsidian shard bed. MG-002 shows the flowers in dense
    groups, not singles; this is the efficient scatter unit."""
    random.seed(640)
    obj, bm = new_mesh("SM_MantleGarden_MineralFlower_Patch_A")
    # obsidian shard bed
    for s in range(9):
        sx = random.uniform(-1.4, 1.4)
        sy = random.uniform(-1.1, 1.1)
        shard = bmesh.ops.create_icosphere(bm, subdivisions=1,
            radius=random.uniform(0.25, 0.55),
            matrix=Matrix.Translation((sx, sy, 0.05)))
        for v in shard['verts']:
            v.co.x = sx + (v.co.x - sx) * random.uniform(0.7, 1.6)
            v.co.y = sy + (v.co.y - sy) * random.uniform(0.7, 1.6)
            v.co.z = max(0.0, 0.05 + (v.co.z - 0.05) * 0.55)
    # 7 starburst blooms: each is a radial burst of needle crystals
    blooms = [(0.0, 0.0, 0.55), (0.9, 0.4, 0.40), (-0.8, 0.6, 0.35),
              (0.5, -0.8, 0.45), (-0.6, -0.6, 0.30), (1.2, -0.2, 0.25),
              (-1.2, 0.0, 0.28)]
    for bx, by, bscale in blooms:
        bz = 0.22
        NEEDLES = 14
        for n in range(NEEDLES):
            # needles burst outward in upper hemisphere directions
            theta = random.uniform(0, TAU)
            phi = random.uniform(0.15, PI / 2)
            dx = math.cos(theta) * math.sin(phi)
            dy = math.sin(theta) * math.sin(phi)
            dz = math.cos(phi)
            length = bscale * random.uniform(0.7, 1.2)
            w = length * 0.13
            # needle: 4-sided tapered spike along (dx,dy,dz)
            tip = bm.verts.new((bx + dx * length, by + dy * length,
                                 bz + dz * length))
            # base ring perpendicular-ish to the needle axis
            ortho1 = Vector((-dy, dx, 0))
            if ortho1.length < 0.01:
                ortho1 = Vector((1, 0, 0))
            ortho1.normalize()
            ortho2 = Vector((dx, dy, dz)).cross(ortho1)
            base_pts = []
            for k in range(4):
                ka = k * TAU / 4
                off = ortho1 * (math.cos(ka) * w) + ortho2 * (math.sin(ka) * w)
                base_pts.append(bm.verts.new((bx + off.x, by + off.y,
                                               bz + off.z)))
            for k in range(4):
                bm.faces.new([base_pts[k], base_pts[(k + 1) % 4], tip])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_magenta_mineral", "mat_obsidian", "mat_heat_crack"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_MantleGarden_MineralFlower_Patch_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_MantleGarden_MineralFlower_Patch_A")
