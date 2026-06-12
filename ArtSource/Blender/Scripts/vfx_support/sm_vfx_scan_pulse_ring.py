"""
SM_VFX_ScanPulseRing — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('VFXSupport')

def build():
    """Scan pulse ring — flat 1m ring quad strip for UAbyssalScanComponent
    pulse visual; scaled outward over pulse duration in-engine."""
    obj, bm = new_mesh("SM_VFX_ScanPulseRing")
    SEGS = 32
    R_OUT, R_IN = 0.5, 0.42
    outer = [bm.verts.new((math.cos(i*TAU/SEGS)*R_OUT,
                            math.sin(i*TAU/SEGS)*R_OUT, 0.01)) for i in range(SEGS)]
    inner = [bm.verts.new((math.cos(i*TAU/SEGS)*R_IN,
                            math.sin(i*TAU/SEGS)*R_IN, 0.01)) for i in range(SEGS)]
    for i in range(SEGS):
        ni = (i + 1) % SEGS
        bm.faces.new([inner[i], inner[ni], outer[ni], outer[i]])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_VFX_ScanPulseRing")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_VFX_ScanPulseRing")
