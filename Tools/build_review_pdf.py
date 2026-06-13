#!/usr/bin/env python3
"""
build_review_pdf.py — Compile the Phase 1 asset review into a fillable PDF.

Lays out a title page, an executive write-up, and one page per hero asset
pairing the concept art against the Blender wireframe (the GO / NO-GO gate).
Each asset page contains interactive AcroForm fields: GO/NO-GO checkboxes and
a multiline comments text field.

Two-step generation:
  1. matplotlib → _visual.pdf  (all visual layout + comparison images)
  2. reportlab → _fields.pdf   (transparent overlay with AcroForm widgets)
  3. pdfrw merges the two into the final fillable PDF

Dependencies (auto-installed):  reportlab>=4.0, pdfrw>=0.4

Usage:
    python3 Tools/build_review_pdf.py \
        --comparisons /tmp/ae_comparisons \
        --out "Docs/Reviews/AbyssalEarth Asset Review Phase 1 - conducted 2026-06-13 Vivek Mannava Nitish Navaneethakrishnan.pdf"
"""
import argparse
import os
import subprocess
import sys
import tempfile
import textwrap

# ── ensure dependencies ───────────────────────────────────────────────
for pkg in ("reportlab>=4.0", "pdfrw>=0.4"):
    try:
        __import__(pkg.split(">=")[0].replace("-", "_").replace(".", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import letter as RL_LETTER  # 612 × 792 pt
from reportlab.lib.colors import Color as RLColor

from pdfrw import PdfReader, PdfWriter, PdfArray
from pdfrw import PageMerge

# ── colour palette ────────────────────────────────────────────────────
INK      = "#0d1b2a"
ACCENT   = "#2e7d9a"
AMBER    = "#c98a3a"
PAPER    = "#f4f6f8"
MUTED    = "#41506b"

# Reportlab colours (RLColor objects)
RL_INK   = RLColor(0.051, 0.106, 0.165)
RL_MUTED = RLColor(0.255, 0.314, 0.420)
RL_FIELD = RLColor(0.973, 0.976, 0.973)
RL_BORD  = RLColor(0.600, 0.640, 0.680)
RL_AMBER = RLColor(0.788, 0.541, 0.227)
RL_WHITE = RLColor(1, 1, 1)
RL_RED   = RLColor(0.72, 0.18, 0.18)

REVIEW_DATE = "June 13, 2026"
REVIEWERS   = ["Vivek Mannava", "Nitish Navaneethakrishnan"]
N_HEADER_PAGES = 2   # title + overview (no form fields on these)

# ── per-asset data ────────────────────────────────────────────────────
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


# ── STEP 1: matplotlib visual layout ─────────────────────────────────

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
    """
    Visual layout for one asset page. The bottom 26% of the page (~206 pt) is
    intentionally left clear — the reportlab AcroForm overlay fills it with
    interactive Comments and Verdict fields.
    """
    fig = plt.figure(figsize=(8.5, 11))
    _style_page(fig)

    # Header band (top 7%)
    hax = fig.add_axes([0, 0.93, 1, 0.07]); hax.axis("off")
    hax.add_patch(plt.Rectangle((0, 0), 1, 1, color=INK, transform=hax.transAxes))
    hax.add_patch(plt.Rectangle((0, 0), 0.012, 1, color=AMBER, transform=hax.transAxes))
    hax.text(0.03, 0.62, f"{index}.  {asset['title']}", color=PAPER, fontsize=15,
             fontweight="bold", ha="left", va="center", transform=hax.transAxes)
    hax.text(0.03, 0.24, f"{asset['biome']}   ·   Concept: {asset['concept']}",
             color="#9fb3c8", fontsize=9, ha="left", va="center",
             transform=hax.transAxes, family="monospace")

    # Comparison image (41% → 91% of page height, slightly taller than before)
    iax = fig.add_axes([0.06, 0.41, 0.88, 0.50]); iax.axis("off")
    img_path = os.path.join(comparisons_dir, asset["file"])
    iax.imshow(mpimg.imread(img_path))

    # Assessment write-up (26% → 39% — sits above the form field zone)
    tax = fig.add_axes([0.08, 0.27, 0.84, 0.12]); tax.axis("off")
    tax.text(0, 1.0, "Assessment", color=INK, fontsize=11, fontweight="bold",
             ha="left", va="top", transform=tax.transAxes)
    ty = 0.72
    for line in textwrap.wrap(asset["body"], width=100):
        tax.text(0, ty, line, color=MUTED, fontsize=9.5, ha="left", va="top",
                 transform=tax.transAxes)
        ty -= 0.16
        if ty < 0:
            break

    # Separator line above the form area
    sep = fig.add_axes([0.06, 0.258, 0.88, 0.002]); sep.axis("off")
    sep.add_patch(plt.Rectangle((0, 0), 1, 1, color="#c8d4e0", transform=sep.transAxes))

    # Form area hint (bottom 25%) — light background so reviewers know it's interactive
    fax = fig.add_axes([0.06, 0.04, 0.88, 0.21]); fax.axis("off")
    fax.add_patch(mpatches.FancyBboxPatch(
        (0.01, 0.01), 0.98, 0.98,
        boxstyle="round,pad=0.01",
        facecolor="#eef2f6", edgecolor="#b0bec8", linewidth=0.8,
        transform=fax.transAxes,
    ))
    # "Form fields" label hint (will be behind the actual AcroForm fields)
    fax.text(0.5, 0.88, "— Interactive Review Fields —",
             color="#8da0b3", fontsize=8, ha="center", va="top",
             transform=fax.transAxes, style="italic")

    pdf.savefig(fig); plt.close(fig)


def build_visual_pdf(comparisons_dir, out_path):
    with PdfPages(out_path) as pdf:
        title_page(pdf)
        overview_page(pdf)
        for i, asset in enumerate(ASSETS, start=1):
            asset_page(pdf, comparisons_dir, asset, i)
        meta = pdf.infodict()
        meta["Title"] = "AbyssalEarth Asset Review Phase 1"
        meta["Author"] = ", ".join(REVIEWERS)
        meta["Subject"] = "Cross-biome hero asset geometry validation against concept art"


# ── STEP 2: reportlab AcroForm overlay ───────────────────────────────

# Layout constants (PDF points, origin = bottom-left of page)
PAGE_W, PAGE_H = RL_LETTER        # 612 × 792
LM = 49                            # left margin (= 0.08 × 612)
RM = PAGE_W - LM                   # right edge
FIELD_W = RM - LM                  # usable width = 514 pt

# Form field zone: bottom 26% of page ≈ 0–206 pt
ZONE_TOP    = 205   # pt — top of entire form zone
SEP_Y       = 196   # pt — thin separator line

COMMENT_LBL_Y  = 182   # pt — "Reviewer Comments:" label baseline
COMMENT_Y      = 98    # pt — bottom of comments textfield
COMMENT_H      = 78    # pt — height of comments textfield

VERDICT_LBL_Y  = 73    # pt — "Verdict:" label baseline
CB_Y           = 56    # pt — checkbox bottom-left y
CB_SIZE        = 18    # pt — checkbox square size

GO_CB_X        = 152   # pt — GO checkbox x
GO_LBL_X       = 176   # pt — "GO" label x
NOGO_CB_X      = 258   # pt — NO-GO checkbox x
NOGO_LBL_X     = 282   # pt — "NO-GO (refine)" label x


def generate_fields_pdf(n_assets, out_path):
    """
    Produce a PDF with n_assets blank pages, each carrying the AcroForm widgets
    for one asset review page.  The pages are transparent — they'll be merged
    on top of the matplotlib visual pages.
    """
    c = rl_canvas.Canvas(out_path, pagesize=RL_LETTER)
    c.setTitle("AcroForm overlay — AbyssalEarth Phase 1")

    for i in range(n_assets):
        # ── thin separator line at top of form zone ──
        c.setStrokeColor(RL_BORD)
        c.setLineWidth(0.5)
        c.line(LM, SEP_Y, RM, SEP_Y)

        # ── Comments label ──
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(RL_MUTED)
        c.drawString(LM, COMMENT_LBL_Y, "Reviewer Comments:")

        # ── Comments multiline textfield ──
        c.acroForm.textfield(
            name=f"comments_{i+1}",
            tooltip="Type reviewer comments here",
            x=LM,
            y=COMMENT_Y,
            width=FIELD_W,
            height=COMMENT_H,
            fontSize=10,
            fontName="Helvetica",
            borderColor=RL_BORD,
            fillColor=RL_FIELD,
            textColor=RL_INK,
            forceBorder=True,
            fieldFlags="multiline",
        )

        # ── Verdict label ──
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(RL_INK)
        c.drawString(LM, VERDICT_LBL_Y, "Verdict:")

        # ── GO checkbox + label ──
        c.acroForm.checkbox(
            name=f"go_{i+1}",
            tooltip="Check for GO",
            x=GO_CB_X,
            y=CB_Y,
            size=CB_SIZE,
            checked=False,
            buttonStyle="check",
            borderColor=RL_BORD,
            fillColor=RL_WHITE,
        )
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(RL_INK)
        c.drawString(GO_LBL_X, VERDICT_LBL_Y, "GO")

        # ── NO-GO checkbox + label ──
        c.acroForm.checkbox(
            name=f"nogo_{i+1}",
            tooltip="Check for NO-GO (refine)",
            x=NOGO_CB_X,
            y=CB_Y,
            size=CB_SIZE,
            checked=False,
            buttonStyle="check",
            borderColor=RL_BORD,
            fillColor=RL_WHITE,
        )
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(RL_RED)
        c.drawString(NOGO_LBL_X, VERDICT_LBL_Y, "NO-GO (refine)")

        # ── amber accent dot beside verdict label ──
        c.setFillColor(RL_AMBER)
        c.circle(LM - 8, VERDICT_LBL_Y + 4, 3, fill=1, stroke=0)

        c.showPage()

    c.save()


# ── STEP 3: pdfrw page merge ──────────────────────────────────────────

def merge_fields(visual_path, fields_path, out_path):
    """
    Merge AcroForm fields onto the asset pages (pages 3–8, 0-indexed 2–7).
    Title and overview pages (0–1) are passed through unchanged.

    pdfrw's PageMerge merges content streams but drops page-level /Annots and
    the document-level /AcroForm.  We copy both manually so interactive widgets
    survive in the output.
    """
    visual = PdfReader(visual_path)
    fields = PdfReader(fields_path)

    writer = PdfWriter()
    all_widgets = []

    for i, vpage in enumerate(visual.pages):
        if i >= N_HEADER_PAGES:
            fpage = fields.pages[i - N_HEADER_PAGES]
            # Merge fields page content (appearance visuals) into base page
            PageMerge(vpage).add(fpage).render()
            # Copy widget annotations from the fields page onto the base page
            if fpage.Annots:
                existing = list(vpage.Annots) if vpage.Annots else []
                vpage.Annots = PdfArray(existing + list(fpage.Annots))
                all_widgets.extend(list(fpage.Annots))
        writer.addpage(vpage)

    # Copy document-level /AcroForm (field registry) from the fields PDF
    if fields.Root.AcroForm:
        acroform = fields.Root.AcroForm
        acroform.Fields = PdfArray(all_widgets)
        writer.trailer.Root.AcroForm = acroform

    writer.write(out_path)


# ── main ──────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comparisons", default="/tmp/ae_comparisons")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        visual_pdf = os.path.join(tmp, "_visual.pdf")
        fields_pdf = os.path.join(tmp, "_fields.pdf")

        print("[review-pdf] Rendering visual layout …")
        build_visual_pdf(args.comparisons, visual_pdf)

        print("[review-pdf] Generating AcroForm overlay …")
        generate_fields_pdf(len(ASSETS), fields_pdf)

        print("[review-pdf] Merging pages …")
        merge_fields(visual_pdf, fields_pdf, args.out)

    print(f"[review-pdf] Fillable PDF written → {args.out}")


if __name__ == "__main__":
    main()
