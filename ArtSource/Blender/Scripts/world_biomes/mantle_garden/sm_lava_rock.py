"""
SM_LAVA_ROCK — AbyssalEarth procedural mesh.
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

def build(name, scale, seed=80):
    """Jagged volcanic rock. Rough geometry, sharp edges, hot fissures.
    Matches: mantle_garden_concept.png — dark jagged formations."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    # ── primary rock mass ─────────────────────────
    res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=scale)
    for v in res['verts']:
        v.co.x *= rng.uniform(0.5, 1.6)
        v.co.y *= rng.uniform(0.5, 1.5)
        v.co.z *= rng.uniform(0.4, 1.4)
        if v.co.z < -scale * 0.3:
            v.co.z = -scale * 0.3
        v.co += Vector((rng.uniform(-0.12,0.12)*scale,
                        rng.uniform(-0.12,0.12)*scale,
                        rng.uniform(-0.06,0.06)*scale))

    # ── secondary spire shards ────────────────────
    for _ in range(rng.randint(2, 4)):
        angle = rng.uniform(0, TAU)
        sr    = scale * rng.uniform(0.3, 0.7)
        sh    = scale * rng.uniform(0.6, 1.4)
        sw    = sh * 0.14
        sx    = math.cos(angle) * sr
        sy    = math.sin(angle) * sr
        sv = [bm.verts.new((sx + math.cos(a*TAU/4)*sw,
                            sy + math.sin(a*TAU/4)*sw,
                            rng.uniform(scale*0.1, scale*0.25)))
              for a in range(4)]
        tip = bm.verts.new((sx + rng.uniform(-sw,sw),
                            sy + rng.uniform(-sw,sw),
                            sh))
        try:
            bm.faces.new(sv)
            for i in range(4):
                bm.faces.new([sv[i], sv[(i+1)%4], tip])
        except: pass

    # ── lava fissure cracks ───────────────────────
    for _ in range(rng.randint(2, 5)):
        angle = rng.uniform(0, TAU)
        fl    = rng.uniform(scale*0.4, scale*1.0)
        for ti in range(6):
            t  = ti/5
            fx = math.cos(angle) * fl * t
            fy = math.sin(angle) * fl * t
            fz = rng.uniform(-scale*0.05, scale*0.15)
            bm.verts.new((fx, fy, fz))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_lava_emissive"])
    set_origin_bottom(obj)
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_LAVA_ROCK")
