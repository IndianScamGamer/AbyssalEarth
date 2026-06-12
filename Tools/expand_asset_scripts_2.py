#!/usr/bin/env python3
"""
expand_asset_scripts_2.py — concept-art-grounded expansion, iteration 2.

Sources (Content/ArtDirection/Concepts/):
  Intro/intro_submarine_wide_concept.png   → submarine exterior, ROV drone,
                                              shaft rim ring, work light
  Items/item_models_toolkit_concept.png    → 7 handheld expedition tools
  Later_Regions/LT-001.png                 → ash cathedral columns, buried
                                              machine slabs, ash dunes
  Environments/ancient_bridge_platform_kit_concept.png
                                           → hanging platform, rope railing,
                                              stair ramp

Run from repo root:  python3 Tools/expand_asset_scripts_2.py
Then:                python3 Tools/regen_run_alls.py  (regenerates runners)
"""

import os

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


ASSETS = []

# ====================================================================
# PROLOGUE EXTERIOR — intro_submarine_wide_concept.png
# ====================================================================

ASSETS.append(("prologue_submarine/exterior", "Prologue", "sm_submarine_exterior",
               "SM_Submarine_Exterior_A", '''
def build():
    """Hero submarine exterior — sleek 24m hull, conning hump, twin bow
    headlights, stern props. Concept: intro_submarine_wide/close."""
    obj, bm = new_mesh("SM_Submarine_Exterior_A")
    # main hull: ring loft, elliptical cross-section, tapered nose/tail
    SEGS = 12
    stations = [  # (y along length, radius, z lift)
        (-12.0, 0.25, 0.9), (-10.8, 0.85, 0.9), (-8.5, 1.35, 1.0),
        (-5.0, 1.60, 1.05), (0.0, 1.65, 1.05), (4.5, 1.55, 1.05),
        (8.0, 1.20, 1.0), (10.5, 0.70, 0.95), (11.8, 0.22, 0.9)]
    rings = []
    for y, r, zl in stations:
        ring = [bm.verts.new((math.cos(i*TAU/SEGS)*r,
                               y,
                               zl + math.sin(i*TAU/SEGS)*r*0.82))
                for i in range(SEGS)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i+1)%SEGS], hi[(i+1)%SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # conning hump (low fairwater, streamlined)
    hump = [(-3.5, 0.55), (-2.0, 0.95), (0.5, 0.95), (1.8, 0.50)]
    h_rings = []
    for y, hh in hump:
        ring = [bm.verts.new((math.cos(i*TAU/8)*0.75, y,
                               2.30 + math.sin(i*TAU/8)*hh*0.5 + hh*0.5))
                for i in range(8)]
        h_rings.append(ring)
    for ri in range(len(h_rings)-1):
        lo, hi = h_rings[ri], h_rings[ri+1]
        for i in range(8):
            bm.faces.new([lo[i], lo[(i+1)%8], hi[(i+1)%8], hi[i]])
    bm.faces.new(list(reversed(h_rings[0])))
    bm.faces.new(h_rings[-1])
    # twin bow headlights
    for side in [-1, 1]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=10,
            radius=0.22, depth=0.25,
            matrix=Matrix.Translation((side*0.55, -11.2, 0.75))
            @ Matrix.Rotation(TAU/4, 4, 'X'))
    # stern prop shrouds
    for side in [-1, 1]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=12,
            radius=0.55, depth=0.5,
            matrix=Matrix.Translation((side*0.95, 11.0, 0.95))
            @ Matrix.Rotation(TAU/4, 4, 'X'))
        # hub + 4 blades
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.12,
            matrix=Matrix.Translation((side*0.95, 11.0, 0.95)))
        for b in range(4):
            ba = b * TAU / 4
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((side*0.95 + math.cos(ba)*0.28,
                                            11.0, 0.95 + math.sin(ba)*0.28))
                @ Matrix.Rotation(ba, 4, 'Y')
                @ Matrix.Scale(0.38, 4, (1,0,0))
                @ Matrix.Scale(0.05, 4, (0,1,0))
                @ Matrix.Scale(0.16, 4, (0,0,1)))
    # dive planes
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side*2.1, -7.5, 1.05))
            @ Matrix.Scale(1.6, 4, (1,0,0))
            @ Matrix.Scale(0.9, 4, (0,1,0))
            @ Matrix.Scale(0.10, 4, (0,0,1)))
    # belly skids
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side*0.9, 0.0, 0.0))
            @ Matrix.Scale(0.18, 4, (1,0,0))
            @ Matrix.Scale(9.0, 4, (0,1,0))
            @ Matrix.Scale(0.14, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive",
                        "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Submarine_Exterior_A")
    return obj
'''))

