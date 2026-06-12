#!/usr/bin/env python3
"""
repair_asset_scripts.py — fixes every defect the validator found in the split
asset scripts:

1. set_origin_bottom → set_origin_to_base (stale helper name)
2. PROLOGUE_DIR / ELEVATOR_DIR / EXPORT_BASE / EXPORT_ROOT → EXPORT_DIR
3. Inject missing helper functions (hex_pts, box, box_from_corners,
   make_spires_*) recovered from the original monolithic scripts in git
4. Parameterized builders: rename build(...) → build_variant(...) and append
   a build() wrapper with the variant configs recovered from the original
   main() call sites
5. Single-asset builders missing an export call: insert
   export_fbx(obj, EXPORT_DIR, "<name>") after set_origin_to_base(obj)
6. characters/sm_collectible_items.py: fix 2-arg export call
7. Move misfiled biome assets to their correct folders
8. Add mat_amber_emissive to the shared palette
9. Regenerate every run_all.py and run_all_assets.py (with correct escaping)

Run from repo root:  python3 Tools/repair_asset_scripts.py
"""

import os
import re
import subprocess

SCRIPTS_DIR = os.path.join("ArtSource", "Blender", "Scripts")
ORIG_COMMIT = "28f54f6"


# ────────────────────────────────────────────────────────────────────
def git_show(path):
    return subprocess.run(
        ["git", "show", f"{ORIG_COMMIT}:{path}"],
        capture_output=True, text=True, check=True).stdout


def extract_function(source, func_name):
    """Return the full source of a top-level function."""
    lines = source.split("\n")
    out = []
    in_func = False
    for i, line in enumerate(lines):
        if re.match(rf"^def {re.escape(func_name)}\(", line):
            in_func = True
        elif in_func and (re.match(r"^def \w+\(", line) or re.match(r"^class \w+", line)):
            break
        if in_func:
            out.append(line)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


ORIG = {
    "env": git_show("ArtSource/Blender/Scripts/gen_luminous_rift_env.py"),
    "machines": git_show("ArtSource/Blender/Scripts/gen_luminous_rift_machines.py"),
    "biomes": git_show("ArtSource/Blender/Scripts/gen_world_biomes.py"),
    "survey": git_show("ArtSource/Blender/Scripts/gen_human_survey_kit.py"),
}

HELPERS = {
    "hex_pts":           extract_function(ORIG["machines"], "hex_pts"),
    "box":               extract_function(ORIG["biomes"], "box"),
    "box_from_corners":  extract_function(ORIG["survey"], "box_from_corners"),
    "make_spires_A_small": extract_function(ORIG["env"], "make_spires_A_small"),
    "make_spires_B_fan":   extract_function(ORIG["env"], "make_spires_B_fan"),
    "make_spires_C_broken": extract_function(ORIG["env"], "make_spires_C_broken"),
    "jitter_verts":      extract_function(ORIG["env"], "jitter_verts"),
}


# ────────────────────────────────────────────────────────────────────
# Variant wrappers per parameterized file (recovered from original main())
# value: (extra_helpers, wrapper_code)
# ────────────────────────────────────────────────────────────────────

