#!/usr/bin/env python3
"""
expand_asset_scripts.py — one-off generator for the massive asset expansion.
Adds 27 new per-asset Blender scripts:
  items/           — 12 pickup meshes, one per DT_ItemDatabase row
  gameplay_props/  — 6 meshes for C++ actors lacking any mesh
  set_dressing/    — 6 scatter/dressing meshes
  vfx_support/     — 3 VFX support meshes
Then regenerates every run_all.py and the root run_all_assets.py by scanning.

Run from repo root:  python3 Tools/expand_asset_scripts.py
"""

import os
import re

SCRIPTS_DIR = os.path.join("ArtSource", "Blender", "Scripts")


def header(sm_name, depth, export_subpath):
    dots = ", ".join(repr("..") for _ in range(depth))
    return f'''"""
{sm_name} — AbyssalEarth procedural mesh.
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
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, {dots}))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, mat_color, extrude_region,
                           add_subdivision, TAU, PI)

EXPORT_DIR = get_export_dir({export_subpath!r})

'''


def footer(sm_name):
    return f'''

if __name__ == "__main__":
    clear_scene()
    build()
    print("  \\u2713 {sm_name}")
'''


# ────────────────────────────────────────────────────────────────────
# Asset bodies.  Each: (folder, export_subpath, file_stem, sm_name, body)
# ────────────────────────────────────────────────────────────────────

ASSETS = []

# ====================================================================
# ITEMS — 12 pickup meshes, one per DT_ItemDatabase ItemId
# All hand-sized (8–30 cm) so they read as pickups; origin at base.
# ====================================================================

