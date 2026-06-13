#!/usr/bin/env python3
"""
render_asset_preview.py — headless mesh preview generator for AbyssalEarth asset scripts.

Patches shared.utils to stub operator calls, runs build(), extracts mesh geometry,
and renders three matplotlib wireframe views (front / side / 3-quarter).

Usage:
    pip install matplotlib numpy bpy
    python3 Tools/render_asset_preview.py --script ArtSource/Blender/Scripts/luminous_rift_machines/sm_orb_hub.py --out /tmp/renders/
    python3 Tools/render_asset_preview.py --all --out /tmp/renders/
    python3 Tools/render_asset_preview.py --changed-since origin/main --out /tmp/renders/

Output: <AssetName>_preview.png  (1800×600, dark background, front/side/3-quarter wireframes)

Dependencies:
    matplotlib numpy   — always required
    bpy                — optional; skips mesh build if absent (preview shows "no bpy" label)
"""

import argparse
import importlib.util
import os
import subprocess
import sys
import traceback
import types

SCRIPTS_DIR = os.path.join("ArtSource", "Blender", "Scripts")

# ── matplotlib ──────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
    from mpl_toolkits.mplot3d.art3d import Line3DCollection
    import numpy as np
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# ── bpy ─────────────────────────────────────────────────────────────
try:
    import bpy      # noqa: F401
    import bmesh    # noqa: F401
    HAS_BPY = True
except ImportError:
    HAS_BPY = False


# ────────────────────────────────────────────────────────────────────
#  Headless shared.utils shim
# ────────────────────────────────────────────────────────────────────

_MATERIAL_COLORS = {
    "mat_ancient_machine_dark":      (0.05, 0.05, 0.06, 1),
    "mat_ancient_machine_edge_wear": (0.12, 0.11, 0.10, 1),
    "mat_gold_emissive":             (1.00, 0.72, 0.10, 1),
    "mat_blue_emissive":             (0.05, 0.45, 1.00, 1),
    "mat_crystal_blue":              (0.10, 0.60, 1.00, 1),
    "mat_wet_basalt":                (0.08, 0.08, 0.09, 1),
    "mat_human_equipment":           (0.18, 0.16, 0.14, 1),
    "mat_collector_glass":           (0.60, 0.85, 1.00, 1),
    "mat_orb_energy":                (0.40, 0.80, 1.00, 1),
    "mat_amber_emissive":            (1.00, 0.50, 0.05, 1),
    "mat_lava_emissive":             (1.00, 0.25, 0.00, 1),
    "mat_purple_emissive":           (0.55, 0.10, 1.00, 1),
    "mat_red_emissive_vein":         (1.00, 0.05, 0.05, 1),
    "mat_glass_bark":                (0.60, 0.90, 0.80, 1),
    "mat_water_bioluminescent":      (0.00, 0.55, 0.65, 1),
    "mat_bone_stone":                (0.82, 0.78, 0.70, 1),
    "mat_fossil_bone":               (0.80, 0.76, 0.68, 1),
    "mat_cyan_fossil_vein":          (0.00, 0.80, 0.75, 1),
    "mat_glassroot_translucent":     (0.55, 0.90, 0.75, 1),
    "mat_red_sap":                   (0.70, 0.08, 0.05, 1),
    "mat_pearl_stone":               (0.88, 0.85, 0.82, 1),
    "mat_wet_edge":                  (0.10, 0.12, 0.14, 1),
    "mat_dark_basalt":               (0.06, 0.06, 0.07, 1),
    "mat_amber_stabilizer":          (1.00, 0.60, 0.10, 1),
    "mat_obsidian":                  (0.04, 0.03, 0.04, 1),
    "mat_heat_crack":                (1.00, 0.35, 0.00, 1),
    "mat_heat_bloom":                (1.00, 0.50, 0.10, 1),
    "mat_magenta_mineral":           (0.85, 0.10, 0.65, 1),
}


