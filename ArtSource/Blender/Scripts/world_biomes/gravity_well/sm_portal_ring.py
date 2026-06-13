"""
SM_GravityWell_PortalRing_A — AbyssalEarth procedural mesh.
Concept: GW-001

GW-001 shows a MASSIVE RECTANGULAR STONE ARCHWAY — two square-section basalt pillars
(5.5 m × 5.5 m × 42 m each) connected at the top by a heavy lintel beam. The opening
is ≈28 m wide × 42 m tall. Amber rune-light panels are embedded in the inner faces at
equal vertical intervals. Carved horizontal groove lines divide each pillar into visual
blocks. Each pillar sits on a wider plinth base. Wall-integration flanges extend behind
the pillars into the cave rock. This is NOT a circular ring tube — it is a gate arch.

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

EXPORT_DIR = get_export_dir('GravityWell')

# ── scale constants ──────────────────────────────────────────────────
PILLAR_W          =  5.5    # pillar cross-section (square)
PILLAR_H          = 42.0    # pillar height (m)
OPENING_W         = 28.0    # clear opening between inner pillar faces
LINTEL_H          =  5.5    # height of top cross-beam
LINTEL_OVERHANG   =  0.55   # beyond outer pillar face
PLINTH_W          =  8.0    # wider plinth base
PLINTH_H          =  2.2    # plinth height
GROOVE_INTERVAL   =  7.0    # distance between carved groove lines
N_RUNE_PANELS     =  5      # amber panels per inner pillar face
RUNE_W            =  0.9    # rune panel width
RUNE_H            =  1.5    # rune panel height
RUNE_DEPTH        =  0.14   # inset depth
BEVEL_W           =  0.30   # corner chamfer
FLANGE_DEPTH      =  4.0    # wall integration flange depth

rng = random.Random(7)


def _quad(bm, pts):
    try:
        bm.faces.new(pts)
    except Exception:
        pass


def build_pillar(bm, side):
    """One square-section pillar with chamfered corners, groove lines, and rune panels.
    side = -1 for left, +1 for right.
    Pillar inner face is at X = side * OPENING_W/2.
    """
    inner_x  = side * OPENING_W / 2
    outer_x  = inner_x + side * PILLAR_W
    half_y   = PILLAR_W / 2
    bevel    = BEVEL_W

    # Build as a sequence of horizontal rings (octagonal cross-section from bevel)
    def _pillar_ring(z, taper=1.0):
        """8-vertex octagonal ring with beveled corners at height z."""
        w = PILLAR_W * taper / 2
        b = bevel * taper
        # Vertices going CCW viewed from +Z:
        # inner face (at x=inner_x) → left → outer face → right → back to inner
        # For right pillar (side=+1): inner_x on left (smaller x), outer_x on right (larger x)
        # 8 pts (2 per edge + 1 bevel point at each corner)
        ix = inner_x
        ox = inner_x + side * (PILLAR_W * taper)
        return [
            bm.verts.new((ix + side * b,  half_y * taper,         z)),  # inner top-L
            bm.verts.new((ix + side * b, -half_y * taper,         z)),  # inner bot-L
            bm.verts.new((ix,            -half_y * taper + b,     z)),  # corner bot-inner
            bm.verts.new((ix,             half_y * taper - b,     z)),  # corner top-inner
            bm.verts.new((ox - side * b,  half_y * taper,         z)),  # outer top-R
            bm.verts.new((ox - side * b, -half_y * taper,         z)),  # outer bot-R
            bm.verts.new((ox,            -half_y * taper + b,     z)),  # corner bot-outer
            bm.verts.new((ox,             half_y * taper - b,     z)),  # corner top-outer
        ]

    # Height rings
    n_groove_steps = int(PILLAR_H / GROOVE_INTERVAL) + 2
    z_rings = sorted(set(
        [0.0, PILLAR_H] +
        [GROOVE_INTERVAL * i for i in range(1, n_groove_steps) if GROOVE_INTERVAL * i < PILLAR_H]
    ))

    rings = []
    for z in z_rings:
        # Slight taper at top
        t = z / PILLAR_H
        taper = 1.0 - t * 0.06
        rings.append(_pillar_ring(z, taper))

    # Loft sides
    n = len(rings[0])
    for ri in range(len(rings) - 1):
        lo, hi = rings[ri], rings[ri + 1]
        for i in range(n):
            ni = (i + 1) % n
            _quad(bm, [lo[i], lo[ni], hi[ni], hi[i]])

    # Cap top and bottom
    try:
        bm.faces.new(list(reversed(rings[0])))
    except Exception:
        pass
    try:
        bm.faces.new(rings[-1])
    except Exception:
        pass

    # Carved groove insets (thin recessed bands at each groove-interval z)
    groove_z_list = [GROOVE_INTERVAL * i for i in range(1, n_groove_steps)
                     if 0.5 < GROOVE_INTERVAL * i < PILLAR_H - 0.5]
    for gz in groove_z_list:
        g_ring = _pillar_ring(gz, 1.0 - gz / PILLAR_H * 0.06)
        # Small inset ring slightly proud of face:
        INSET = 0.08
        # Just add the ring verts as a horizontal band (visual separation line)
        for v in g_ring:
            v.co.x -= side * INSET * 0.5

    # Amber rune panels on the inner face (facing opening)
    inner_face_x = inner_x + side * 0.02   # just proud of inner face
    rune_y_half  = RUNE_W / 2
    rune_spacing = (PILLAR_H - 2.0) / (N_RUNE_PANELS + 1)
    for rp in range(N_RUNE_PANELS):
        rz_centre = 1.0 + rune_spacing * (rp + 1)
        rz_bot    = rz_centre - RUNE_H / 2
        rz_top    = rz_centre + RUNE_H / 2
        # Front face of rune panel (facing opening = facing -side in X)
        rune_face = [
            bm.verts.new((inner_face_x, -rune_y_half, rz_bot)),
            bm.verts.new((inner_face_x,  rune_y_half, rz_bot)),
            bm.verts.new((inner_face_x,  rune_y_half, rz_top)),
            bm.verts.new((inner_face_x, -rune_y_half, rz_top)),
        ]
        _quad(bm, rune_face)
        # Sides of rune panel recess
        back_x = inner_face_x + side * RUNE_DEPTH
        rune_back = [
            bm.verts.new((back_x, -rune_y_half, rz_bot)),
            bm.verts.new((back_x,  rune_y_half, rz_bot)),
            bm.verts.new((back_x,  rune_y_half, rz_top)),
            bm.verts.new((back_x, -rune_y_half, rz_top)),
        ]
        _quad(bm, [rune_face[0], rune_back[0], rune_back[1], rune_face[1]])   # bottom
        _quad(bm, [rune_face[2], rune_back[2], rune_back[3], rune_face[3]])   # top
        _quad(bm, [rune_face[1], rune_back[1], rune_back[2], rune_face[2]])   # side+Y
        _quad(bm, [rune_face[3], rune_back[3], rune_back[0], rune_face[0]])   # side-Y
        _quad(bm, [rune_back[0], rune_back[3], rune_back[2], rune_back[1]])   # back


def build_lintel(bm):
    """Horizontal connecting beam spanning both pillars at the top."""
    half_y = (PILLAR_W / 2 + LINTEL_OVERHANG)
    total_span_half = OPENING_W / 2 + PILLAR_W + LINTEL_OVERHANG
    z_bot = PILLAR_H
    z_top = PILLAR_H + LINTEL_H

    ring_verts_per_z = lambda z: [
        bm.verts.new((-total_span_half, -half_y, z)),
        bm.verts.new(( total_span_half, -half_y, z)),
        bm.verts.new(( total_span_half,  half_y, z)),
        bm.verts.new((-total_span_half,  half_y, z)),
    ]
    lo = ring_verts_per_z(z_bot)
    hi = ring_verts_per_z(z_top)
    for i in range(4):
        ni = (i + 1) % 4
        _quad(bm, [lo[i], lo[ni], hi[ni], hi[i]])
    try:
        bm.faces.new(list(reversed(lo)))
    except Exception:
        pass
    try:
        bm.faces.new(hi)
    except Exception:
        pass

    # Rune panels on front face of lintel
    lrune_y_half = RUNE_W * 0.65
    lrune_spacing = total_span_half * 2 / 5
    for lrp in range(4):
        lx_c = -total_span_half + lrune_spacing * (lrp + 0.5)
        lz_c = z_bot + LINTEL_H * 0.5
        ld = 0.12
        # Front face (facing -Y)
        lf = [
            bm.verts.new((lx_c - RUNE_W / 2, -half_y, lz_c - lrune_y_half)),
            bm.verts.new((lx_c + RUNE_W / 2, -half_y, lz_c - lrune_y_half)),
            bm.verts.new((lx_c + RUNE_W / 2, -half_y, lz_c + lrune_y_half)),
            bm.verts.new((lx_c - RUNE_W / 2, -half_y, lz_c + lrune_y_half)),
        ]
        _quad(bm, lf)


def build_plinths(bm):
    """Wide base blocks under each pillar."""
    phalf_y = PLINTH_W / 2
    for side in (-1, 1):
        inner_x = side * OPENING_W / 2
        outer_x = inner_x + side * PILLAR_W
        cx = (inner_x + outer_x) / 2
        for z in (0, PLINTH_H):
            bm.verts.new((cx - side * PLINTH_W / 2 - side * PILLAR_W / 2, -phalf_y, z))
            bm.verts.new((cx - side * PLINTH_W / 2 - side * PILLAR_W / 2,  phalf_y, z))
            bm.verts.new((cx + side * PLINTH_W / 2 - side * PILLAR_W / 2,  phalf_y, z))
            bm.verts.new((cx + side * PLINTH_W / 2 - side * PILLAR_W / 2, -phalf_y, z))

    # Build actual geometry for plinths
    for side in (-1, 1):
        inner_x = side * OPENING_W / 2
        outer_x = inner_x + side * PILLAR_W
        cx = (inner_x + outer_x) / 2
        half_p = PLINTH_W / 2
        lo = [
            bm.verts.new((cx - half_p, -half_p, 0)),
            bm.verts.new((cx + half_p, -half_p, 0)),
            bm.verts.new((cx + half_p,  half_p, 0)),
            bm.verts.new((cx - half_p,  half_p, 0)),
        ]
        hi = [
            bm.verts.new((cx - half_p, -half_p, PLINTH_H)),
            bm.verts.new((cx + half_p, -half_p, PLINTH_H)),
            bm.verts.new((cx + half_p,  half_p, PLINTH_H)),
            bm.verts.new((cx - half_p,  half_p, PLINTH_H)),
        ]
        for i in range(4):
            ni = (i + 1) % 4
            _quad(bm, [lo[i], lo[ni], hi[ni], hi[i]])
        try:
            bm.faces.new(list(reversed(lo)))
        except Exception:
            pass


def build_wall_flanges(bm):
    """Triangular fins behind each pillar integrating into the cave wall."""
    for side in (-1, 1):
        inner_x = side * OPENING_W / 2
        outer_x = inner_x + side * PILLAR_W
        # Flange extends in +Y direction (into the cave wall behind the gate)
        base_y  = PILLAR_W / 2
        apex_y  = base_y + FLANGE_DEPTH
        for xi in (inner_x + side * 0.5, outer_x - side * 0.5):
            for hz in (2, PILLAR_H * 0.4, PILLAR_H * 0.75):
                # Triangle: two base pts on pillar face, one apex point in cave wall
                flange = [
                    bm.verts.new((xi,  base_y, hz)),
                    bm.verts.new((xi,  base_y, hz + PILLAR_H * 0.1)),
                    bm.verts.new((xi,  apex_y, hz + PILLAR_H * 0.05)),
                ]
                try:
                    bm.faces.new(flange)
                except Exception:
                    pass


def build():
    print("Building SM_GravityWell_PortalRing_A …")
    obj, bm = new_mesh("SM_GravityWell_PortalRing_A")

    for side in (-1, 1):
        build_pillar(bm, side)
    build_lintel(bm)
    build_plinths(bm)
    build_wall_flanges(bm)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, [
        "mat_wet_basalt",
        "mat_dark_basalt",
        "mat_ancient_machine_dark",
        "mat_amber_stabilizer",
        "mat_ancient_machine_edge_wear",
    ])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_PortalRing_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_GravityWell_PortalRing_A")
