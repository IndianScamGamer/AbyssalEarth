"""
SM_VFX_BeamCylinder — AbyssalEarth procedural mesh.
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
    """Unit beam cylinder — 1m long, 0.5m diameter open tube. Scaled per-beam
    in-engine; collector beam material pans along its length."""
    obj, bm = new_mesh("SM_VFX_BeamCylinder")
    bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False, segments=16,
        radius1=0.25, radius2=0.25, depth=1.0,
        matrix=Matrix.Translation((0, 0, 0.5)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_orb_energy"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_VFX_BeamCylinder")
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \u2713 SM_VFX_BeamCylinder")
