"""
SM_MantleGarden_MineralFlower_A — AbyssalEarth procedural mesh.
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
    """SM_MantleGarden_MineralFlower_A — magenta mineral bloom, 7 crystal petals."""
    import random; random.seed(53)
    obj, bm = new_mesh("SM_MantleGarden_MineralFlower_A")
    # central bud
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.28,
        matrix=Matrix.Translation((0,0,0.30)))
    # 7 petal lobes
    for i in range(7):
        a = i*TAU/7
        px = math.cos(a)*0.55
        py = math.sin(a)*0.55
        # tapered hex prism petal
        petal_levels = [(0,0.16),(0.5,0.14),(1.2,0.10),(2.0,0.04)]
        p_rings = []
        for pz, pr in petal_levels:
            ring = [bm.verts.new((px + math.cos(j*TAU/6)*pr,
                                   py + math.sin(j*TAU/6)*pr,
                                   pz + random.uniform(-0.02,0.02)))
                    for j in range(6)]
            p_rings.append(ring)
        for ri in range(len(p_rings)-1):
            lo, hi = p_rings[ri], p_rings[ri+1]
            for j in range(6):
                bm.faces.new([lo[j],lo[(j+1)%6],hi[(j+1)%6],hi[j]])
        bm.faces.new(list(reversed(p_rings[0])))
        bm.faces.new(p_rings[-1])
    # basalt base
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.80, depth=0.25,
        matrix=Matrix.Translation((0,0,-0.12)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_magenta_mineral", "mat_heat_crack", "mat_obsidian"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_MantleGarden_MineralFlower_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_MantleGarden_MineralFlower_A")
