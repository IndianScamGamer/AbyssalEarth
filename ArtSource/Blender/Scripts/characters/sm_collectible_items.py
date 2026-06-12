"""
SM_COLLECTIBLE_ITEMS — AbyssalEarth procedural mesh.
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

EXPORT_DIR = get_export_dir('Characters')

def build():
    """Batch: crystal shard, data chip, ancient coin, fabricator core."""

    items = [
        ("SM_Item_CrystalShard_A", "mat_crystal_blue"),
        ("SM_Item_DataChip_A",     "mat_human_equipment"),
        ("SM_Item_AncientCoin_A",  "mat_gold_emissive"),
        ("SM_Item_FabricatorCore_A","mat_blue_emissive"),
    ]

    for idx, (name, mat_name) in enumerate(items):
        clear_scene()
        ob, me = new_mesh(name)
        bm = bmesh.new()

        if "Crystal" in name:
            # Hexagonal prism shard — faceted top
            result = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                                segments=6, radius1=0.06, radius2=0.015,
                                                depth=0.18,
                                                matrix=Matrix.Translation((0, 0, 0.09)))
            for v in bm.verts:
                if v.co.z > 0.12:
                    v.co.z += 0.05 * (v.co.z - 0.12) * 3

        elif "DataChip" in name:
            # Thin rectangular chip with notch
            bmesh.ops.create_cube(bm, size=0.10,
                                   matrix=Matrix.Scale(1.0, 4) @ Matrix.Translation((0, 0, 0.015))
                                   @ Matrix.Scale(0.12, 4, (0, 0, 1)))
            # Notch corner
            bmesh.ops.create_cube(bm, size=0.025,
                                   matrix=Matrix.Translation((0.04, 0.04, 0.015)))

        elif "AncientCoin" in name:
            # Disc with radial grooves
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=16, radius1=0.065, radius2=0.065,
                                       depth=0.012,
                                       matrix=Matrix.Translation((0, 0, 0.006)))
            # Inner ring detail
            bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                                       segments=16, radius1=0.042, radius2=0.042,
                                       depth=0.013,
                                       matrix=Matrix.Translation((0, 0, 0.006)))

        elif "FabricatorCore" in name:
            # Small dodecahedron-ish: scaled icosphere
            result = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.07,
                                                 matrix=Matrix.Translation((0, 0, 0.07)))
            # Equatorial band
            bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                                       segments=12, radius1=0.075, radius2=0.075,
                                       depth=0.018,
                                       matrix=Matrix.Translation((0, 0, 0.07)))

        finalise(ob, me, bm)
        smart_uv(ob)
        add_mat_slots(ob, [mat_name])
        set_origin_to_base(ob)
        export_fbx(ob, EXPORT_DIR, name)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ SM_COLLECTIBLE_ITEMS")