ASSETS.append(("prologue_submarine/exterior", "Prologue", "sm_rov_drone",
               "SM_ROV_Drone_A", '''
def build():
    """Small support ROV drone — 80cm boxy body, 4 thruster pods, light bar.
    Concept: small lit drones around the submarine in intro_submarine_wide."""
    obj, bm = new_mesh("SM_ROV_Drone_A")
    # body
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.30))
        @ Matrix.Scale(0.55, 4, (1,0,0))
        @ Matrix.Scale(0.80, 4, (0,1,0))
        @ Matrix.Scale(0.35, 4, (0,0,1)))
    # 4 thruster pods at corners
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            bmesh.ops.create_cylinder(bm, cap_ends=False, segments=10,
                radius=0.10, depth=0.16,
                matrix=Matrix.Translation((sx*0.34, sy*0.46, 0.30))
                @ Matrix.Rotation(TAU/4, 4, 'X'))
    # front light bar
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, -0.42, 0.34))
        @ Matrix.Scale(0.42, 4, (1,0,0))
        @ Matrix.Scale(0.06, 4, (0,1,0))
        @ Matrix.Scale(0.08, 4, (0,0,1)))
    # top antenna + sensor dome
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.09,
        matrix=Matrix.Translation((0, 0.1, 0.52)))
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=5,
        radius=0.012, depth=0.22,
        matrix=Matrix.Translation((0.15, 0.3, 0.58)))
    # belly manipulator stub
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
        radius=0.035, depth=0.18,
        matrix=Matrix.Translation((0, -0.25, 0.08)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_ROV_Drone_A")
    return obj
'''))

ASSETS.append(("prologue_submarine/exterior", "Prologue", "sm_shaft_rim_segment",
               "SM_ShaftRim_Segment_A", '''
def build():
    """Modular rim segment of the great shaft pit — 30° arc of the ring lip
    with terraced inner wall and 3 work-light posts. Tiles 12x for full ring.
    Concept: ringed pit in intro_submarine_wide."""
    random.seed(310)
    obj, bm = new_mesh("SM_ShaftRim_Segment_A")
    ARC = TAU / 12
    R_OUT, R_IN = 30.0, 22.0
    SEGS = 8
    # rim deck (flat annular sector)
    out_lo, in_lo = [], []
    for i in range(SEGS + 1):
        a = -ARC/2 + (i/SEGS) * ARC
        out_lo.append(bm.verts.new((math.cos(a)*R_OUT, math.sin(a)*R_OUT, 0)))
        in_lo.append(bm.verts.new((math.cos(a)*R_IN, math.sin(a)*R_IN, 0)))
    for i in range(SEGS):
        bm.faces.new([out_lo[i], out_lo[i+1], in_lo[i+1], in_lo[i]])
    # terraced inner wall: 3 steps down into the pit
    prev = in_lo
    for step, (dr, dz) in enumerate([(1.5, -4.0), (1.5, -4.0), (1.2, -4.0)]):
        r = R_IN - (step + 1) * dr
        z = (step + 1) * dz
        cur = []
        for i in range(SEGS + 1):
            a = -ARC/2 + (i/SEGS) * ARC
            cur.append(bm.verts.new((math.cos(a)*r, math.sin(a)*r, z)))
        for i in range(SEGS):
            bm.faces.new([prev[i], prev[i+1], cur[i+1], cur[i]])
        prev = cur
    # 3 work-light posts on the rim
    for t in [0.2, 0.5, 0.8]:
        a = -ARC/2 + t * ARC
        px, py = math.cos(a)*(R_IN + 1.0), math.sin(a)*(R_IN + 1.0)
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
            radius=0.08, depth=2.5,
            matrix=Matrix.Translation((px, py, 1.25)))
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((px, py, 2.6))
            @ Matrix.Scale(0.45, 4, (1,0,0))
            @ Matrix.Scale(0.18, 4, (0,1,0))
            @ Matrix.Scale(0.18, 4, (0,0,1)))
    # rocky outer edge irregularity
    for i in range(6):
        a = -ARC/2 + random.uniform(0.05, 0.95) * ARC
        rr = R_OUT - random.uniform(0, 1.5)
        s = random.uniform(0.6, 1.8)
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=s,
            matrix=Matrix.Translation((math.cos(a)*rr, math.sin(a)*rr, s*0.3)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_human_equipment",
                        "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_ShaftRim_Segment_A")
    return obj
'''))

