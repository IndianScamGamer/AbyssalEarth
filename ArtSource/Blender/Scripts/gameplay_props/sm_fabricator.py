"""
SM_FabricatorStation_A — AbyssalEarth procedural mesh.
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
    print("Building SM_FabricatorStation_A …")
    obj, bm = new_mesh("SM_FabricatorStation_A")

    # ── base disc ────────────────────────────────
    base_verts = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                          segments=32, radius=1.1)
    base_faces = [f for f in bm.faces if len(f.verts) > 4]
    extrude_region(bm, base_faces, 0.06, Vector((0, 0, -1)))
    extrude_region(bm, base_faces, 0.04)

    # ── inner recessed groove ring ────────────────
    groove = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                      segments=32, radius=0.9)
    gf = [f for f in bm.faces if f.calc_center_median().z > 0.08
          and f.calc_center_median().length < 0.95]
    bmesh.ops.translate(bm, verts=groove['verts'], vec=Vector((0, 0, 0.04)))

    # ── raised central hex plinth ──────────────────
    hex_verts = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                         segments=6, radius=0.42)
    bmesh.ops.translate(bm, verts=hex_verts['verts'], vec=Vector((0, 0, 0.10)))
    hf = [f for f in bm.faces
          if all(abs(v.co.z - 0.10) < 0.01 for v in f.verts) and
          f.calc_center_median().length < 0.45]
    if hf:
        extrude_region(bm, hf, 0.30)
        # bevel top
        top_faces = [f for f in bm.faces
                     if all(abs(v.co.z - 0.40) < 0.01 for v in f.verts)
                     and f.calc_center_median().length < 0.45]

    # ── 6 radial arms ─────────────────────────────
    for i in range(6):
        angle = i * TAU / 6
        dx, dy = math.cos(angle), math.sin(angle)
        # arm box: thin rectangular prism
        arm_verts = []
        w, h, l = 0.06, 0.06, 0.58          # width, height, length
        for sx in (-1, 1):
            for sy in (-1, 1):
                for sz in (0, 1):
                    lx = dx * (0.42 + sz * l) - dy * sx * w
                    ly = dy * (0.42 + sz * l) + dx * sx * w
                    lz = 0.10 + sy * h
                    arm_verts.append(bm.verts.new((lx, ly, lz)))
        bm.verts.ensure_lookup_table()
        # faces: 6 faces of box (skip for brevity — build as loop)
        v = arm_verts
        faces_idx = [(0,1,3,2),(4,5,7,6),(0,4,6,2),(1,5,7,3),
                     (0,1,5,4),(2,3,7,6)]
        for fi in faces_idx:
            try:
                bm.faces.new([v[j] for j in fi])
            except Exception:
                pass

        # node at tip: small sphere approximation (ico)
        cx = dx * (0.42 + 0.58 + 0.09)
        cy = dy * (0.42 + 0.58 + 0.09)
        node_verts = bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.09,
            matrix=Matrix.Translation(Vector((cx, cy, 0.16))))['verts']

    # ── central orb socket ─────────────────────────
    orb = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.14,
                                      matrix=Matrix.Translation(
                                          Vector((0, 0, 0.50))))
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  2. INTERFACE TERMINAL
# ══════════════════════════════════════════════
# Wall-mounted ancient terminal. Thick backplate, central circular display
# with radial petal geometry, 4 small control nodes at cardinal directions.
# Matches: ancient_terminal_concept.png

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_FabricatorStation_A")
