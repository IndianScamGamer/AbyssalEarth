"""
SM_Rift_BeamEmitterNode_A — AbyssalEarth procedural mesh.
Run standalone:  blender --background --python <this_file>.py
Concept: LR-007, LR-008
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
    print("Building SM_Rift_BeamEmitterNode_A …")
    obj, bm = new_mesh("SM_Rift_BeamEmitterNode_A")

    segs = 20
    # ── mounting disc ─────────────────────────────
    disc = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                    segments=segs, radius=1.1)
    bmesh.ops.translate(bm, verts=disc['verts'], vec=Vector((0, 0, 0)))
    df = [f for f in bm.faces if f.calc_center_median().length < 1.15
          and abs(f.calc_center_median().z) < 0.01]
    if df:
        back = bmesh.ops.extrude_face_region(bm, geom=df)
        bverts = [v for v in back['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=bverts, vec=Vector((0, 0, -0.35)))

    # ── concave emitter face ──────────────────────
    inner = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=segs, radius=0.70)
    bmesh.ops.translate(bm, verts=inner['verts'], vec=Vector((0, 0, 0.12)))
    emf = [f for f in bm.faces if f.calc_center_median().length < 0.72
           and abs(f.calc_center_median().z - 0.12) < 0.01]
    if emf:
        em_back = bmesh.ops.extrude_face_region(bm, geom=emf)
        emverts = [v for v in em_back['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=emverts, vec=Vector((0, 0, -0.22)))

    # ── gold emissive ring ─────────────────────────
    for r_off in [0.80, 0.90]:
        rv = [bm.verts.new((math.cos(i*TAU/segs)*r_off,
                            math.sin(i*TAU/segs)*r_off, 0.06))
              for i in range(segs)]
        for i in range(segs):
            ni=(i+1)%segs
            bv = [bm.verts.new((rv[i].co.x, rv[i].co.y, -0.01)),
                  bm.verts.new((rv[ni].co.x,rv[ni].co.y,-0.01))]
            try:
                bm.faces.new([rv[i],rv[ni],bv[1],bv[0]])
            except Exception:
                pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Rift_BeamEmitterNode_A")
    return obj


# ══════════════════════════════════════════════
#  BRIDGE SPAN
# ══════════════════════════════════════════════
# Layered slab construction, 24m long × 8m wide. Circular insets, blue strips,
# exposed broken undersides on variant B. Matches: ancient_bridge_platform_kit_concept.png

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_Rift_BeamEmitterNode_A")