ASSETS.append(("items", "Items", "sm_item_abyssal_core", "SM_Item_AbyssalCore_A", '''
def build():
    """ITEM_MINERAL_ABYSSAL_CORE — dense crystalline mineral chunk."""
    random.seed(101)
    obj, bm = new_mesh("SM_Item_AbyssalCore_A")
    # core chunk: deformed icosphere
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.10,
        matrix=Matrix.Translation((0, 0, 0.10)))
    for v in result['verts']:
        v.co += Vector((random.uniform(-0.015, 0.015),
                        random.uniform(-0.015, 0.015),
                        random.uniform(-0.012, 0.012)))
    # 3 small crystal facets protruding
    for i in range(3):
        a = i * TAU / 3 + 0.4
        cx, cy = math.cos(a) * 0.07, math.sin(a) * 0.07
        tip = bm.verts.new((cx * 1.9, cy * 1.9, 0.14 + i * 0.02))
        ring = [bm.verts.new((cx + math.cos(j*TAU/4)*0.025,
                               cy + math.sin(j*TAU/4)*0.025,
                               0.08 + i * 0.02)) for j in range(4)]
        for j in range(4):
            bm.faces.new([ring[j], ring[(j+1)%4], tip])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_AbyssalCore_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_fossil_shard", "SM_Item_FossilShard_A", '''
def build():
    """ITEM_MINERAL_FOSSIL_SHARD — curved fragment of fossilized bone."""
    random.seed(102)
    obj, bm = new_mesh("SM_Item_FossilShard_A")
    # curved shard: arc of tapered segments
    SEGS = 8
    rings = []
    for i in range(SEGS + 1):
        t = i / SEGS
        cx = math.sin(t * PI * 0.6) * 0.16
        cz = t * 0.22
        r = 0.030 * (1 - t * 0.7) + 0.008
        ring = [bm.verts.new((cx + math.cos(j*TAU/6)*r,
                               math.sin(j*TAU/6)*r * 0.55,
                               cz)) for j in range(6)]
        rings.append(ring)
    for ri in range(SEGS):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(6):
            bm.faces.new([lo[j], lo[(j+1)%6], hi[(j+1)%6], hi[j]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_FossilShard_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_magma_residue", "SM_Item_MagmaResidue_A", '''
def build():
    """ITEM_MINERAL_MAGMA_RESIDUE — lumpy cooled magma nugget, glowing cracks."""
    random.seed(103)
    obj, bm = new_mesh("SM_Item_MagmaResidue_A")
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.09,
        matrix=Matrix.Translation((0, 0, 0.08)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.85, 1.25)
        v.co.y *= random.uniform(0.85, 1.25)
        if v.co.z < 0.05:
            v.co.z = 0.05 - (0.05 - v.co.z) * 0.3   # flatten base
    # crack ridge verts (heat glow strip)
    for i in range(6):
        a = i * TAU / 6
        bm.verts.new((math.cos(a)*0.095, math.sin(a)*0.095, 0.08))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_obsidian", "mat_heat_crack"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_MagmaResidue_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_gravity_crystal", "SM_Item_GravityCrystal_A", '''
def build():
    """ITEM_MINERAL_GRAVITY_CRYSTAL — octahedral crystal that distorts gravity."""
    obj, bm = new_mesh("SM_Item_GravityCrystal_A")
    # octahedron: 6 verts
    R, H = 0.07, 0.12
    top = bm.verts.new((0, 0, 0.13 + H))
    bot = bm.verts.new((0, 0, 0.13 - H))
    mid = [bm.verts.new((math.cos(i*TAU/4)*R, math.sin(i*TAU/4)*R, 0.13))
           for i in range(4)]
    for i in range(4):
        ni = (i + 1) % 4
        bm.faces.new([mid[i], mid[ni], top])
        bm.faces.new([mid[ni], mid[i], bot])
    # small orbit ring (floats around crystal)
    ring = [bm.verts.new((math.cos(i*TAU/16)*0.11,
                           math.sin(i*TAU/16)*0.11, 0.13)) for i in range(16)]
    ring2 = [bm.verts.new((math.cos(i*TAU/16)*0.118,
                            math.sin(i*TAU/16)*0.118, 0.13)) for i in range(16)]
    for i in range(16):
        ni = (i + 1) % 16
        bm.faces.new([ring[i], ring[ni], ring2[ni], ring2[i]])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_purple_emissive", "mat_ancient_machine_dark"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_GravityCrystal_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_suit_patch", "SM_Item_SuitPatch_A", '''
def build():
    """ITEM_TOOL_SUIT_PATCH — rounded square emergency hull patch."""
    obj, bm = new_mesh("SM_Item_SuitPatch_A")
    # rounded square plate
    S, T = 0.09, 0.014
    SEGS = 4
    pts = []
    for corner in [(1,1),(-1,1),(-1,-1),(1,-1)]:
        cx, cy = corner[0]*S*0.7, corner[1]*S*0.7
        base_a = math.atan2(corner[1], corner[0]) - TAU/8
        for s in range(SEGS+1):
            a = base_a + s * (TAU/4) / SEGS
            pts.append((cx + math.cos(a)*S*0.3, cy + math.sin(a)*S*0.3))
    lo = [bm.verts.new((x, y, 0)) for x, y in pts]
    hi = [bm.verts.new((x, y, T)) for x, y in pts]
    n = len(pts)
    for i in range(n):
        ni = (i + 1) % n
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # cross seam detail on top
    for axis in range(2):
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, 0, T + 0.003))
            @ Matrix.Rotation(axis * TAU/4, 4, 'Z')
            @ Matrix.Scale(S*1.7, 4, (1,0,0))
            @ Matrix.Scale(0.012, 4, (0,1,0))
            @ Matrix.Scale(0.005, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_SuitPatch_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_air_canister", "SM_Item_AirCanister_A", '''
def build():
    """ITEM_TOOL_AIR_CANISTER — compressed oxygen cylinder with valve."""
    obj, bm = new_mesh("SM_Item_AirCanister_A")
    # tank body
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=12,
        radius=0.045, depth=0.20,
        matrix=Matrix.Translation((0, 0, 0.10)))
    # dome top
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.045,
        matrix=Matrix.Translation((0, 0, 0.20)))
    for v in result['verts']:
        if v.co.z < 0.20:
            v.co.z = 0.20
    # valve stem + knob
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.012, depth=0.035,
        matrix=Matrix.Translation((0, 0, 0.262)))
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
        radius=0.022, depth=0.012,
        matrix=Matrix.Translation((0, 0, 0.286)))
    # gauge band
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=14,
        radius=0.048, depth=0.018,
        matrix=Matrix.Translation((0, 0, 0.155)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_AirCanister_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_heat_shield_cell", "SM_Item_HeatShieldCell_A", '''
def build():
    """ITEM_TOOL_HEAT_SHIELD — hexagonal insulation cell cassette."""
    obj, bm = new_mesh("SM_Item_HeatShieldCell_A")
    # hex cassette body
    R, T = 0.07, 0.030
    lo = [bm.verts.new((math.cos(i*TAU/6)*R, math.sin(i*TAU/6)*R, 0))
          for i in range(6)]
    hi = [bm.verts.new((math.cos(i*TAU/6)*R, math.sin(i*TAU/6)*R, T))
          for i in range(6)]
    for i in range(6):
        ni = (i + 1) % 6
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # inner hex emissive core inset
    lo2 = [bm.verts.new((math.cos(i*TAU/6)*R*0.55,
                          math.sin(i*TAU/6)*R*0.55, T)) for i in range(6)]
    hi2 = [bm.verts.new((math.cos(i*TAU/6)*R*0.55,
                          math.sin(i*TAU/6)*R*0.55, T + 0.006)) for i in range(6)]
    for i in range(6):
        ni = (i + 1) % 6
        bm.faces.new([lo2[i], lo2[ni], hi2[ni], hi2[i]])
    bm.faces.new(hi2)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_heat_bloom"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_HeatShieldCell_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_pressure_liner", "SM_Item_PressureLiner_A", '''
def build():
    """ITEM_UPGRADE_PRESSURE_LINER — curved suit plate segment."""
    obj, bm = new_mesh("SM_Item_PressureLiner_A")
    # curved plate: arc strip
    SEGS = 10
    W = 0.10
    lo_out, lo_in, hi_out, hi_in = [], [], [], []
    for i in range(SEGS + 1):
        a = -TAU/8 + (i / SEGS) * TAU/4
        R_OUT, R_IN = 0.16, 0.145
        for lst, r, z in [(lo_out, R_OUT, 0), (lo_in, R_IN, 0),
                           (hi_out, R_OUT, W), (hi_in, R_IN, W)]:
            lst.append(bm.verts.new((math.cos(a)*r, math.sin(a)*r, z)))
    for i in range(SEGS):
        bm.faces.new([lo_out[i], lo_out[i+1], hi_out[i+1], hi_out[i]])
        bm.faces.new([lo_in[i+1], lo_in[i], hi_in[i], hi_in[i+1]])
        bm.faces.new([lo_in[i], lo_in[i+1], lo_out[i+1], lo_out[i]])
        bm.faces.new([hi_out[i], hi_out[i+1], hi_in[i+1], hi_in[i]])
    for cap in [(lo_out[0], lo_in[0], hi_in[0], hi_out[0]),
                (lo_in[-1], lo_out[-1], hi_out[-1], hi_in[-1])]:
        bm.faces.new(cap)
    # rivet studs
    for i in range(3):
        a = -TAU/10 + i * TAU/10
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.008,
            matrix=Matrix.Translation((math.cos(a)*0.162, math.sin(a)*0.162, W/2)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_PressureLiner_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_rebreather_mod", "SM_Item_RebreatherMod_A", '''
def build():
    """ITEM_UPGRADE_REBREATHER_MOD — twin-tube oxygen expansion module."""
    obj, bm = new_mesh("SM_Item_RebreatherMod_A")
    # twin tubes
    for side in [-1, 1]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=10,
            radius=0.028, depth=0.13,
            matrix=Matrix.Translation((side * 0.035, 0, 0.065)))
    # manifold block joining them
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.135))
        @ Matrix.Scale(0.115, 4, (1,0,0))
        @ Matrix.Scale(0.05, 4, (0,1,0))
        @ Matrix.Scale(0.028, 4, (0,0,1)))
    # connector hose arc
    SEGS = 6
    for i in range(SEGS):
        t = i / (SEGS - 1)
        hx = -0.035 + t * 0.07
        hz = 0.16 + math.sin(t * PI) * 0.025
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.010,
            matrix=Matrix.Translation((hx, 0.02, hz)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_RebreatherMod_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_thermal_weave", "SM_Item_ThermalWeave_A", '''
def build():
    """ITEM_UPGRADE_THERMAL_WEAVE — rolled insulating fabric bolt."""
    random.seed(109)
    obj, bm = new_mesh("SM_Item_ThermalWeave_A")
    # rolled cylinder (lying on side)
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=14,
        radius=0.045, depth=0.16,
        matrix=Matrix.Translation((0, 0, 0.045))
        @ Matrix.Rotation(TAU/4, 4, 'X'))
    # spiral edge detail: outer wrap lip
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=14,
        radius=0.048, depth=0.02,
        matrix=Matrix.Translation((0, 0.06, 0.045))
        @ Matrix.Rotation(TAU/4, 4, 'X'))
    # binding straps
    for sy in [-0.05, 0.05]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=10,
            radius=0.049, depth=0.012,
            matrix=Matrix.Translation((0, sy, 0.045))
            @ Matrix.Rotation(TAU/4, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_heat_bloom"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_ThermalWeave_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_rift_stabiliser", "SM_Item_RiftStabiliser_A", '''
def build():
    """ITEM_KEY_RIFT_STABILISER — alien fabricated key device: ring + core."""
    obj, bm = new_mesh("SM_Item_RiftStabiliser_A")
    # outer ring (torus approximation: ring of spheres)
    R = 0.085
    for i in range(14):
        a = i * TAU / 14
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.014,
            matrix=Matrix.Translation((math.cos(a)*R, math.sin(a)*R, 0.10)))
    # core octahedron
    top = bm.verts.new((0, 0, 0.10 + 0.05))
    bot = bm.verts.new((0, 0, 0.10 - 0.05))
    mid = [bm.verts.new((math.cos(i*TAU/4)*0.032,
                          math.sin(i*TAU/4)*0.032, 0.10)) for i in range(4)]
    for i in range(4):
        ni = (i + 1) % 4
        bm.faces.new([mid[i], mid[ni], top])
        bm.faces.new([mid[ni], mid[i], bot])
    # 3 anchor prongs from ring to core
    for i in range(3):
        a = i * TAU / 3
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=5,
            radius=0.006, depth=R - 0.035,
            matrix=Matrix.Translation((math.cos(a)*R*0.55,
                                        math.sin(a)*R*0.55, 0.10))
            @ Matrix.Rotation(a + TAU/4, 4, 'Z')
            @ Matrix.Rotation(TAU/4, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive", "mat_orb_energy"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_RiftStabiliser_A")
    return obj
'''))

