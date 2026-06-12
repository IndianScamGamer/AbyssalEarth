"""
SM_Glassroot_PoolTerrace_Rim_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GlassrootForest')


def build():
    """Rimstone pool terrace — 8m cluster of 4 interlocking mineral pools
    with raised travertine rims, the floor texture of GR-002. Water planes
    are added in-engine inside each rim."""
    random.seed(610)
    obj, bm = new_mesh("SM_Glassroot_PoolTerrace_Rim_A")
    pools = [(0.0, 0.0, 2.6, 0.00), (3.1, 1.2, 2.0, 0.18),
             (-2.4, 2.6, 1.7, 0.30), (1.0, -3.0, 1.9, -0.12)]
    for px, py, pr, pz in pools:
        SEGS = 16
        # lobed rim ring: raised lip, irregular radius
        radii = [pr * random.uniform(0.85, 1.15) for _ in range(SEGS)]
        out_lo, out_hi, in_hi, in_lo = [], [], [], []
        for i in range(SEGS):
            a = i * TAU / SEGS
            r = radii[i]
            out_lo.append(bm.verts.new((px + math.cos(a) * (r + 0.22),
                                         py + math.sin(a) * (r + 0.22), pz)))
            out_hi.append(bm.verts.new((px + math.cos(a) * (r + 0.12),
                                         py + math.sin(a) * (r + 0.12),
                                         pz + 0.22)))
            in_hi.append(bm.verts.new((px + math.cos(a) * r,
                                        py + math.sin(a) * r, pz + 0.20)))
            in_lo.append(bm.verts.new((px + math.cos(a) * (r - 0.10),
                                        py + math.sin(a) * (r - 0.10),
                                        pz + 0.02)))
        for i in range(SEGS):
            ni = (i + 1) % SEGS
            bm.faces.new([out_lo[i], out_lo[ni], out_hi[ni], out_hi[i]])
            bm.faces.new([out_hi[i], out_hi[ni], in_hi[ni], in_hi[i]])
            bm.faces.new([in_hi[i], in_hi[ni], in_lo[ni], in_lo[i]])
        # pool floor disc
        floor_verts = [bm.verts.new((px + math.cos(i * TAU / SEGS) * (radii[i] - 0.10),
                                      py + math.sin(i * TAU / SEGS) * (radii[i] - 0.10),
                                      pz + 0.02)) for i in range(SEGS)]
        bm.faces.new(floor_verts)
    # connecting ground skirt between pools
    skirt = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=4.6,
        matrix=Matrix.Translation((0.4, 0.2, 0)))
    for v in skirt['verts']:
        if v.co.z > 0:
            v.co.z *= 0.02
        else:
            v.co.z = -0.05
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_pearl_stone", "mat_wet_edge"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_PoolTerrace_Rim_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Glassroot_PoolTerrace_Rim_A")