ASSETS.append(("prologue_submarine/exterior", "Prologue", "sm_work_light_post",
               "SM_WorkLight_Post_A", '''
def build():
    """Standalone seafloor work light — weighted tripod base, 3m mast,
    twin amber flood heads. Scatter around the shaft rim."""
    obj, bm = new_mesh("SM_WorkLight_Post_A")
    # weighted base disc
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=10,
        radius=0.45, depth=0.15,
        matrix=Matrix.Translation((0, 0, 0.075)))
    # mast
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.06, depth=3.0,
        matrix=Matrix.Translation((0, 0, 1.65)))
    # crossbar
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 3.15))
        @ Matrix.Scale(1.1, 4, (1,0,0))
        @ Matrix.Scale(0.08, 4, (0,1,0))
        @ Matrix.Scale(0.08, 4, (0,0,1)))
    # twin flood heads, angled down
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side*0.48, -0.06, 3.12))
            @ Matrix.Rotation(-0.5, 4, 'X')
            @ Matrix.Scale(0.30, 4, (1,0,0))
            @ Matrix.Scale(0.12, 4, (0,1,0))
            @ Matrix.Scale(0.22, 4, (0,0,1)))
    # cable drape stub
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=5,
        radius=0.02, depth=0.8,
        matrix=Matrix.Translation((0.3, 0.2, 0.4))
        @ Matrix.Rotation(0.9, 4, 'X'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_WorkLight_Post_A")
    return obj
'''))

# ====================================================================
# TOOLS — item_models_toolkit_concept.png (7 handheld expedition tools)
# ====================================================================

ASSETS.append(("tools", "Tools", "sm_tool_hand_scanner", "SM_Tool_HandScanner_A", '''
def build():
    """Handheld survey scanner — pistol grip, boxy head with screen and
    sensor snout. Physical prop for UAbyssalScanComponent in-hand visual."""
    obj, bm = new_mesh("SM_Tool_HandScanner_A")
    # head box
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.16))
        @ Matrix.Scale(0.10, 4, (1,0,0))
        @ Matrix.Scale(0.16, 4, (0,1,0))
        @ Matrix.Scale(0.11, 4, (0,0,1)))
    # screen plate (angled back face)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.085, 0.18))
        @ Matrix.Rotation(-0.25, 4, 'X')
        @ Matrix.Scale(0.085, 4, (1,0,0))
        @ Matrix.Scale(0.012, 4, (0,1,0))
        @ Matrix.Scale(0.075, 4, (0,0,1)))
    # sensor snout
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.030, depth=0.06,
        matrix=Matrix.Translation((0, -0.11, 0.17))
        @ Matrix.Rotation(TAU/4, 4, 'X'))
    # pistol grip
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.03, 0.055))
        @ Matrix.Rotation(0.30, 4, 'X')
        @ Matrix.Scale(0.045, 4, (1,0,0))
        @ Matrix.Scale(0.055, 4, (0,1,0))
        @ Matrix.Scale(0.11, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_HandScanner_A")
    return obj
'''))

