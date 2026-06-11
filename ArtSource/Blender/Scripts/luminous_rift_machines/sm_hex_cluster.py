"""
SM_HEX_CLUSTER — AbyssalEarth procedural mesh.
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

def build(name, broken=False, seed=1):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    tile_r   = 2.0
    gap      = 0.18
    spacing  = (tile_r + gap) * math.sqrt(3)

    tile_positions = [(0, 0, 0)]
    for i in range(6):
        angle  = i * TAU/6
        tx     = math.cos(angle) * spacing
        ty     = math.sin(angle) * spacing
        tilt_z = rng.uniform(-0.06, 0.06) if not broken else rng.uniform(-0.4, 0.4)
        tile_positions.append((tx, ty, tilt_z))

    skip_tiles = {3, 5} if broken else set()
    frame_w = 0.22

    for idx, (tx, ty, tz) in enumerate(tile_positions):
        if idx in skip_tiles:
            continue

        outer_pts = hex_pts(tx, ty, tile_r)
        inner_pts = hex_pts(tx, ty, tile_r - frame_w)

        # frame
        for i in range(6):
            ni = (i+1)%6
            rot_z = tz + (rng.uniform(-0.12,0.12) if broken else 0)
            ov = [bm.verts.new((outer_pts[i][0], outer_pts[i][1], tz)),
                  bm.verts.new((outer_pts[ni][0],outer_pts[ni][1], tz)),
                  bm.verts.new((inner_pts[ni][0],inner_pts[ni][1], tz)),
                  bm.verts.new((inner_pts[i][0], inner_pts[i][1], tz))]
            try:
                bm.faces.new(ov)
                bv = [bm.verts.new((v.co.x, v.co.y, tz - 0.14)) for v in ov]
                bm.faces.new(list(reversed(bv)))
                for j in range(4):
                    nj=(j+1)%4
                    bm.faces.new([ov[j],ov[nj],bv[nj],bv[j]])
            except Exception:
                pass

        # pane
        pane_pts = hex_pts(tx, ty, tile_r - frame_w - 0.04)
        pf = [bm.verts.new((p[0],p[1], tz - 0.01)) for p in pane_pts]
        try:
            bm.faces.new(pf)
        except Exception:
            pass

    # central hub node
    hub = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.55,
                                      matrix=Matrix.Translation(Vector((0,0,0.3))))
    # ring around hub
    for r_off in [0.65, 0.72]:
        rv = [bm.verts.new((math.cos(i*TAU/24)*r_off,
                            math.sin(i*TAU/24)*r_off,
                            0.08 + (r_off-0.65)*3))
              for i in range(24)]
        for i in range(24):
            ni=(i+1)%24
            try:
                bv = [bm.verts.new((rv[i].co.x, rv[i].co.y, rv[i].co.z-0.06)),
                      bm.verts.new((rv[ni].co.x,rv[ni].co.y,rv[ni].co.z-0.06))]
                bm.faces.new([rv[i], rv[ni], bv[1], bv[0]])
            except Exception:
                pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_gold_emissive", "mat_collector_glass",
                        "mat_ancient_machine_dark", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  ORB FRAME
# ══════════════════════════════════════════════
# Massive partial ring frame (~30m diameter) around the central orb.
# Not a perfect circle — asymmetric, damaged, with beam arm attachment
# points. Matches: AD-001 (Orb Apparatus — Mechanical Hub).

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_HEX_CLUSTER")
