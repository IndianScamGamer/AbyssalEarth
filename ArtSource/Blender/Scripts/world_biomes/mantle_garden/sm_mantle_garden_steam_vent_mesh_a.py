"""
SM_MantleGarden_SteamVent_Mesh_A — AbyssalEarth procedural mesh.
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
    """SM_MantleGarden_SteamVent_Mesh_A — obsidian vent cone 4m diameter."""
    import random; random.seed(52)
    obj, bm = new_mesh("SM_MantleGarden_SteamVent_Mesh_A")
    SEGS = 10
    levels = [(0,2.0),(0.3,1.9),(0.7,1.7),(1.2,1.4),(1.8,1.0),(2.5,0.6),(3.0,0.28)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/SEGS)*r*(1+random.uniform(-0.06,0.06)),
                               math.sin(i*TAU/SEGS)*r*(1+random.uniform(-0.06,0.06)),
                               z + random.uniform(-0.04,0.04)))
                for i in range(SEGS)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i+1)%SEGS], hi[(i+1)%SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    # vent pipe top
    pipe_top = [bm.verts.new((math.cos(i*TAU/8)*0.20,
                               math.sin(i*TAU/8)*0.20, 3.0)) for i in range(8)]
    bm.faces.new(pipe_top)
    # heat bloom ring
    for j in range(16):
        a = j*TAU/16
        bm.verts.new((math.cos(a)*2.1, math.sin(a)*2.1, 0.05))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_obsidian", "mat_heat_bloom"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_MantleGarden_SteamVent_Mesh_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_MantleGarden_SteamVent_Mesh_A")