ASSETS.append(("items", "Items", "sm_item_armor_plating", "SM_Item_ArmorPlating_A", '''
def build():
    """ITEM_UPGRADE_ARMOR_PLATING — angular stacked hull plates."""
    obj, bm = new_mesh("SM_Item_ArmorPlating_A")
    # 3 stacked offset angular plates
    for i in range(3):
        z = i * 0.018
        off = i * 0.012
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((off, off * 0.5, z + 0.008))
            @ Matrix.Rotation(i * 0.12, 4, 'Z')
            @ Matrix.Scale(0.13 - i*0.015, 4, (1,0,0))
            @ Matrix.Scale(0.10 - i*0.012, 4, (0,1,0))
            @ Matrix.Scale(0.014, 4, (0,0,1)))
    # corner bolts on top plate
    for cx, cy in [(-0.04, -0.03), (0.06, -0.02), (0.05, 0.05), (-0.03, 0.045)]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.007,
            matrix=Matrix.Translation((cx + 0.024, cy + 0.012, 0.062)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Item_ArmorPlating_A")
    return obj
'''))

# ====================================================================
# GAMEPLAY PROPS — meshes for C++ actors that currently have none
# ====================================================================

ASSETS.append(("gameplay_props", "Slice", "sm_power_node", "SM_PowerNode_A", '''
def build():
    """AAbyssalPowerNode — ancient power relay pylon, 2.2m. Emissive core
    sphere visible through 4 frame ribs; conduit ports at 4 compass points."""
    obj, bm = new_mesh("SM_PowerNode_A")
    # base plinth (octagon)
    lo = [bm.verts.new((math.cos(i*TAU/8)*0.45, math.sin(i*TAU/8)*0.45, 0))
          for i in range(8)]
    hi = [bm.verts.new((math.cos(i*TAU/8)*0.38, math.sin(i*TAU/8)*0.38, 0.25))
          for i in range(8)]
    for i in range(8):
        ni = (i + 1) % 8
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # central column
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.10, depth=0.55,
        matrix=Matrix.Translation((0, 0, 0.52)))
    # core energy sphere
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.22,
        matrix=Matrix.Translation((0, 0, 1.15)))
    # 4 cage frame ribs around the core
    for i in range(4):
        a = i * TAU / 4
        SEGS = 8
        for s in range(SEGS + 1):
            t = s / SEGS
            ring_a = -PI/2 + t * PI
            rx = math.cos(ring_a) * 0.32
            rz = 1.15 + math.sin(ring_a) * 0.32
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.030,
                matrix=Matrix.Translation((math.cos(a)*rx, math.sin(a)*rx, rz)))
    # top cap antenna
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
        radius=0.04, depth=0.45,
        matrix=Matrix.Translation((0, 0, 1.75)))
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.07,
        matrix=Matrix.Translation((0, 0, 2.05)))
    # 4 conduit ports on plinth
    for i in range(4):
        a = i * TAU / 4 + TAU/8
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
            radius=0.07, depth=0.12,
            matrix=Matrix.Translation((math.cos(a)*0.44, math.sin(a)*0.44, 0.12))
            @ Matrix.Rotation(a + TAU/4, 4, 'Z')
            @ Matrix.Rotation(TAU/4, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_orb_energy"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_PowerNode_A")
    return obj
'''))

