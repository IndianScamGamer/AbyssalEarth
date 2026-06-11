#!/usr/bin/env python3
"""
generate_asset_scripts.py
Reads the 7 monolithic Blender scripts and splits each build_* function
into its own individual .py file in the correct category folder.

Run from the repo root:
    python3 Tools/generate_asset_scripts.py
"""

import os
import re
import textwrap

SCRIPTS_DIR = os.path.join("ArtSource", "Blender", "Scripts")

# ─────────────────────────────────────────────
# Shared utils.py content
# ─────────────────────────────────────────────

SHARED_UTILS = '''"""
shared/utils.py — Common helpers for all AbyssalEarth Blender asset scripts.
Import with:
    from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                               add_mat_slots, set_origin_to_base, export_fbx,
                               get_export_dir, mat_color, extrude_region)
"""
import bpy
import bmesh
import math
import os
from mathutils import Matrix, Vector

TAU = math.tau
PI  = math.pi


def _get_repo_root():
    """Walk up from this file to find the directory containing Content/."""
    path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isdir(os.path.join(path, "Content")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    raise RuntimeError("Cannot find repo root (no Content/ directory found)")


def get_export_dir(subpath):
    """Return and create Content/ArtSourceExports/<subpath>."""
    d = os.path.join(_get_repo_root(), "Content", "ArtSourceExports", subpath)
    os.makedirs(d, exist_ok=True)
    return d


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def new_mesh(name):
    mesh = bpy.data.meshes.new(name)
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj, bmesh.new()


def finalise(obj, bm):
    bm.to_mesh(obj.data)
    bm.free()
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def smart_uv(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")


_MATERIAL_COLORS = {
    "mat_ancient_machine_dark":   (0.05, 0.05, 0.06, 1),
    "mat_ancient_machine_edge_wear": (0.12, 0.11, 0.10, 1),
    "mat_gold_emissive":          (1.00, 0.72, 0.10, 1),
    "mat_blue_emissive":          (0.05, 0.45, 1.00, 1),
    "mat_crystal_blue":           (0.10, 0.60, 1.00, 1),
    "mat_wet_basalt":             (0.08, 0.08, 0.09, 1),
    "mat_human_equipment":        (0.18, 0.16, 0.14, 1),
    "mat_collector_glass":        (0.60, 0.85, 1.00, 1),
    "mat_orb_energy":             (0.40, 0.80, 1.00, 1),
    "mat_lava_emissive":          (1.00, 0.25, 0.00, 1),
    "mat_purple_emissive":        (0.55, 0.10, 1.00, 1),
    "mat_red_emissive_vein":      (1.00, 0.05, 0.05, 1),
    "mat_glass_bark":             (0.60, 0.90, 0.80, 1),
    "mat_water_bioluminescent":   (0.00, 0.55, 0.65, 1),
    # Biome-specific
    "mat_bone_stone":             (0.82, 0.78, 0.70, 1),
    "mat_cyan_fossil_vein":       (0.00, 0.80, 0.75, 1),
    "mat_glassroot_translucent":  (0.55, 0.90, 0.75, 1),
    "mat_red_sap":                (0.70, 0.08, 0.05, 1),
    "mat_pearl_stone":            (0.88, 0.85, 0.82, 1),
    "mat_wet_edge":               (0.10, 0.12, 0.14, 1),
    "mat_dark_basalt":            (0.06, 0.06, 0.07, 1),
    "mat_amber_stabilizer":       (1.00, 0.60, 0.10, 1),
    "mat_obsidian":               (0.04, 0.03, 0.04, 1),
    "mat_heat_crack":             (1.00, 0.35, 0.00, 1),
    "mat_heat_bloom":             (1.00, 0.50, 0.10, 1),
    "mat_magenta_mineral":        (0.85, 0.10, 0.65, 1),
    "mat_fossil_bone":            (0.80, 0.76, 0.68, 1),
}


def mat_color(name):
    return _MATERIAL_COLORS.get(name, (0.50, 0.50, 0.50, 1))


def add_mat_slots(obj, names):
    for name in names:
        if name not in bpy.data.materials:
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = mat_color(name)
        obj.data.materials.append(bpy.data.materials[name])


def set_origin_to_base(obj):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    min_z = min((obj.matrix_world @ v.co).z for v in obj.data.vertices)
    bpy.context.scene.cursor.location = (obj.location.x, obj.location.y, min_z)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    obj.location = (0, 0, 0)


def export_fbx(obj, export_dir, filename):
    """Export obj as FBX.  filename should NOT include .fbx extension."""
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = os.path.join(export_dir, filename + ".fbx")
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        global_scale=100.0,
        apply_unit_scale=True,
        apply_scale_options="FBX_SCALE_ALL",
        mesh_smooth_type="FACE",
        use_mesh_modifiers=True,
        bake_anim=False,
    )
    print(f"  [export] {path}")


def add_subdivision(obj, levels=1):
    mod = obj.modifiers.new("Subsurf", "SUBSURF")
    mod.levels = levels
    mod.render_levels = levels


def extrude_region(bm, faces, dist, direction=None):
    if direction is None:
        direction = faces[0].normal.copy()
    geom = bmesh.ops.extrude_face_region(bm, geom=faces)
    verts = [e for e in geom["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts, vec=direction * dist)
    return [f for f in geom["geom"] if isinstance(f, bmesh.types.BMFace)]
'''

