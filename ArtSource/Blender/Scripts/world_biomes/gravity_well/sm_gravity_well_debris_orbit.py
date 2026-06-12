"""
SM_GravityWell_DebrisOrbit_Cluster_A — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('GravityWell')


def build():
    """Orbiting debris ring — 5m halo of 24 small tumbling rock shards on a
    tilted elliptical band, as seen streaming around the anomaly and the
    floating islands in GW-002. Rotate slowly in-engine for ambient motion."""
    random.seed(631)
    obj, bm = new_mesh("SM_GravityWell_DebrisOrbit_Cluster_A")
    N = 24
    for i in range(N):
        a = i * TAU / N + random.uniform(-0.08, 0.08)
        # tilted elliptical orbit band with thickness scatter
        r = 2.5 * random.uniform(0.88, 1.12)
        x = math.cos(a) * r
        y = math.sin(a) * r * 0.75
        z = 2.5 + math.sin(a) * 0.6 + random.uniform(-0.25, 0.25)
        s = random.uniform(0.06, 0.22)
        shard = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=s,
            matrix=Matrix.Translation((x, y, z)))
        for v in shard['verts']:
            v.co.x = x + (v.co.x - x) * random.uniform(0.6, 1.5)
            v.co.y = y + (v.co.y - y) * random.uniform(0.6, 1.5)
            v.co.z = z + (v.co.z - z) * random.uniform(0.6, 1.5)
    # a few larger anchor chunks
    for i in range(3):
        a = i * TAU / 3 + 0.5
        chunk = bmesh.ops.create_icosphere(bm, subdivisions=1,
            radius=random.uniform(0.30, 0.45),
            matrix=Matrix.Translation((math.cos(a) * 2.5,
                                        math.sin(a) * 1.9,
                                        2.5 + math.sin(a) * 0.6)))
        for v in chunk['verts']:
            v.co += Vector((random.uniform(-0.06, 0.06),
                            random.uniform(-0.06, 0.06),
                            random.uniform(-0.06, 0.06)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_dark_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_DebrisOrbit_Cluster_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_GravityWell_DebrisOrbit_Cluster_A")
