"""
SM_PURPLE_CRYSTAL — AbyssalEarth procedural mesh.
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

def build_variant(name, scale, seed=90):
    """Purple amethyst-style crystal cluster. Similar silhouette to blue
    crystals but shorter, stockier, more angular.
    Matches: mantle_garden_concept.png — purple accents on dark lava rock."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    # rock base
    res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=scale*0.55)
    for v in res['verts']:
        if v.co.z < 0: v.co.z *= 0.3
        v.co += Vector((rng.uniform(-0.04,0.04)*scale,
                        rng.uniform(-0.04,0.04)*scale,
                        rng.uniform(-0.02,0.02)*scale))

    # 4-6 crystals (stockier than blue: h/w ≈ 5:1 vs blue's 8:1)
    n = rng.randint(4, 7)
    for i in range(n):
        angle = i * TAU/n + rng.uniform(-0.2, 0.2)
        spread = rng.uniform(0.02, scale*0.5)
        cx = math.cos(angle)*spread
        cy = math.sin(angle)*spread
        h  = rng.uniform(scale*0.6, scale*1.3)
        w  = h * rng.uniform(0.17, 0.23)
        sides = 6  # hexagonal prism
        bv = [bm.verts.new((cx + math.cos(a*TAU/sides)*w,
                            cy + math.sin(a*TAU/sides)*w, 0.0))
              for a in range(sides)]
        tv = [bm.verts.new((cx + math.cos(a*TAU/sides)*w*0.08,
                            cy + math.sin(a*TAU/sides)*w*0.08, h))
              for a in range(sides)]
        tip = bm.verts.new((cx, cy, h*1.06))
        try:
            bm.faces.new(list(reversed(bv)))
            for s in range(sides):
                ns=(s+1)%sides
                bm.faces.new([bv[s],bv[ns],tv[ns],tv[s]])
                bm.faces.new([tv[s],tv[ns],tip])
        except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_purple_emissive"])
    set_origin_to_base(obj)
    return obj

VARIANTS = [
    ('SM_MantleGarden_PurpleCrystal_A', 1.8, 90),
    ('SM_MantleGarden_PurpleCrystal_B', 1.0, 95),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_PURPLE_CRYSTAL")