CRYSTAL_KIT_WRAPPER = '''

def _cfg_S_A(): return {'base_r':0.22,'rock_h':0.12,'spires':make_spires_A_small(1)}
def _cfg_S_B(): return {'base_r':0.22,'rock_h':0.10,'spires':make_spires_B_fan(2)}
def _cfg_S_C(): return {'base_r':0.22,'rock_h':0.08,'spires':make_spires_C_broken(3)}
def _cfg_M_A(): return {'base_r':0.36,'rock_h':0.20,'spires':make_spires_A_small(4)*2}
def _cfg_M_B(): return {'base_r':0.36,'rock_h':0.18,'spires':make_spires_B_fan(5)}
def _cfg_M_C(): return {'base_r':0.36,'rock_h':0.16,'spires':make_spires_C_broken(6)*2}
def _cfg_L_A(): return {'base_r':0.55,'rock_h':0.30,'spires':[
    {'ox':0,'oy':0,'h':1.35,'w':0.14,'sides':5},
    {'ox':-0.18,'oy':0.12,'h':1.05,'w':0.12,'sides':5,'tilt':(-0.12, 0.05)},
    {'ox':0.20,'oy':-0.10,'h':0.90,'w':0.11,'sides':5,'tilt':(0.10,-0.08)},
    {'ox':-0.08,'oy':-0.22,'h':0.60,'w':0.09,'sides':4,'tilt':(-0.06,-0.15)},
]}
def _cfg_L_B(): return {'base_r':0.55,'rock_h':0.28,
                        'spires':make_spires_B_fan(8) + make_spires_C_broken(9)}
def _cfg_Hero(): return {'base_r':0.90,'rock_h':0.45,'spires':[
    {'ox':0,'oy':0,'h':2.80,'w':0.22,'sides':6},
    {'ox':-0.35,'oy':0.20,'h':2.10,'w':0.18,'sides':5,'tilt':(-0.10, 0.06)},
    {'ox':0.38,'oy':-0.15,'h':1.85,'w':0.16,'sides':5,'tilt':(0.12,-0.06)},
    {'ox':-0.20,'oy':-0.40,'h':1.40,'w':0.14,'sides':5,'tilt':(-0.08,-0.18)},
    {'ox':0.25,'oy':0.38,'h':1.20,'w':0.13,'sides':4,'tilt':(0.08, 0.20)},
    {'ox':-0.50,'oy':-0.10,'h':0.80,'w':0.10,'sides':4,'tilt':(-0.25,-0.05)},
    {'ox':0.15,'oy':-0.52,'h':0.65,'w':0.09,'sides':4,'tilt':(0.04,-0.28)},
]}

VARIANTS = [
    ("SM_Rift_CrystalCluster_S_A", 1, _cfg_S_A),
    ("SM_Rift_CrystalCluster_S_B", 2, _cfg_S_B),
    ("SM_Rift_CrystalCluster_S_C", 3, _cfg_S_C),
    ("SM_Rift_CrystalCluster_M_A", 4, _cfg_M_A),
    ("SM_Rift_CrystalCluster_M_B", 5, _cfg_M_B),
    ("SM_Rift_CrystalCluster_M_C", 6, _cfg_M_C),
    ("SM_Rift_CrystalCluster_L_A", 7, _cfg_L_A),
    ("SM_Rift_CrystalCluster_L_B", 8, _cfg_L_B),
    ("SM_Rift_CrystalCluster_Hero_A", 9, _cfg_Hero),
]


def build():
    for name, seed, cfg in VARIANTS:
        clear_scene()
        obj = build_variant(name, seed, cfg())
        export_fbx(obj, EXPORT_DIR, name)
'''


def simple_wrapper(variants, star_args=True):
    """Wrapper for build_variant(name, *rest) style functions."""
    lines = "VARIANTS = [\n"
    for v in variants:
        lines += f"    {v!r},\n"
    lines += "]\n"
    return f'''

{lines}

def build():
    for args in VARIANTS:
        clear_scene()
        obj = build_variant(*args)
        export_fbx(obj, EXPORT_DIR, args[0])
'''


def noname_wrapper(call_args, export_name):
    """Wrapper for builders whose signature has no name argument."""
    return f'''

def build():
    clear_scene()
    obj = build_variant({call_args})
    export_fbx(obj, EXPORT_DIR, "{export_name}")
'''