ASSETS.append(("gameplay_props", "Slice", "sm_rift_core", "SM_RiftActor_Core_A", '''
def build():
    """AAbyssalRiftActor — endgame rift anchor: 6m double-ring gate with
    central void sphere and 6 stabiliser sockets (for ITEM_KEY_RIFT_STABILISER)."""
    obj, bm = new_mesh("SM_RiftActor_Core_A")
    # twin vertical rings (gyroscope arrangement)
    for ring_rot in [0, TAU/4]:
        SEGS = 24
        for s in range(SEGS):
            a = s * TAU / SEGS
            x = math.cos(a) * 2.6
            z = 3.0 + math.sin(a) * 2.6
            pos = Vector((x * math.cos(ring_rot), x * math.sin(ring_rot), z))
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.16,
                matrix=Matrix.Translation(pos))
    # central void sphere
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0,
        matrix=Matrix.Translation((0, 0, 3.0)))
    # base pedestal
    lo = [bm.verts.new((math.cos(i*TAU/6)*1.6, math.sin(i*TAU/6)*1.6, 0))
          for i in range(6)]
    hi = [bm.verts.new((math.cos(i*TAU/6)*1.1, math.sin(i*TAU/6)*1.1, 0.6))
          for i in range(6)]
    for i in range(6):
        ni = (i + 1) % 6
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # 6 stabiliser sockets around pedestal rim
    for i in range(6):
        a = i * TAU / 6 + TAU/12
        sx, sy = math.cos(a)*1.35, math.sin(a)*1.35
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=8,
            radius=0.14, depth=0.10,
            matrix=Matrix.Translation((sx, sy, 0.62)))
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
            radius=0.10, depth=0.04,
            matrix=Matrix.Translation((sx, sy, 0.60)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive",
                        "mat_orb_energy", "mat_purple_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_RiftActor_Core_A")
    return obj
'''))