# ─────────────────────────────────────────────
# Map: source monolithic file → (category_folder, export_subpath, [assets])
# Each asset: (sm_name, build_func_name_in_source, filename_override)
# ─────────────────────────────────────────────

CATEGORY_MAP = [
    # (source_file, folder, depth_to_scripts_root, export_subpath)
    ("gen_gameplay_props.py",       "gameplay_props",          1, "Slice"),
    ("gen_luminous_rift_env.py",    "luminous_rift_env",       1, "LuminousRift"),
    ("gen_luminous_rift_machines.py","luminous_rift_machines", 1, "LuminousRift"),
    ("gen_human_survey_kit.py",     "human_survey_kit",        1, "Slice"),
    ("gen_world_biomes.py",         "world_biomes",            1, None),   # sub-biome logic below
    ("gen_characters.py",           "characters",              1, "Characters"),
    ("gen_prologue_submarine.py",   "prologue_submarine",      1, None),   # sub-folder logic below
]

# World biomes sub-folder map: function name prefix → (subfolder, export_subpath)
BIOME_SUBFOLDER = {
    "fossil_sky":   ("fossil_sky",      "FossilSky"),
    "rib_arch":     ("fossil_sky",      "FossilSky"),
    "spine":        ("fossil_sky",      "FossilSky"),
    "wood_dock_fossil": ("fossil_sky",  "FossilSky"),
    "glassroot":    ("glassroot_forest","GlassrootForest"),
    "trunk":        ("glassroot_forest","GlassrootForest"),
    "floating_plat":("glassroot_forest","GlassrootForest"),
    "gravity":      ("gravity_well",    "GravityWell"),
    "portal":       ("gravity_well",    "GravityWell"),
    "inner_sea":    ("inner_sea",       "InnerSea"),
    "stalactite":   ("inner_sea",       "InnerSea"),
    "wood_dock":    ("inner_sea",       "InnerSea"),
    "mantle":       ("mantle_garden",   "MantleGarden"),
    "lava":         ("mantle_garden",   "MantleGarden"),
    "purple_crystal":("mantle_garden",  "MantleGarden"),
    "steam_column": ("mantle_garden",   "MantleGarden"),
}

# Prologue sub-folder map
PROLOGUE_SUBFOLDER = {
    "corridor":   ("submarine", "Prologue"),
    "bulkhead":   ("submarine", "Prologue"),
    "bunk":       ("submarine", "Prologue"),
    "engine":     ("submarine", "Prologue"),
    "airlock":    ("submarine", "Prologue"),
    "pipe":       ("submarine", "Prologue"),
    "shaft":      ("elevator_shaft", "ElevatorShaft"),
    "elevator":   ("elevator_shaft", "ElevatorShaft"),
    "crashed":    ("elevator_shaft", "ElevatorShaft"),
    "mechanism":  ("elevator_shaft", "ElevatorShaft"),
    "debris":     ("elevator_shaft", "ElevatorShaft"),
}


def extract_top_level_functions(source_code):
    """Return list of (func_name, func_source_code) for all top-level defs."""
    lines = source_code.split("\n")
    functions = []
    i = 0
    while i < len(lines):
        m = re.match(r'^def (\w+)\(', lines[i])
        if m:
            fname = m.group(1)
            start = i
            # collect until next top-level def or end
            j = i + 1
            while j < len(lines):
                if re.match(r'^def \w+\(', lines[j]) or re.match(r'^class \w+', lines[j]):
                    break
                j += 1
            func_lines = lines[start:j]
            # strip trailing blank lines
            while func_lines and not func_lines[-1].strip():
                func_lines.pop()
            functions.append((fname, "\n".join(func_lines)))
            i = j
        else:
            i += 1
    return functions


def make_file_header(sm_name, depth_to_scripts_root, export_subpath):
    dots = os.path.join(*(['..'] * depth_to_scripts_root))
    return f'''"""
{sm_name} — AbyssalEarth procedural mesh.
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
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, {', '.join(repr('..') for _ in range(depth_to_scripts_root))}))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, mat_color, extrude_region,
                           add_subdivision, TAU, PI)

EXPORT_DIR = get_export_dir({repr(export_subpath)})

'''


def make_file_footer(build_func_name, sm_name):
    return f'''

if __name__ == "__main__":
    clear_scene()
    build()
    print(f"  ✓ {sm_name}")
'''