ASSETS.append(("tools", "Tools", "sm_tool_plasma_drill", "SM_Tool_PlasmaDrill_A", '''
def build():
    """Compact harvest drill — body with side grip, tapered bit, heat fins.
    In-hand visual for harvesting interactions."""
    obj, bm = new_mesh("SM_Tool_PlasmaDrill_A")
    # body
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=10,
        radius=0.055, depth=0.20,
        matrix=Matrix.Translation((0, 0, 0.14))
        @ Matrix.Rotation(TAU/4, 4, 'X'))
    # drill bit (tapered, fluted)
    bit_levels = [(0, 0.030), (0.06, 0.022), (0.12, 0.010), (0.16, 0.002)]
    rings = []
    for d, r in bit_levels:
        ring = [bm.verts.new((math.cos(i*TAU/6)*r,
                               -0.10 - d,
                               0.14 + math.sin(i*TAU/6)*r)) for i in range(6)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(6):
            bm.faces.new([lo[i], lo[(i+1)%6], hi[(i+1)%6], hi[i]])
    # heat fins
    for fy in [0.04, 0.08, 0.12]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, fy, 0.205))
            @ Matrix.Scale(0.13, 4, (1,0,0))
            @ Matrix.Scale(0.012, 4, (0,1,0))
            @ Matrix.Scale(0.035, 4, (0,0,1)))
    # grip handle below
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.07, 0.045))
        @ Matrix.Rotation(0.25, 4, 'X')
        @ Matrix.Scale(0.040, 4, (1,0,0))
        @ Matrix.Scale(0.050, 4, (0,1,0))
        @ Matrix.Scale(0.10, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_heat_bloom"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_PlasmaDrill_A")
    return obj
'''))

ASSETS.append(("tools", "Tools", "sm_tool_data_tablet", "SM_Tool_DataTablet_A", '''
def build():
    """Ruggedised data tablet — narrative pickup prop for journal/terminal
    beats (NarrativeSubsystem). Corner bumpers, screen inset, side clasps."""
    obj, bm = new_mesh("SM_Tool_DataTablet_A")
    # slab
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.012))
        @ Matrix.Scale(0.16, 4, (1,0,0))
        @ Matrix.Scale(0.22, 4, (0,1,0))
        @ Matrix.Scale(0.022, 4, (0,0,1)))
    # screen inset (raised lip frame)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.026))
        @ Matrix.Scale(0.13, 4, (1,0,0))
        @ Matrix.Scale(0.18, 4, (0,1,0))
        @ Matrix.Scale(0.004, 4, (0,0,1)))
    # corner bumpers
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
                radius=0.022, depth=0.030,
                matrix=Matrix.Translation((sx*0.075, sy*0.105, 0.015)))
    # side clasps
    for sy in [-0.06, 0.06]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0.085, sy, 0.012))
            @ Matrix.Scale(0.015, 4, (1,0,0))
            @ Matrix.Scale(0.030, 4, (0,1,0))
            @ Matrix.Scale(0.018, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_DataTablet_A")
    return obj
'''))

ASSETS.append(("tools", "Tools", "sm_tool_flare", "SM_Tool_Flare_A", '''
def build():
    """Emergency flare stick — grip tube with cap and red glow tip."""
    obj, bm = new_mesh("SM_Tool_Flare_A")
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.016, depth=0.18,
        matrix=Matrix.Translation((0, 0, 0.09)))
    # grip rings
    for gz in [0.04, 0.08, 0.12]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=8,
            radius=0.018, depth=0.010,
            matrix=Matrix.Translation((0, 0, gz)))
    # glow tip
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.014, depth=0.035,
        matrix=Matrix.Translation((0, 0, 0.198)))
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.015,
        matrix=Matrix.Translation((0, 0, 0.216)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_red_emissive_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_Flare_A")
    return obj
'''))

