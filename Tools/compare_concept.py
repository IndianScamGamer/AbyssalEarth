#!/usr/bin/env python3
"""
compare_concept.py — side-by-side concept art vs rendered wireframe composite.

Usage:
    # Single comparison
    python3 Tools/compare_concept.py \
        --render /tmp/renders/sm_orb_hub_preview.png \
        --concept Content/ArtDirection/Concepts/Asset_Details/AD-001.png \
        --out /tmp/comparisons/sm_orb_hub_vs_concept.png

    # Batch: auto-match renders to concept art via Concept: line in script
    python3 Tools/compare_concept.py \
        --renders-dir /tmp/renders/ \
        --scripts-dir ArtSource/Blender/Scripts/ \
        --concepts-dir Content/ArtDirection/Concepts/ \
        --out /tmp/comparisons/

Output: 1920×960 PNG with concept art (top) and wireframe preview (bottom),
        labelled with asset name and concept ID.

Requires: Pillow   (pip install Pillow)
"""

import argparse
import os
import re
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

CONCEPTS_ROOT = os.path.join("Content", "ArtDirection", "Concepts")
SCRIPTS_DIR   = os.path.join("ArtSource", "Blender", "Scripts")

TARGET_W = 1920
HALF_H   = 480   # half of 960 total height
BG_COLOR = (13, 13, 20)
LABEL_BG = (20, 20, 35)
LABEL_FG = (170, 200, 255)
SEP_COL  = (40, 50, 80)


def _resize_fit(img, w, h):
    """Resize img to fit within (w, h), preserving aspect ratio."""
    iw, ih = img.size
    scale = min(w / iw, h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    return img.resize((nw, nh), Image.LANCZOS)


def make_composite(render_path, concept_path, out_path, label=""):
    if not HAS_PIL:
        print("ERROR: Pillow not installed. pip install Pillow")
        return False

    canvas = Image.new("RGB", (TARGET_W, HALF_H * 2 + 40), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    def _load_panel(path, y_offset, title):
        if path and os.path.exists(path):
            img = Image.open(path).convert("RGB")
            img = _resize_fit(img, TARGET_W - 4, HALF_H - 30)
            x = (TARGET_W - img.width) // 2
            canvas.paste(img, (x, y_offset + 26))
        else:
            draw.text((TARGET_W // 2, y_offset + HALF_H // 2),
                      f"[{title} not found]",
                      fill=(100, 80, 80), anchor="mm")
        draw.rectangle([0, y_offset, TARGET_W, y_offset + 24], fill=LABEL_BG)
        draw.text((8, y_offset + 4), title, fill=LABEL_FG)

    _load_panel(concept_path, 0, f"CONCEPT ART — {label}")
    draw.line([(0, HALF_H + 20), (TARGET_W, HALF_H + 20)], fill=SEP_COL, width=2)
    _load_panel(render_path,  HALF_H + 22, f"BLENDER WIREFRAME — {label}")

    # Bottom label bar
    draw.rectangle([0, HALF_H * 2 + 2, TARGET_W, HALF_H * 2 + 40], fill=LABEL_BG)
    note = (
        "Visual acceptance gate: geometry silhouette must clearly echo the concept art. "
        "Scale, mass distribution, and distinctive shape language are the checkpoints."
    )
    draw.text((TARGET_W // 2, HALF_H * 2 + 22), note, fill=(90, 100, 130), anchor="mm")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    canvas.save(out_path)
    print(f"  [compare] Saved: {out_path}")
    return True


# ────────────────────────────────────────────────────────────────────
#  Batch mode helpers
# ────────────────────────────────────────────────────────────────────

_FOLDER_MAP = {
    "LR": "Luminous_Rift",
    "AD": "Asset_Details",
    "GR": "Glassroot_Forest",
    "IS": "Inner_Sea",
    "FS": "Fossil_Sky",
    "GW": "Gravity_Well",
    "MG": "Mantle_Garden",
    "HE": "Human_Explorer",
    "NR": "Narrative_Beats",
    "LT": "Later_Regions",
    "MS": "Material_Studies",
    "CC": "Composition_Studies",
    "PW": "Panoramas",
}


def _find_concept(image_id, concepts_dir):
    prefix = image_id.split("-")[0]
    folder = _FOLDER_MAP.get(prefix)
    if folder:
        p = os.path.join(concepts_dir, folder, f"{image_id}.png")
        if os.path.exists(p):
            return p
    for root, _, files in os.walk(concepts_dir):
        for f in files:
            if f.startswith(image_id) and f.endswith(".png"):
                return os.path.join(root, f)
    return None


def _extract_concept_ids(script_path):
    """Return list of concept image IDs found in the script's Concept: line."""
    try:
        with open(script_path, encoding="utf-8") as fh:
            src = fh.read()
        m = re.search(r"Concept:\s*([^\n]+)", src)
        if not m:
            return []
        raw = m.group(1)
        return re.findall(r"[A-Z]{2,3}-\d+", raw)
    except OSError:
        return []


def batch_compare(renders_dir, scripts_dir, concepts_dir, out_dir):
    """Auto-match rendered previews to concept art via Concept: line in script src."""
    if not HAS_PIL:
        print("ERROR: Pillow not installed. pip install Pillow")
        return

    # Build map: stem → script path
    stem_to_script = {}
    for root, _, files in os.walk(scripts_dir):
        for f in files:
            if f.startswith("sm_") and f.endswith(".py"):
                stem_to_script[f[:-3]] = os.path.join(root, f)

    rendered = [
        f for f in os.listdir(renders_dir)
        if f.endswith("_preview.png")
    ]
    if not rendered:
        print(f"  [compare] No *_preview.png files found in {renders_dir}")
        return

    ok = 0
    for fname in sorted(rendered):
        stem = fname[: -len("_preview.png")]
        render_path = os.path.join(renders_dir, fname)
        script_path = stem_to_script.get(stem)
        concept_ids = _extract_concept_ids(script_path) if script_path else []
        concept_path = None
        for cid in concept_ids:
            candidate = _find_concept(cid, concepts_dir)
            if candidate:
                concept_path = candidate
                break
        out_path = os.path.join(out_dir, f"{stem}_vs_concept.png")
        label = f"{stem}  [{', '.join(concept_ids) or 'no Concept: tag'}]"
        make_composite(render_path, concept_path, out_path, label=label)
        ok += 1

    print(f"\n[compare] {ok} composite(s) written to {out_dir}/")


# ────────────────────────────────────────────────────────────────────
#  CLI
# ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Concept art vs wireframe comparison composites")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--render",      help="Path to single rendered preview PNG")
    mode.add_argument("--renders-dir", help="Directory of *_preview.png files (batch mode)")
    parser.add_argument("--concept",      help="Path to concept art PNG (single mode)")
    parser.add_argument("--concepts-dir", default=CONCEPTS_ROOT,
                        help=f"Root concepts directory (default: {CONCEPTS_ROOT})")
    parser.add_argument("--scripts-dir",  default=SCRIPTS_DIR,
                        help=f"Scripts root for Concept: tag lookup (default: {SCRIPTS_DIR})")
    parser.add_argument("--out", required=True,
                        help="Output path (single: file) or directory (batch)")
    args = parser.parse_args()

    if not HAS_PIL:
        print("ERROR: Pillow is required.  pip install Pillow")
        sys.exit(1)

    if args.render:
        label = os.path.basename(args.render).replace("_preview.png", "")
        make_composite(args.render, args.concept, args.out, label=label)
    else:
        batch_compare(args.renders_dir, args.scripts_dir, args.concepts_dir, args.out)


if __name__ == "__main__":
    main()
