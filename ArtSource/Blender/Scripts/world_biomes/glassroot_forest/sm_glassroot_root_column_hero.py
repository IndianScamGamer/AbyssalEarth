"""
SM_Glassroot_RootColumn_Hero — AbyssalEarth procedural mesh.
Concept: GR-001, GR-002

GR-001 shows massive translucent root columns (50-80 m tall, 4-10 m diameter at base)
with dramatic sweeping buttress-root fins that curve from the trunk body all the way to the
ground, spreading 12-16 m outward — the defining visual of the Glassroot Forest biome.
Red mineral sap veins run vertically along the trunk surface. Teal crystal deposits
cluster at the base where buttress roots contact stone.

Run standalone:  blender --background --python <this_file>.py
"""
import sys
import os
import math
import random
import bpy
import bmesh
from mathutils import Matrix, Vector

_HERE         = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, TAU, PI)

EXPORT_DIR = get_export_dir('GlassrootForest')

# ── scale constants ──────────────────────────────────────────────────
TRUNK_HEIGHT   = 70.0    # full visible height (m)
TRUNK_SIDES    = 20      # polygon count — smoother than original 12
TRUNK_R_BASE   =  3.8    # radius at ground
TRUNK_R_MID    =  2.7    # radius at z=20m
TRUNK_R_UPPER  =  1.4    # radius at z=45m
TRUNK_R_TOP    =  0.45   # radius at z=70m
N_BUTTRESS     =  5      # sweeping fin buttress roots
BUTTRESS_REACH = 14.5    # horizontal spread from trunk centre (m)
BUTTRESS_SEGS  =  9      # cross-section rings along buttress sweep path
N_VEIN_RIDGES  =  5      # red sap vertical ridges on trunk surface
VEIN_W         =  0.09   # width of each vein ridge (m)
VEIN_PROUD     =  0.07   # how far ridge stands proud of surface (m)
N_CRYSTAL_BASE =  3      # small crystal accents at buttress feet


rng = random.Random(77)


def _lerp(a, b, t):
    return a + (b - a) * t


def _trunk_radius(z):
    """Smooth interpolation of trunk radius by height."""
    levels = [
        (0.0,           TRUNK_R_BASE),
        (TRUNK_HEIGHT * 0.1, TRUNK_R_BASE * 0.92),
        (TRUNK_HEIGHT * 0.28, TRUNK_R_MID),
        (TRUNK_HEIGHT * 0.55, _lerp(TRUNK_R_MID, TRUNK_R_UPPER, 0.5)),
        (TRUNK_HEIGHT * 0.65, TRUNK_R_UPPER),
        (TRUNK_HEIGHT * 0.82, _lerp(TRUNK_R_UPPER, TRUNK_R_TOP, 0.5)),
        (TRUNK_HEIGHT,         TRUNK_R_TOP),
    ]
    for i in range(len(levels) - 1):
        z0, r0 = levels[i]
        z1, r1 = levels[i + 1]
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return r0 + (r1 - r0) * t
    return TRUNK_R_TOP


def build_trunk(bm):
    """20-sided lofted column with organic noise."""
    N_Z = 12
    zlevels = [TRUNK_HEIGHT * i / (N_Z - 1) for i in range(N_Z)]
    rings = []
    for z in zlevels:
        r = _trunk_radius(z)
        ring = [
            bm.verts.new((
                math.cos(i * TAU / TRUNK_SIDES) * r * (1 + rng.uniform(-0.035, 0.035)),
                math.sin(i * TAU / TRUNK_SIDES) * r * (1 + rng.uniform(-0.035, 0.035)),
                z,
            ))
            for i in range(TRUNK_SIDES)
        ]
        rings.append(ring)

    for ri in range(len(rings) - 1):
        lo, hi = rings[ri], rings[ri + 1]
        for i in range(TRUNK_SIDES):
            ni = (i + 1) % TRUNK_SIDES
            try:
                bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
            except Exception:
                pass

    # Close top
    cx_top = sum(v.co.x for v in rings[-1]) / TRUNK_SIDES
    cy_top = sum(v.co.y for v in rings[-1]) / TRUNK_SIDES
    top_c  = bm.verts.new((cx_top, cy_top, TRUNK_HEIGHT))
    for i in range(TRUNK_SIDES):
        ni = (i + 1) % TRUNK_SIDES
        try:
            bm.faces.new([rings[-1][i], rings[-1][ni], top_c])
        except Exception:
            pass


