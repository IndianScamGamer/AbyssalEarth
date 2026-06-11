"""
SM_CRYSTAL_KIT — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('LuminousRift')

def build(name, seed, config):
    """
    config = {
      'base_r': float,          rock footprint radius (m)
      'rock_h': float,          max rock height
      'spires': [               list of spire defs
        { 'ox':float, 'oy':float, 'h':float, 'w':float,
          'tilt': (tx,ty), 'sides':int }
      ]
    }
    """
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    base_r = config['base_r']
    rock_h = config['rock_h']

    # ── rock base (deformed icosphere) ────────────
    res = bmesh.ops.create_icosphere(bm, subdivisions=3,
                                      radius=base_r * 0.85)
    for v in res['verts']:
        # flatten bottom
        if v.co.z < -base_r * 0.3:
            v.co.z = -base_r * 0.3
        elif v.co.z < 0:
            v.co.z *= 0.35
        # cap top to rock_h
        if v.co.z > rock_h:
            v.co.z = rock_h * rng.uniform(0.85, 1.0)
        # organic noise
        v.co += Vector((rng.uniform(-0.05,0.05)*base_r,
                        rng.uniform(-0.05,0.05)*base_r,
                        rng.uniform(-0.03,0.03)*base_r))

    # ── crystal spires ────────────────────────────
    for sp in config['spires']:
        ox, oy = sp['ox'], sp['oy']
        h, w   = sp['h'], sp['w']
        sides  = sp.get('sides', 5)
        tx, ty = sp.get('tilt', (rng.uniform(-0.15, 0.15),
                                  rng.uniform(-0.15, 0.15)))
        tilt   = Vector((tx, ty, 1)).normalized()
        base_z = rock_h * rng.uniform(0.05, 0.15)

        base_verts, top_verts = [], []
        for s in range(sides):
            a = s * TAU / sides + rng.uniform(-0.1, 0.1)
            bx = ox + math.cos(a) * w
            by = oy + math.sin(a) * w
            base_verts.append(bm.verts.new((bx, by, base_z)))
            tx2 = ox + math.cos(a) * w * 0.06 + tilt.x * h * 0.22
            ty2 = oy + math.sin(a) * w * 0.06 + tilt.y * h * 0.22
            top_verts.append(bm.verts.new((tx2, ty2, base_z + h)))

        tip = bm.verts.new((ox + tilt.x * h * 0.08,
                            oy + tilt.y * h * 0.08,
                            base_z + h * 1.04))

        try:
            bm.faces.new(list(reversed(base_verts)))
        except Exception:
            pass
        for s in range(sides):
            ns = (s+1)%sides
            try:
                bm.faces.new([base_verts[s], base_verts[ns],
                               top_verts[ns], top_verts[s]])
                bm.faces.new([top_verts[s], top_verts[ns], tip])
            except Exception:
                pass

    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    return obj

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_CRYSTAL_KIT")
