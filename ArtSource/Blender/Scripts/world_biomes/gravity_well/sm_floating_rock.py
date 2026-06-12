"""
SM_FLOATING_ROCK — AbyssalEarth procedural mesh.
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

def build_variant(name, scale, seed=30):
    """Irregular floating rock chunk. Fractured faces, no clean flat bottom.
    Matches: gravity_well_concept.png — debris spiraling around vortex."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=scale)
    for v in res['verts']:
        # organic rocky deformation
        v.co.x *= rng.uniform(0.6, 1.4)
        v.co.y *= rng.uniform(0.6, 1.4)
        v.co.z *= rng.uniform(0.5, 1.3)
        v.co += Vector((rng.uniform(-0.08,0.08)*scale,
                        rng.uniform(-0.08,0.08)*scale,
                        rng.uniform(-0.08,0.08)*scale))

    # ── fracture detail: create bevelled crack ─────
    for _ in range(rng.randint(2, 4)):
        crack_dir = Vector((rng.uniform(-1,1), rng.uniform(-1,1),
                            rng.uniform(-1,1))).normalized()
        for v in bm.verts:
            proj = v.co.dot(crack_dir)
            if abs(proj - rng.uniform(scale*0.1, scale*0.5)) < scale*0.08:
                v.co += crack_dir * rng.uniform(-0.04,0.04)*scale

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt"])
    set_origin_to_base(obj)
    return obj

VARIANTS = [
    ('SM_GravityWell_FloatingRock_A', 4.0, 30),
    ('SM_GravityWell_FloatingRock_B', 2.2, 35),
    ('SM_GravityWell_FloatingRock_C', 1.0, 40),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_FLOATING_ROCK")
