"""
SM_Submarine_Exterior_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Prologue')

def build():
    """Hero submarine exterior — sleek 24m hull, conning hump, twin bow
    headlights, stern props. Concept: intro_submarine_wide/close."""
    obj, bm = new_mesh("SM_Submarine_Exterior_A")
    # main hull: ring loft, elliptical cross-section, tapered nose/tail
    SEGS = 12
    stations = [  # (y along length, radius, z lift)
        (-12.0, 0.25, 0.9), (-10.8, 0.85, 0.9), (-8.5, 1.35, 1.0),
        (-5.0, 1.60, 1.05), (0.0, 1.65, 1.05), (4.5, 1.55, 1.05),
        (8.0, 1.20, 1.0), (10.5, 0.70, 0.95), (11.8, 0.22, 0.9)]
    rings = []
    for y, r, zl in stations:
        ring = [bm.verts.new((math.cos(i*TAU/SEGS)*r,
                               y,
                               zl + math.sin(i*TAU/SEGS)*r*0.82))
                for i in range(SEGS)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i+1)%SEGS], hi[(i+1)%SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # conning hump (low fairwater, streamlined)
    hump = [(-3.5, 0.55), (-2.0, 0.95), (0.5, 0.95), (1.8, 0.50)]
    h_rings = []
    for y, hh in hump:
        ring = [bm.verts.new((math.cos(i*TAU/8)*0.75, y,
                               2.30 + math.sin(i*TAU/8)*hh*0.5 + hh*0.5))
                for i in range(8)]
        h_rings.append(ring)
    for ri in range(len(h_rings)-1):
        lo, hi = h_rings[ri], h_rings[ri+1]
        for i in range(8):
            bm.faces.new([lo[i], lo[(i+1)%8], hi[(i+1)%8], hi[i]])
    bm.faces.new(list(reversed(h_rings[0])))
    bm.faces.new(h_rings[-1])
    # twin bow headlights
    for side in [-1, 1]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=10,
            radius=0.22, depth=0.25,
            matrix=Matrix.Translation((side*0.55, -11.2, 0.75))
            @ Matrix.Rotation(TAU/4, 4, 'X'))
    # stern prop shrouds
    for side in [-1, 1]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=12,
            radius=0.55, depth=0.5,
            matrix=Matrix.Translation((side*0.95, 11.0, 0.95))
            @ Matrix.Rotation(TAU/4, 4, 'X'))
        # hub + 4 blades
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.12,
            matrix=Matrix.Translation((side*0.95, 11.0, 0.95)))
        for b in range(4):
            ba = b * TAU / 4
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((side*0.95 + math.cos(ba)*0.28,
                                            11.0, 0.95 + math.sin(ba)*0.28))
                @ Matrix.Rotation(ba, 4, 'Y')
                @ Matrix.Scale(0.38, 4, (1,0,0))
                @ Matrix.Scale(0.05, 4, (0,1,0))
                @ Matrix.Scale(0.16, 4, (0,0,1)))
    # dive planes
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side*2.1, -7.5, 1.05))
            @ Matrix.Scale(1.6, 4, (1,0,0))
            @ Matrix.Scale(0.9, 4, (0,1,0))
            @ Matrix.Scale(0.10, 4, (0,0,1)))
    # belly skids
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side*0.9, 0.0, 0.0))
            @ Matrix.Scale(0.18, 4, (1,0,0))
            @ Matrix.Scale(9.0, 4, (0,1,0))
            @ Matrix.Scale(0.14, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive",
                        "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Submarine_Exterior_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_Submarine_Exterior_A")
