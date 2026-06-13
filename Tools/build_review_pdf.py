#!/usr/bin/env python3
"""
build_review_pdf.py — Compile the Phase 1 asset review into a single PDF.

Lays out a title page, an executive write-up, and one page per hero asset
pairing the concept art against the Blender wireframe (the GO / NO-GO gate).

Usage:
    python3 Tools/build_review_pdf.py \
        --comparisons /tmp/ae_comparisons \
        --out "Docs/Reviews/AbyssalEarth Asset Review Phase 1 - conducted 2026-06-13 Vivek Mannava Nitish Navaneethakrishnan.pdf"
"""
import argparse
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# ── colour palette (matches the abyssal art direction) ───────────────
INK      = "#0d1b2a"
ACCENT   = "#2e7d9a"
AMBER    = "#c98a3a"
PAPER    = "#f4f6f8"
MUTED    = "#41506b"

REVIEW_DATE = "June 13, 2026"
REVIEWERS   = ["Vivek Mannava", "Nitish Navaneethakrishnan"]

# ── per-asset narrative (concept → wireframe verdict notes) ──────────
ASSETS = [
    {
        "file": "sm_orb_hub_vs_concept.png",
        "title": "Orb Hub — Luminous Rift",
        "concept": "AD-001, LR-006, LR-007",
        "biome": "Luminous Rift",
        "body": (
            "The original build produced a 2.8 m sphere with eight wire-thin arms in the wrong "
            "plane — roughly a fifth of the intended scale and none of the mechanical mass. The "
            "rewrite lays a 76 m annular ring (48-segment tube) in the XY plane, drives eight "
            "rectangular box-beam spoke arms inward to a 24 m central orb, and hangs an "
            "observation platform below on cable struts. Cable grooves, junction nodes and beam "
            "emitter ports restore the heavy machined silhouette AD-001 looks up into."
        ),
    },
    {
        "file": "sm_glassroot_root_column_hero_vs_concept.png",
        "title": "Glassroot Root Column — Glassroot Forest",
        "concept": "GR-001, GR-002",
        "biome": "Glassroot Forest",
        "body": (
            "The defining feature of GR-001 — sweeping buttress roots — was previously authored "
            "as loose vertices with no faces, rendering invisible. The rewrite sweeps five fin "
            "cross-sections along a curved path from trunk to ground as a true lofted surface, "
            "flares the 20-sided trunk with organic radius noise, and replaces the floating vein "
            "ridges with connected quad strips. Crystal accents anchor the buttress feet."
        ),
    },
    {
        "file": "sm_inner_sea_submerged_ruin_a_vs_concept.png",
        "title": "Submerged Ruin — Inner Sea",
        "concept": "IS-001, IS-003",
        "biome": "Inner Sea",
        "body": (
            "What read as a flat machine wall panel is now ancient stone architecture: a "
            "four-sided tapered tower with gothic arched window recesses per floor, pilaster "
            "corners, a jagged broken crown, base erosion boulders and waterline barnacles. A "
            "22 degree tilt sells the sinking, collapsing pose IS-001 frames in the dark teal sea."
        ),
    },
    {
        "file": "sm_fossil_sky_ceiling_skeleton_hero_a_vs_concept.png",
        "title": "Ceiling Skeleton — Fossil Sky",
        "concept": "FS-002, FS-003",
        "biome": "Fossil Sky",
        "body": (
            "The previous skeleton was a string of unmerged icosphere blobs. The spine is now a "
            "continuous lofted tube whose radius profile swells at mid-body and tapers toward the "
            "skull, with dorsal vertebrae bumps; ribs are swept tubes following parametric arcs; "
            "the skull resolves into cranium, rostrum, jaw and eye-socket rings. The assembly is "
            "ceiling-mounted (Z <= 0) so the bones hang as the concept demands."
        ),
    },
    {
        "file": "sm_portal_ring_vs_concept.png",
        "title": "Portal Ring — Gravity Well",
        "concept": "GW-001",
        "biome": "Gravity Well",
        "body": (
            "A circular pipe torus was standing in for what GW-001 clearly shows as a rectangular "
            "stone gate. The rewrite builds two chamfered pillars and a connecting lintel, insets "
            "amber rune panels along the inner faces, seats the pillars on wide plinths, and adds "
            "triangular flanges that key the gate into the cave wall."
        ),
    },
    {
        "file": "sm_mantle_garden_mineral_flower_a_vs_concept.png",
        "title": "Mineral Flower — Mantle Garden",
        "concept": "MG-001, MG-002",
        "biome": "Mantle Garden",
        "body": (
            "Fat hexagonal prisms became sharp faceted spires. Each spire lofts a hexagonal "
            "cross-section with a per-metre twist and an ease=t^1.6 taper down to a near-zero "
            "0.005 m tip, clustered in a burst with outward tilt over an obsidian mound carved "
            "with heat-crack channels. Two variants ship: A (9 primary spires, 2.8 m) and "
            "B (21 primary spires, 3.5 m)."
        ),
    },
]