def sanitize_func_body(func_src, original_func_name):
    """Rename function to build(), remove local helper imports, fix EXPORT_ROOT refs."""
    # rename def original_name( → def build(
    func_src = re.sub(
        rf'^def {re.escape(original_func_name)}\(',
        'def build(',
        func_src
    )
    # strip internal 'import random' lines (already in header)
    func_src = re.sub(r'^\s*import random\s*$', '', func_src, flags=re.MULTILINE)
    # remove export_fbx calls that use old signature (2-arg)
    # old: export_fbx(obj, "SM_X.fbx")
    # new: export_fbx(obj, EXPORT_DIR, "SM_X")
    def fix_export(m):
        obj_arg = m.group(1)
        fname = m.group(2).rstrip('.fbx').strip('"').strip("'")
        return f'export_fbx({obj_arg}, EXPORT_DIR, "{fname}")'
    func_src = re.sub(
        r'export_fbx\((\w+),\s*["\']([^"\']+)["\']\)',
        fix_export,
        func_src
    )
    return func_src


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def write_empty_init(folder):
    path = os.path.join(folder, '__init__.py')
    os.makedirs(folder, exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass


def infer_biome_subfolder(func_name, func_src):
    """Return (subfolder, export_subpath) for a world_biomes build function."""
    fn = func_name.lower()
    # Direct matches
    for key, val in BIOME_SUBFOLDER.items():
        if key in fn:
            return val
    # Try to infer from SM_ name in function body
    m = re.search(r'new_mesh\(["\']SM_([\w]+)', func_src)
    if m:
        sm = m.group(1).lower()
        for key, val in BIOME_SUBFOLDER.items():
            if key in sm:
                return val
    return ("fossil_sky", "FossilSky")  # fallback


def infer_prologue_subfolder(func_name):
    fn = func_name.lower()
    for key, val in PROLOGUE_SUBFOLDER.items():
        if key in fn:
            return val
    return ("submarine", "Prologue")


def get_sm_name(func_src, func_name):
    """Extract SM_ name from new_mesh() call in function body."""
    m = re.search(r'new_mesh\(["\']([^"\']+)["\']', func_src)
    if m:
        return m.group(1)
    return func_name.replace('build_', 'SM_').upper()


def func_name_to_file(func_name):
    """build_crystal_cluster → sm_crystal_cluster"""
    name = re.sub(r'^build_', 'sm_', func_name)
    return name.lower()


# ─────────────────────────────────────────────
# Extra new assets not in existing scripts
# ─────────────────────────────────────────────

NEW_ASSETS = {
    "world_biomes/fossil_sky": [
        ("SM_FossilSky_GiantRib_A",
         "fossil_sky", "FossilSky",
         "sm_fossil_sky_giant_rib_a",
         '''
def build():
    """SM_FossilSky_GiantRib_A — single 25m parabolic rib arch, bone cross-section."""
    import random; random.seed(55)
    obj, bm = new_mesh("SM_FossilSky_GiantRib_A")
    SEGS = 22
    SPAN = 25.0
    HEIGHT = 22.0
    for i in range(SEGS + 1):
        t = i / SEGS
        x = (t - 0.5) * SPAN
        z = HEIGHT * math.sin(t * math.pi)
        # oval cross-section: 0.7 wide x 1.0 tall
        for ci in range(8):
            a = ci * TAU / 8
            cx = x + math.cos(a) * 0.35 * random.uniform(0.92, 1.08)
            cz = z + math.sin(a) * 0.50 * random.uniform(0.92, 1.08)
            bm.verts.new((cx, math.sin(a) * 0.20, cz))
    bm.verts.ensure_lookup_table()
    v = bm.verts
    n = 8
    for ring in range(SEGS):
        base = ring * n
        for i in range(n):
            ni = (i + 1) % n
            bm.faces.new([v[base+i], v[base+ni],
                           v[base+n+ni], v[base+n+i]])
    for cap_base in [0, SEGS*n]:
        bm.faces.new([v[cap_base + i] for i in range(n)])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_GiantRib_A")
    return obj
'''),

        ("SM_FossilSky_ObservationWalkway_A",
         "fossil_sky", "FossilSky",
         "sm_fossil_sky_observation_walkway_a",
         '''
def build():
    """SM_FossilSky_ObservationWalkway_A — 4×40m suspended walkway, bone planks."""
    obj, bm = new_mesh("SM_FossilSky_ObservationWalkway_A")
    W, L, THICK = 4.0, 40.0, 0.18
    # deck planks
    for i in range(20):
        px = -L/2 + i*2.1 + 0.5
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((px, 0, 0))
            @ Matrix.Scale(1.9, 4, (1,0,0))
            @ Matrix.Scale(W, 4, (0,1,0))
            @ Matrix.Scale(THICK, 4, (0,0,1)))
    # metal bracket supports every 4m
    for bx in range(-18, 20, 4):
        for side in [-1, 1]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
                radius=0.05, depth=2.0,
                matrix=Matrix.Translation((bx, side*W*0.4, 0.9)))
            # anchor node
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.08,
                matrix=Matrix.Translation((bx, side*W*0.4, 1.9)))
    # side rails
    for side in [-1, 1]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
            radius=0.04, depth=L,
            matrix=Matrix.Translation((0, side*W*0.48, 1.0))
            @ Matrix.Rotation(TAU/4, 4, 'Y'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_ancient_machine_dark", "mat_ancient_machine_edge_wear"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_ObservationWalkway_A")
    return obj
'''),

        ("SM_FossilSky_CeilingSkeleton_Hero_A",
         "fossil_sky", "FossilSky",
         "sm_fossil_sky_ceiling_skeleton_hero_a",
         '''
def build():
    """SM_FossilSky_CeilingSkeleton_Hero_A — 120m hero ceiling fossil."""
    import random; random.seed(13)
    obj, bm = new_mesh("SM_FossilSky_CeilingSkeleton_Hero_A")
    # spine chain
    SPINE_LEN = 120.0
    SPINE_SEGS = 30
    for i in range(SPINE_SEGS):
        t = i / (SPINE_SEGS-1)
        sx = (t - 0.5) * SPINE_LEN
        sz = random.uniform(-1.5, 1.5)
        r = 1.2 - t * 0.6
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r,
            matrix=Matrix.Translation((sx, 0, sz)))
    # 6 large ribs
    for ri in range(6):
        t = (ri + 1) / 7
        rx = (t - 0.5) * SPINE_LEN * 0.85
        for side in [-1, 1]:
            RIB_SPAN = random.uniform(8, 16)
            RIB_H = random.uniform(6, 12)
            SEGS = 10
            for si in range(SEGS + 1):
                rt = si / SEGS
                x = rx + side * math.sin(rt * math.pi) * RIB_SPAN
                z = -RIB_H * math.sin(rt * math.pi) + random.uniform(-0.3, 0.3)
                bmesh.ops.create_icosphere(bm, subdivisions=1,
                    radius=0.35 * (1-rt*0.7),
                    matrix=Matrix.Translation((x, side*0.4, z)))
    # skull mass at one end
    skull_x = -SPINE_LEN * 0.45
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=4.5,
        matrix=Matrix.Translation((skull_x, 0, 0)))
    for eye_side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.2,
            matrix=Matrix.Translation((skull_x - 1.5, eye_side*2.5, 1.0)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_bone_stone", "mat_cyan_fossil_vein"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_FossilSky_CeilingSkeleton_Hero_A")
    return obj
'''),
    ],

    "world_biomes/glassroot_forest": [
        ("SM_Glassroot_RootColumn_S",
         "glassroot_forest", "GlassrootForest",
         "sm_glassroot_root_column_s",
         '''
def build():
    """SM_Glassroot_RootColumn_S — 3m translucent root column, hex tapered."""
    obj, bm = new_mesh("SM_Glassroot_RootColumn_S")
    levels = [(0, 0.28), (0.5, 0.24), (1.2, 0.20), (2.0, 0.15), (3.0, 0.06)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/6)*r, math.sin(i*TAU/6)*r, z))
                for i in range(6)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(6):
            bm.faces.new([lo[i], lo[(i+1)%6], hi[(i+1)%6], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_red_sap"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootColumn_S")
    return obj
'''),

        ("SM_Glassroot_RootColumn_M",
         "glassroot_forest", "GlassrootForest",
         "sm_glassroot_root_column_m",
         '''
def build():
    """SM_Glassroot_RootColumn_M — 10m translucent root column."""
    import random; random.seed(22)
    obj, bm = new_mesh("SM_Glassroot_RootColumn_M")
    levels = [(0,0.55),(0.8,0.50),(2.5,0.44),(5.0,0.36),(8.0,0.22),(10.0,0.09)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/8)*r*(1+random.uniform(-0.05,0.05)),
                               math.sin(i*TAU/8)*r*(1+random.uniform(-0.05,0.05)), z))
                for i in range(8)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(8):
            bm.faces.new([lo[i], lo[(i+1)%8], hi[(i+1)%8], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # root flanges at base
    for i in range(4):
        a = i * TAU/4 + TAU/8
        fx, fy = math.cos(a)*0.90, math.sin(a)*0.90
        for z in [0.0, 0.5, 1.2]:
            t = z/1.2
            bm.verts.new((fx*(1-t), fy*(1-t), z))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_red_sap", "mat_pearl_stone"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootColumn_M")
    return obj
'''),

        ("SM_Glassroot_RootColumn_Hero",
         "glassroot_forest", "GlassrootForest",
         "sm_glassroot_root_column_hero",
         '''
def build():
    """SM_Glassroot_RootColumn_Hero — 50m cathedral hero root column."""
    import random; random.seed(77)
    obj, bm = new_mesh("SM_Glassroot_RootColumn_Hero")
    levels = [(0,2.2),(2,2.0),(8,1.75),(18,1.40),(30,1.0),(42,0.55),(50,0.20)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/12)*r*(1+random.uniform(-0.04,0.04)),
                               math.sin(i*TAU/12)*r*(1+random.uniform(-0.04,0.04)), z))
                for i in range(12)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(12):
            bm.faces.new([lo[i], lo[(i+1)%12], hi[(i+1)%12], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # massive root flanges
    for i in range(6):
        a = i*TAU/6
        for z, ext, w in [(0,3.5,0.6),(1.5,2.5,0.5),(4.0,1.2,0.35)]:
            bm.verts.new((math.cos(a)*(2.2+ext), math.sin(a)*(2.2+ext), z+w*0.5))
    # red vein ridges
    for i in range(5):
        a = i*TAU/5
        for lz in range(0, 50, 3):
            bm.verts.new((math.cos(a)*2.25, math.sin(a)*2.25, lz))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_red_sap", "mat_pearl_stone"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootColumn_Hero")
    return obj
'''),

        ("SM_Glassroot_Terrace_PearlStone_A",
         "glassroot_forest", "GlassrootForest",
         "sm_glassroot_terrace_pearl_stone_a",
         '''
def build():
    """SM_Glassroot_Terrace_PearlStone_A — 12m irregular pearl-white terrace."""
    import random; random.seed(33)
    obj, bm = new_mesh("SM_Glassroot_Terrace_PearlStone_A")
    VERTS = 14
    outer = []
    for i in range(VERTS):
        a = i * TAU / VERTS
        r = 6.0 * random.uniform(0.75, 1.25)
        outer.append(bm.verts.new((math.cos(a)*r, math.sin(a)*r, 0)))
    centre = bm.verts.new((0,0,0))
    for i in range(VERTS):
        bm.faces.new([outer[i], outer[(i+1)%VERTS], centre])
    extrude_region(bm, list(bm.faces), 0.35, Vector((0,0,-1)))
    # rounded top edge bevels
    for v in bm.verts:
        if v.co.z > -0.05:
            dist = (v.co.x**2 + v.co.y**2)**0.5
            v.co.z += max(0, 0.12 * (1 - dist/6))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_pearl_stone", "mat_wet_edge"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_Terrace_PearlStone_A")
    return obj
'''),

        ("SM_Glassroot_RootBridge_A",
         "glassroot_forest", "GlassrootForest",
         "sm_glassroot_root_bridge_a",
         '''
def build():
    """SM_Glassroot_RootBridge_A — 30m organic living root bridge."""
    import random; random.seed(44)
    obj, bm = new_mesh("SM_Glassroot_RootBridge_A")
    L, W = 30.0, 4.0
    # deck — organic path segments
    for i in range(15):
        t = i/14
        dx = random.uniform(-0.3, 0.3)
        bz = -math.sin(t*math.pi)*0.8
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((-L/2 + t*L + dx, 0, bz))
            @ Matrix.Scale(2.2, 4, (1,0,0))
            @ Matrix.Scale(W*(0.85+random.uniform(-0.1,0.1)), 4, (0,1,0))
            @ Matrix.Scale(0.22, 4, (0,0,1)))
    # 3 root ribs underneath spanning the bridge
    for ri in range(3):
        rx = -L/3 + ri*L/3
        for side in [-1, 1]:
            for si in range(8):
                st = si/7
                x = rx + side*math.sin(st*math.pi)*W*0.6
                z = -math.sin(st*math.pi)*2.5 - 0.3
                bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
                    radius=0.15*(1-st*0.5), depth=0.5,
                    matrix=Matrix.Translation((x, 0, z)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glassroot_translucent", "mat_red_sap"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_Glassroot_RootBridge_A")
    return obj
'''),
    ],

    "world_biomes/gravity_well": [
        ("SM_GravityWell_FloatingPlatform_A",
         "gravity_well", "GravityWell",
         "sm_gravity_well_floating_platform_a",
         '''
def build():
    """SM_GravityWell_FloatingPlatform_A — 15m irregular floating rock platform."""
    import random; random.seed(66)
    obj, bm = new_mesh("SM_GravityWell_FloatingPlatform_A")
    result = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=7.5,
        matrix=Matrix.Translation((0,0,1.5)))
    for v in result['verts']:
        v.co.x *= random.uniform(0.85, 1.15)
        v.co.y *= random.uniform(0.85, 1.15)
        if v.co.z < 1.5:
            v.co.z = 1.5 - (1.5 - v.co.z) * 0.35
        else:
            v.co.z = 1.5 + (v.co.z - 1.5) * 0.22
    # anchor cable stubs
    for i in range(4):
        a = i*TAU/4
        bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
            radius=0.15, depth=2.5,
            matrix=Matrix.Translation((math.cos(a)*4, math.sin(a)*4, -0.5)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_dark_basalt", "mat_blue_emissive"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_FloatingPlatform_A")
    return obj
'''),

        ("SM_GravityWell_CurvedTower_A",
         "gravity_well", "GravityWell",
         "sm_gravity_well_curved_tower_a",
         '''
def build():
    """SM_GravityWell_CurvedTower_A — 60m curved ancient stabilizer tower."""
    import random; random.seed(88)
    obj, bm = new_mesh("SM_GravityWell_CurvedTower_A")
    SEGS = 20
    H = 60.0
    rings = []
    for i in range(SEGS + 1):
        t = i/SEGS
        # curve: leans over by 8m at top
        x = math.sin(t*math.pi*0.5)*8.0
        z = t * H
        r = 3.5 - t*2.2
        ring = [bm.verts.new((x + math.cos(j*TAU/10)*r,
                               math.sin(j*TAU/10)*r, z))
                for j in range(10)]
        rings.append(ring)
    for ri in range(SEGS):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(10):
            bm.faces.new([lo[j], lo[(j+1)%10], hi[(j+1)%10], hi[j]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    # vertical groove details
    for groove in range(5):
        ga = groove*TAU/5
        for gz in range(0, 60, 4):
            t = gz/60
            gx = math.sin(t*math.pi*0.5)*8.0 + math.cos(ga)*(3.5-t*2.2+0.1)
            gy = math.sin(ga)*(3.5-t*2.2+0.1)
            bm.verts.new((gx, gy, gz))
    # amber emissive bands
    for bz in [10, 25, 42, 55]:
        t = bz/60
        br = 3.5 - t*2.2 + 0.12
        bx = math.sin(t*math.pi*0.5)*8.0
        for j in range(16):
            bm.verts.new((bx + math.cos(j*TAU/16)*br,
                           math.sin(j*TAU/16)*br, bz))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_amber_stabilizer"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_CurvedTower_A")
    return obj
'''),
    ],

    "world_biomes/inner_sea": [
        ("SM_InnerSea_BasaltDock_A",
         "inner_sea", "InnerSea",
         "sm_inner_sea_basalt_dock_a",
         '''
def build():
    """SM_InnerSea_BasaltDock_A — wet stone dock 10×30m with dock posts."""
    obj, bm = new_mesh("SM_InnerSea_BasaltDock_A")
    # main deck
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Scale(30.0, 4, (1,0,0))
        @ Matrix.Scale(10.0, 4, (0,1,0))
        @ Matrix.Scale(0.5, 4, (0,0,1))
        @ Matrix.Translation((0, 0, 0.25)))
    # dock posts
    for px in [-12, -6, 0, 6, 12]:
        for py in [-4, 4]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
                radius=0.22, depth=2.5,
                matrix=Matrix.Translation((px, py, 1.5)))
            # mooring ring
            bmesh.ops.create_cylinder(bm, cap_ends=False, segments=12,
                radius=0.30, depth=0.08,
                matrix=Matrix.Translation((px, py, 2.2)))
    # edge lip detail
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=0.12,
            matrix=Matrix.Translation((0, side*5.06, 0.3))
            @ Matrix.Scale(30.5/0.12, 4, (1,0,0))
            @ Matrix.Scale(0.5/0.12, 4, (0,0,1)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_human_equipment"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_InnerSea_BasaltDock_A")
    return obj
'''),

        ("SM_InnerSea_BrokenPier_A",
         "inner_sea", "InnerSea",
         "sm_inner_sea_broken_pier_a",
         '''
def build():
    """SM_InnerSea_BrokenPier_A — 5×40m pier, broken end."""
    import random; random.seed(19)
    obj, bm = new_mesh("SM_InnerSea_BrokenPier_A")
    # intact section (0-26m)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((-7, 0, 0.2))
        @ Matrix.Scale(26, 4, (1,0,0))
        @ Matrix.Scale(5, 4, (0,1,0))
        @ Matrix.Scale(0.45, 4, (0,0,1)))
    # support legs every 4m
    for lx in range(-18, 8, 4):
        for ly in [-1.8, 1.8]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, segments=6,
                radius=0.18, depth=3.5,
                matrix=Matrix.Translation((lx, ly, -1.5)))
    # broken end (angled, cracked)
    for i in range(5):
        t = i/4
        bx = 12 + t*10
        bz = -t*2.5
        brot = random.uniform(-0.2, 0.2)
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((bx, random.uniform(-0.4,0.4), bz))
            @ Matrix.Scale(2.2, 4, (1,0,0))
            @ Matrix.Scale(4.5, 4, (0,1,0))
            @ Matrix.Scale(0.45, 4, (0,0,1))
            @ Matrix.Rotation(brot, 4, 'Z'))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_InnerSea_BrokenPier_A")
    return obj
'''),

        ("SM_InnerSea_SubmergedRuin_A",
         "inner_sea", "InnerSea",
         "sm_inner_sea_submerged_ruin_a",
         '''
def build():
    """SM_InnerSea_SubmergedRuin_A — half-submerged ancient wall fragment 20m."""
    import random; random.seed(27)
    obj, bm = new_mesh("SM_InnerSea_SubmergedRuin_A")
    # main wall slab — upper half visible, lower submerged
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 2))
        @ Matrix.Scale(20, 4, (1,0,0))
        @ Matrix.Scale(2.5, 4, (0,1,0))
        @ Matrix.Scale(8.0, 4, (0,0,1))
        @ Matrix.Rotation(random.uniform(-0.08,0.08), 4, 'Z'))
    # machine grooves on face
    for gx in range(-8, 9, 2):
        bmesh.ops.create_cube(bm, size=0.15,
            matrix=Matrix.Translation((gx, 1.28, 4))
            @ Matrix.Scale(0.4/0.15, 4, (1,0,0))
            @ Matrix.Scale(0.08/0.15, 4, (0,1,0))
            @ Matrix.Scale(6/0.15, 4, (0,0,1)))
    # crystal sockets
    for i in range(3):
        sx = -6 + i*6
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=8,
            radius=0.45, depth=0.12,
            matrix=Matrix.Translation((sx, 1.32, 5.5)))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.35,
            matrix=Matrix.Translation((sx, 1.35, 5.5)))
    # eroded chunk missing
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.8,
        matrix=Matrix.Translation((7, 0, 5)))
    for v in result['verts']:
        v.co *= 0.0  # dissolve these verts to create hole (simplified)
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_wet_basalt"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_InnerSea_SubmergedRuin_A")
    return obj
'''),
    ],

    "world_biomes/mantle_garden": [
        ("SM_MantleGarden_ObsidianRidge_A",
         "mantle_garden", "MantleGarden",
         "sm_mantle_garden_obsidian_ridge_a",
         '''
def build():
    """SM_MantleGarden_ObsidianRidge_A — 50m walkable obsidian ridge, heat cracks."""
    import random; random.seed(51)
    obj, bm = new_mesh("SM_MantleGarden_ObsidianRidge_A")
    SEGS = 20
    L = 50.0
    rings = []
    for i in range(SEGS + 1):
        t = i/SEGS
        cx = (t-0.5)*L
        cz = math.sin(t*math.pi)*1.5 + random.uniform(-0.3,0.3)
        # sharp diamond cross-section
        pts = [
            (cx, -2.0, cz),
            (cx, -0.5, cz + 1.2 + random.uniform(-0.1,0.1)),
            (cx,  0.5, cz + 1.2 + random.uniform(-0.1,0.1)),
            (cx,  2.0, cz),
        ]
        ring = [bm.verts.new(p) for p in pts]
        rings.append(ring)
    for ri in range(SEGS):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(3):
            bm.faces.new([lo[j], lo[j+1], hi[j+1], hi[j]])
    # heat crack fissures
    for i in range(8):
        t = i/7
        cx = (t-0.5)*L*0.9
        cz = math.sin(t*math.pi)*1.5
        for fi in range(4):
            ft = fi/3
            bm.verts.new((cx + random.uniform(-1,1),
                           random.uniform(-0.3,0.3),
                           cz + 0.5 + ft*0.8))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_obsidian", "mat_heat_crack"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_MantleGarden_ObsidianRidge_A")
    return obj
'''),

        ("SM_MantleGarden_SteamVent_Mesh_A",
         "mantle_garden", "MantleGarden",
         "sm_mantle_garden_steam_vent_mesh_a",
         '''
def build():
    """SM_MantleGarden_SteamVent_Mesh_A — obsidian vent cone 4m diameter."""
    import random; random.seed(52)
    obj, bm = new_mesh("SM_MantleGarden_SteamVent_Mesh_A")
    SEGS = 10
    levels = [(0,2.0),(0.3,1.9),(0.7,1.7),(1.2,1.4),(1.8,1.0),(2.5,0.6),(3.0,0.28)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/SEGS)*r*(1+random.uniform(-0.06,0.06)),
                               math.sin(i*TAU/SEGS)*r*(1+random.uniform(-0.06,0.06)),
                               z + random.uniform(-0.04,0.04)))
                for i in range(SEGS)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(SEGS):
            bm.faces.new([lo[i], lo[(i+1)%SEGS], hi[(i+1)%SEGS], hi[i]])
    bm.faces.new(list(reversed(rings[0])))
    # vent pipe top
    pipe_top = [bm.verts.new((math.cos(i*TAU/8)*0.20,
                               math.sin(i*TAU/8)*0.20, 3.0)) for i in range(8)]
    bm.faces.new(pipe_top)
    # heat bloom ring
    for j in range(16):
        a = j*TAU/16
        bm.verts.new((math.cos(a)*2.1, math.sin(a)*2.1, 0.05))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_obsidian", "mat_heat_bloom"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_MantleGarden_SteamVent_Mesh_A")
    return obj
'''),

        ("SM_MantleGarden_MineralFlower_A",
         "mantle_garden", "MantleGarden",
         "sm_mantle_garden_mineral_flower_a",
         '''
def build():
    """SM_MantleGarden_MineralFlower_A — magenta mineral bloom, 7 crystal petals."""
    import random; random.seed(53)
    obj, bm = new_mesh("SM_MantleGarden_MineralFlower_A")
    # central bud
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.28,
        matrix=Matrix.Translation((0,0,0.30)))
    # 7 petal lobes
    for i in range(7):
        a = i*TAU/7
        px = math.cos(a)*0.55
        py = math.sin(a)*0.55
        # tapered hex prism petal
        petal_levels = [(0,0.16),(0.5,0.14),(1.2,0.10),(2.0,0.04)]
        p_rings = []
        for pz, pr in petal_levels:
            ring = [bm.verts.new((px + math.cos(j*TAU/6)*pr,
                                   py + math.sin(j*TAU/6)*pr,
                                   pz + random.uniform(-0.02,0.02)))
                    for j in range(6)]
            p_rings.append(ring)
        for ri in range(len(p_rings)-1):
            lo, hi = p_rings[ri], p_rings[ri+1]
            for j in range(6):
                bm.faces.new([lo[j],lo[(j+1)%6],hi[(j+1)%6],hi[j]])
        bm.faces.new(list(reversed(p_rings[0])))
        bm.faces.new(p_rings[-1])
    # basalt base
    bmesh.ops.create_cylinder(bm, cap_ends=True, segments=8,
        radius=0.80, depth=0.25,
        matrix=Matrix.Translation((0,0,-0.12)))
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_magenta_mineral", "mat_heat_crack", "mat_obsidian"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_MantleGarden_MineralFlower_A")
    return obj
'''),
    ],
}

# ─────────────────────────────────────────────
# Main generation logic
# ─────────────────────────────────────────────

HELPER_FUNCS = {
    "clear_scene", "new_mesh", "finalise", "smart_uv", "add_mat_slots",
    "mat_color", "set_origin_to_base", "export_fbx", "add_subdivision",
    "extrude_region", "main",
}


def is_build_func(name):
    return name.startswith("build_") or name == "build"


def generate_all():
    scripts_dir = SCRIPTS_DIR

    # 1. Write shared/utils.py
    shared_dir = os.path.join(scripts_dir, "shared")
    os.makedirs(shared_dir, exist_ok=True)
    write_file(os.path.join(shared_dir, "__init__.py"), "")
    write_file(os.path.join(shared_dir, "utils.py"), SHARED_UTILS)
    print("  ✓ shared/utils.py")

    # track all build functions per category for run_all.py generation
    category_builds = {}  # folder → [(file_stem, func_name_in_file)]

    # 2. Process each monolithic script
    for src_file, folder, depth, export_subpath in CATEGORY_MAP:
        src_path = os.path.join(scripts_dir, src_file)
        if not os.path.exists(src_path):
            print(f"  SKIP (not found): {src_path}")
            continue

        with open(src_path, encoding="utf-8") as f:
            source = f.read()

        functions = extract_top_level_functions(source)
        build_funcs = [(n, s) for n, s in functions if is_build_func(n) and n not in HELPER_FUNCS]

        print(f"\n  Processing {src_file} → {folder}/ ({len(build_funcs)} build functions)")

        cat_dir = os.path.join(scripts_dir, folder)
        write_empty_init(cat_dir)

        if folder not in category_builds:
            category_builds[folder] = []

        for func_name, func_src in build_funcs:
            sm_name = get_sm_name(func_src, func_name)

            # Determine subfolder for world_biomes / prologue_submarine
            actual_folder = folder
            actual_depth  = depth
            actual_export  = export_subpath

            if folder == "world_biomes":
                subfolder, actual_export = infer_biome_subfolder(func_name, func_src)
                actual_folder = os.path.join(folder, subfolder)
                actual_depth  = 2

            elif folder == "prologue_submarine":
                subfolder, actual_export = infer_prologue_subfolder(func_name)
                actual_folder = os.path.join(folder, subfolder)
                actual_depth  = 2

            target_dir = os.path.join(scripts_dir, actual_folder)
            write_empty_init(target_dir)

            file_stem = func_name_to_file(func_name)
            file_path = os.path.join(target_dir, file_stem + ".py")

            # Build file content
            header = make_file_header(sm_name, actual_depth, actual_export)

            body = sanitize_func_body(func_src, func_name)
            # Rename build_X → build
            body = re.sub(r'^def build_\w+\(', 'def build(', body)

            footer = make_file_footer("build", sm_name)

            full_content = header + body + footer
            write_file(file_path, full_content)

            cat_key = actual_folder
            if cat_key not in category_builds:
                category_builds[cat_key] = []
            category_builds[cat_key].append((file_stem, sm_name))

            print(f"    ✓ {actual_folder}/{file_stem}.py  ({sm_name})")

    # 3. Write new assets
    print("\n  Writing new assets from manifests ...")
    for folder_key, assets in NEW_ASSETS.items():
        for sm_name, subfolder, export_sub, file_stem, body_code in assets:
            parts = folder_key.split("/")
            depth = len(parts)
            target_dir = os.path.join(scripts_dir, *parts)
            write_empty_init(target_dir)
            # Ensure parent inits
            for i in range(1, len(parts)):
                write_empty_init(os.path.join(scripts_dir, *parts[:i]))

            file_path = os.path.join(target_dir, file_stem + ".py")
            header = make_file_header(sm_name, depth, export_sub)
            footer = make_file_footer("build", sm_name)
            full_content = header + textwrap.dedent(body_code) + footer
            write_file(file_path, full_content)

            if folder_key not in category_builds:
                category_builds[folder_key] = []
            category_builds[folder_key].append((file_stem, sm_name))
            print(f"    ✓ {folder_key}/{file_stem}.py  ({sm_name})")

    # 4. Write run_all.py for every collected folder
    print("\n  Writing run_all.py files ...")
    for folder, builds in category_builds.items():
        if not builds:
            continue
        parts = folder.split("/") if "/" in folder else [folder]
        depth = len(parts)
        target_dir = os.path.join(scripts_dir, *parts)

        # Relative import path
        imports = []
        calls   = []
        for file_stem, sm_name in builds:
            module = file_stem
            imports.append(f"from {module} import build as build_{module}")
            calls.append(f"    build_{module}()  # {sm_name}")

        dots = ", ".join(repr("..") for _ in range(depth))
        run_all_content = f'''"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, {dots}))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

{chr(10).join(imports)}


def run_all():
{chr(10).join(calls) if calls else "    pass"}


if __name__ == "__main__":
    run_all()
'''
        write_file(os.path.join(target_dir, "run_all.py"), run_all_content)
        print(f"    ✓ {folder}/run_all.py  ({len(builds)} assets)")

    # 5. Write root run_all_assets.py
    top_folders = sorted(set(f.split("/")[0] for f in category_builds.keys()))
    master_imports = []
    master_calls   = []
    for folder in top_folders:
        alias = folder.replace("/", "_")
        master_imports.append(f"from {folder}.run_all import run_all as run_{alias}")
        master_calls.append(f"    print(f'\\n--- {folder} ---'); run_{alias}()")

    master_content = f'''"""run_all_assets.py — master runner for ALL AbyssalEarth assets.

Usage:
    blender --background --python run_all_assets.py
"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

{chr(10).join(master_imports)}


def main():
    print("=== AbyssalEarth Full Asset Generation ===")
{chr(10).join(master_calls)}
    print("\\n=== ALL ASSETS COMPLETE ===")


if __name__ == "__main__":
    main()
'''
    write_file(os.path.join(scripts_dir, "run_all_assets.py"), master_content)
    print("\n  ✓ run_all_assets.py")

    # 6. Remove old monolithic files
    for src_file, *_ in CATEGORY_MAP:
        path = os.path.join(scripts_dir, src_file)
        if os.path.exists(path):
            os.remove(path)
            print(f"  ✗ removed {src_file}")

    print("\n=== generate_asset_scripts.py DONE ===")


if __name__ == "__main__":
    generate_all()
