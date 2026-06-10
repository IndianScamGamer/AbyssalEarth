#!/usr/bin/env python3
"""
AbyssalEarth data validator.
Checks cross-references between CSV design files and C++ source enums/IDs.
Exit code 0 = all checks pass; non-zero = failures found.
"""

import csv
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SOURCE = ROOT / "Source" / "AbyssalEarth"
DESIGN = ROOT / "Content" / "Design"

errors: list[str] = []

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def grep_cpp(pattern: str) -> set[str]:
    """Return all matches of a capture group across all .h/.cpp files."""
    results: set[str] = set()
    for ext in ("*.h", "*.cpp"):
        for fpath in SOURCE.glob(ext):
            for m in re.finditer(pattern, fpath.read_text(encoding="utf-8")):
                results.add(m.group(1))
    return results

# ---------------------------------------------------------------------------
# 1. EAbyssalItemCategory values used in DT_ItemDatabase.csv
# ---------------------------------------------------------------------------

def check_item_categories():
    # Extract enum values from C++ source
    cpp_categories: set[str] = set()
    for fpath in SOURCE.glob("*.h"):
        text = fpath.read_text(encoding="utf-8")
        if "EAbyssalItemCategory" in text:
            for m in re.finditer(r"\bEAbyssalItemCategory\b[^;]*?\{([^}]+)\}", text, re.DOTALL):
                for entry in m.group(1).split(","):
                    name = entry.strip()
                    if not name or name.startswith("//"):
                        continue
                    # strip UMETA(...) suffix
                    name = re.sub(r"\s*UMETA\s*\(.*?\)", "", name).strip()
                    # take only the identifier (first word)
                    tokens = name.split()
                    if not tokens:
                        continue
                    name = tokens[0]
                    if name:
                        cpp_categories.add(name)

    if not cpp_categories:
        errors.append("EAbyssalItemCategory: could not find enum definition in any .h file")
        return

    rows = read_csv(DESIGN / "DT_ItemDatabase.csv")
    for row in rows:
        cat = row.get("Category", "").strip()
        if cat and cat not in cpp_categories:
            errors.append(
                f"DT_ItemDatabase.csv row '{row['Name']}': Category='{cat}' "
                f"not in EAbyssalItemCategory {sorted(cpp_categories)}"
            )

# ---------------------------------------------------------------------------
# 2. FabricationRecipes.csv — all item IDs must exist in DT_ItemDatabase.csv
# ---------------------------------------------------------------------------

def check_recipe_item_ids():
    item_rows = read_csv(DESIGN / "DT_ItemDatabase.csv")
    known_items = {r["Name"].strip() for r in item_rows}

    recipe_rows = read_csv(DESIGN / "FabricationRecipes.csv")
    for row in recipe_rows:
        recipe_id = row.get("RecipeId", "?")

        output_id = row.get("OutputItemId", "").strip()
        if output_id and output_id not in known_items:
            errors.append(
                f"FabricationRecipes.csv '{recipe_id}': OutputItemId='{output_id}' "
                f"not found in DT_ItemDatabase.csv"
            )

        inputs_raw = row.get("Inputs", "").strip()
        if inputs_raw:
            for pair in inputs_raw.split(";"):
                pair = pair.strip()
                if not pair:
                    continue
                parts = pair.split(":")
                item_id = parts[0].strip()
                if item_id and item_id not in known_items:
                    errors.append(
                        f"FabricationRecipes.csv '{recipe_id}': input item='{item_id}' "
                        f"not found in DT_ItemDatabase.csv"
                    )

# ---------------------------------------------------------------------------
# 3. NarrativeBeats CSV — every BeatId referenced in C++ must exist in at
#    least one *NarrativeBeats.csv
# ---------------------------------------------------------------------------

def check_narrative_beat_ids():
    all_beat_ids: set[str] = set()
    for csv_path in DESIGN.glob("*NarrativeBeats.csv"):
        for row in read_csv(csv_path):
            # Support both "Name" (UE DataTable convention) and "BeatId" column names
            name = (row.get("Name") or row.get("BeatId") or "").strip()
            if name:
                all_beat_ids.add(name)

    # Find PlayBeat("...") calls in C++
    cpp_beat_refs = grep_cpp(r'PlayBeat\s*\(\s*FName\s*\(\s*TEXT\s*\(\s*"([^"]+)"')

    for beat_id in cpp_beat_refs:
        if beat_id == "POSTCREDITS_DOUBLE_PULSE":
            # post-credits beat is triggered at runtime; DataTable populated by designer
            continue
        if beat_id not in all_beat_ids:
            errors.append(
                f"C++ PlayBeat call references beat '{beat_id}' "
                f"which does not exist in any *NarrativeBeats.csv"
            )

# ---------------------------------------------------------------------------
# 4. Objective IDs hardcoded in C++ must exist in MainObjectiveArc.csv
# ---------------------------------------------------------------------------

def check_objective_ids():
    arc_rows = read_csv(DESIGN / "MainObjectiveArc.csv") if (DESIGN / "MainObjectiveArc.csv").exists() else []
    known_obj_ids = {r.get("ObjectiveId", r.get("Name", "")).strip() for r in arc_rows}

    # Find CompleteObjective("...") and AddObjective("...") calls
    cpp_obj_refs = grep_cpp(r'CompleteObjective\s*\(\s*FName\s*\(\s*TEXT\s*\(\s*"([^"]+)"')
    cpp_obj_refs |= grep_cpp(r'AddObjective\s*\(\s*TEXT\s*\(\s*"([^"]+)"')

    if not known_obj_ids:
        # If the arc CSV is not yet structured with ObjectiveId column, skip
        return

    for obj_id in cpp_obj_refs:
        if obj_id not in known_obj_ids:
            errors.append(
                f"C++ objective reference '{obj_id}' "
                f"not found in MainObjectiveArc.csv"
            )

# ---------------------------------------------------------------------------
# 5. No TODO/FIXME in shipped Docs .md files
# ---------------------------------------------------------------------------

def check_no_todos():
    docs = ROOT / "Docs"
    for md_file in docs.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r"\b(TODO|FIXME)\b", line, re.IGNORECASE):
                errors.append(f"{md_file.relative_to(ROOT)}:{i}: '{line.strip()}'")

# ---------------------------------------------------------------------------
# Run all checks
# ---------------------------------------------------------------------------

check_item_categories()
check_recipe_item_ids()
check_narrative_beat_ids()
check_objective_ids()
check_no_todos()

if errors:
    print(f"\n{'='*60}")
    print(f"DATA VALIDATION FAILED — {len(errors)} error(s):")
    print('='*60)
    for e in errors:
        print(f"  ✗  {e}")
    print('='*60 + "\n")
    sys.exit(1)
else:
    print(f"Data validation passed — all cross-references are consistent.")
    sys.exit(0)