def _style_page(fig):
    fig.patch.set_facecolor(PAPER)


def title_page(pdf):
    fig = plt.figure(figsize=(8.5, 11))
    _style_page(fig)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")

    ax.add_patch(plt.Rectangle((0, 0.86), 1, 0.14, color=INK, transform=ax.transAxes))
    ax.add_patch(plt.Rectangle((0, 0.845), 1, 0.015, color=AMBER, transform=ax.transAxes))

    ax.text(0.5, 0.945, "ABYSSALEARTH", color=PAPER, fontsize=30, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes, family="monospace")
    ax.text(0.5, 0.895, "ASSET REVIEW  ·  PHASE 1", color="#cfd8e3", fontsize=14,
            ha="center", va="center", transform=ax.transAxes, family="monospace")

    ax.text(0.5, 0.70, "Cross-Biome Hero Asset", color=INK, fontsize=22, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes)
    ax.text(0.5, 0.655, "Geometry Validation Against Concept Art", color=ACCENT, fontsize=16,
            ha="center", va="center", transform=ax.transAxes)

    ax.text(0.5, 0.50, f"Conducted {REVIEW_DATE}", color=MUTED, fontsize=13,
            ha="center", va="center", transform=ax.transAxes)
    ax.text(0.5, 0.45, "Reviewers", color=MUTED, fontsize=11,
            ha="center", va="center", transform=ax.transAxes, family="monospace")
    for i, name in enumerate(REVIEWERS):
        ax.text(0.5, 0.41 - i * 0.035, name, color=INK, fontsize=14, fontweight="bold",
                ha="center", va="center", transform=ax.transAxes)

    ax.text(0.5, 0.09,
            "Ground truth: the concept art.  This document is the GO / NO-GO gate before\n"
            "Phase 2 (full Luminous Rift sweep) and, ultimately, UE5 implementation.",
            color=MUTED, fontsize=9, ha="center", va="center",
            transform=ax.transAxes, style="italic")
    pdf.savefig(fig); plt.close(fig)