def build_buttress_root(bm, root_idx):
    """
    One sweeping buttress-root fin. The fin curves from mid-trunk (z≈20m) down
    to the ground and outward to BUTTRESS_REACH. The cross-section is a teardrop/
    fin profile (narrow at the top, wide and flat where it meets stone).
    """
    angle = root_idx * TAU / N_BUTTRESS

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    # Path: BUTTRESS_SEGS points from (trunk attachment) to (ground foot)
    # Each path point has (x, y, z, local_width, local_height)
    def _path_pt(seg):
        t = seg / (BUTTRESS_SEGS - 1)
        # Ease-in curve: starts steeply vertical, flattens out at ground
        ease = math.sin(t * PI / 2)     # 0→1 with fast start, slow end
        reach_t = ease * BUTTRESS_REACH + _trunk_radius(TRUNK_HEIGHT * 0.28)
        # z descends from trunk attach height to 0
        z = TRUNK_HEIGHT * 0.28 * (1 - t) ** 1.5
        w = _lerp(0.4, 3.2, ease)       # fin narrows at top, fans at base
        h = _lerp(2.6, 0.18, ease)      # fin tall at top, flat at base
        x = cos_a * reach_t
        y = sin_a * reach_t
        return x, y, z, w, h

    path = [_path_pt(s) for s in range(BUTTRESS_SEGS)]

    PROFILE_SEGS = 6   # verts across the fin cross-section
    all_rings = []

    for (px, py, pz, pw, ph) in path:
        # Local fin axes: thick in Z, wide in the tangential direction
        ring = []
        for p in range(PROFILE_SEGS):
            tp   = p / (PROFILE_SEGS - 1) - 0.5   # -0.5 to 0.5
            side = tp * pw   # tangential offset
            # Teardrop profile: leading edge (outer) = thick, trailing (inner) = thin
            dz_offset = ph * (1 - (2 * abs(tp)) ** 1.4) * 0.5
            fx = px - sin_a * side
            fy = py + cos_a * side
            fz = pz + dz_offset
            ring.append(bm.verts.new((fx, fy, fz)))
        all_rings.append(ring)

    # Loft the rings
    for ri in range(len(all_rings) - 1):
        lo, hi = all_rings[ri], all_rings[ri + 1]
        for i in range(PROFILE_SEGS - 1):
            try:
                bm.faces.new([lo[i], lo[i + 1], hi[i + 1], hi[i]])
            except Exception:
                pass

    # Cap top of fin
    try:
        bm.faces.new(all_rings[0])
    except Exception:
        pass
    # Cap ground foot (wide base pad)
    try:
        bm.faces.new(list(reversed(all_rings[-1])))
    except Exception:
        pass

    return angle  # return angle so crystal accents know where to go


def build_vein_ridge(bm, vein_idx):
    """Thin vertical raised strip on the trunk surface (red sap vein)."""
    angle   = vein_idx * TAU / N_VEIN_RIDGES + 0.15   # slight offset from buttress angles
    N_Z_PTS = 20
    prev_row = None
    for zi in range(N_Z_PTS):
        t   = zi / (N_Z_PTS - 1)
        z   = t * TRUNK_HEIGHT * 0.88    # veins don't quite reach the tip
        r   = _trunk_radius(z)
        r_o = r + VEIN_PROUD
        # 2-vert wide ridge at this z
        l_angle = angle - VEIN_W / (r_o + 0.01)
        r_angle = angle + VEIN_W / (r_o + 0.01)
        vL = bm.verts.new((math.cos(l_angle) * r_o, math.sin(l_angle) * r_o, z))
        vR = bm.verts.new((math.cos(r_angle) * r_o, math.sin(r_angle) * r_o, z))
        row = (vL, vR)
        if prev_row is not None:
            pL, pR = prev_row
            try:
                bm.faces.new([pL, pR, vR, vL])
            except Exception:
                pass
        prev_row = row


def build_crystal_accents(bm, buttress_angles):
    """Small crystal spires at the foot of each buttress root."""
    for angle in buttress_angles:
        foot_x = math.cos(angle) * (BUTTRESS_REACH + 1.0)
        foot_y = math.sin(angle) * (BUTTRESS_REACH + 1.0)
        for ci in range(N_CRYSTAL_BASE):
            spread = rng.uniform(0.8, 2.5)
            off_a  = angle + rng.uniform(-0.4, 0.4)
            cx     = foot_x + math.cos(off_a) * spread
            cy     = foot_y + math.sin(off_a) * spread
            height = rng.uniform(0.6, 1.8)
            base_r = rng.uniform(0.10, 0.22)
            SEGS   = 6
            rings  = []
            for zi in range(4):
                zt   = zi / 3.0
                zpos = height * zt
                zr   = base_r * (1 - zt ** 1.5)
                rings.append([
                    bm.verts.new((
                        cx + math.cos(j * TAU / SEGS) * zr,
                        cy + math.sin(j * TAU / SEGS) * zr,
                        zpos,
                    ))
                    for j in range(SEGS)
                ])
            for ri in range(len(rings) - 1):
                lo, hi = rings[ri], rings[ri + 1]
                for i in range(SEGS):
                    ni = (i + 1) % SEGS
                    try:
                        bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
                    except Exception:
                        pass
            try:
                bm.faces.new(list(reversed(rings[0])))
            except Exception:
                pass


def build():
    print("Building SM_Glassroot_RootColumn_Hero …")
    obj, bm = new_mesh("SM_Glassroot_RootColumn_Hero")

    build_trunk(bm)
    buttress_angles = [build_buttress_root(bm, i) for i in range(N_BUTTRESS)]
    for i in range(N_VEIN_RIDGES):
        build_vein_ridge(bm, i)
    build_crystal_accents(bm, buttress_angles)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, [
        "mat_glassroot_translucent",
        "mat_red_sap",
        "mat_pearl_stone",
        "mat_crystal_blue",
    ])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootColumn_Hero")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Glassroot_RootColumn_Hero")
