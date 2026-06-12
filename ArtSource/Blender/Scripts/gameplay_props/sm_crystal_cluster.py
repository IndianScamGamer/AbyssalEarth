"""
SM_CRYSTAL_CLUSTER — AbyssalEarth procedural mesh.
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

def build_variant(name, base_r, crystal_count, heights, rock_r):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)

    # ── basalt rock base ──────────────────────────
    rock = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=rock_r)
    # flatten bottom
    for v in rock['verts']:
        if v.co.z < -rock_r * 0.4:
            v.co.z = -rock_r * 0.4
        elif v.co.z < 0:
            v.co.z *= 0.4
    # add some rocky asymmetry
    import random; random.seed(hash(name) % 999)
    for v in rock['verts']:
        v.co += Vector((random.uniform(-0.03, 0.03)*rock_r,
                        random.uniform(-0.03, 0.03)*rock_r,
                        random.uniform(-0.02, 0.02)*rock_r))

    # ── crystal spires ────────────────────────────
    for i in range(crystal_count):
        angle  = i * TAU / crystal_count + random.uniform(-0.2, 0.2)
        spread = random.uniform(0.05, base_r * 0.6)
        cx     = math.cos(angle) * spread
        cy     = math.sin(angle) * spread
        h      = heights[i % len(heights)] * random.uniform(0.85, 1.15)
        w      = h * random.uniform(0.12, 0.18)
        tilt   = Vector((random.uniform(-0.15,0.15), random.uniform(-0.15,0.15),1)).normalized()

        # crystal = tapered prism with 5 sides (pentagon cross-section)
        sides = 5
        base_pts, top_pts = [], []
        for s in range(sides):
            a2 = s * TAU / sides + random.uniform(-0.1, 0.1)
            bx = cx + math.cos(a2) * w
            by = cy + math.sin(a2) * w
            base_pts.append(bm.verts.new((bx, by, 0.0)))
            tx = cx + math.cos(a2) * w * 0.07 + tilt.x * h * 0.25
            ty = cy + math.sin(a2) * w * 0.07 + tilt.y * h * 0.25
            top_pts.append(bm.verts.new((tx, ty, h)))

        # tip
        tip = bm.verts.new((cx + tilt.x*h*0.1, cy + tilt.y*h*0.1, h*1.05))

        # build faces
        bm.faces.new(list(reversed(base_pts)))       # base cap
        for s in range(sides):
            ns = (s + 1) % sides
            bm.faces.new([base_pts[s], base_pts[ns],
                          top_pts[ns],  top_pts[s]])  # side quad
        for s in range(sides):
            ns = (s + 1) % sides
            bm.faces.new([top_pts[s], top_pts[ns], tip])  # tip tris

    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  4. DEPLOYABLE BEACON
# ══════════════════════════════════════════════
# Compact expedition stake. 50cm stake, ring light band at mid-point,
# small base disc with grip teeth, top emitter dome.
# Matches: Regenerated/Beacon/deployable_beacon_prop_concept.png

VARIANTS = [
    ('SM_HarvestableNode_S', 0.18, 3, [0.28, 0.22, 0.32], 0.16),
    ('SM_HarvestableNode_M', 0.28, 5, [0.55, 0.4, 0.65, 0.45, 0.5], 0.24),
    ('SM_HarvestableNode_L', 0.4, 7, [0.9, 0.75, 1.05, 0.8, 0.7, 0.95, 0.85], 0.34),
]


def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_CRYSTAL_CLUSTER")