PARAMETERIZED = {
    "luminous_rift_env/sm_crystal_kit.py": (
        ["make_spires_A_small", "make_spires_B_fan", "make_spires_C_broken"],
        CRYSTAL_KIT_WRAPPER),
    "luminous_rift_env/sm_foreground_ledge.py": ([], simple_wrapper([
        ("SM_Rift_ForegroundLedge_A", False, 7),
        ("SM_Rift_ForegroundLedge_B_Broken", True, 14)])),
    "luminous_rift_env/sm_rock_arch.py": ([], simple_wrapper([
        ("SM_Rift_RockArch_A", 28, 18, 3.5, 3),
        ("SM_Rift_RockArch_B", 42, 25, 5.0, 6)])),
    "luminous_rift_env/sm_overhang.py": ([], simple_wrapper([
        ("SM_Rift_Overhang_A", 22, 12, 11),
        ("SM_Rift_Overhang_B", 35, 18, 22)])),
    "luminous_rift_env/sm_hanging_slab.py": ([], simple_wrapper([
        ("SM_Rift_HangingSlab_A", 12, 25, 2.5, 42),
        ("SM_Rift_HangingSlab_B", 8, 18, 3.5, 55),
        ("SM_Rift_HangingSlab_C", 20, 40, 4.0, 68)])),
    "luminous_rift_env/sm_cavern_wall.py": ([], simple_wrapper([
        ("SM_Rift_CavernWall_Large_A", 40, 30, 5, 99),
        ("SM_Rift_CavernWall_Large_B", 60, 40, 8, 111)])),
    "luminous_rift_machines/sm_hex_tile.py": (
        ["hex_pts"],
        noname_wrapper('"SM_Rift_HexCollector_Tile_A"', "SM_Rift_HexCollector_Tile_A")),
    "luminous_rift_machines/sm_hex_cluster.py": (
        ["hex_pts"], simple_wrapper([
            ("SM_Rift_HexCollector_Cluster_A", False, 1),
            ("SM_Rift_HexCollector_Cluster_B_Broken", True, 2)])),
    "luminous_rift_machines/sm_bridge_span.py": ([], simple_wrapper([
        ("SM_Rift_BridgeSpan_A", 24, False, 3),
        ("SM_Rift_BridgeSpan_B_Broken", 24, True, 6)])),
    "luminous_rift_machines/sm_tower.py": ([], simple_wrapper([
        ("SM_Rift_TowerSegment_A", 6, 40, 2),
        ("SM_Rift_TowerSegment_B", 10, 70, 5),
        ("SM_Rift_TowerSegment_C", 14, 100, 8)])),
    "gameplay_props/sm_crystal_cluster.py": ([], simple_wrapper([
        ("SM_HarvestableNode_S", 0.18, 3, [0.28, 0.22, 0.32], 0.16),
        ("SM_HarvestableNode_M", 0.28, 5, [0.55, 0.40, 0.65, 0.45, 0.50], 0.24),
        ("SM_HarvestableNode_L", 0.40, 7, [0.90, 0.75, 1.05, 0.80, 0.70, 0.95, 0.85], 0.34)])),
    "world_biomes/fossil_sky/sm_rib_arch.py": ([], simple_wrapper([
        ("SM_FossilSky_RibArch_A", 22, 14, 2.2, 1),
        ("SM_FossilSky_RibArch_B", 32, 20, 3.0, 5),
        ("SM_FossilSky_RibArch_C", 15, 10, 1.6, 9)])),
    "world_biomes/fossil_sky/sm_spine_segment.py": ([], simple_wrapper([
        ("SM_FossilSky_SpineSegment_A", 8, 3.5, 3),
        ("SM_FossilSky_SpineSegment_B", 5, 2.4, 7)])),
    "world_biomes/glassroot_forest/sm_glassroot_trunk.py": ([], simple_wrapper([
        ("SM_Glassroot_TrunkBase_A", 2.2, 10),
        ("SM_Glassroot_TrunkBase_B", 3.5, 17)])),
    "world_biomes/inner_sea/sm_stalactite.py": ([], simple_wrapper([
        ("SM_InnerSea_Stalactite_A", 0.9, 6.5, 50),
        ("SM_InnerSea_Stalactite_B", 0.55, 4.0, 55),
        ("SM_InnerSea_Stalactite_C", 1.4, 10.0, 60)])),
    "world_biomes/mantle_garden/sm_lava_rock.py": ([], simple_wrapper([
        ("SM_MantleGarden_LavaRock_A", 5.0, 80),
        ("SM_MantleGarden_LavaRock_B", 3.0, 85)])),
    "world_biomes/mantle_garden/sm_purple_crystal.py": ([], simple_wrapper([
        ("SM_MantleGarden_PurpleCrystal_A", 1.8, 90),
        ("SM_MantleGarden_PurpleCrystal_B", 1.0, 95)])),
    # builders whose signature has no usable name argument
    "world_biomes/fossil_sky/sm_floating_rock.py": ([], simple_wrapper([
        ("SM_GravityWell_FloatingRock_A", 4.0, 30),
        ("SM_GravityWell_FloatingRock_B", 2.2, 35),
        ("SM_GravityWell_FloatingRock_C", 1.0, 40)])),
    "world_biomes/inner_sea/sm_wood_dock.py": (
        ["box"], noname_wrapper("8.0, 4", "SM_FossilSky_WoodDock_A")),
}

# Files to move: (src_rel, dst_rel, old_export, new_export)
MOVES = [
    ("world_biomes/fossil_sky/sm_floating_rock.py",
     "world_biomes/gravity_well/sm_floating_rock.py", "FossilSky", "GravityWell"),
    ("world_biomes/inner_sea/sm_wood_dock.py",
     "world_biomes/fossil_sky/sm_wood_dock.py", "InnerSea", "FossilSky"),
]

