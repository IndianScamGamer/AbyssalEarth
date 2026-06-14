"""
SM_Creature_* pack — AbyssalEarth procedural meshes.
The five creature designs from rift_creature_silhouettes_concept.png,
left to right: CrystalProwler, StiltDancer, VeilDrifter, ArmoredGrazer,
SpindleWalker.

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

EXPORT_DIR = get_export_dir('Characters')


def _chain(bm, pts, radii, segs=6):
    """Loft a tube through a list of points with per-point radii."""
    prev = None
    for (px, py, pz), r in zip(pts, radii):
        ring = [bm.verts.new((px + math.cos(i * TAU / segs) * r,
                               py + math.sin(i * TAU / segs) * r,
                               pz)) for i in range(segs)]
        if prev:
            for i in range(segs):
                bm.faces.new([prev[i], prev[(i + 1) % segs],
                               ring[(i + 1) % segs], ring[i]])
        prev = ring
    return prev


def build_crystal_prowler():
    """Low crystal-backed quadruped — crocodilian stance, glowing spine
    crystals, dragging tail. Concept silhouette 1 (far left)."""
    random.seed(801)
    obj, bm = new_mesh("SM_Creature_CrystalProwler_A")
    # body: low-slung lofted torso, nose to tail along +y
    spine_pts = [(0, -1.5, 0.50), (0, -1.0, 0.62), (0, -0.3, 0.72),
                 (0, 0.4, 0.70), (0, 1.0, 0.58), (0, 1.7, 0.42),
                 (0, 2.5, 0.28), (0, 3.2, 0.16)]
    radii = [0.18, 0.34, 0.44, 0.46, 0.38, 0.22, 0.12, 0.05]
    body = []
    for (px, py, pz), r in zip(spine_pts, radii):
        ring = []
        for i in range(8):
            a = i * TAU / 8
            # wide, low cross-section
            ring.append(bm.verts.new((px + math.cos(a) * r * 1.35,
                                       py,
                                       pz + math.sin(a) * r)))
        body.append(ring)
    for ri in range(len(body) - 1):
        lo, hi = body[ri], body[ri + 1]
        for i in range(8):
            bm.faces.new([lo[i], lo[(i + 1) % 8], hi[(i + 1) % 8], hi[i]])
    bm.faces.new(list(reversed(body[0])))
    bm.faces.new(body[-1])
    # head: wedge snout with brow ridges
    _chain(bm, [(0, -1.5, 0.50), (0, -1.95, 0.44), (0, -2.35, 0.36)],
           [0.30, 0.22, 0.08])
    for side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.07,
            matrix=Matrix.Translation((side * 0.20, -1.75, 0.62)))
    # crystal ridge down the back: angular shards, biggest mid-back
    for k in range(9):
        t = k / 8
        cy = -1.1 + t * 3.4
        ch = (0.55 - abs(t - 0.4) * 0.7) * random.uniform(0.8, 1.2)
        if ch < 0.12:
            continue
        cw = ch * 0.30
        base_z = 0.72 + (0.46 - abs(t - 0.4) * 0.5) * 0.6
        tip = bm.verts.new((random.uniform(-0.06, 0.06), cy,
                             base_z + ch))
        ring = [bm.verts.new((math.cos(i * TAU / 4) * cw,
                               cy + math.sin(i * TAU / 4) * cw,
                               base_z)) for i in range(4)]
        for i in range(4):
            bm.faces.new([ring[i], ring[(i + 1) % 4], tip])
    # 4 stocky splayed legs with claw toes
    for sy in [-0.7, 0.9]:
        for side in [-1, 1]:
            hip = (side * 0.55, sy, 0.55)
            knee = (side * 0.95, sy + 0.1, 0.35)
            foot = (side * 1.05, sy + 0.15, 0.06)
            _chain(bm, [hip, knee, foot], [0.16, 0.12, 0.10], segs=6)
            for c in range(3):
                ca = (c - 1) * 0.5
                bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=4,
                    radius1=0.025, radius2=0.025, depth=0.18,
                    matrix=Matrix.Translation((side * (1.05 + 0.10),
                                                sy + 0.15 + ca * 0.1, 0.04))
                    @ Matrix.Rotation(side * (0.9 + ca * 0.3), 4, 'Y'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Creature_CrystalProwler_A")
    return obj


def build_stilt_dancer():
    """Tall vertical dancer — narrow segmented body held 2.5m up on
    backward-kneed legs, twin whip antennae. Concept silhouette 2."""
    random.seed(802)
    obj, bm = new_mesh("SM_Creature_StiltDancer_A")
    # vertical body: stacked tapering segments
    _chain(bm, [(0, 0, 1.6), (0, 0, 2.0), (0.05, 0, 2.45),
                (0.02, 0, 2.9), (0, 0, 3.3)],
           [0.14, 0.22, 0.26, 0.20, 0.12], segs=7)
    # head knot
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.16,
        matrix=Matrix.Translation((0, 0, 3.45)))
    # twin whip antennae: long arcs of shrinking beads
    for side in [-1, 1]:
        SEG = 16
        for s in range(SEG):
            t = s / (SEG - 1)
            ax = side * (0.1 + math.sin(t * PI * 0.8) * 1.3)
            az = 3.55 + t * 1.4 - t * t * 0.5
            ay = -t * 0.6 * side * 0.3
            bmesh.ops.create_icosphere(bm, subdivisions=1,
                radius=0.045 * (1 - t * 0.8) + 0.008,
                matrix=Matrix.Translation((ax, ay, az)))
    # arm pair: thin, held folded like a mantis
    for side in [-1, 1]:
        _chain(bm, [(side * 0.22, 0, 2.75), (side * 0.55, -0.3, 2.45),
                    (side * 0.35, -0.65, 2.75)],
               [0.06, 0.045, 0.02], segs=5)
    # legs: 2 backward-kneed stilts with wide hip flare
    for side in [-1, 1]:
        hip = (side * 0.20, 0, 1.55)
        knee = (side * 0.45, 0.55, 0.95)     # knee bends backward (+y)
        shin = (side * 0.35, -0.15, 0.35)
        foot = (side * 0.35, -0.35, 0.04)
        _chain(bm, [hip, knee, shin, foot], [0.10, 0.075, 0.05, 0.04], segs=5)
        # splayed two-toe foot
        for ta in [-0.45, 0.45]:
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=4,
                radius1=0.022, radius2=0.022, depth=0.22,
                matrix=Matrix.Translation((side * 0.35 + math.sin(ta) * 0.1,
                                            -0.42, 0.03))
                @ Matrix.Rotation(ta, 4, 'Z')
                @ Matrix.Rotation(TAU / 4 - 0.2, 4, 'X'))
    # segment collar fringes on the body
    for cz in [1.9, 2.3, 2.7]:
        bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False, segments=8,
            radius1=0.30, radius2=0.30, depth=0.04,
            matrix=Matrix.Translation((0.02, 0, cz)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_water_bioluminescent",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Creature_StiltDancer_A")
    return obj


def build_veil_drifter():
    """Floating veil creature — huge ragged membrane sail above a knotted
    body core with long trailing tendrils. Concept silhouette 3 (centre).
    Membrane uses two-sided material; animate with cloth/shader in-engine."""
    random.seed(803)
    obj, bm = new_mesh("SM_Creature_VeilDrifter_A")
    # body core: knotted mass at sail root
    for k in range(5):
        bmesh.ops.create_icosphere(bm, subdivisions=1,
            radius=random.uniform(0.12, 0.22),
            matrix=Matrix.Translation((random.uniform(-0.15, 0.15),
                                        random.uniform(-0.1, 0.1),
                                        2.0 + random.uniform(-0.15, 0.15))))
    # membrane sail: fan of triangular panels sweeping up-right, ragged edge
    APEX = (0.0, 0.0, 2.1)
    N_PANELS = 9
    for p in range(N_PANELS):
        a0 = -0.35 + p * 0.22
        a1 = a0 + 0.22
        r0 = 2.4 * random.uniform(0.8, 1.15)
        r1 = 2.4 * random.uniform(0.8, 1.15)
        # sail sweeps up and to one side
        v_apex = bm.verts.new(APEX)
        v0 = bm.verts.new((math.sin(a0) * r0 * 0.8,
                            math.cos(a0) * 0.3 - 0.15,
                            2.1 + math.cos(a0 * 0.8) * r0 * 0.75))
        v1 = bm.verts.new((math.sin(a1) * r1 * 0.8,
                            math.cos(a1) * 0.3 - 0.15,
                            2.1 + math.cos(a1 * 0.8) * r1 * 0.75))
        bm.faces.new([v_apex, v0, v1])
        # ragged fringe streamer off each panel edge
        if p % 2 == 0:
            fx = math.sin(a1) * r1 * 0.8
            fz = 2.1 + math.cos(a1 * 0.8) * r1 * 0.75
            for s in range(4):
                st = s / 3
                bmesh.ops.create_icosphere(bm, subdivisions=1,
                    radius=0.03 * (1 - st * 0.7),
                    matrix=Matrix.Translation((fx + st * 0.3,
                                                -0.15 - st * 0.2,
                                                fz - st * 0.7)))
    # rib veins through the sail: thin bead arcs from apex
    for rv in range(4):
        a = -0.25 + rv * 0.5
        SEG = 7
        for s in range(1, SEG):
            t = s / (SEG - 1)
            r = 2.2 * t
            bmesh.ops.create_icosphere(bm, subdivisions=1,
                radius=0.035 * (1 - t * 0.6),
                matrix=Matrix.Translation((math.sin(a) * r * 0.8,
                                            math.cos(a) * 0.3 - 0.15,
                                            2.1 + math.cos(a * 0.8) * r * 0.75)))
    # trailing tendrils: 6 long droops below the core to the ground
    for td in range(6):
        ta = td * TAU / 6 + 0.3
        tx0 = math.cos(ta) * 0.18
        ty0 = math.sin(ta) * 0.18
        drop = random.uniform(1.4, 2.0)
        SEG = 10
        for s in range(SEG):
            t = s / (SEG - 1)
            sway = math.sin(t * PI * 1.5 + td) * 0.18
            bmesh.ops.create_icosphere(bm, subdivisions=1,
                radius=0.035 * (1 - t * 0.75) + 0.006,
                matrix=Matrix.Translation((tx0 + sway,
                                            ty0 + sway * 0.5,
                                            1.95 - t * drop)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_water_bioluminescent", "mat_purple_emissive",
                        "mat_collector_glass"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Creature_VeilDrifter_A")
    return obj


def build_armored_grazer():
    """Massive armored grazer — domed shell of layered plates over a heavy
    body, tusked feet, head low to the ground. Concept silhouette 4."""
    random.seed(804)
    obj, bm = new_mesh("SM_Creature_ArmoredGrazer_A")
    # body dome: flattened icosphere
    dome = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.3,
        matrix=Matrix.Translation((0, 0, 1.15)))
    for v in dome['verts']:
        v.co.y *= 1.25
        if v.co.z < 1.15:
            v.co.z = 1.15 - (1.15 - v.co.z) * 0.55
    # layered shell plates: overlapping arc rows down the dome
    for row in range(4):
        rz = 2.15 - row * 0.30
        rr = 0.55 + row * 0.28
        N = 5 + row * 2
        for k in range(N):
            a = (k + 0.5) * PI / N - PI / 2     # front-facing arc
            px = math.sin(a) * rr
            py = math.cos(a) * rr * 1.25 - 0.1
            plate = bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((px, py, rz))
                @ Matrix.Rotation(a, 4, 'Z')
                @ Matrix.Rotation(0.35 + row * 0.18, 4, 'X')
                @ Matrix.Scale(0.42, 4, (1, 0, 0))
                @ Matrix.Scale(0.34, 4, (0, 1, 0))
                @ Matrix.Scale(0.07, 4, (0, 0, 1)))
    # head: low wedge with twin nose tusks
    _chain(bm, [(0, -1.7, 0.65), (0, -2.15, 0.50), (0, -2.5, 0.40)],
           [0.42, 0.34, 0.18], segs=7)
    for side in [-1, 1]:
        # curved tusk: bead arc
        for s in range(5):
            t = s / 4
            bmesh.ops.create_icosphere(bm, subdivisions=1,
                radius=0.06 * (1 - t * 0.6),
                matrix=Matrix.Translation((side * (0.22 + t * 0.15),
                                            -2.45 - t * 0.25,
                                            0.35 - t * 0.18 + t * t * 0.3)))
    # 4 pillar legs with claw tusks at the feet
    for sy in [-0.9, 0.95]:
        for side in [-1, 1]:
            _chain(bm, [(side * 0.85, sy, 0.9), (side * 0.95, sy, 0.4),
                        (side * 0.95, sy, 0.05)],
                   [0.30, 0.26, 0.28], segs=7)
            for c in range(3):
                ca = (c - 1) * 0.45
                bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=4,
                    radius1=0.05, radius2=0.05, depth=0.28,
                    matrix=Matrix.Translation((side * 1.05,
                                                sy - 0.18 + ca * 0.2, 0.07))
                    @ Matrix.Rotation(ca, 4, 'Z')
                    @ Matrix.Rotation(1.1, 4, 'X'))
    # dragging armored tail
    _chain(bm, [(0, 1.9, 0.75), (0, 2.5, 0.45), (0, 3.0, 0.20)],
           [0.30, 0.18, 0.07], segs=6)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_fossil_bone", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Creature_ArmoredGrazer_A")
    return obj


def build_spindle_walker():
    """Spindle walker — extreme 4.5m vertical: tripod stilt legs, narrow
    thorax, antler-crown head. Concept silhouette 5 (far right)."""
    random.seed(805)
    obj, bm = new_mesh("SM_Creature_SpindleWalker_A")
    HIP_Z = 2.6
    # 3 stilt legs in tripod arrangement, each with a mid-knee
    for li in range(3):
        la = li * TAU / 3 + TAU / 12
        hip = (math.cos(la) * 0.18, math.sin(la) * 0.18, HIP_Z)
        knee = (math.cos(la) * 0.85, math.sin(la) * 0.85, HIP_Z * 0.55)
        foot = (math.cos(la) * 1.15, math.sin(la) * 1.15, 0.04)
        _chain(bm, [hip, knee, foot], [0.07, 0.05, 0.035], segs=5)
        # knee spur
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.07,
            matrix=Matrix.Translation(knee))
        # needle foot tip
        tipring = [bm.verts.new((foot[0] + math.cos(i * TAU / 4) * 0.03,
                                  foot[1] + math.sin(i * TAU / 4) * 0.03,
                                  0.10)) for i in range(4)]
        tip = bm.verts.new((foot[0], foot[1], -0.02))
        for i in range(4):
            bm.faces.new([tipring[i], tipring[(i + 1) % 4], tip])
    # thorax: narrow vertical loft from hips to shoulders
    _chain(bm, [(0, 0, HIP_Z), (0.03, 0, 3.1), (0, 0, 3.6), (0, 0, 4.0)],
           [0.16, 0.20, 0.15, 0.10], segs=6)
    # rib fringe collars
    for cz in [2.85, 3.25]:
        bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False, segments=7,
            radius1=0.24, radius2=0.24, depth=0.035,
            matrix=Matrix.Translation((0.02, 0, cz)))
    # head: small bulb with antler crown
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.13,
        matrix=Matrix.Translation((0, 0, 4.15)))
    # antler crown: branching bead arcs
    for ai in range(4):
        aa = ai * TAU / 4 + TAU / 8
        SEG = 6
        for s in range(SEG):
            t = s / (SEG - 1)
            ax = math.cos(aa) * (0.1 + t * 0.45)
            ay = math.sin(aa) * (0.1 + t * 0.45)
            az = 4.25 + t * 0.45 - t * t * 0.1
            bmesh.ops.create_icosphere(bm, subdivisions=1,
                radius=0.030 * (1 - t * 0.6) + 0.006,
                matrix=Matrix.Translation((ax, ay, az)))
            # fork at mid-antler
            if s == 3:
                bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.02,
                    matrix=Matrix.Translation((ax * 1.15, ay * 1.15,
                                                az + 0.12)))
    # drooping forelimbs (vestigial, hang from shoulders)
    for side in [-1, 1]:
        _chain(bm, [(side * 0.18, 0, 3.55), (side * 0.28, -0.15, 3.0),
                    (side * 0.22, -0.20, 2.5)],
               [0.04, 0.03, 0.015], segs=4)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_water_bioluminescent",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Creature_SpindleWalker_A")
    return obj


def build():
    for fn in (build_crystal_prowler, build_stilt_dancer, build_veil_drifter,
               build_armored_grazer, build_spindle_walker):
        clear_scene()
        fn()


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Creature_* pack (5 creatures)")