ASSETS.append(("gameplay_props", "Slice", "sm_discovery_marker", "SM_DiscoveryMarker_A", '''
def build():
    """ADiscoveryActor — scannable discovery marker: tilted ancient stele
    with glyph face and crystal inclusion at the crown, 1.6m."""
    random.seed(120)
    obj, bm = new_mesh("SM_DiscoveryMarker_A")
    # tilted stele slab
    TILT = 0.12
    levels = [(0, 0.30, 0.18), (0.9, 0.26, 0.15), (1.6, 0.16, 0.10)]
    rings = []
    for z, w, d in levels:
        cx = z * TILT
        ring = [bm.verts.new((cx + sx*w, sy*d, z))
                for sx, sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(4):
            bm.faces.new([lo[i], lo[(i+1)%4], hi[(i+1)%4], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # glyph grooves on front face
    for gz in [0.35, 0.62, 0.89, 1.16]:
        gx = gz * TILT
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((gx, -0.165, gz))
            @ Matrix.Scale(0.30, 4, (1,0,0))
            @ Matrix.Scale(0.015, 4, (0,1,0))
            @ Matrix.Scale(0.05, 4, (0,0,1)))
    # crystal inclusion at crown
    tip = bm.verts.new((1.6*TILT, 0, 1.85))
    base_ring = [bm.verts.new((1.6*TILT + math.cos(i*TAU/5)*0.07,
                                math.sin(i*TAU/5)*0.07, 1.58)) for i in range(5)]
    for i in range(5):
        bm.faces.new([base_ring[i], base_ring[(i+1)%5], tip])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_blue_emissive", "mat_crystal_blue"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_DiscoveryMarker_A")
    return obj
'''))

