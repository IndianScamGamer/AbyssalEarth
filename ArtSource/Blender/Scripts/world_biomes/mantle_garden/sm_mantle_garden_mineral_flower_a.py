"""
SM_MantleGarden_MineralFlower_A — AbyssalEarth procedural mesh.
SM_MantleGarden_MineralFlower_B — AbyssalEarth procedural mesh.
Concept: MG-001, MG-002

MG-001/MG-002 show SHARP FACETED CRYSTAL SPIRES erupting from the obsidian ground —
magenta/pink, pointed (near-zero tip radius), with outward tilts and varying heights.
They are NOT rounded hex prisms; they are elongated hexagonal or octagonal PYRAMIDS with
a strong faceted twist. A central dominant spire is surrounded by a burst of shorter
secondary spires and a scatter of tiny tertiary tips. The base is a cracked obsidian
mound with heat-crack channels.

Variant A: 9 primary spires, 1-3 m cluster
Variant B: 21 primary spires, larger 3.5 m cluster

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

EXPORT_DIR = get_export_dir('MantleGarden')

# ── scale constants (Variant A) ──────────────────────────────────────
N_PRIMARY_A     =  9       # primary spires in Variant A
BASE_SPREAD_A   =  0.75    # m — cluster radius for primary spires
MAX_H_A         =  2.8     # tallest spire height (m)
MIN_H_A         =  0.65    # shortest primary spire
BASE_W_A        =  0.09    # spire base radius
TIP_W           =  0.005   # near-zero tip radius → sharp spike
N_SECONDARY_A   = 14       # tiny secondary spires
BASE_MOUND_R_A  =  0.90    # obsidian mound radius

# ── scale constants (Variant B) ──────────────────────────────────────
N_PRIMARY_B     = 21
BASE_SPREAD_B   =  1.55
MAX_H_B         =  3.5
MIN_H_B         =  0.80
BASE_W_B        =  0.11
N_SECONDARY_B   = 28
BASE_MOUND_R_B  =  1.75

SPIRE_SIDES     =  6       # hexagonal cross-section (matches crystal faceting)
N_FACET_RINGS   =  3       # intermediate rings for faceted twist


def _make_spire(bm, cx, cy, height, base_r, tilt_angle, tilt_dir, rotation, twist_rate=0.35):
    """
    Build one crystal spire as a lofted hexagonal pyramid with a slight twist.
    - tilt_angle: lean from vertical (radians)
    - tilt_dir: azimuth direction of the lean
    - twist_rate: how many radians the cross-section rotates per metre of height
    """
    rings = []
    # N_FACET_RINGS intermediate + tip
    total_rings = N_FACET_RINGS + 2   # base, 3 intermediates, tip
    for ri in range(total_rings):
        t   = ri / (total_rings - 1)
        # Ease: bottom half tapers slowly, top half tapers quickly to near-zero
        ease = t ** 1.6
        r   = base_r * (1 - ease) + TIP_W * ease

        z   = height * t
        # Apply outward tilt (lean)
        dx  = math.sin(tilt_angle) * z * math.cos(tilt_dir)
        dy  = math.sin(tilt_angle) * z * math.sin(tilt_dir)
        px  = cx + dx
        py  = cy + dy

        ring_rotation = rotation + twist_rate * z
        ring = [
            bm.verts.new((
                px + math.cos(j * TAU / SPIRE_SIDES + ring_rotation) * r,
                py + math.sin(j * TAU / SPIRE_SIDES + ring_rotation) * r,
                z,
            ))
            for j in range(SPIRE_SIDES)
        ]
        rings.append(ring)

    # Loft rings into faces
    for ri in range(len(rings) - 1):
        lo, hi = rings[ri], rings[ri + 1]
        n = len(lo)
        for i in range(n):
            ni = (i + 1) % n
            try:
                bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
            except Exception:
                pass

    # Base cap
    try:
        bm.faces.new(list(reversed(rings[0])))
    except Exception:
        pass

    # Tip cap (tiny hexagon → centre point)
    if len(rings[-1]) > 0:
        tip_z  = height + 0.002
        tip_cx = rings[-1][0].co.x
        tip_cy = rings[-1][0].co.y
        tip_c  = bm.verts.new((tip_cx, tip_cy, tip_z))
        for i in range(SPIRE_SIDES):
            ni = (i + 1) % SPIRE_SIDES
            try:
                bm.faces.new([rings[-1][i], rings[-1][ni], tip_c])
            except Exception:
                pass


def build_base_mound(bm, mound_r, rng):
    """Irregular obsidian mound base with heat-crack channels."""
    N_MOUND = 16
    mound_rings = []
    # Bottom (flat on ground)
    mound_rings.append([
        bm.verts.new((
            math.cos(i * TAU / N_MOUND) * mound_r * rng.uniform(0.88, 1.12),
            math.sin(i * TAU / N_MOUND) * mound_r * rng.uniform(0.88, 1.12),
            0.0,
        ))
        for i in range(N_MOUND)
    ])
    # Upper crown (slightly contracted, elevated)
    mound_rings.append([
        bm.verts.new((
            math.cos(i * TAU / N_MOUND) * mound_r * 0.62 * rng.uniform(0.92, 1.08),
            math.sin(i * TAU / N_MOUND) * mound_r * 0.62 * rng.uniform(0.92, 1.08),
            rng.uniform(0.12, 0.24),
        ))
        for i in range(N_MOUND)
    ])

    for ri in range(len(mound_rings) - 1):
        lo, hi = mound_rings[ri], mound_rings[ri + 1]
        for i in range(N_MOUND):
            ni = (i + 1) % N_MOUND
            try:
                bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
            except Exception:
                pass

    # Bottom cap
    try:
        bm.faces.new(list(reversed(mound_rings[0])))
    except Exception:
        pass

    # Heat-crack channels — 3 thin grooves across the mound surface
    N_CRACKS = 3
    for ci in range(N_CRACKS):
        crack_angle = ci * TAU / N_CRACKS + rng.uniform(-0.3, 0.3)
        crack_len   = mound_r * rng.uniform(0.6, 0.95)
        N_CRACK_PTS = 8
        prev_verts  = None
        for cpi in range(N_CRACK_PTS):
            t_c   = cpi / (N_CRACK_PTS - 1)
            cx_c  = math.cos(crack_angle + rng.uniform(-0.1, 0.1)) * crack_len * t_c
            cy_c  = math.sin(crack_angle + rng.uniform(-0.1, 0.1)) * crack_len * t_c
            cz_c  = rng.uniform(0.01, 0.06)
            w_c   = 0.035 * (1 - t_c * 0.5)
            perp  = crack_angle + PI / 2
            cvL   = bm.verts.new((cx_c + math.cos(perp) * w_c, cy_c + math.sin(perp) * w_c, cz_c))
            cvR   = bm.verts.new((cx_c - math.cos(perp) * w_c, cy_c - math.sin(perp) * w_c, cz_c))
            if prev_verts is not None:
                pL, pR = prev_verts
                try:
                    bm.faces.new([pL, cvL, cvR, pR])
                except Exception:
                    pass
            prev_verts = (cvL, cvR)


def build_variant(name, n_primary, base_spread, max_h, min_h, base_w, n_secondary, mound_r, seed):
    rng = random.Random(seed)
    obj, bm = new_mesh(name)

    # Central dominant spire (tallest, near-vertical)
    _make_spire(bm, 0, 0, max_h, base_w * 1.45, 0.04, 0, 0, twist_rate=0.28)

    # Primary spires in a burst pattern around centre
    for i in range(n_primary - 1):
        angle   = i * TAU / (n_primary - 1) + rng.uniform(-0.18, 0.18)
        radius  = rng.uniform(base_spread * 0.3, base_spread)
        cx      = math.cos(angle) * radius
        cy      = math.sin(angle) * radius
        h       = rng.uniform(min_h, max_h * 0.82)
        tilt    = rng.uniform(0.04, 0.20)          # radians lean from vertical
        rot     = rng.uniform(0, TAU)
        _make_spire(bm, cx, cy, h, rng.uniform(base_w * 0.75, base_w * 1.2),
                    tilt, angle + rng.uniform(-0.3, 0.3), rot, twist_rate=rng.uniform(0.15, 0.45))

    # Secondary tiny spires (gap-fillers and scatter)
    for i in range(n_secondary):
        angle2  = rng.uniform(0, TAU)
        radius2 = rng.uniform(base_spread * 0.05, mound_r * 0.95)
        cx2     = math.cos(angle2) * radius2
        cy2     = math.sin(angle2) * radius2
        h2      = rng.uniform(0.12, min_h * 0.7)
        bm.verts  # ensure bm is active
        _make_spire(bm, cx2, cy2, h2, rng.uniform(0.025, 0.065),
                    rng.uniform(0.0, 0.25), angle2, rng.uniform(0, TAU), twist_rate=0)

    build_base_mound(bm, mound_r, rng)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, [
        "mat_magenta_mineral",
        "mat_purple_emissive",
        "mat_obsidian",
        "mat_heat_crack",
    ])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, name)
    return obj


def build():
    print("Building SM_MantleGarden_MineralFlower_A / B …")
    build_variant(
        "SM_MantleGarden_MineralFlower_A",
        N_PRIMARY_A, BASE_SPREAD_A, MAX_H_A, MIN_H_A, BASE_W_A,
        N_SECONDARY_A, BASE_MOUND_R_A, seed=53,
    )
    build_variant(
        "SM_MantleGarden_MineralFlower_B",
        N_PRIMARY_B, BASE_SPREAD_B, MAX_H_B, MIN_H_B, BASE_W_B,
        N_SECONDARY_B, BASE_MOUND_R_B, seed=97,
    )


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_MantleGarden_MineralFlower_A/B")
