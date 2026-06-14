"""
SM_HeliosRobot_Static — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Slice')

def build():
    print("Building SM_HeliosRobot_Static …")
    obj, bm = new_mesh("SM_HeliosRobot_Static")

    def sphere(cx, cy, cz, r, subdiv=1):
        return bmesh.ops.create_icosphere(
            bm, subdivisions=subdiv, radius=r,
            matrix=Matrix.Translation(Vector((cx, cy, cz))))['verts']

    def cyl(cx, cy, cz, r, h, segs=10):
        return bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=False, segments=segs,
            radius1=r, radius2=r, depth=h,
            matrix=Matrix.Translation(Vector((cx, cy, cz + h/2))))['verts']

    # ── pelvis ─────────────────────────────────────
    sphere(0, 0, 0.88, 0.12, 2)

    # ── torso ──────────────────────────────────────
    cyl(0, 0, 0.94, 0.16, 0.40)                    # lower torso
    cyl(0, 0, 1.32, 0.17, 0.14)                    # chest
    sphere(0, 0, 1.50, 0.155, 2)                   # shoulder yoke

    # ── neck + head ────────────────────────────────
    cyl(0, 0, 1.52, 0.04, 0.07)                    # neck
    sphere(0, 0, 1.64, 0.095, 2)                   # head
    # faceplate (oval inset — flattened sphere)
    fv = sphere(0.0, -0.10, 1.64, 0.070, 1)
    for v in fv:
        v.co.y += 0.04
        v.co.z = 1.64 + (v.co.z - 1.64) * 0.55    # squash

    # ── left arm ──────────────────────────────────
    sphere(-0.22, 0, 1.50, 0.055)                  # shoulder joint (black)
    cyl(-0.22, 0, 1.20, 0.042, 0.30)               # upper arm
    sphere(-0.22, 0, 1.18, 0.048)                  # elbow joint (black)
    cyl(-0.22, 0, 0.90, 0.036, 0.28)               # lower arm
    sphere(-0.22, 0, 0.88, 0.04)                   # wrist
    cyl(-0.22, 0, 0.76, 0.035, 0.12, 8)            # hand

    # ── right arm (mirror) ─────────────────────────
    sphere(0.22, 0, 1.50, 0.055)
    cyl(0.22, 0, 1.20, 0.042, 0.30)
    sphere(0.22, 0, 1.18, 0.048)
    cyl(0.22, 0, 0.90, 0.036, 0.28)
    sphere(0.22, 0, 0.88, 0.04)
    cyl(0.22, 0, 0.76, 0.035, 0.12, 8)

    # ── left leg ──────────────────────────────────
    sphere(-0.10, 0, 0.88, 0.052)                  # hip joint
    cyl(-0.10, 0, 0.56, 0.055, 0.32)               # thigh
    sphere(-0.10, 0, 0.54, 0.052)                  # knee
    cyl(-0.10, 0, 0.24, 0.046, 0.30)               # shin
    # foot
    fv = [bm.verts.new((-0.10 + dx*0.05, dy*0.04, 0.04))
          for dx in (-1.4, -0.4, 0.6, 1.0) for dy in (-1, 1)]
    bm.faces.new([fv[0],fv[2],fv[4],fv[6]])
    bm.faces.new([fv[1],fv[3],fv[5],fv[7]])

    # ── right leg (mirror) ─────────────────────────
    sphere(0.10, 0, 0.88, 0.052)
    cyl(0.10, 0, 0.56, 0.055, 0.32)
    sphere(0.10, 0, 0.54, 0.052)
    cyl(0.10, 0, 0.24, 0.046, 0.30)
    rfv = [bm.verts.new((0.10 + dx*0.05, dy*0.04, 0.04))
           for dx in (-1.4, -0.4, 0.6, 1.0) for dy in (-1, 1)]
    bm.faces.new([rfv[0],rfv[2],rfv[4],rfv[6]])
    bm.faces.new([rfv[1],rfv[3],rfv[5],rfv[7]])

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_ancient_machine_dark"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_HeliosRobot_Static")
    return obj


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_HeliosRobot_Static")