ASSETS.append(("gameplay_props", "Slice", "sm_ember_vent", "SM_EmberVent_A", '''
def build():
    """AEmberVentHazard — Mantle Garden ember vent: low rocky mound with
    8 small spit-holes and glowing throat, 1.2m diameter."""
    random.seed(121)
    obj, bm = new_mesh("SM_EmberVent_A")
    # mound
    SEGS = 12
    levels = [(0, 0.60), (0.12, 0.55), (0.28, 0.42), (0.42, 0.26), (0.50, 0.14)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/SEGS)*r*random.uniform(0.9, 1.1),
                               math.sin(i*TAU/SEGS)*r*random.uniform(0.9, 1.1),
                               z + random.uniform(-0.02, 0.02)))
                for i in range(SEGS)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i+1)%SEGS], hi[(i+1)%SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    # glowing throat (inner ring at top)
    throat = [bm.verts.new((math.cos(i*TAU/8)*0.10,
                             math.sin(i*TAU/8)*0.10, 0.46)) for i in range(8)]
    bm.faces.new(throat)
    # 8 ember spit-holes on the flanks
    for i in range(8):
        a = i * TAU / 8 + 0.2
        hr = random.uniform(0.30, 0.48)
        hz = random.uniform(0.10, 0.30)
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
            radius=0.035, depth=0.06,
            matrix=Matrix.Translation((math.cos(a)*hr, math.sin(a)*hr, hz))
            @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Rotation(TAU/4, 4, 'Y'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_obsidian", "mat_heat_crack", "mat_lava_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_EmberVent_A")
    return obj
'''))

ASSETS.append(("gameplay_props", "Slice", "sm_gravity_shear_emitter", "SM_GravityShear_Emitter_A", '''
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
'''))

ASSETS.append(("gameplay_props", "Slice", "sm_structural_debris", "SM_StructuralDebris_A", '''
def build():
    """StructuralHazards falling debris — jagged rock slab cluster used by
    the falling-debris hazard, 1.5m chunk."""
    random.seed(122)
    obj, bm = new_mesh("SM_StructuralDebris_A")
    # primary jagged chunk
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.7,
        matrix=Matrix.Translation((0, 0, 0.7)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.7, 1.3)
        v.co.y *= random.uniform(0.7, 1.3)
        v.co.z = 0.7 + (v.co.z - 0.7) * random.uniform(0.6, 1.2)
    # 2 satellite shards
    for sx, sy, sr in [(0.75, 0.3, 0.28), (-0.6, -0.4, 0.22)]:
        result = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=sr,
            matrix=Matrix.Translation((sx, sy, sr)))
        for v in result['verts']:
            v.co.x = sx + (v.co.x - sx) * random.uniform(0.6, 1.4)
            v.co.y = sy + (v.co.y - sy) * random.uniform(0.6, 1.4)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_StructuralDebris_A")
    return obj
'''))

# ====================================================================
# SET DRESSING — scatter kit used by every biome
# ====================================================================

for size_tag, radius, seed in [("S", 0.25, 201), ("M", 0.65, 202), ("L", 1.6, 203)]:
    ASSETS.append(("set_dressing", "SetDressing",
                   f"sm_scatter_rock_{size_tag.lower()}",
                   f"SM_Scatter_Rock_{size_tag}_A", f'''
def build():
    """Scatter rock {size_tag} — generic deformed boulder for set dressing."""
    random.seed({seed})
    obj, bm = new_mesh("SM_Scatter_Rock_{size_tag}_A")
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius={radius},
        matrix=Matrix.Translation((0, 0, {radius} * 0.8)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.75, 1.30)
        v.co.y *= random.uniform(0.75, 1.30)
        zc = {radius} * 0.8
        if v.co.z < zc:
            v.co.z = zc - (zc - v.co.z) * 0.45   # flatten underside
        else:
            v.co.z = zc + (v.co.z - zc) * random.uniform(0.7, 1.1)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Scatter_Rock_{size_tag}_A")
    return obj
'''))

ASSETS.append(("set_dressing", "SetDressing", "sm_kelp_strand_a", "SM_Kelp_Strand_A", '''
def build():
    """Bioluminescent kelp strand — 2.5m swaying flora for Inner Sea / Rift."""
    random.seed(204)
    obj, bm = new_mesh("SM_Kelp_Strand_A")
    # main stem: chain of segments with slight S-curve
    SEGS = 12
    for i in range(SEGS):
        t = i / (SEGS - 1)
        sx = math.sin(t * PI * 1.5) * 0.12
        sz = t * 2.5
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=5,
            radius=0.025 * (1 - t * 0.6), depth=0.24,
            matrix=Matrix.Translation((sx, 0, sz + 0.12)))
    # leaf blades alternating sides
    for i in range(8):
        t = (i + 1) / 9
        sx = math.sin(t * PI * 1.5) * 0.12
        sz = t * 2.5
        side = 1 if i % 2 == 0 else -1
        # blade: flat tapered quad strip
        blade_pts = []
        for b in range(4):
            bt = b / 3
            blade_pts.append(bm.verts.new((
                sx + side * bt * 0.30,
                side * bt * 0.08,
                sz + bt * 0.15 + math.sin(bt * PI) * 0.05)))
        for b in range(3):
            w = 0.04 * (1 - b/3 * 0.7)
            v0 = blade_pts[b]
            v1 = blade_pts[b+1]
            v2 = bm.verts.new(v1.co + Vector((0, 0, w)))
            v3 = bm.verts.new(v0.co + Vector((0, 0, w)))
            bm.faces.new([v0, v1, v2, v3])
    # glow bulb at tip
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.045,
        matrix=Matrix.Translation((math.sin(PI*1.5)*0.12, 0, 2.55)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_water_bioluminescent", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Kelp_Strand_A")
    return obj
'''))

