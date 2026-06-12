#!/usr/bin/env python3
"""
validate_asset_scripts.py — thorough validation of every Blender asset script.

Checks, per sm_*.py file:
  1. Valid Python syntax (AST parse)
  2. Defines a build() function
  3. Calls new_mesh() with an SM_-prefixed asset name
  4. Calls export_fbx(obj, EXPORT_DIR, <name>) where <name> matches the mesh name
  5. Calls add_mat_slots with material names from the canonical palette
  6. Imports from shared.utils (no duplicated local helpers)
  7. _SCRIPTS_ROOT depth matches the file's actual folder depth
  8. Calls finalise, smart_uv, set_origin_to_base in build()

Cross-file checks:
  9.  Every run_all.py imports every sm_*.py sibling
  10. Asset (SM_) names are globally unique
  11. Root run_all_assets.py covers every category folder
  12. shared/utils.py palette is a superset of all used materials

Exit code 0 on success, 1 on any failure.  Run from repo root:
    python3 Tools/validate_asset_scripts.py
"""

import ast
import os
import re
import sys

SCRIPTS_DIR = os.path.join("ArtSource", "Blender", "Scripts")

errors = []
warnings = []


def err(path, msg):
    errors.append(f"  ERROR {path}: {msg}")


def warn(path, msg):
    warnings.append(f"  warn  {path}: {msg}")


# ── load canonical palette from shared/utils.py ─────────────────────
def load_palette():
    utils_path = os.path.join(SCRIPTS_DIR, "shared", "utils.py")
    with open(utils_path, encoding="utf-8") as f:
        src = f.read()
    return set(re.findall(r'"(mat_[a-z_]+)"\s*:', src))


# ── per-file analysis ────────────────────────────────────────────────
def find_str_args(call_node):
    out = []
    for a in call_node.args:
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            out.append(a.value)
    return out


