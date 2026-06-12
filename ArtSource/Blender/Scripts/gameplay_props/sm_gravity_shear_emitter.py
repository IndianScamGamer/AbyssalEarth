"""
SM_GravityShear_Emitter_A — AbyssalEarth procedural mesh.
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
    """AGravityShearHazard — gravity shear source: inverted ancient pylon
    hovering ring stack, 3m tall. VFX handles the distortion field."""
    obj, bm = new_mesh("SM_GravityShear_Emitter_A")
    # ground anchor spike (inverted cone)
    tip = bm.verts.new((0, 0, 0))
    ring = [bm.verts.new((math.cos(i*TAU/8)*0.35,
                           math.sin(i*TAU/8)*0.35, 0.8)) for i in range(8)]
    for i in range(8):
        bm.faces.new([ring[i], ring[(i+1)%8], tip])
    bm.faces.new(list(reversed(ring)))
    # 3 floating ring discs of decreasing size going up
    for ri, (rz, rr) in enumerate([(1.4, 0.55), (2.1, 0.40), (2.7, 0.26)]):
        SEGS = 16
        lo = [bm.verts.new((math.cos(i*TAU/SEGS)*rr,
                             math.sin(i*TAU/SEGS)*rr, rz)) for i in range(SEGS)]
        hi = [bm.verts.new((math.cos(i*TAU/SEGS)*rr,
                             math.sin(i*TAU/SEGS)*rr, rz + 0.10)) for i in range(SEGS)]
        inner_lo = [bm.verts.new((math.cos(i*TAU/SEGS)*rr*0.7,
                                   math.sin(i*TAU/SEGS)*rr*0.7, rz)) for i in range(SEGS)]
        inner_hi = [bm.verts.new((math.cos(i*TAU/SEGS)*rr*0.7,
                                   math.sin(i*TAU/SEGS)*rr*0.7, rz + 0.10)) for i in range(SEGS)]
        for i in range(SEGS):
            ni = (i + 1) % SEGS
            bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
            bm.faces.new([inner_hi[i], inner_hi[ni], inner_lo[ni], inner_lo[i]])
            bm.faces.new([hi[i], hi[ni], inner_hi[ni], inner_hi[i]])
            bm.faces.new([inner_lo[i], inner_lo[ni], lo[ni], lo[i]])
    # apex orb
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.14,
        matrix=Matrix.Translation((0, 0, 3.05)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_purple_emissive",
                        "mat_orb_energy"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityShear_Emitter_A")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_GravityShear_Emitter_A")