ASSETS.append(("set_dressing", "SetDressing", "sm_ancient_rubble_a", "SM_Ancient_Rubble_A", '''
def build():
    """Ancient machine rubble pile — broken dark-metal fragments, 1.2m spread."""
    random.seed(205)
    obj, bm = new_mesh("SM_Ancient_Rubble_A")
    # angular machine fragments at random orientations
    for i in range(7):
        px = random.uniform(-0.5, 0.5)
        py = random.uniform(-0.5, 0.5)
        s = random.uniform(0.12, 0.35)
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((px, py, s * 0.4))
            @ Matrix.Rotation(random.uniform(0, TAU), 4, 'Z')
            @ Matrix.Rotation(random.uniform(-0.4, 0.4), 4, 'X')
            @ Matrix.Scale(s, 4, (1,0,0))
            @ Matrix.Scale(s * random.uniform(0.5, 1.2), 4, (0,1,0))
            @ Matrix.Scale(s * random.uniform(0.2, 0.5), 4, (0,0,1)))
    # one recognisable curved shell piece
    SEGS = 8
    for s in range(SEGS):
        a = s * (TAU / 4) / SEGS
        bmesh.ops.create_cube(bm, size=0.10,
            matrix=Matrix.Translation((0.1 + math.cos(a)*0.35,
                                        -0.15, 0.05 + math.sin(a)*0.35))
            @ Matrix.Rotation(a, 4, 'Y'))
    # faint emissive vein fragment
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((-0.2, 0.25, 0.05))
        @ Matrix.Scale(0.30, 4, (1,0,0))
        @ Matrix.Scale(0.02, 4, (0,1,0))
        @ Matrix.Scale(0.02, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Ancient_Rubble_A")
    return obj
'''))

ASSETS.append(("set_dressing", "SetDressing", "sm_crystal_scatter_a", "SM_Crystal_Scatter_A", '''
def build():
    """Tiny crystal scatter clump — 30cm breadcrumb accent, cheap tri count."""
    random.seed(206)
    obj, bm = new_mesh("SM_Crystal_Scatter_A")
    for i in range(5):
        a = i * TAU / 5 + random.uniform(-0.3, 0.3)
        cx = math.cos(a) * random.uniform(0.02, 0.10)
        cy = math.sin(a) * random.uniform(0.02, 0.10)
        h = random.uniform(0.08, 0.28)
        w = h * random.uniform(0.18, 0.28)
        tilt_x = random.uniform(-0.2, 0.2)
        tip = bm.verts.new((cx + tilt_x * h, cy, h))
        ring = [bm.verts.new((cx + math.cos(j*TAU/4)*w,
                               cy + math.sin(j*TAU/4)*w, 0)) for j in range(4)]
        for j in range(4):
            bm.faces.new([ring[j], ring[(j+1)%4], tip])
        bm.faces.new(list(reversed(ring)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Crystal_Scatter_A")
    return obj
'''))

# ====================================================================
# VFX SUPPORT — simple meshes driven by materials/Niagara
# ====================================================================

ASSETS.append(("vfx_support", "VFXSupport", "sm_vfx_beam_cylinder", "SM_VFX_BeamCylinder", '''
def build():
    """Unit beam cylinder — 1m long, 0.5m diameter open tube. Scaled per-beam
    in-engine; collector beam material pans along its length."""
    obj, bm = new_mesh("SM_VFX_BeamCylinder")
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=16,
        radius=0.25, depth=1.0,
        matrix=Matrix.Translation((0, 0, 0.5)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_orb_energy"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_VFX_BeamCylinder")
    return obj
'''))