def analyze_file(path, palette):
    rel = os.path.relpath(path)
    with open(path, encoding="utf-8") as f:
        src = f.read()

    # 1. syntax
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        err(rel, f"syntax error: {e}")
        return None

    info = {
        "mesh_names": [],
        "export_names": [],
        "materials": [],
        "has_build": False,
        "calls": set(),
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "build":
            info["has_build"] = True
        if isinstance(node, ast.Call):
            fname = ""
            if isinstance(node.func, ast.Name):
                fname = node.func.id
            elif isinstance(node.func, ast.Attribute):
                fname = node.func.attr
            info["calls"].add(fname)
            if fname == "new_mesh":
                info["mesh_names"] += find_str_args(node)
            elif fname == "export_fbx":
                strs = find_str_args(node)
                if strs:
                    info["export_names"].append(strs[-1])
            elif fname == "add_mat_slots":
                for a in node.args:
                    if isinstance(a, (ast.List, ast.Tuple)):
                        for el in a.elts:
                            if isinstance(el, ast.Constant) and isinstance(el.value, str):
                                info["materials"].append(el.value)

    # Variant-kit files: build() drives a parameterized builder with names
    # supplied via a VARIANTS/items list — collect every literal SM_ string
    # in the module as the asset names instead.
    is_variant_kit = ("build_variant" in info["calls"] or
                      "def build_variant(" in src or
                      (not info["mesh_names"] and "new_mesh" in info["calls"]))
    if is_variant_kit and not info["mesh_names"]:
        sm_literals = [n.value for n in ast.walk(tree)
                       if isinstance(n, ast.Constant) and
                       isinstance(n.value, str) and n.value.startswith("SM_")]
        info["mesh_names"] = sorted(set(sm_literals))
        if not info["mesh_names"]:
            err(rel, "variant kit has no literal SM_ asset names anywhere")
        if "export_fbx" not in info["calls"]:
            err(rel, "variant kit never calls export_fbx()")

    # 2. build()
    if not info["has_build"]:
        err(rel, "no build() function defined")

    # 3. mesh name
    if not info["mesh_names"]:
        err(rel, "no new_mesh() call with a literal asset name")
    for n in info["mesh_names"]:
        if not n.startswith("SM_"):
            err(rel, f"mesh name {n!r} does not start with SM_")

    # 4. export name matches mesh name (skip for variant kits — the export
    # name is args[0] at runtime)
    if is_variant_kit:
        pass
    elif not info["export_names"]:
        err(rel, "no export_fbx() call with a literal filename")
    else:
        for en in info["export_names"]:
            if en.endswith(".fbx"):
                err(rel, f"export filename {en!r} should not include .fbx (utils appends it)")
            base = en[:-4] if en.endswith(".fbx") else en
            if info["mesh_names"] and base not in info["mesh_names"]:
                # multi-asset files (e.g. crystal kit) build names dynamically — only
                # flag when the file has exactly one literal mesh name
                if len(info["mesh_names"]) == 1:
                    err(rel, f"export name {base!r} != mesh name {info['mesh_names'][0]!r}")

    # 5. materials in palette
    for m in info["materials"]:
        if m not in palette:
            err(rel, f"material {m!r} not in shared/utils.py palette")

    # 6. imports shared.utils
    if "from shared.utils import" not in src:
        err(rel, "does not import from shared.utils")

    # 7. depth check
    rel_to_scripts = os.path.relpath(path, SCRIPTS_DIR)
    actual_depth = len(rel_to_scripts.split(os.sep)) - 1   # folders above file
    m = re.search(r"_SCRIPTS_ROOT = os\.path\.normpath\(os\.path\.join\(_HERE(?:, '\.\.')+\)\)", src)
    declared_depth = src.count("'..'")
    if declared_depth != actual_depth:
        err(rel, f"_SCRIPTS_ROOT depth is {declared_depth} but file is {actual_depth} folder(s) deep")

    # 8. required pipeline calls
    for required in ("finalise", "smart_uv", "set_origin_to_base"):
        if required not in info["calls"]:
            err(rel, f"build() never calls {required}()")

    # 9. undefined-name lint: any Name loaded but never bound anywhere in the
    # module (imports, assignments, defs, args, loop targets) and not a
    # builtin is a runtime NameError waiting to happen (e.g. a helper typo).
    import builtins
    bound = set(dir(builtins)) | {"__file__", "__name__", "__doc__",
                                   "__package__", "__spec__", "__loader__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            bound.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                bound.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                bound.add(alias.asname or alias.name)
        elif isinstance(node, (ast.Lambda,)):
            for a in node.args.args:
                bound.add(a.arg)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in bound:
                err(rel, f"undefined name {node.id!r} at line {node.lineno} "
                         "(typo or missing import — would NameError at runtime)")

    return info


# ── cross-file checks ────────────────────────────────────────────────
def check_run_all(folder, stems):
    run_all = os.path.join(folder, "run_all.py")
    rel = os.path.relpath(run_all)
    if not os.path.exists(run_all):
        err(rel, "missing run_all.py")
        return
    with open(run_all, encoding="utf-8") as f:
        src = f.read()
    try:
        ast.parse(src)
    except SyntaxError as e:
        err(rel, f"syntax error: {e}")
        return
    for stem in stems:
        if f"from {stem} import" not in src and f"import {stem}" not in src:
            err(rel, f"does not import {stem}")


def main():
    if not os.path.isdir(SCRIPTS_DIR):
        print(f"ERROR: {SCRIPTS_DIR} not found — run from repo root")
        return 1

    palette = load_palette()
    print(f"Palette: {len(palette)} canonical materials")

    all_mesh_names = {}
    leaf_folders = []
    file_count = 0

    for root, dirs, files in os.walk(SCRIPTS_DIR):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        if os.path.basename(root) == "shared":
            continue
        stems = sorted(f[:-3] for f in files if f.startswith("sm_") and f.endswith(".py"))
        if stems:
            leaf_folders.append((root, stems))
        for f in files:
            if f.startswith("sm_") and f.endswith(".py"):
                file_count += 1
                path = os.path.join(root, f)
                info = analyze_file(path, palette)
                if info:
                    for n in info["mesh_names"]:
                        if n in all_mesh_names:
                            err(os.path.relpath(path),
                                f"duplicate asset name {n!r} (also in {all_mesh_names[n]})")
                        else:
                            all_mesh_names[n] = os.path.relpath(path)

    # 9. run_all coverage
    for folder, stems in leaf_folders:
        check_run_all(folder, stems)

    # 11. root master coverage
    root_runner = os.path.join(SCRIPTS_DIR, "run_all_assets.py")
    if os.path.exists(root_runner):
        with open(root_runner, encoding="utf-8") as f:
            master = f.read()
        try:
            ast.parse(master)
        except SyntaxError as e:
            err(os.path.relpath(root_runner), f"syntax error: {e}")
        tops = sorted(d for d in os.listdir(SCRIPTS_DIR)
                      if os.path.isdir(os.path.join(SCRIPTS_DIR, d)) and
                      d not in ("shared", "__pycache__"))
        for t in tops:
            if t not in master:
                err(os.path.relpath(root_runner), f"does not reference category {t!r}")
    else:
        err(SCRIPTS_DIR, "missing run_all_assets.py")

    # report
    print(f"Scanned {file_count} asset scripts in {len(leaf_folders)} folders; "
          f"{len(all_mesh_names)} unique asset names")
    if warnings:
        print(f"\n{len(warnings)} warnings:")
        for w in warnings:
            print(w)
    if errors:
        print(f"\n{len(errors)} ERRORS:")
        for e in errors:
            print(e)
        return 1
    print("\nAsset script validation passed — all checks green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