def _make_shim():
    """Create a fake shared.utils module with bpy-free implementations."""
    import math
    import bpy as _bpy
    import bmesh as _bmesh
    from mathutils import Vector

    mesh_store = {}   # mesh_name → {verts, edges, polys}

    def _mat_color(name):
        return _MATERIAL_COLORS.get(name, (0.5, 0.5, 0.5, 1))

    def _new_mesh(name):
        mesh = _bpy.data.meshes.new(name)
        obj = _bpy.data.objects.new(name, mesh)
        for coll in [
            getattr(getattr(_bpy.context, "scene", None), "collection", None),
            getattr(_bpy.context, "collection", None),
        ]:
            if coll is not None:
                try:
                    coll.objects.link(obj)
                    break
                except Exception:
                    pass
        return obj, _bmesh.new()

    def _finalise(obj, bm):
        bm.to_mesh(obj.data)
        bm.free()
        try:
            verts = [(v.co.x, v.co.y, v.co.z) for v in obj.data.vertices]
            edges = [(e.vertices[0], e.vertices[1]) for e in obj.data.edges]
            polys = [list(p.vertices) for p in obj.data.polygons]
            mesh_store[obj.data.name] = {
                "verts": verts, "edges": edges, "polys": polys,
                "name": obj.data.name,
            }
        except Exception as exc:
            print(f"    [render] mesh extraction failed: {exc}")

    def _clear_scene():
        for o in list(_bpy.data.objects):
            try:
                _bpy.data.objects.remove(o, do_unlink=True)
            except Exception:
                pass
        for m in list(_bpy.data.meshes):
            try:
                _bpy.data.meshes.remove(m)
            except Exception:
                pass

    def _get_export_dir(subpath):
        d = os.path.join("Content", "ArtSourceExports", subpath)
        os.makedirs(d, exist_ok=True)
        return d

    def _extrude_region(bm, faces, dist, direction=None):
        if direction is None:
            direction = faces[0].normal.copy()
        geom = _bmesh.ops.extrude_face_region(bm, geom=faces)
        verts = [e for e in geom["geom"] if isinstance(e, _bmesh.types.BMVert)]
        _bmesh.ops.translate(bm, verts=verts, vec=direction * dist)
        return [f for f in geom["geom"] if isinstance(f, _bmesh.types.BMFace)]

    mod = types.ModuleType("shared.utils")
    mod.TAU = math.tau
    mod.PI = math.pi
    mod.mat_color = _mat_color
    mod.new_mesh = _new_mesh
    mod.finalise = _finalise
    mod.smart_uv = lambda obj: None
    mod.set_origin_to_base = lambda obj: None
    mod.export_fbx = lambda *a, **kw: None
    mod.add_mat_slots = lambda obj, names: None
    mod.clear_scene = _clear_scene
    mod.extrude_region = _extrude_region
    mod.add_subdivision = lambda obj, levels=1: None
    mod.get_export_dir = _get_export_dir
    mod._mesh_store = mesh_store
    return mod


# ────────────────────────────────────────────────────────────────────
#  Script runner
# ────────────────────────────────────────────────────────────────────

def run_script(script_path):
    """Run build() from an asset script and return {mesh_name: data} dict."""
    if not HAS_BPY:
        print(f"  [render] SKIP {script_path}: bpy not installed")
        return {}

    script_path = os.path.abspath(script_path)
    if not os.path.exists(script_path):
        print(f"  [render] ERROR: {script_path} not found")
        return {}

    scripts_root = os.path.abspath(SCRIPTS_DIR)
    shim = _make_shim()
    mesh_store = shim._mesh_store

    # Inject patched shared package before importing the script
    fake_shared = types.ModuleType("shared")
    fake_shared.utils = shim
    sys.modules["shared"] = fake_shared
    sys.modules["shared.utils"] = shim

    if scripts_root not in sys.path:
        sys.path.insert(0, scripts_root)
    script_dir = os.path.dirname(script_path)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    mod_name = os.path.basename(script_path)[:-3]
    sys.modules.pop(mod_name, None)

    try:
        spec = importlib.util.spec_from_file_location(mod_name, script_path)
        asset_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(asset_mod)   # runs top-level; __main__ guard blocks main()
        if hasattr(asset_mod, "build"):
            asset_mod.build()
        else:
            print(f"  [render] WARNING: {mod_name} has no build() function")
    except SystemExit:
        pass   # some scripts call sys.exit() at end of __main__ block
    except Exception as exc:
        print(f"  [render] ERROR in {mod_name}: {exc}")
        traceback.print_exc()

    return dict(mesh_store)


