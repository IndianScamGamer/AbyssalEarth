"""
SM_InterfaceTerminal_A — AbyssalEarth procedural mesh.
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
    print("Building SM_InterfaceTerminal_A …")
    obj, bm = new_mesh("SM_InterfaceTerminal_A")

    # ── backplate ─────────────────────────────────
    bmesh.ops.create_grid(bm, x_segments=4, y_segments=6, size=1.0)
    bm.verts.ensure_lookup_table()
    # select all faces and extrude back
    back_faces = list(bm.faces)
    extrude_region(bm, back_faces, 0.12, Vector((0, -1, 0)))

    # ── display circle ring ───────────────────────
    outer = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=24, radius=0.44)
    bmesh.ops.translate(bm, verts=outer['verts'], vec=Vector((0, 0.14, 0.10)))
    inner = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=24, radius=0.28)
    bmesh.ops.translate(bm, verts=inner['verts'], vec=Vector((0, 0.14, 0.10)))

    # ── 8 petal segments around display ──────────
    for i in range(8):
        angle = i * TAU / 8 + TAU / 16
        r_in, r_out = 0.30, 0.42
        a0, a1 = angle - TAU/24, angle + TAU/24
        pts = [
            (math.cos(a0)*r_in,  0.16, 0.10 + math.sin(a0)*r_in),
            (math.cos(a1)*r_in,  0.16, 0.10 + math.sin(a1)*r_in),
            (math.cos(a1)*r_out, 0.16, 0.10 + math.sin(a1)*r_out),
            (math.cos(a0)*r_out, 0.16, 0.10 + math.sin(a0)*r_out),
        ]
        face_verts = [bm.verts.new(p) for p in pts]
        pf = bm.faces.new(face_verts)
        # extrude petal slightly
        extrude_region(bm, [pf], 0.02)

    # ── 4 control nodes ───────────────────────────
    for a in (0, PI/2, PI, 3*PI/2):
        cx = math.cos(a) * 0.58
        cz = 0.10 + math.sin(a) * 0.58
        bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.055,
            matrix=Matrix.Translation(Vector((cx, 0.16, cz))))

    # ── gold ring bezel ────────────────────────────
    bezel = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=32, radius=0.46)
    bmesh.ops.translate(bm, verts=bezel['verts'], vec=Vector((0, 0.15, 0.10)))
    bm.faces.ensure_lookup_table()
    ring_faces = [f for f in bm.faces
                  if abs(f.calc_center_median().y - 0.15) < 0.01
                  and 0.43 < f.calc_center_median().xz.length < 0.47]
    if ring_faces:
        extrude_region(bm, ring_faces, 0.025)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_blue_emissive",
                        "mat_gold_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_InterfaceTerminal_A")
    return obj


# ══════════════════════════════════════════════
#  3. HARVESTABLE CRYSTAL NODES
# ══════════════════════════════════════════════
# Three sizes: S (~50cm), M (~90cm), L (~140cm)
# Dark basalt rock base with angular faceted crystal spires.
# Matches: blue_crystal_harvestable_concept.png

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_InterfaceTerminal_A")
