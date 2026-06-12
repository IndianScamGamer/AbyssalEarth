"""
SM_DiscoveryMarker_A — AbyssalEarth procedural mesh.
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
    """ADiscoveryActor — scannable discovery marker: tilted ancient stele
    with glyph face and crystal inclusion at the crown, 1.6m."""
    random.seed(120)
    obj, bm = new_mesh("SM_DiscoveryMarker_A")
    # tilted stele slab
    TILT = 0.12
    levels = [(0, 0.30, 0.18), (0.9, 0.26, 0.15), (1.6, 0.16, 0.10)]
    rings = []
    for z, w, d in levels:
        cx = z * TILT
        ring = [bm.verts.new((cx + sx*w, sy*d, z))
                for sx, sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(4):
            bm.faces.new([lo[i], lo[(i+1)%4], hi[(i+1)%4], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # glyph grooves on front face
    for gz in [0.35, 0.62, 0.89, 1.16]:
        gx = gz * TILT
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((gx, -0.165, gz))
            @ Matrix.Scale(0.30, 4, (1,0,0))
            @ Matrix.Scale(0.015, 4, (0,1,0))
            @ Matrix.Scale(0.05, 4, (0,0,1)))
    # crystal inclusion at crown
    tip = bm.verts.new((1.6*TILT, 0, 1.85))
    base_ring = [bm.verts.new((1.6*TILT + math.cos(i*TAU/5)*0.07,
                                math.sin(i*TAU/5)*0.07, 1.58)) for i in range(5)]
    for i in range(5):
        bm.faces.new([base_ring[i], base_ring[(i+1)%5], tip])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_blue_emissive", "mat_crystal_blue"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_DiscoveryMarker_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_DiscoveryMarker_A")
