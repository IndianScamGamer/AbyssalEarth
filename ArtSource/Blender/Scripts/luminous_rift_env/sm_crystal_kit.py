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


def make_spires_A_small(seed):
    """Vertical spear cluster — 3 spires, upright."""
    rng = random.Random(seed)
    return [{'ox': rng.uniform(-0.04,0.04), 'oy': rng.uniform(-0.04,0.04),
             'h': h, 'w': h*0.13, 'sides': 5,
             'tilt': (rng.uniform(-0.06,0.06), rng.uniform(-0.06,0.06))}
            for h in [rng.uniform(0.22,0.30), rng.uniform(0.16,0.22),
                      rng.uniform(0.18,0.26)]]

def make_spires_B_fan(seed):
    """Fan spread — 5 spires fanning outward."""
    rng = random.Random(seed)
    spires = []
    for i in range(5):
        angle  = i * TAU/5
        spread = rng.uniform(0.04, 0.10)
        h      = rng.uniform(0.18, 0.32)
        spires.append({'ox': math.cos(angle)*spread,
                       'oy': math.sin(angle)*spread,
                       'h': h, 'w': h*0.11, 'sides': 5,
                       'tilt': (math.cos(angle)*0.18, math.sin(angle)*0.18)})
    return spires

def make_spires_C_broken(seed):
    """Low broken — short stumps and shards, some horizontal lean."""
    rng = random.Random(seed)
    spires = []
    for _ in range(4):
        h = rng.uniform(0.08, 0.18)
        spires.append({'ox': rng.uniform(-0.06,0.06),
                       'oy': rng.uniform(-0.06,0.06),
                       'h': h, 'w': h*0.18, 'sides': 4,
                       'tilt': (rng.uniform(-0.3,0.3), rng.uniform(-0.3,0.3))})
    return spires


# ══════════════════════════════════════════════
#  FOREGROUND LEDGE
# ══════════════════════════════════════════════
# The First Overlook platform the player stands on.
# Uneven walkable top, jagged outer edges, layered basalt striations.
# Matches: AD-004 (rock arch framing view), ancient_bridge_platform_kit_concept.png

def build_variant(name, seed, config):
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

def _cfg_S_A(): return {'base_r':0.22,'rock_h':0.12,'spires':make_spires_A_small(1)}
def _cfg_S_B(): return {'base_r':0.22,'rock_h':0.10,'spires':make_spires_B_fan(2)}
def _cfg_S_C(): return {'base_r':0.22,'rock_h':0.08,'spires':make_spires_C_broken(3)}
def _cfg_M_A(): return {'base_r':0.36,'rock_h':0.20,'spires':make_spires_A_small(4)*2}
def _cfg_M_B(): return {'base_r':0.36,'rock_h':0.18,'spires':make_spires_B_fan(5)}
def _cfg_M_C(): return {'base_r':0.36,'rock_h':0.16,'spires':make_spires_C_broken(6)*2}
def _cfg_L_A(): return {'base_r':0.55,'rock_h':0.30,'spires':[
    {'ox':0,'oy':0,'h':1.35,'w':0.14,'sides':5},
    {'ox':-0.18,'oy':0.12,'h':1.05,'w':0.12,'sides':5,'tilt':(-0.12, 0.05)},
    {'ox':0.20,'oy':-0.10,'h':0.90,'w':0.11,'sides':5,'tilt':(0.10,-0.08)},
    {'ox':-0.08,'oy':-0.22,'h':0.60,'w':0.09,'sides':4,'tilt':(-0.06,-0.15)},
]}
def _cfg_L_B(): return {'base_r':0.55,'rock_h':0.28,
                        'spires':make_spires_B_fan(8) + make_spires_C_broken(9)}
def _cfg_Hero(): return {'base_r':0.90,'rock_h':0.45,'spires':[
    {'ox':0,'oy':0,'h':2.80,'w':0.22,'sides':6},
    {'ox':-0.35,'oy':0.20,'h':2.10,'w':0.18,'sides':5,'tilt':(-0.10, 0.06)},
    {'ox':0.38,'oy':-0.15,'h':1.85,'w':0.16,'sides':5,'tilt':(0.12,-0.06)},
    {'ox':-0.20,'oy':-0.40,'h':1.40,'w':0.14,'sides':5,'tilt':(-0.08,-0.18)},
    {'ox':0.25,'oy':0.38,'h':1.20,'w':0.13,'sides':4,'tilt':(0.08, 0.20)},
    {'ox':-0.50,'oy':-0.10,'h':0.80,'w':0.10,'sides':4,'tilt':(-0.25,-0.05)},
    {'ox':0.15,'oy':-0.52,'h':0.65,'w':0.09,'sides':4,'tilt':(0.04,-0.28)},
]}

VARIANTS = [
    ("SM_Rift_CrystalCluster_S_A", 1, _cfg_S_A),
    ("SM_Rift_CrystalCluster_S_B", 2, _cfg_S_B),
    ("SM_Rift_CrystalCluster_S_C", 3, _cfg_S_C),
    ("SM_Rift_CrystalCluster_M_A", 4, _cfg_M_A),
    ("SM_Rift_CrystalCluster_M_B", 5, _cfg_M_B),
    ("SM_Rift_CrystalCluster_M_C", 6, _cfg_M_C),
    ("SM_Rift_CrystalCluster_L_A", 7, _cfg_L_A),
    ("SM_Rift_CrystalCluster_L_B", 8, _cfg_L_B),
    ("SM_Rift_CrystalCluster_Hero_A", 9, _cfg_Hero),
]


def build():
    for name, seed, cfg in VARIANTS:
        clear_scene()
        obj = build_variant(name, seed, cfg())
        export_fbx(obj, EXPORT_DIR, name)


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_CRYSTAL_KIT")