# ────────────────────────────────────────────────────────────────────
#  Wireframe renderer
# ────────────────────────────────────────────────────────────────────

_DARK_BG   = "#0d0d14"
_EDGE_COL  = "#3a7ad5"
_TITLE_COL = "#aaccff"
_SUB_COL   = "#667799"

VIEW_PARAMS = [
    ("Front  (XZ)", 90, -90),
    ("Side   (YZ)", 90,   0),
    ("3/4 View",    28,  45),
]


def _all_verts_arr(mesh_data):
    pts = []
    for md in mesh_data.values():
        pts.extend(md["verts"])
    return np.array(pts) if pts else np.zeros((1, 3))


def render_wireframe(mesh_data, out_path, label=""):
    if not HAS_MPL:
        print("  [render] SKIP: matplotlib not installed")
        return False
    if not mesh_data:
        print("  [render] SKIP: empty mesh data")
        return False

    all_v = _all_verts_arr(mesh_data)
    center = all_v.mean(axis=0)
    span = (all_v.max(axis=0) - all_v.min(axis=0)).max()
    margin = max(span * 0.58, 0.5)

    fig = plt.figure(figsize=(18, 6), facecolor=_DARK_BG)

    for col_idx, (title, elev, azim) in enumerate(VIEW_PARAMS):
        ax = fig.add_subplot(1, 3, col_idx + 1, projection="3d")
        ax.set_facecolor(_DARK_BG)
        ax.grid(False)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("#22223a")

        segments = []
        for md in mesh_data.values():
            v = np.array(md["verts"]) if md["verts"] else None
            if v is None or len(v) == 0:
                continue
            seen = set()
            for poly in md["polys"]:
                n = len(poly)
                for i in range(n):
                    a, b = poly[i], poly[(i + 1) % n]
                    key = (min(a, b), max(a, b))
                    if key in seen or a >= len(v) or b >= len(v):
                        continue
                    seen.add(key)
                    segments.append([v[a].tolist(), v[b].tolist()])
            if not md["polys"]:
                for (a, b) in md["edges"]:
                    if a < len(v) and b < len(v):
                        key = (min(a, b), max(a, b))
                        if key not in seen:
                            seen.add(key)
                            segments.append([v[a].tolist(), v[b].tolist()])

        if segments:
            lc = Line3DCollection(
                segments, linewidths=0.35, colors=_EDGE_COL, alpha=0.75
            )
            ax.add_collection3d(lc)

        ax.set_xlim(center[0] - margin, center[0] + margin)
        ax.set_ylim(center[1] - margin, center[1] + margin)
        ax.set_zlim(center[2] - margin, center[2] + margin)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title, color=_SUB_COL, fontsize=9, pad=3)

    asset_label = label or (next(iter(mesh_data)) if mesh_data else "unknown")
    n_verts = sum(len(md["verts"]) for md in mesh_data.values())
    n_faces = sum(len(md["polys"]) for md in mesh_data.values())
    fig.suptitle(
        f"{asset_label}   ({n_verts:,} verts · {n_faces:,} faces)",
        color=_TITLE_COL, fontsize=12, y=0.99,
    )

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(out_path, dpi=110, bbox_inches="tight", facecolor=_DARK_BG)
    plt.close(fig)
    print(f"  [render] Saved: {out_path}")
    return True