def overview_page(pdf):
    fig = plt.figure(figsize=(8.5, 11))
    _style_page(fig)
    ax = fig.add_axes([0.08, 0.05, 0.84, 0.9]); ax.axis("off")

    y = 0.97
    ax.text(0, y, "Executive Summary", color=INK, fontsize=20, fontweight="bold",
            ha="left", va="top", transform=ax.transAxes)
    y -= 0.05
    ax.add_patch(plt.Rectangle((0, y), 1, 0.004, color=AMBER, transform=ax.transAxes))
    y -= 0.03

    paras = [
        "Phase 1 selects one hero asset from each of the six biomes and rebuilds its Blender "
        "greybox geometry so the silhouette reads unambiguously as the concept art intends. "
        "These six are the most visually distinctive shapes in their biomes; getting their mass, "
        "scale and shape language right de-risks the long tail of supporting assets that follow.",

        "Every prior build shared one of two failure modes. The first is broken geometry: loose "
        "vertices authored with no faces (the Glassroot buttress roots, the vein ridges) or "
        "chains of unmerged primitives masquerading as a single form (the Fossil Sky spine). "
        "The second is wrong shape language at the right-ish scale: a circular pipe where a "
        "rectangular gate belongs, fat prisms where sharp crystal spires belong, a flat panel "
        "where a leaning stone tower belongs.",

        "Each rewrite is documented against its reference image IDs (recorded in the script "
        "docstring under a Concept: tag) and constrained by named UPPER_CASE scale constants so "
        "the dimensions are auditable rather than buried as magic numbers. All sixteen CI "
        "validation checks pass on the branch, including the new concept-reference, "
        "floating-vertex, scale-constant and render-guard checks.",

        "The pages that follow pair each concept image (top) with the Blender wireframe (bottom). "
        "The reviewer checkpoints are scale, mass distribution, and distinctive shape language — "
        "not surface finish, which is a UE5 material and lighting concern handled at handoff. A "
        "GO advances the asset; a NO-GO triggers a geometry refinement round before Phase 2.",
    ]
    for p in paras:
        for line in textwrap.wrap(p, width=92):
            ax.text(0, y, line, color=MUTED, fontsize=10.5, ha="left", va="top",
                    transform=ax.transAxes)
            y -= 0.025
        y -= 0.015

    y -= 0.01
    ax.text(0, y, "Assets under review", color=INK, fontsize=13, fontweight="bold",
            ha="left", va="top", transform=ax.transAxes)
    y -= 0.032
    for a in ASSETS:
        ax.text(0.02, y, f"•  {a['title']}", color=INK, fontsize=10.5, ha="left", va="top",
                transform=ax.transAxes)
        ax.text(0.66, y, f"Concept: {a['concept']}", color=ACCENT, fontsize=9,
                ha="left", va="top", transform=ax.transAxes, family="monospace")
        y -= 0.028
    pdf.savefig(fig); plt.close(fig)


def asset_page(pdf, comparisons_dir, asset, index):
    fig = plt.figure(figsize=(8.5, 11))
    _style_page(fig)

    # header band
    hax = fig.add_axes([0, 0.93, 1, 0.07]); hax.axis("off")
    hax.add_patch(plt.Rectangle((0, 0), 1, 1, color=INK, transform=hax.transAxes))
    hax.add_patch(plt.Rectangle((0, 0), 0.012, 1, color=AMBER, transform=hax.transAxes))
    hax.text(0.03, 0.62, f"{index}.  {asset['title']}", color=PAPER, fontsize=15,
             fontweight="bold", ha="left", va="center", transform=hax.transAxes)
    hax.text(0.03, 0.24, f"{asset['biome']}   ·   Concept: {asset['concept']}",
             color="#9fb3c8", fontsize=9, ha="left", va="center",
             transform=hax.transAxes, family="monospace")

    # comparison image
    iax = fig.add_axes([0.06, 0.40, 0.88, 0.50]); iax.axis("off")
    img_path = os.path.join(comparisons_dir, asset["file"])
    iax.imshow(mpimg.imread(img_path))

    # write-up
    tax = fig.add_axes([0.08, 0.06, 0.84, 0.30]); tax.axis("off")
    y = 0.98
    tax.text(0, y, "Assessment", color=INK, fontsize=12, fontweight="bold",
             ha="left", va="top", transform=tax.transAxes)
    y -= 0.10
    for line in textwrap.wrap(asset["body"], width=96):
        tax.text(0, y, line, color=MUTED, fontsize=10, ha="left", va="top",
                 transform=tax.transAxes)
        y -= 0.075
    y -= 0.04
    tax.text(0, y, "Verdict:  ☐ GO        ☐ NO-GO (refine)", color=INK, fontsize=11,
             fontweight="bold", ha="left", va="top", transform=tax.transAxes)
    pdf.savefig(fig); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comparisons", default="/tmp/ae_comparisons")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with PdfPages(args.out) as pdf:
        title_page(pdf)
        overview_page(pdf)
        for i, asset in enumerate(ASSETS, start=1):
            asset_page(pdf, args.comparisons, asset, i)
        meta = pdf.infodict()
        meta["Title"] = "AbyssalEarth Asset Review Phase 1"
        meta["Author"] = ", ".join(REVIEWERS)
        meta["Subject"] = "Cross-biome hero asset geometry validation against concept art"
    print(f"[review-pdf] wrote {args.out}")


if __name__ == "__main__":
    main()
