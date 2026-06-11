"""
SM_HEX_TILE — AbyssalEarth procedural mesh.
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

def build(name="SM_Rift_HexCollector_Tile_A",
                   outer_r=2.0, frame_w=0.22, pane_depth=0.04):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)

    inner_r = outer_r - frame_w

    # ── outer hex frame (6 trapezoidal frame segments) ──
    outer_pts = hex_pts(0, 0, outer_r)
    inner_pts = hex_pts(0, 0, inner_r)

    for i in range(6):
        ni = (i+1)%6
        # front face of frame segment
        ov = [bm.verts.new((outer_pts[i][0], outer_pts[i][1], 0.0)),
              bm.verts.new((outer_pts[ni][0],outer_pts[ni][1], 0.0)),
              bm.verts.new((inner_pts[ni][0],inner_pts[ni][1], 0.0)),
              bm.verts.new((inner_pts[i][0], inner_pts[i][1], 0.0))]
        bm.faces.new(ov)
        # back face
        bv = [bm.verts.new((v.co.x, v.co.y, -frame_w*0.6)) for v in ov]
        bm.faces.new(list(reversed(bv)))
        # side faces
        for j in range(4):
            nj = (j+1)%4
            try:
                bm.faces.new([ov[j], ov[nj], bv[nj], bv[j]])
            except Exception:
                pass

    # ── frosted inner pane ──────────────────────
    pane_pts = hex_pts(0, 0, inner_r - 0.04)
    pane_f = [bm.verts.new((p[0], p[1], -0.008)) for p in pane_pts]
    pane_b = [bm.verts.new((p[0], p[1], -0.008 - pane_depth)) for p in pane_pts]
    bm.faces.new(pane_f)
    bm.faces.new(list(reversed(pane_b)))
    for i in range(6):
        ni = (i+1)%6
        try:
            bm.faces.new([pane_f[i], pane_f[ni], pane_b[ni], pane_b[i]])
        except Exception:
            pass

    # ── corner joint nodes ───────────────────────
    for ox, oy, _ in outer_pts:
        node = bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.12,
            matrix=Matrix.Translation(Vector((ox, oy, 0.0))))

    # ── bevelled centre-strut radials ────────────
    for i in range(6):
        angle = i * TAU/6 + PI/6
        mx = math.cos(angle) * (inner_r * 0.55)
        my = math.sin(angle) * (inner_r * 0.55)
        sv = [bm.verts.new((math.cos(angle + da)*0.04,
                            math.sin(angle + da)*0.04,
                            dz))
              for da, dz in [(-PI/2, 0),( PI/2, 0),
                              (PI/2, -0.03),(-PI/2,-0.03)]]
        ev = [bm.verts.new((mx + math.cos(angle + da)*0.04,
                            my + math.sin(angle + da)*0.04,
                            dz))
              for da, dz in [(-PI/2, 0),( PI/2, 0),
                              (PI/2, -0.03),(-PI/2,-0.03)]]
        try:
            bm.faces.new([sv[0],sv[1],ev[1],ev[0]])
            bm.faces.new([sv[2],sv[3],ev[3],ev[2]])
            bm.faces.new([sv[0],sv[3],ev[3],ev[0]])
            bm.faces.new([sv[1],sv[2],ev[2],ev[1]])
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_gold_emissive", "mat_collector_glass",
                        "mat_ancient_machine_dark"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  HEX COLLECTOR CLUSTER
# ══════════════════════════════════════════════
# 7-tile flower arrangement (1 centre + 6 surrounding).
# Centre connection node where all beam lines converge.
# Matches: Luminous Rift hero image, AD-002.

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_HEX_TILE")
