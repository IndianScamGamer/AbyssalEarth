"""
SM_Rift_AncientWall_Gate_A — AbyssalEarth procedural mesh.
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

def build():
    print("Building SM_Rift_AncientWall_Gate_A …")
    obj, bm = new_mesh("SM_Rift_AncientWall_Gate_A")

    rng = random.Random(17)
    w, h, d = 25.0, 50.0, 6.0

    # ── main wall body ────────────────────────────
    nx, nz = 8, 12
    verts = []
    for ix in range(nx):
        col = []
        for iz in range(nz):
            x = (ix/(nx-1) - 0.5) * w + rng.uniform(-0.3, 0.3)
            z =  iz/(nz-1)       * h + rng.uniform(-0.2, 0.2)
            y = -d * 0.5 + math.sin(x*0.3)*1.2 + math.cos(z*0.15)*0.8
            col.append(bm.verts.new((x, y, z)))
        verts.append(col)

    for ix in range(nx-1):
        for iz in range(nz-1):
            try:
                bm.faces.new([verts[ix][iz], verts[ix+1][iz],
                               verts[ix+1][iz+1], verts[ix][iz+1]])
            except Exception:
                pass

    # ── two large circular socket features ────────
    for sock_cx, sock_cz in [(-6.0, 20.0), (5.0, 38.0)]:
        sock_r = rng.uniform(4.5, 6.0)
        # outer ring
        for r_off in [sock_r, sock_r-0.8, sock_r-2.2]:
            rv = [bm.verts.new((
                     sock_cx + math.cos(a*TAU/24)*r_off,
                     0.2 + (r_off - sock_r)*0.15,
                     sock_cz + math.sin(a*TAU/24)*r_off))
                  for a in range(24)]
            for i in range(24):
                ni=(i+1)%24
                bv = [bm.verts.new((rv[i].co.x, rv[i].co.y-0.35, rv[i].co.z)),
                      bm.verts.new((rv[ni].co.x,rv[ni].co.y-0.35,rv[ni].co.z))]
                try:
                    bm.faces.new([rv[i], rv[ni], bv[1], bv[0]])
                except Exception:
                    pass

        # emissive centre disc
        cv = [bm.verts.new((sock_cx + math.cos(a*TAU/12)*(sock_r-2.5),
                            0.25,
                            sock_cz + math.sin(a*TAU/12)*(sock_r-2.5)))
              for a in range(12)]
        try:
            bm.faces.new(cv)
        except Exception:
            pass

    # ── 4 radial groove lines ─────────────────────
    for gx in (-9.0, -3.0, 3.0, 9.0):
        for iz in range(nz):
            z0 = iz/(nz-1) * h
            z1 = (iz+1)/(nz-1) * h if iz < nz-1 else h
            gv = [bm.verts.new((gx - 0.12, -0.08, z0)),
                  bm.verts.new((gx + 0.12, -0.08, z0)),
                  bm.verts.new((gx + 0.12, -0.08, z1)),
                  bm.verts.new((gx - 0.12, -0.08, z1))]
            try:
                bm.faces.new(gv)
            except Exception:
                pass

    # ── rock intrusion base ───────────────────────
    for rx, rr in [(-10, 3.5), (8, 2.8), (0, 4.2)]:
        res = bmesh.ops.create_icosphere(bm, subdivisions=2,
                                          radius=rr)
        for v in res['verts']:
            v.co.x += rx
            v.co.y -= d * 0.3
            if v.co.z < 0:
                v.co.z *= 0.25

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark",
                        "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_AncientWall_Gate_A")
    return obj


# ══════════════════════════════════════════════
#  TOWER SEGMENTS
# ══════════════════════════════════════════════
# Distant silhouette towers. Vertical grooves, cyan emissive strips,
# broken tops. Matches: AD-003 (Tower Segment — Distant Structure).

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Rift_AncientWall_Gate_A")
