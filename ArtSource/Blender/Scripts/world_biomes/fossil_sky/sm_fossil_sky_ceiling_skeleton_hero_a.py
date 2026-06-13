"""
SM_FossilSky_CeilingSkeleton_Hero_A — AbyssalEarth procedural mesh.
Concept: FS-002, FS-003

FS-002 shows a massive fossil whale skeleton embedded in the cave ceiling — bone-white,
120+ m long, hanging downward. Key anatomical reads: a CONTINUOUS LOFTED TUBE for the spine
(not icosphere chains which produce undifferentiated blobs), 7 pairs of arced rib bones that
sweep outward and downward, a flattened cranium with rostrum and lower jaw, and subtle
vertebrae dorsal-process bumps. Z=0 is the ceiling surface; all bones hang in -Z.
Cyan fossil vein channels and amber fossil-stone surface complete the palette.

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

EXPORT_DIR = get_export_dir('FossilSky')

# ── scale constants ──────────────────────────────────────────────────
SPINE_LEN      = 115.0   # full skeleton length (m)
SPINE_SEGS     =  28     # cross-section rings along spine
SPINE_SIDES    =  12     # polygon sides on spine tube
N_RIB_PAIRS   =   7     # major rib pairs (both sides)
RIB_SEGS       =  14    # cross-section rings per rib
RIB_SIDES      =   8    # polygon sides on rib tube
SKULL_L        =  10.0   # skull total length
SKULL_W        =   7.0   # skull cranium width
SKULL_D        =   4.5   # skull cranium depth (Z)

rng = random.Random(13)


def _lerp(a, b, t):
    return a + (b - a) * t


def _spine_radius(t):
    """Radius profile along the spine (t=0 is skull-end, t=1 is tail-tip)."""
    if t < 0.08:
        return _lerp(0.5, 1.1, t / 0.08)
    elif t < 0.45:
        return _lerp(1.1, 1.35, (t - 0.08) / 0.37)
    elif t < 0.65:
        return 1.35
    else:
        return _lerp(1.35, 0.28, (t - 0.65) / 0.35)


def _ring_tube(bm, cx, cy, cz, r, n, normal_axis='Z'):
    """Create n verts in a circle of radius r at (cx,cy,cz), perpendicular to normal_axis."""
    verts = []
    for i in range(n):
        a = i * TAU / n
        if normal_axis == 'Z':
            verts.append(bm.verts.new((cx + math.cos(a) * r, cy + math.sin(a) * r, cz)))
        elif normal_axis == 'X':
            verts.append(bm.verts.new((cx, cy + math.cos(a) * r, cz + math.sin(a) * r)))
        elif normal_axis == 'Y':
            verts.append(bm.verts.new((cx + math.cos(a) * r, cy, cz + math.sin(a) * r)))
    return verts


def _loft_rings(bm, rings):
    n = len(rings[0])
    for ri in range(len(rings) - 1):
        lo, hi = rings[ri], rings[ri + 1]
        for i in range(n):
            ni = (i + 1) % n
            try:
                bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
            except Exception:
                pass


def _cap_ring_centre(bm, ring, flip=False):
    cx = sum(v.co.x for v in ring) / len(ring)
    cy = sum(v.co.y for v in ring) / len(ring)
    cz = sum(v.co.z for v in ring) / len(ring)
    c  = bm.verts.new((cx, cy, cz))
    n  = len(ring)
    for i in range(n):
        ni = (i + 1) % n
        try:
            if flip:
                bm.faces.new([ring[ni], ring[i], c])
            else:
                bm.faces.new([ring[i], ring[ni], c])
        except Exception:
            pass


def build_spine(bm):
    """Continuous lofted tube spine in XZ plane, hanging from ceiling (Z <= 0)."""
    rings = []
    for si in range(SPINE_SEGS):
        t    = si / (SPINE_SEGS - 1)
        x    = (t - 0.5) * SPINE_LEN            # skull end = -SPINE_LEN/2
        z_wave = -rng.uniform(0.4, 1.2) * math.sin(t * PI * 2.5) - t * 4.0  # hangs down
        r    = _spine_radius(t)
        # Slightly flatten (squash in Y) for bone-like cross-section
        ring = []
        for i in range(SPINE_SIDES):
            a  = i * TAU / SPINE_SIDES
            ry = math.cos(a) * r * 1.05    # slight Y flare
            rz = math.sin(a) * r * 0.75   # compressed Z (ceiling-flat bone look)
            ring.append(bm.verts.new((x, ry, z_wave + rz)))
        rings.append(ring)

    _loft_rings(bm, rings)
    _cap_ring_centre(bm, rings[0])
    _cap_ring_centre(bm, rings[-1], flip=True)

    # Vertebrae dorsal processes — extruded bumps at every 4th ring
    for si in range(0, SPINE_SEGS - 4, 4):
        t    = si / (SPINE_SEGS - 1)
        r    = _spine_radius(t)
        x    = (t - 0.5) * SPINE_LEN
        z_wave = -rng.uniform(0.4, 1.2) * math.sin(t * PI * 2.5) - t * 4.0
        bump_h = r * 0.65
        spine_top_z = z_wave + r * 0.75   # top of the tube at this position
        # Small fin/bump verts
        bump_verts = [
            bm.verts.new((x - 0.45, 0, spine_top_z)),
            bm.verts.new((x + 0.45, 0, spine_top_z)),
            bm.verts.new((x + 0.20, 0, spine_top_z + bump_h)),
            bm.verts.new((x - 0.20, 0, spine_top_z + bump_h)),
        ]
        try:
            bm.faces.new(bump_verts)
        except Exception:
            pass

    return rings   # return rings so skull knows the head-end position


def build_rib(bm, spine_x, spine_y_off, spine_z, side, rib_idx):
    """One rib bone: a swept tube that curves outward and downward."""
    rib_span  = rng.uniform(16, 26)       # lateral reach (m)
    rib_drop  = rng.uniform(8,  16)       # Z drop from spine to rib tip
    r_base    =  0.48
    r_tip     =  0.10

    rib_rings = []
    for ri in range(RIB_SEGS):
        t     = ri / (RIB_SEGS - 1)
        # Parametric arc: starts at spine attachment, curves outward and down
        rib_y = spine_y_off + side * math.sin(t * PI) * rib_span
        rib_z = spine_z - math.sin(t * PI) * rib_drop + rng.uniform(-0.2, 0.2)
        rib_x = spine_x + rng.uniform(-0.4, 0.4) * (1 - t)   # slight X sway
        rib_r = _lerp(r_base, r_tip, t ** 0.8)

        # Rib tube cross-section — elliptical (compressed in the arc's radial direction)
        ring = []
        for i in range(RIB_SIDES):
            a  = i * TAU / RIB_SIDES
            # Slightly flatten the cross-section perpendicular to sweep direction
            ry = math.cos(a) * rib_r
            rz = math.sin(a) * rib_r * 0.65
            ring.append(bm.verts.new((rib_x, rib_y + ry, rib_z + rz)))
        rib_rings.append(ring)

    _loft_rings(bm, rib_rings)
    _cap_ring_centre(bm, rib_rings[0])
    _cap_ring_centre(bm, rib_rings[-1], flip=True)


def build_skull(bm):
    """Flattened cranium + rostrum + lower jaw at the skull-end of the spine."""
    skull_x = -SPINE_LEN / 2

    # Cranium: deformed icosphere — squash Z, stretch X and Y
    mat = (Matrix.Translation(Vector((skull_x, 0, -2.5))) @
           Matrix.Scale(SKULL_L * 0.5, 4, (1, 0, 0)) @
           Matrix.Scale(SKULL_W * 0.5, 4, (0, 1, 0)) @
           Matrix.Scale(SKULL_D * 0.5, 4, (0, 0, 1)))
    # Use a cylinder to approximate flattened skull shape
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat)

    # Rostrum (long beak/snout extending forward)
    ROST_L = 7.0
    rostrum_rings = []
    for ri in range(8):
        t      = ri / 7
        rx     = skull_x - SKULL_L * 0.4 - t * ROST_L
        rr     = _lerp(SKULL_W * 0.28, 0.35, t)
        rz_off = _lerp(-1.8, -1.5, t)
        ring   = []
        for i in range(8):
            a = i * TAU / 8
            ring.append(bm.verts.new((rx, math.cos(a) * rr * 0.7, rz_off + math.sin(a) * rr * 0.4)))
        rostrum_rings.append(ring)
    _loft_rings(bm, rostrum_rings)
    _cap_ring_centre(bm, rostrum_rings[0])
    _cap_ring_centre(bm, rostrum_rings[-1], flip=True)

    # Lower jaw (separate narrower element, angled slightly open)
    jaw_rings = []
    for ji in range(6):
        t     = ji / 5
        jx    = skull_x - SKULL_L * 0.25 - t * ROST_L * 0.82
        jr    = _lerp(SKULL_W * 0.20, 0.22, t)
        jz    = _lerp(-SKULL_D * 0.6, -SKULL_D * 0.9 - 1.5, t)
        ring  = []
        for i in range(6):
            a = i * TAU / 6
            ring.append(bm.verts.new((jx, math.cos(a) * jr * 0.8, jz + math.sin(a) * jr * 0.3)))
        jaw_rings.append(ring)
    _loft_rings(bm, jaw_rings)
    _cap_ring_centre(bm, jaw_rings[0])
    _cap_ring_centre(bm, jaw_rings[-1], flip=True)

    # Eye socket rims (pair of disc rings, not spheres)
    for eye_side in (-1, 1):
        ey = eye_side * SKULL_W * 0.32
        for er in (0.9, 0.65):   # outer and inner ring
            socket_ring = []
            for i in range(10):
                a  = i * TAU / 10
                socket_ring.append(bm.verts.new((
                    skull_x + 0.5,
                    ey + math.cos(a) * er,
                    -1.5 + math.sin(a) * er * 0.7,
                )))
            bm.verts.new((skull_x, ey, -1.5))   # socket depth hint

    # Cranial ridge (extruded edge across the top)
    ridge_pts = [
        bm.verts.new((skull_x + SKULL_L * 0.3, -0.4, -0.8)),
        bm.verts.new((skull_x + SKULL_L * 0.1,  0.0, -0.3)),
        bm.verts.new((skull_x - SKULL_L * 0.1,  0.0, -0.3)),
        bm.verts.new((skull_x - SKULL_L * 0.3, -0.4, -0.8)),
        bm.verts.new((skull_x - SKULL_L * 0.3, -0.4, -0.3)),
        bm.verts.new((skull_x - SKULL_L * 0.1,  0.0,  0.15)),
        bm.verts.new((skull_x + SKULL_L * 0.1,  0.0,  0.15)),
        bm.verts.new((skull_x + SKULL_L * 0.3, -0.4, -0.3)),
    ]
    try:
        bm.faces.new(ridge_pts)
    except Exception:
        pass


def build():
    print("Building SM_FossilSky_CeilingSkeleton_Hero_A …")
    obj, bm = new_mesh("SM_FossilSky_CeilingSkeleton_Hero_A")

    spine_rings = build_spine(bm)

    # Rib pairs distributed along spine body (avoid skull and tail ends)
    for ri in range(N_RIB_PAIRS):
        t_rib  = 0.12 + ri * (0.68 / (N_RIB_PAIRS - 1))   # 12%–80% along spine
        spine_x = (t_rib - 0.5) * SPINE_LEN
        spine_z = -rng.uniform(0.4, 1.2) * math.sin(t_rib * PI * 2.5) - t_rib * 4.0
        for side in (-1, 1):
            build_rib(bm, spine_x, 0, spine_z, side, ri)

    build_skull(bm)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, [
        "mat_bone_stone",
        "mat_fossil_bone",
        "mat_cyan_fossil_vein",
        "mat_amber_emissive",
    ])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_CeilingSkeleton_Hero_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_FossilSky_CeilingSkeleton_Hero_A")
