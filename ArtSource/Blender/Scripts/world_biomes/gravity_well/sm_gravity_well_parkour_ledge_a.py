"""
SM_GravityWell_ParkourLedge_A — AbyssalEarth procedural mesh.
Concept: GW-003

Angled stone shelf for the parkour approach corridor — a broken slab of cave wall that
juts out at an angle. Players jump from one to the next to navigate the Gravity Well
approach. The wall edge is clean (bolted anchor face) and the outer edge is crumbled
and irregular. An amber rune strip inset into the top face acts as a wayfinding cue,
and iron grip bars along the outer lip give the player a visual read on landing spots.

Run standalone:  blender --background --python <this_file>.py
"""
import sys, os, math, random
import bpy, bmesh
from mathutils import Matrix, Vector

_HERE         = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, TAU, PI)

EXPORT_DIR = get_export_dir('GravityWell')

LEDGE_L      = 2.8    # ledge length (long axis)
LEDGE_W      = 0.85   # ledge width (depth from wall)
LEDGE_H      = 0.38   # ledge thickness at thickest point
LEDGE_TAPER  = 0.18   # taper: the outer edge is thinner than the wall edge
CRUMBLE_VERTS= 8      # number of crumble deformation verts on outer edge
RUNE_STRIP_W = 0.04   # width of amber rune inset strip
GRIP_BAR_H   = 0.24   # height of iron grip bar stub
GRIP_BAR_R   = 0.018  # grip bar radius
N_GRIP_BARS  = 2      # number of grip bars on outer edge


def build():
    rng = random.Random(17)
    obj, bm = new_mesh("SM_GravityWell_ParkourLedge_A")

    # 1. Main ledge body — 8-vert tapered box
    hl = LEDGE_L / 2
    # Bottom face verts (z=0): wall side y=0, outer side y=LEDGE_W
    b0 = bm.verts.new((-hl,       0.0,     0.0))
    b1 = bm.verts.new(( hl,       0.0,     0.0))
    b2 = bm.verts.new(( hl,  LEDGE_W,     0.0))
    b3 = bm.verts.new((-hl,  LEDGE_W,     0.0))
    # Top face verts (z=LEDGE_H): wall side is full height, outer side is tapered
    t0 = bm.verts.new((-hl,       0.0,  LEDGE_H))
    t1 = bm.verts.new(( hl,       0.0,  LEDGE_H))
    t2 = bm.verts.new(( hl,  LEDGE_W,  LEDGE_H - LEDGE_TAPER))
    t3 = bm.verts.new((-hl,  LEDGE_W,  LEDGE_H - LEDGE_TAPER))

    # Apply crumble deformation to the 4 outer-edge verts (y ≈ LEDGE_W)
    for v in (b2, b3, t2, t3):
        v.co.x += rng.uniform(-0.15, 0.15)
        v.co.z += rng.uniform(-0.06, 0.04)

    # 6 faces: bottom, top, wall side, outer side, left end, right end
    bm.faces.new([b0, b3, b2, b1])          # bottom
    bm.faces.new([t0, t1, t2, t3])          # top
    bm.faces.new([b0, b1, t1, t0])          # wall side (y=0)
    bm.faces.new([b3, b2, t2, t3])          # outer side (y=LEDGE_W) — but deformed
    bm.faces.new([b0, t0, t3, b3])          # left end (-x)
    bm.faces.new([b1, b2, t2, t1])          # right end (+x)

    # 2. Amber rune strip — thin rectangle inset on top face along outer edge
    rx0 = -hl + 0.1
    rx1 =  hl - 0.1
    ry0 = LEDGE_W - RUNE_STRIP_W
    ry1 = LEDGE_W
    rz  = LEDGE_H + 0.005
    rs0 = bm.verts.new((rx0, ry0, rz))
    rs1 = bm.verts.new((rx1, ry0, rz))
    rs2 = bm.verts.new((rx1, ry1, rz))
    rs3 = bm.verts.new((rx0, ry1, rz))
    bm.faces.new([rs0, rs1, rs2, rs3])

    # 3. Iron grip bars — 2 stubs along the outer edge
    for gi in range(N_GRIP_BARS):
        gx = -LEDGE_L / 3 + gi * (LEDGE_L / 3)
        gy = LEDGE_W
        gz_base = LEDGE_H
        # Grip bar post (cone used as cylinder: equal radii)
        bar_mat = Matrix.Translation(Vector((gx, gy, gz_base + GRIP_BAR_H / 2)))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
                              radius1=GRIP_BAR_R, radius2=GRIP_BAR_R,
                              depth=GRIP_BAR_H, matrix=bar_mat)
        # Knurled end cap — small icosphere on top of bar
        cap_mat = Matrix.Translation(Vector((gx, gy, gz_base + GRIP_BAR_H + GRIP_BAR_R * 1.4)))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=GRIP_BAR_R * 1.4,
                                   matrix=cap_mat)

    # 4. Crumbled debris pile — 3 small deformed icospheres at wall base
    debris_radii = [0.08, 0.13, 0.18]
    debris_xs    = [-0.6, 0.1, 0.7]
    for dr, dx in zip(debris_radii, debris_xs):
        d_mat = Matrix.Translation(Vector((dx, 0.0, 0.0)))
        d_result = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=dr, matrix=d_mat)
        for v in d_result['verts']:
            v.co.x += rng.uniform(-dr * 0.3, dr * 0.3)
            v.co.y += rng.uniform(-dr * 0.3, dr * 0.3)
            v.co.z += rng.uniform(-dr * 0.2, dr * 0.1)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_amber_stabilizer", "mat_ancient_machine_dark"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_ParkourLedge_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_GravityWell_ParkourLedge_A")