ASSETS.append(("tools", "Tools", "sm_tool_battery_case", "SM_Tool_BatteryCase_A", '''
def build():
    """Battery cell case — hinged box with 6 visible cells in foam."""
    obj, bm = new_mesh("SM_Tool_BatteryCase_A")
    # case base
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.030))
        @ Matrix.Scale(0.20, 4, (1,0,0))
        @ Matrix.Scale(0.13, 4, (0,1,0))
        @ Matrix.Scale(0.055, 4, (0,0,1)))
    # open lid (tilted back)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.085, 0.095))
        @ Matrix.Rotation(1.15, 4, 'X')
        @ Matrix.Scale(0.20, 4, (1,0,0))
        @ Matrix.Scale(0.12, 4, (0,1,0))
        @ Matrix.Scale(0.015, 4, (0,0,1)))
    # 6 cells in 2x3 grid
    for cx in [-0.06, 0.0, 0.06]:
        for cy in [-0.028, 0.028]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
                radius=0.020, depth=0.045,
                matrix=Matrix.Translation((cx, cy, 0.068)))
    # latch
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, -0.068, 0.035))
        @ Matrix.Scale(0.035, 4, (1,0,0))
        @ Matrix.Scale(0.010, 4, (0,1,0))
        @ Matrix.Scale(0.030, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_BatteryCase_A")
    return obj
'''))

ASSETS.append(("tools", "Tools", "sm_tool_multitool", "SM_Tool_Multitool_A", '''
def build():
    """Folding multitool — open scissor-pose with two handle slabs and
    plier head."""
    obj, bm = new_mesh("SM_Tool_Multitool_A")
    # two handle slabs in shallow V
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side*0.030, -0.035, 0.012))
            @ Matrix.Rotation(side*0.35, 4, 'Z')
            @ Matrix.Scale(0.022, 4, (1,0,0))
            @ Matrix.Scale(0.115, 4, (0,1,0))
            @ Matrix.Scale(0.020, 4, (0,0,1)))
    # pivot boss
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.014, depth=0.026,
        matrix=Matrix.Translation((0, 0.030, 0.012)))
    # plier jaws
    for side in [-1, 1]:
        jaw_levels = [(0, 0.010), (0.030, 0.007), (0.055, 0.003)]
        rings = []
        for d, r in jaw_levels:
            ring = [bm.verts.new((side*0.006 + math.cos(i*TAU/4)*r,
                                   0.045 + d,
                                   0.012 + math.sin(i*TAU/4)*r))
                    for i in range(4)]
            rings.append(ring)
        for ri in range(len(rings)-1):
            lo, hi = rings[ri], rings[ri+1]
            for i in range(4):
                bm.faces.new([lo[i], lo[(i+1)%4], hi[(i+1)%4], hi[i]])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_Multitool_A")
    return obj
'''))

ASSETS.append(("tools", "Tools", "sm_tool_dome_beacon", "SM_Tool_DomeBeacon_A", '''
def build():
    """Deployable dome beacon — squat ribbed dome with caged lamp on top.
    Matches the domed device in the toolkit sheet; alt beacon style."""
    obj, bm = new_mesh("SM_Tool_DomeBeacon_A")
    # dome body (hemisphere)
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.12,
        matrix=Matrix.Translation((0, 0, 0.04)))
    for v in result['verts']:
        if v.co.z < 0.04:
            v.co.z = 0.04
    # base skirt
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=12,
        radius=0.135, depth=0.045,
        matrix=Matrix.Translation((0, 0, 0.0225)))
    # rib bands over dome
    for band_a in [0, TAU/4]:
        SEGS = 8
        for s in range(SEGS + 1):
            t = s / SEGS
            arc = -PI/2 + t * PI
            rx = math.cos(arc) * 0.125
            rz = 0.045 + math.sin(arc) * 0.115 + 0.115
            if rz < 0.045:
                continue
            bmesh.ops.create_cube(bm, size=0.018,
                matrix=Matrix.Translation((math.cos(band_a)*rx,
                                            math.sin(band_a)*rx, rz)))
    # caged lamp on top
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.030, depth=0.045,
        matrix=Matrix.Translation((0, 0, 0.185)))
    for i in range(4):
        a = i * TAU / 4
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=4,
            radius=0.004, depth=0.05,
            matrix=Matrix.Translation((math.cos(a)*0.032,
                                        math.sin(a)*0.032, 0.185)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Tool_DomeBeacon_A")
    return obj
'''))

