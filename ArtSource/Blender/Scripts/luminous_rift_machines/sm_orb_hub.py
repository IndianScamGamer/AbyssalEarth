"""
SM_Rift_OrbHub_A — AbyssalEarth procedural mesh.
Concept: AD-001, LR-006, LR-007

AD-001 shows the orb hub from below: a massive dark annular ring (≈76 m span) with 8 heavy
rectangular spoke arms radiating from the ring to the central blue-white energy sphere (24 m
diameter). Cable-bundle channels run along each spoke. A circular observation platform with
railing hangs below the hub on 4 cable struts. Gold beam emitter ports punctuate the spokes.

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
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, extrude_region, TAU, PI)

EXPORT_DIR = get_export_dir('LuminousRift')

# ── scale constants ──────────────────────────────────────────────────
OUTER_RING_R   = 38.0    # 76 m total span (within 80-140 m spec)
RING_TUBE_R    =  2.6    # thick cross-section tube
ORB_R          = 12.0    # 24 m diameter (within 18-28 m spec)
N_ARMS         =  8
ARM_W          =  1.8    # spoke arm half-width (rectangular box beam)
ARM_H          =  1.4    # spoke arm height
PLATFORM_R     =  5.5    # observation platform radius
PLATFORM_Z     = -18.0   # hangs below the hub centre
CABLE_STRUT_R  =  0.14   # radius of platform suspension cables
EMITTER_R      =  0.55   # gold beam emitter port radius
EMITTER_DEPTH  =  0.18


def _ring_verts(bm, cx, cy, cz, r, n):
    """Return a list of n verts forming a circle of radius r centred at (cx,cy,cz)."""
    return [bm.verts.new((cx + math.cos(i * TAU / n) * r,
                          cy + math.sin(i * TAU / n) * r,
                          cz))
            for i in range(n)]


def _loft_rings(bm, rings):
    """Connect a list of vert rings with quad faces (same n per ring)."""
    for ri in range(len(rings) - 1):
        lo, hi = rings[ri], rings[ri + 1]
        n = len(lo)
        for i in range(n):
            ni = (i + 1) % n
            try:
                bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
            except Exception:
                pass


def _cap_ring(bm, ring, flip=False):
    """Fill a single ring with a fan of triangular faces from the centroid."""
    cx = sum(v.co.x for v in ring) / len(ring)
    cy = sum(v.co.y for v in ring) / len(ring)
    cz = sum(v.co.z for v in ring) / len(ring)
    centre = bm.verts.new((cx, cy, cz))
    n = len(ring)
    for i in range(n):
        ni = (i + 1) % n
        try:
            if flip:
                bm.faces.new([ring[ni], ring[i], centre])
            else:
                bm.faces.new([ring[i], ring[ni], centre])
        except Exception:
            pass


def build_outer_ring(bm):
    """48-segment torus ring in the XY plane at Z=0."""
    RING_SEGS   = 48   # around the major circle
    TUBE_SEGS   = 12   # around the tube cross-section
    rings = []
    for seg in range(RING_SEGS):
        angle = seg * TAU / RING_SEGS
        cx = math.cos(angle) * OUTER_RING_R
        cy = math.sin(angle) * OUTER_RING_R
        ring = []
        for t in range(TUBE_SEGS):
            ta = t * TAU / TUBE_SEGS
            # radial outward = (cos(angle), sin(angle), 0); up = (0,0,1)
            dx = math.cos(ta) * math.cos(angle)
            dy = math.cos(ta) * math.sin(angle)
            dz = math.sin(ta)
            ring.append(bm.verts.new((
                cx + dx * RING_TUBE_R,
                cy + dy * RING_TUBE_R,
                dz * RING_TUBE_R,
            )))
        rings.append(ring)
    # close the torus (last → first)
    rings.append(rings[0])
    _loft_rings(bm, rings)

    # armour panel extrusions on the outer face every ~22.5°
    PANEL_COUNT = 16
    for p in range(PANEL_COUNT):
        angle = p * TAU / PANEL_COUNT
        cx = math.cos(angle) * (OUTER_RING_R + RING_TUBE_R)
        cy = math.sin(angle) * (OUTER_RING_R + RING_TUBE_R)
        # small rectangular panel proud of the ring surface
        half_w = 1.4
        half_h = 0.6
        panel_verts = []
        for (dz, da) in [(-half_h, -half_w), (-half_h, half_w),
                          ( half_h, half_w),  ( half_h, -half_w)]:
            px = cx + math.cos(angle) * 0.25 + math.sin(angle) * da
            py = cy + math.sin(angle) * 0.25 - math.cos(angle) * da
            panel_verts.append(bm.verts.new((px, py, dz)))
        try:
            bm.faces.new(panel_verts)
        except Exception:
            pass


def build_spoke_arm(bm, arm_idx):
    """Rectangular box-beam arm from inner ring edge to orb collar."""
    angle  = arm_idx * TAU / N_ARMS
    cos_a  = math.cos(angle)
    sin_a  = math.sin(angle)
    # Local axes: along = radial inward; across = tangent; up = Z
    r_start = OUTER_RING_R - RING_TUBE_R - 0.5   # just inside ring inner edge
    r_end   = ORB_R + 1.5                          # just outside orb collar

    # 4-corner cross-section of the box beam
    # corners are ±ARM_W in the tangential direction, ±ARM_H in Z
    def arm_cross(r, frac):
        """4 verts for the box cross-section at radial distance r."""
        taper = 1.0 - frac * 0.28   # slight taper toward centre
        w = ARM_W * taper
        h = ARM_H * taper
        cx_r = cos_a * r
        cy_r = sin_a * r
        return [
            bm.verts.new((cx_r - sin_a * w, cy_r + cos_a * w,  h)),
            bm.verts.new((cx_r + sin_a * w, cy_r - cos_a * w,  h)),
            bm.verts.new((cx_r + sin_a * w, cy_r - cos_a * w, -h)),
            bm.verts.new((cx_r - sin_a * w, cy_r + cos_a * w, -h)),
        ]

    N_SEGS = 14
    radii  = [r_start + (r_end - r_start) * i / (N_SEGS - 1) for i in range(N_SEGS)]
    rings  = [arm_cross(r, i / (N_SEGS - 1)) for i, r in enumerate(radii)]
    _loft_rings(bm, rings)

    # end caps
    try:
        bm.faces.new(list(reversed(rings[0])))
    except Exception:
        pass
    try:
        bm.faces.new(rings[-1])
    except Exception:
        pass

    # cable bundle grooves — 3 thin ridges on the top face of the arm
    top_z = ARM_H + 0.05
    groove_offsets = [-ARM_W * 0.5, 0.0, ARM_W * 0.5]
    for go in groove_offsets:
        gr_verts = []
        for r in radii[::3]:
            cx_r = cos_a * r
            cy_r = sin_a * r
            gx = cx_r - sin_a * go + cos_a * 0.04
            gy = cy_r + cos_a * go + sin_a * 0.04
            gr_verts.append(bm.verts.new((gx, gy, top_z)))
        # thin ridge: extrude each pair as a narrow quad strip
        for i in range(len(gr_verts) - 1):
            a, b = gr_verts[i], gr_verts[i + 1]
            c = bm.verts.new((b.co.x, b.co.y, b.co.z + 0.06))
            d = bm.verts.new((a.co.x, a.co.y, a.co.z + 0.06))
            try:
                bm.faces.new([a, b, c, d])
            except Exception:
                pass

    # junction nodes at 1/3 and 2/3 along arm
    for frac in (0.33, 0.67):
        r_node = r_start + (r_end - r_start) * frac
        cx_n   = cos_a * r_node
        cy_n   = sin_a * r_node
        node_r = ARM_W * 1.45
        bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=False, segments=16,
            radius1=node_r, radius2=node_r, depth=ARM_H * 0.55,
            matrix=Matrix.Translation(Vector((cx_n, cy_n, 0))),
        )

    # gold emitter port at mid-arm, inset into side face
    r_emit = r_start + (r_end - r_start) * 0.5
    cx_e   = cos_a * r_emit
    cy_e   = sin_a * r_emit
    # small disc perpendicular to the arm's radial direction
    emit_mat = (Matrix.Translation(Vector((cx_e, cy_e, 0))) @
                Matrix.Rotation(angle + PI / 2, 4, 'Z') @
                Matrix.Translation(Vector((0, ARM_W + EMITTER_DEPTH, 0))))
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=12,
        radius1=EMITTER_R, radius2=EMITTER_R, depth=EMITTER_DEPTH,
        matrix=emit_mat,
    )


def build_orb(bm):
    """Central blue-white energy sphere."""
    bmesh.ops.create_icosphere(bm, subdivisions=4, radius=ORB_R)

    # Orb collar ring (mounting interface) — torus in XY plane at Z=0
    COLLAR_SEGS  = 32
    COLLAR_MAJOR = ORB_R + 0.85
    COLLAR_MINOR = 0.70
    collar_rings = []
    for seg in range(COLLAR_SEGS):
        angle = seg * TAU / COLLAR_SEGS
        cx = math.cos(angle) * COLLAR_MAJOR
        cy = math.sin(angle) * COLLAR_MAJOR
        ring = [bm.verts.new((
            cx + math.cos(t * TAU / 8) * math.cos(angle) * COLLAR_MINOR,
            cy + math.cos(t * TAU / 8) * math.sin(angle) * COLLAR_MINOR,
            math.sin(t * TAU / 8) * COLLAR_MINOR,
        )) for t in range(8)]
        collar_rings.append(ring)
    collar_rings.append(collar_rings[0])
    _loft_rings(bm, collar_rings)

    # 8 mechanical clip nodes on the collar
    for i in range(8):
        angle = i * TAU / 8
        cx = math.cos(angle) * COLLAR_MAJOR
        cy = math.sin(angle) * COLLAR_MAJOR
        bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=COLLAR_MINOR * 1.5,
            matrix=Matrix.Translation(Vector((cx, cy, 0))),
        )


def build_platform(bm):
    """Circular observation platform below the hub centre."""
    PLAT_SEGS   = 24
    PLAT_DEPTH  =  0.30
    RAIL_MINOR  =  0.07

    # Main disc
    plat_rings = [
        _ring_verts(bm, 0, 0, PLATFORM_Z,             PLATFORM_R,      PLAT_SEGS),
        _ring_verts(bm, 0, 0, PLATFORM_Z - PLAT_DEPTH, PLATFORM_R,      PLAT_SEGS),
        _ring_verts(bm, 0, 0, PLATFORM_Z - PLAT_DEPTH, PLATFORM_R * 0.1, PLAT_SEGS),
    ]
    _loft_rings(bm, plat_rings[:2])
    _cap_ring(bm, plat_rings[0])
    _cap_ring(bm, plat_rings[2], flip=True)

    # Outer railing — thin torus at platform edge
    RAIL_SEGS  = 24
    RAIL_MAJOR = PLATFORM_R + 0.08
    rail_rings = []
    for seg in range(RAIL_SEGS):
        angle = seg * TAU / RAIL_SEGS
        cx = math.cos(angle) * RAIL_MAJOR
        cy = math.sin(angle) * RAIL_MAJOR
        ring = [bm.verts.new((
            cx + math.cos(t * TAU / 6) * math.cos(angle) * RAIL_MINOR,
            cy + math.cos(t * TAU / 6) * math.sin(angle) * RAIL_MINOR,
            PLATFORM_Z + 0.8 + math.sin(t * TAU / 6) * RAIL_MINOR,
        )) for t in range(6)]
        rail_rings.append(ring)
    rail_rings.append(rail_rings[0])
    _loft_rings(bm, rail_rings)

    # 4 vertical cable struts from hub centre to platform
    for i in range(4):
        angle   = i * TAU / 4 + PI / 4
        strut_x = math.cos(angle) * PLATFORM_R * 0.5
        strut_y = math.sin(angle) * PLATFORM_R * 0.5
        N_STRUT = 8
        strut_rings = []
        for j in range(N_STRUT):
            t    = j / (N_STRUT - 1)
            sz   = PLATFORM_Z * t              # 0 at hub → PLATFORM_Z at platform
            strut_rings.append(_ring_verts(bm, strut_x, strut_y, sz, CABLE_STRUT_R, 6))
        _loft_rings(bm, strut_rings)
        _cap_ring(bm, strut_rings[0])
        _cap_ring(bm, strut_rings[-1], flip=True)


def build():
    print("Building SM_Rift_OrbHub_A …")
    obj, bm = new_mesh("SM_Rift_OrbHub_A")

    build_outer_ring(bm)
    for i in range(N_ARMS):
        build_spoke_arm(bm, i)
    build_orb(bm)
    build_platform(bm)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, [
        "mat_ancient_machine_dark",
        "mat_ancient_machine_edge_wear",
        "mat_orb_energy",
        "mat_gold_emissive",
        "mat_blue_emissive",
    ])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_OrbHub_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_Rift_OrbHub_A")