# Helper-dependency injection for zero-arg files that reference helpers
HELPER_TOKENS = ["hex_pts", "box_from_corners", "jitter_verts"]
# 'box(' is too generic; handle explicitly:
BOX_FILES = ["world_biomes/inner_sea/sm_inner_sea_dock.py"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def inject_helpers(src, helper_names):
    """Insert helper functions right after the EXPORT_DIR line."""
    block = "\n\n" + "\n\n".join(HELPERS[h] for h in helper_names) + "\n"
    return re.sub(r"(EXPORT_DIR = get_export_dir\([^\)]*\)\n)",
                  r"\1" + block, src, count=1)


def main():
    # ── 1+2: global token fixes across every script ──────────────────
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        for f in files:
            if not f.endswith(".py"):
                continue
            path = os.path.join(root, f)
            src = read(path)
            orig = src
            src = src.replace("set_origin_bottom(", "set_origin_to_base(")
            for tok in ("PROLOGUE_DIR", "ELEVATOR_DIR", "EXPORT_BASE", "EXPORT_ROOT"):
                src = re.sub(rf"\b{tok}\b", "EXPORT_DIR", src)
            if src != orig:
                write(path, src)
                print(f"  token-fix {os.path.relpath(path)}")

    # ── 8: palette addition ───────────────────────────────────────────
    utils_path = os.path.join(SCRIPTS_DIR, "shared", "utils.py")
    src = read(utils_path)
    if "mat_amber_emissive" not in src:
        src = src.replace(
            '"mat_lava_emissive":',
            '"mat_amber_emissive":       (1.00, 0.50, 0.05, 1),\n    "mat_lava_emissive":')
        write(utils_path, src)
        print("  palette: added mat_amber_emissive")

    # ── 3+4: parameterized files — rename + helpers + wrapper ─────────
    for rel, (helper_names, wrapper) in PARAMETERIZED.items():
        path = os.path.join(SCRIPTS_DIR, *rel.split("/"))
        if not os.path.exists(path):
            print(f"  SKIP missing {rel}")
            continue
        src = read(path)
        if "def build_variant(" in src:
            continue  # already repaired
        src = re.sub(r"^def build\(", "def build_variant(", src, count=1, flags=re.M)
        if helper_names:
            src = inject_helpers(src, helper_names)
        # insert wrapper before the __main__ footer
        src = src.replace('\n\nif __name__ == "__main__":',
                          wrapper + '\n\nif __name__ == "__main__":', 1)
        write(path, src)
        print(f"  variant-wrap {rel}")

    # box helper for inner sea dock
    for rel in BOX_FILES:
        path = os.path.join(SCRIPTS_DIR, *rel.split("/"))
        src = read(path)
        if "def box(" not in src and re.search(r"\bbox\(", src):
            src = inject_helpers(src, ["box"])
            write(path, src)
            print(f"  helper-inject {rel} (box)")

    # ── 6: collectible items export signature ─────────────────────────
    path = os.path.join(SCRIPTS_DIR, "characters", "sm_collectible_items.py")
    src = read(path)
    fixed = re.sub(r"export_fbx\((\w+),\s*(\w+)\)", r"export_fbx(\1, EXPORT_DIR, \2)", src)
    if fixed != src:
        write(path, fixed)
        print("  export-sig characters/sm_collectible_items.py")

    # ── 5: zero-arg builders missing export ───────────────────────────
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        if os.path.basename(root) == "shared":
            continue
        for f in files:
            if not (f.startswith("sm_") and f.endswith(".py")):
                continue
            path = os.path.join(root, f)
            src = read(path)
            if "export_fbx(" in src.split("from shared.utils import")[-1].split(")\n", 1)[-1]:
                # an export call exists somewhere after the import block
                if re.search(r"^\s+export_fbx\(", src, flags=re.M):
                    continue
            # find literal mesh name + zero-arg build
            m_name = re.search(r'new_mesh\(["\']([^"\']+)["\']', src)
            m_build = re.search(r"^def build\(\)", src, flags=re.M)
            if not (m_name and m_build):
                continue
            name = m_name.group(1)
            # insert export after the LAST set_origin_to_base(obj) in build
            lines = src.split("\n")
            insert_at = None
            for i, line in enumerate(lines):
                if re.match(r"\s+set_origin_to_base\(obj\)", line):
                    insert_at = i
            if insert_at is None:
                print(f"  !! cannot repair {os.path.relpath(path)} — no set_origin_to_base(obj)")
                continue
            indent = re.match(r"(\s*)", lines[insert_at]).group(1)
            lines.insert(insert_at + 1, f'{indent}export_fbx(obj, EXPORT_DIR, "{name}")')
            write(path, "\n".join(lines))
            print(f"  export-insert {os.path.relpath(path)}  ({name})")

    # ── 7: moves ───────────────────────────────────────────────────────
    for src_rel, dst_rel, old_exp, new_exp in MOVES:
        src_path = os.path.join(SCRIPTS_DIR, *src_rel.split("/"))
        dst_path = os.path.join(SCRIPTS_DIR, *dst_rel.split("/"))
        if not os.path.exists(src_path):
            continue
        content = read(src_path).replace(
            f"get_export_dir({old_exp!r})", f"get_export_dir({new_exp!r})")
        write(dst_path, content)
        os.remove(src_path)
        print(f"  move {src_rel} → {dst_rel}  (export {new_exp})")

    print("\nRepair pass complete. Now regenerating run_all files ...")

    # ── 9: regen run_alls with correct escaping ───────────────────────
    leaf_dirs = []
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        if os.path.basename(root) == "shared":
            continue
        stems = sorted(x[:-3] for x in files if x.startswith("sm_") and x.endswith(".py"))
        if stems:
            leaf_dirs.append((root, stems))

    for root, stems in leaf_dirs:
        rel = os.path.relpath(root, SCRIPTS_DIR)
        depth = len(rel.split(os.sep))
        dots = ", ".join(repr("..") for _ in range(depth))
        imports = "\n".join(f"from {s} import build as build_{s}" for s in stems)
        calls = "\n".join(f"    build_{s}()" for s in stems)
        content = (
            '"""run_all.py — build all assets in this folder."""\n'
            "import sys, os\n"
            "_HERE = os.path.dirname(os.path.abspath(__file__))\n"
            f"_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, {dots}))\n"
            "if _SCRIPTS_ROOT not in sys.path:\n"
            "    sys.path.insert(0, _SCRIPTS_ROOT)\n"
            "if _HERE not in sys.path:\n"
            "    sys.path.insert(0, _HERE)\n\n"
            f"{imports}\n\n\n"
            "def run_all():\n"
            f"{calls}\n\n\n"
            'if __name__ == "__main__":\n'
            "    run_all()\n")
        write(os.path.join(root, "run_all.py"), content)

    for parent in ["world_biomes", "prologue_submarine"]:
        pdir = os.path.join(SCRIPTS_DIR, parent)
        subs = sorted(d for d in os.listdir(pdir)
                      if os.path.isdir(os.path.join(pdir, d)) and
                      os.path.exists(os.path.join(pdir, d, "run_all.py")))
        imports = "\n".join(
            f"from {parent}.{s}.run_all import run_all as run_{s}" for s in subs)
        calls = "\n".join(f"    run_{s}()" for s in subs)
        content = (
            '"""run_all.py — build all sub-folder assets."""\n'
            "import sys, os\n"
            "_HERE = os.path.dirname(os.path.abspath(__file__))\n"
            "_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))\n"
            "if _SCRIPTS_ROOT not in sys.path:\n"
            "    sys.path.insert(0, _SCRIPTS_ROOT)\n\n"
            f"{imports}\n\n\n"
            "def run_all():\n"
            f"{calls}\n\n\n"
            'if __name__ == "__main__":\n'
            "    run_all()\n")
        write(os.path.join(pdir, "run_all.py"), content)

    tops = sorted(d for d in os.listdir(SCRIPTS_DIR)
                  if os.path.isdir(os.path.join(SCRIPTS_DIR, d)) and
                  d != "shared" and
                  os.path.exists(os.path.join(SCRIPTS_DIR, d, "run_all.py")))
    imports = "\n".join(f"from {t}.run_all import run_all as run_{t}" for t in tops)
    calls = "\n".join(
        f"    print()\n    print('--- {t} ---')\n    run_{t}()" for t in tops)
    content = (
        '"""run_all_assets.py — master runner for ALL AbyssalEarth assets.\n\n'
        "Usage:\n"
        "    blender --background --python run_all_assets.py\n"
        '"""\n'
        "import sys, os\n"
        "_HERE = os.path.dirname(os.path.abspath(__file__))\n"
        "if _HERE not in sys.path:\n"
        "    sys.path.insert(0, _HERE)\n\n"
        f"{imports}\n\n\n"
        "def main():\n"
        '    print("=== AbyssalEarth Full Asset Generation ===")\n'
        f"{calls}\n"
        '    print()\n'
        '    print("=== ALL ASSETS COMPLETE ===")\n\n\n'
        'if __name__ == "__main__":\n'
        "    main()\n")
    write(os.path.join(SCRIPTS_DIR, "run_all_assets.py"), content)
    print(f"  regen run_all_assets.py ({len(tops)} categories)")
    print("\n=== repair done ===")


if __name__ == "__main__":
    main()