# ====================================================================
# LATER REGIONS — LT-001 ash cathedral
# ====================================================================

ASSETS.append(("later_regions", "LaterRegions", "sm_later_cathedral_column",
               "SM_Later_CathedralColumn_A", '''
def build():
    """Ash cathedral column — eroded natural gothic column 45m tall that
    flares into pointed-arch buttresses at the top. Concept: LT-001."""
    random.seed(401)
    obj, bm = new_mesh("SM_Later_CathedralColumn_A")
    SEGS = 10
    H = 45.0
    # main shaft with entasis (slight swell) and erosion jitter
    stations = [(0, 3.2), (5, 2.9), (15, 2.5), (28, 2.3), (38, 2.6), (45, 3.4)]
    rings = []
    for z, r in stations:
        ring = [bm.verts.new((math.cos(i*TAU/SEGS)*r*random.uniform(0.92, 1.08),
                               math.sin(i*TAU/SEGS)*r*random.uniform(0.92, 1.08),
                               z + random.uniform(-0.4, 0.4)))
                for i in range(SEGS)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i+1)%SEGS], hi[(i+1)%SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # 4 arch buttresses flaring from the crown (pointed-arch ribs)
    for i in range(4):
        a = i * TAU / 4
        ARC_SEGS = 7
        for s in range(ARC_SEGS):
            t = s / (ARC_SEGS - 1)
            # quarter arch sweeping out and down from crown
            reach = math.sin(t * PI / 2) * 9.0
            drop = (1 - math.cos(t * PI / 2)) * 12.0
            px = math.cos(a) * (3.0 + reach)
            py = math.sin(a) * (3.0 + reach)
            pz = 44.0 - drop
            r = 1.1 * (1 - t * 0.5)
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r,
                matrix=Matrix.Translation((px, py, pz)))
    # vertical erosion flutes
    for i in range(5):
        a = i * TAU / 5 + 0.3
        for z in range(4, 40, 5):
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((math.cos(a)*2.55, math.sin(a)*2.55, z))
                @ Matrix.Rotation(a, 4, 'Z')
                @ Matrix.Scale(0.25, 4, (1,0,0))
                @ Matrix.Scale(0.5, 4, (0,1,0))
                @ Matrix.Scale(3.5, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_pearl_stone", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Later_CathedralColumn_A")
    return obj
'''))

ASSETS.append(("later_regions", "LaterRegions", "sm_later_buried_machine_slab",
               "SM_Later_BuriedMachineSlab_A", '''
def build():
    """Half-buried angular machine wreck — tilted slab emerging from ash,
    cyan edge-light strip along one face. Concept: LT-001 foreground."""
    random.seed(402)
    obj, bm = new_mesh("SM_Later_BuriedMachineSlab_A")
    # main tilted slab
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.9))
        @ Matrix.Rotation(0.35, 4, 'Y')
        @ Matrix.Rotation(0.12, 4, 'X')
        @ Matrix.Scale(6.5, 4, (1,0,0))
        @ Matrix.Scale(3.0, 4, (0,1,0))
        @ Matrix.Scale(0.8, 4, (0,0,1)))
    # second smaller slab leaning on it
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((3.2, 1.2, 0.5))
        @ Matrix.Rotation(-0.5, 4, 'Y')
        @ Matrix.Rotation(0.3, 4, 'Z')
        @ Matrix.Scale(3.0, 4, (1,0,0))
        @ Matrix.Scale(1.8, 4, (0,1,0))
        @ Matrix.Scale(0.5, 4, (0,0,1)))
    # cyan edge-light strip along the exposed long edge
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((-0.5, -1.45, 1.85))
        @ Matrix.Rotation(0.35, 4, 'Y')
        @ Matrix.Scale(5.8, 4, (1,0,0))
        @ Matrix.Scale(0.08, 4, (0,1,0))
        @ Matrix.Scale(0.08, 4, (0,0,1)))
    # panel seams
    for sx in [-2.0, 0.0, 2.0]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((sx, 0, 1.45 + sx * 0.35))
            @ Matrix.Rotation(0.35, 4, 'Y')
            @ Matrix.Scale(0.06, 4, (1,0,0))
            @ Matrix.Scale(3.05, 4, (0,1,0))
            @ Matrix.Scale(0.06, 4, (0,0,1)))
    # ash drift piled against the base
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=2.4,
        matrix=Matrix.Translation((-2.0, 0.5, 0)))
    for v in result['verts']:
        if v.co.z > 0:
            v.co.z *= 0.25
        else:
            v.co.z = 0
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_pearl_stone"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Later_BuriedMachineSlab_A")
    return obj
'''))