ASSETS.append(("vfx_support", "VFXSupport", "sm_vfx_orb_sphere", "SM_VFX_OrbSphere", '''
def build():
    """Unit orb sphere — 1m diameter smooth sphere for energy-orb materials
    (collector orb, rift void, anomaly core)."""
    obj, bm = new_mesh("SM_VFX_OrbSphere")
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=0.5,
        matrix=Matrix.Translation((0, 0, 0.5)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_orb_energy"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_VFX_OrbSphere")
    return obj
'''))

ASSETS.append(("vfx_support", "VFXSupport", "sm_vfx_scan_pulse_ring", "SM_VFX_ScanPulseRing", '''
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
'''))


# ────────────────────────────────────────────────────────────────────
# Writers
# ────────────────────────────────────────────────────────────────────

def write_assets():
    for folder, export_sub, stem, sm_name, body in ASSETS:
        parts = folder.split("/")
        depth = len(parts)
        target = os.path.join(SCRIPTS_DIR, *parts)
        os.makedirs(target, exist_ok=True)
        init = os.path.join(target, "__init__.py")
        if not os.path.exists(init):
            open(init, "w").close()
        path = os.path.join(target, stem + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(header(sm_name, depth, export_sub) + body.strip("\n") + footer(sm_name))
        print(f"  + {folder}/{stem}.py  ({sm_name})")


def regen_run_alls():
    """Scan every category folder and regenerate run_all.py from sm_*.py files."""
    leaf_dirs = []
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        if root.endswith("shared"):
            continue
        stems = sorted(f[:-3] for f in files
                       if f.startswith("sm_") and f.endswith(".py"))
        if stems:
            leaf_dirs.append((root, stems))

    for root, stems in leaf_dirs:
        rel = os.path.relpath(root, SCRIPTS_DIR)
        depth = len(rel.split(os.sep))
        dots = ", ".join(repr("..") for _ in range(depth))
        imports = "\n".join(f"from {s} import build as build_{s}" for s in stems)
        calls = "\n".join(f"    build_{s}()" for s in stems)
        content = f'''"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, {dots}))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from shared.utils import clear_scene

{imports}


def run_all():
{calls}


if __name__ == "__main__":
    run_all()
'''
        with open(os.path.join(root, "run_all.py"), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ~ {rel}/run_all.py  ({len(stems)} assets)")

    # intermediate run_alls for parent dirs that only contain subfolders
    for parent in ["world_biomes", "prologue_submarine"]:
        pdir = os.path.join(SCRIPTS_DIR, parent)
        if not os.path.isdir(pdir):
            continue
        subs = sorted(d for d in os.listdir(pdir)
                      if os.path.isdir(os.path.join(pdir, d)) and
                      os.path.exists(os.path.join(pdir, d, "run_all.py")))
        imports = "\n".join(
            f"from {parent}.{s}.run_all import run_all as run_{s}" for s in subs)
        calls = "\n".join(f"    run_{s}()" for s in subs)
        content = f'''"""run_all.py — build all sub-biome assets."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

{imports}


def run_all():
{calls}


if __name__ == "__main__":
    run_all()
'''
        with open(os.path.join(pdir, "run_all.py"), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ~ {parent}/run_all.py  (delegates to {len(subs)} sub-biomes)")

    # root master runner
    tops = sorted(d for d in os.listdir(SCRIPTS_DIR)
                  if os.path.isdir(os.path.join(SCRIPTS_DIR, d)) and
                  d != "shared" and
                  os.path.exists(os.path.join(SCRIPTS_DIR, d, "run_all.py")))
    imports = "\n".join(f"from {t}.run_all import run_all as run_{t}" for t in tops)
    calls = "\n".join(
        f"    print('\\\\n--- {t} ---')\\n    run_{t}()" for t in tops)
    content = f'''"""run_all_assets.py — master runner for ALL AbyssalEarth assets.

Usage:
    blender --background --python run_all_assets.py
"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

{imports}


def main():
    print("=== AbyssalEarth Full Asset Generation ===")
{calls}
    print("\\\\n=== ALL ASSETS COMPLETE ===")


if __name__ == "__main__":
    main()
'''
    with open(os.path.join(SCRIPTS_DIR, "run_all_assets.py"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ~ run_all_assets.py  ({len(tops)} categories)")


if __name__ == "__main__":
    print("=== Massive asset expansion ===")
    write_assets()
    print()
    regen_run_alls()
    print("\n=== DONE ===")