# ────────────────────────────────────────────────────────────────────
#  File discovery
# ────────────────────────────────────────────────────────────────────

def find_all_scripts():
    scripts = []
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", "shared")]
        for f in files:
            if f.startswith("sm_") and f.endswith(".py"):
                scripts.append(os.path.join(root, f))
    return sorted(scripts)


def find_changed_scripts(base_ref="origin/main"):
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
            capture_output=True, text=True, check=True,
        )
        return [
            p for p in result.stdout.splitlines()
            if p.startswith("ArtSource/Blender/Scripts/") and
               os.path.basename(p).startswith("sm_") and
               p.endswith(".py")
        ]
    except subprocess.CalledProcessError as e:
        print(f"  [render] git diff failed: {e}")
        return []


# ────────────────────────────────────────────────────────────────────
#  Concept art lookup helper
# ────────────────────────────────────────────────────────────────────

CONCEPTS_ROOT = os.path.join("Content", "ArtDirection", "Concepts")


def find_concept_image(script_src):
    """
    Scan script source for 'Concept: ID1, ID2, ...' and return the first
    matching concept art PNG path, or None.
    """
    import re
    m = re.search(r"Concept:\s*([A-Z]{2,3}-\d+)", script_src)
    if not m:
        return None
    image_id = m.group(1)
    prefix = image_id.split("-")[0]
    folder_map = {
        "LR": "Luminous_Rift", "AD": "Asset_Details",
        "GR": "Glassroot_Forest", "IS": "Inner_Sea",
        "FS": "Fossil_Sky", "GW": "Gravity_Well", "MG": "Mantle_Garden",
        "HE": "Human_Explorer", "NR": "Narrative_Beats", "LT": "Later_Regions",
        "MS": "Material_Studies", "CC": "Composition_Studies", "PW": "Panoramas",
    }
    folder = folder_map.get(prefix)
    if folder:
        candidate = os.path.join(CONCEPTS_ROOT, folder, f"{image_id}.png")
        if os.path.exists(candidate):
            return candidate
    # Fallback: walk the whole concepts tree
    for root, _, files in os.walk(CONCEPTS_ROOT):
        for f in files:
            if f.startswith(image_id):
                return os.path.join(root, f)
    return None


# ────────────────────────────────────────────────────────────────────
#  Main
# ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Render AbyssalEarth asset wireframe previews")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--script", help="Path to a single sm_*.py script")
    group.add_argument("--all",    action="store_true", help="Render all asset scripts")
    group.add_argument("--changed-since", metavar="REF",
                       help="Render scripts changed since git ref (e.g. origin/main)")
    parser.add_argument("--out", default="/tmp/renders",
                        help="Output directory for PNG previews (default: /tmp/renders)")
    args = parser.parse_args()

    if not HAS_MPL:
        print("ERROR: matplotlib and numpy are required.\n"
              "  pip install matplotlib numpy")
        sys.exit(1)
    if not HAS_BPY:
        print("WARNING: bpy not found — previews will be empty placeholders.\n"
              "  pip install bpy")

    if args.script:
        scripts = [args.script]
    elif args.all:
        scripts = find_all_scripts()
    else:
        scripts = find_changed_scripts(args.changed_since)

    if not scripts:
        print("No scripts to render.")
        return

    os.makedirs(args.out, exist_ok=True)
    ok = fail = 0
    for script in scripts:
        stem = os.path.basename(script)[:-3]
        print(f"\n→ {stem}")
        mesh_data = run_script(script)
        out_png = os.path.join(args.out, f"{stem}_preview.png")
        if render_wireframe(mesh_data, out_png, label=stem):
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} rendered, {fail} failed. Output: {args.out}/")


if __name__ == "__main__":
    main()