ASSETS.append(("later_regions", "LaterRegions", "sm_later_ash_dune",
               "SM_Later_AshDune_A", '''
def build():
    """Soft ash dune — 12m wind-formed mound with crest ridge, used to bury
    the cathedral floor. Concept: LT-001 ground plane."""
    random.seed(403)
    obj, bm = new_mesh("SM_Later_AshDune_A")
    # dune: stretched, flattened icosphere with leeward steepening
    result = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=6.0,
        matrix=Matrix.Translation((0, 0, 0)))
    for v in result['verts']:
        v.co.y *= 1.6
        if v.co.z < 0:
            v.co.z = 0
        else:
            v.co.z *= 0.30
            # windward side (x<0) gentle, leeward steeper
            if v.co.x > 0:
                v.co.x *= 0.72
        v.co.z += random.uniform(-0.04, 0.04)
    # crest ripple bumps
    for i in range(6):
        t = i / 5
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.5,
            matrix=Matrix.Translation((random.uniform(-0.5, 0.5),
                                        -7 + t * 14,
                                        1.55 + random.uniform(-0.15, 0.15))))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_pearl_stone"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Later_AshDune_A")
    return obj
'''))

# ====================================================================
# LUMINOUS RIFT — bridge/platform kit additions
# ====================================================================

ASSETS.append(("luminous_rift_machines", "LuminousRift", "sm_hanging_platform",
               "SM_Rift_HangingPlatform_A", '''
def build():
    """Chain-suspended platform — 8m deck hanging from 4 chain runs with
    anchor ring above. Concept: ancient_bridge_platform_kit."""
    random.seed(420)
    obj, bm = new_mesh("SM_Rift_HangingPlatform_A")
    # deck (octagonal slab)
    R, T = 4.0, 0.5
    lo = [bm.verts.new((math.cos(i*TAU/8)*R, math.sin(i*TAU/8)*R, 0))
          for i in range(8)]
    hi = [bm.verts.new((math.cos(i*TAU/8)*R, math.sin(i*TAU/8)*R, T))
          for i in range(8)]
    for i in range(8):
        ni = (i + 1) % 8
        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(lo)))
    bm.faces.new(hi)
    # circular inset detail on deck
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=16,
        radius=2.2, depth=0.06,
        matrix=Matrix.Translation((0, 0, T + 0.02)))
    # 4 chain runs to anchor ring (chain = stacks of small tori approximated
    # by alternating-rotation rings of spheres)
    CHAIN_H = 6.0
    for i in range(4):
        a = i * TAU / 4 + TAU / 8
        bx, by = math.cos(a) * R * 0.8, math.sin(a) * R * 0.8
        LINKS = 9
        for l in range(LINKS):
            t = (l + 0.5) / LINKS
            cx = bx * (1 - t * 0.85)
            cy = by * (1 - t * 0.85)
            cz = T + t * CHAIN_H
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.13,
                matrix=Matrix.Translation((cx, cy, cz)))
    # anchor ring at top
    SEGS = 12
    for s in range(SEGS):
        a = s * TAU / SEGS
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.18,
            matrix=Matrix.Translation((math.cos(a)*0.8, math.sin(a)*0.8,
                                        T + CHAIN_H + 0.3)))
    # corner anchor lugs on deck
    for i in range(4):
        a = i * TAU / 4 + TAU / 8
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
            radius=0.18, depth=0.35,
            matrix=Matrix.Translation((math.cos(a)*R*0.8,
                                        math.sin(a)*R*0.8, T + 0.17)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_HangingPlatform_A")
    return obj
'''))

ASSETS.append(("luminous_rift_machines", "LuminousRift", "sm_rope_railing",
               "SM_Rift_RopeRailing_A", '''
def build():
    """Expedition rope railing strung between ancient posts — 4m modular run,
    2 posts, 2 sagging rope spans. Concept: bridge kit foreground railings."""
    obj, bm = new_mesh("SM_Rift_RopeRailing_A")
    L = 4.0
    # 2 posts
    for px in [-L/2, L/2]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=7,
            radius=0.07, depth=1.1,
            matrix=Matrix.Translation((px, 0, 0.55)))
        # post cap
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.085,
            matrix=Matrix.Translation((px, 0, 1.12)))
    # 2 sagging rope spans (catenary approximated by sphere chains)
    for rope_z in [0.55, 1.0]:
        SEGS = 11
        for s in range(SEGS):
            t = (s + 0.5) / SEGS
            x = -L/2 + t * L
            sag = math.sin(t * PI) * 0.12
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035,
                matrix=Matrix.Translation((x, 0, rope_z - sag)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_ancient_machine_dark"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_RopeRailing_A")
    return obj
'''))

ASSETS.append(("luminous_rift_machines", "LuminousRift", "sm_stair_ramp",
               "SM_Rift_StairRamp_A", '''
def build():
    """Ancient stepped ramp — 8 broad stone-machine steps climbing 3m over
    8m, linking platform tiers. Concept: bridge kit connectors."""
    random.seed(421)
    obj, bm = new_mesh("SM_Rift_StairRamp_A")
    STEPS = 8
    W = 3.5
    RUN, RISE = 1.0, 0.375
    for s in range(STEPS):
        y = s * RUN
        z = s * RISE
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, y + RUN/2, z + RISE/2))
            @ Matrix.Scale(W, 4, (1,0,0))
            @ Matrix.Scale(RUN + 0.08, 4, (0,1,0))
            @ Matrix.Scale(RISE, 4, (0,0,1)))
        # worn edge chamfer detail (thin strip on nose)
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, y + 0.04, z + RISE - 0.03))
            @ Matrix.Scale(W*0.98, 4, (1,0,0))
            @ Matrix.Scale(0.10, 4, (0,1,0))
            @ Matrix.Scale(0.05, 4, (0,0,1)))
    # side stringer walls
    for side in [-1, 1]:
        for s in range(STEPS):
            y = s * RUN
            z = s * RISE
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((side*(W/2 + 0.12), y + RUN/2, z*0.5 + RISE))
                @ Matrix.Scale(0.24, 4, (1,0,0))
                @ Matrix.Scale(RUN, 4, (0,1,0))
                @ Matrix.Scale(z + RISE*2, 4, (0,0,1)))
    # blue guide strip up the centre
    for s in range(STEPS):
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((0, s*RUN + RUN/2, s*RISE + RISE + 0.005))
            @ Matrix.Scale(0.15, 4, (1,0,0))
            @ Matrix.Scale(RUN*0.8, 4, (0,1,0))
            @ Matrix.Scale(0.01, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_StairRamp_A")
    return obj
'''))


# ────────────────────────────────────────────────────────────────────
def main():
    for folder, export_sub, stem, sm_name, body in ASSETS:
        parts = folder.split("/")
        depth = len(parts)
        target = os.path.join(SCRIPTS_DIR, *parts)
        os.makedirs(target, exist_ok=True)
        for i in range(1, len(parts) + 1):
            init = os.path.join(SCRIPTS_DIR, *parts[:i], "__init__.py")
            if not os.path.exists(init):
                open(init, "w").close()
        path = os.path.join(target, stem + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(header(sm_name, depth, export_sub) + body.strip("\n") + footer(sm_name))
        print(f"  + {folder}/{stem}.py  ({sm_name})")


if __name__ == "__main__":
    print("=== Concept-grounded expansion 2 ===")
    main()
    print("=== DONE — now regen run_alls ===")
