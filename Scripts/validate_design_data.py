#!/usr/bin/env python3
"""Validate Abyssal Earth design data that can drift outside Unreal.

This script is intentionally standard-library only so Linux/OpenClaw and
Windows workers can run it before committing docs, manifests, and prompts.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN_DIR = ROOT / "Content" / "Design"

CSV_SPECS = {
    "AbyssalInterfaceResponseModes.csv": {
        "columns": ["Mode", "Use", "MaxLength", "CanSuggestEvents", "Tone"],
        "id": "Mode",
    },
    "DT_LuminousRiftAmbience.csv": {
        "columns": [
            "CueId", "Zone", "Priority", "LoopCue", "StingerCue", "Intensity",
            "FadeInSeconds", "FadeOutSeconds", "ReverbProfile", "Notes",
        ],
        "id": "CueId",
    },
    "DiscoveryCatalog.csv": {
        "columns": ["DiscoveryId", "DisplayName", "Category", "Zone", "JournalText"],
        "id": "DiscoveryId",
    },
    "LuminousRiftAssetManifest.csv": {
        "columns": [
            "AssetName", "Priority", "AssetType", "ZoneOrUse",
            "ApproxDimensionsMeters", "MaterialSlots", "Status", "Notes",
        ],
        "id": "AssetName",
    },
    "LuminousRiftAssetImportChecklist.csv": {
        "columns": [
            "AssetName", "Priority", "ImportTargetPath", "SourcePrompt",
            "RequiredMaterialSlots", "PivotCheck", "CollisionCheck",
            "NaniteOrLOD", "PlacementZone", "AcceptanceCheck", "Status", "Notes",
        ],
        "id": "AssetName",
    },
    "LuminousRiftBlockoutChecklist.csv": {
        "columns": [
            "ChecklistId", "Zone", "ObjectType", "TargetName", "Priority",
            "ApproxLocation", "Status", "AcceptanceCriteria", "Notes",
        ],
        "id": "ChecklistId",
    },
    "MainObjectiveArc.csv": {
        "columns": ["ObjectiveId", "Title", "Phase", "Description", "GameplayMeaning"],
        "id": "ObjectiveId",
    },
    "PrologueSequence.csv": {
        "columns": [
            "BeatId", "BeatName", "Location", "PlayerControl", "PrimaryPurpose",
            "KeyContent", "ExitCondition",
        ],
        "id": "BeatId",
    },
    "WorldAssetManifest.csv": {
        "columns": [
            "MapId", "AssetName", "Priority", "AssetType",
            "ApproxDimensionsMeters", "MaterialSlots", "Status", "Notes",
        ],
        "id": ("MapId", "AssetName"),
    },
    "WorldMapManifest.csv": {
        "columns": [
            "MapId", "MapName", "Priority", "ReferenceImage", "CoreFantasy",
            "PrimaryTraversal", "ColorTriad", "KeyLandmark", "PrimaryHazard", "Status",
        ],
        "id": "MapId",
    },
}

VALID_PRIORITIES = {"P0", "P1", "P2", "P3", "Later"}
VALID_ASSET_STATUSES = {"Needed", "PromptReady", "InProgress", "Exported", "Imported", "Placed", "Done"}
PROMPT_RE = re.compile(r"Docs/AssetPrompts/[^\s.,)]+\.md")


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def read_csv(path: Path, expected_columns: list[str], errors: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        add_error(errors, f"Missing CSV: {path.relative_to(ROOT)}")
        return []

    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != expected_columns:
                add_error(
                    errors,
                    f"{path.relative_to(ROOT)} header mismatch: expected {expected_columns}, got {reader.fieldnames}",
                )
                return []
            rows = list(reader)
    except csv.Error as exc:
        add_error(errors, f"{path.relative_to(ROOT)} CSV parse error: {exc}")
        return []

    if not rows:
        add_error(errors, f"{path.relative_to(ROOT)} has no data rows")
    return rows


def key_for(row: dict[str, str], key_spec: str | tuple[str, ...]) -> str:
    if isinstance(key_spec, tuple):
        return "::".join(row.get(part, "").strip() for part in key_spec)
    return row.get(key_spec, "").strip()


def validate_required_values(path: Path, rows: list[dict[str, str]], errors: list[str]) -> None:
    optional_columns = {"Notes", "JournalText", "Description", "GameplayMeaning", "KeyContent", "ExitCondition"}
    for index, row in enumerate(rows, start=2):
        for column, value in row.items():
            if value is None:
                add_error(errors, f"{path.relative_to(ROOT)} line {index}: malformed row")
                continue
            if column in optional_columns:
                continue
            if not value.strip():
                add_error(errors, f"{path.relative_to(ROOT)} line {index}: empty {column}")


def validate_unique_ids(
    path: Path,
    rows: list[dict[str, str]],
    key_spec: str | tuple[str, ...],
    errors: list[str],
) -> None:
    seen: dict[str, int] = {}
    for index, row in enumerate(rows, start=2):
        key = key_for(row, key_spec)
        if not key:
            add_error(errors, f"{path.relative_to(ROOT)} line {index}: empty key {key_spec}")
        elif key in seen:
            add_error(errors, f"{path.relative_to(ROOT)} line {index}: duplicate key {key} first seen on line {seen[key]}")
        else:
            seen[key] = index


def validate_priorities(path: Path, rows: list[dict[str, str]], errors: list[str]) -> None:
    for index, row in enumerate(rows, start=2):
        priority = row.get("Priority", "").strip()
        if priority and priority not in VALID_PRIORITIES:
            add_error(errors, f"{path.relative_to(ROOT)} line {index}: unknown Priority {priority}")


def validate_asset_manifest(path: Path, rows: list[dict[str, str]], errors: list[str]) -> None:
    for index, row in enumerate(rows, start=2):
        asset_name = row["AssetName"].strip()
        status = row["Status"].strip()
        notes = row["Notes"]
        material_slots = [slot.strip() for slot in row["MaterialSlots"].split(";") if slot.strip()]

        if not asset_name.startswith(("SM_", "BP_", "M_", "T_", "VFX_")):
            add_error(errors, f"{path.relative_to(ROOT)} line {index}: asset name {asset_name} should use project prefix")
        if not material_slots:
            add_error(errors, f"{path.relative_to(ROOT)} line {index}: no material slots listed for {asset_name}")
        if status not in VALID_ASSET_STATUSES:
            add_error(errors, f"{path.relative_to(ROOT)} line {index}: unknown Status {status}")

        prompt_matches = PROMPT_RE.findall(notes)
        if status == "PromptReady" and not prompt_matches:
            add_error(errors, f"{path.relative_to(ROOT)} line {index}: PromptReady asset {asset_name} lacks prompt path")
        for prompt in prompt_matches:
            if not (ROOT / prompt).exists():
                add_error(errors, f"{path.relative_to(ROOT)} line {index}: missing prompt file {prompt}")


def validate_luminous_rift_import_checklist(rows: list[dict[str, str]], errors: list[str]) -> None:
    manifest_rows = read_csv(
        DESIGN_DIR / "LuminousRiftAssetManifest.csv",
        CSV_SPECS["LuminousRiftAssetManifest.csv"]["columns"],
        errors,
    )
    manifest_assets = {row["AssetName"].strip() for row in manifest_rows}

    for index, row in enumerate(rows, start=2):
        asset_name = row["AssetName"].strip()
        status = row["Status"].strip()
        import_target = row["ImportTargetPath"].strip()
        source_prompt = row["SourcePrompt"].strip()
        material_slots = [slot.strip() for slot in row["RequiredMaterialSlots"].split(";") if slot.strip()]

        if asset_name not in manifest_assets:
            add_error(errors, f"Content/Design/LuminousRiftAssetImportChecklist.csv line {index}: {asset_name} is not listed in LuminousRiftAssetManifest.csv")
        if status not in VALID_ASSET_STATUSES:
            add_error(errors, f"Content/Design/LuminousRiftAssetImportChecklist.csv line {index}: unknown Status {status}")
        if not import_target.startswith("Content/ArtSourceExports/LuminousRift/"):
            add_error(errors, f"Content/Design/LuminousRiftAssetImportChecklist.csv line {index}: import target should live under Content/ArtSourceExports/LuminousRift/")
        if not import_target.endswith((".fbx", ".glb")):
            add_error(errors, f"Content/Design/LuminousRiftAssetImportChecklist.csv line {index}: import target should be .fbx or .glb")
        if source_prompt and not (ROOT / source_prompt).exists():
            add_error(errors, f"Content/Design/LuminousRiftAssetImportChecklist.csv line {index}: missing source prompt {source_prompt}")
        if not material_slots:
            add_error(errors, f"Content/Design/LuminousRiftAssetImportChecklist.csv line {index}: no required material slots listed")


def validate_world_maps(rows: list[dict[str, str]], errors: list[str]) -> set[str]:
    map_ids = set()
    for index, row in enumerate(rows, start=2):
        map_id = row["MapId"].strip()
        map_ids.add(map_id)
        reference = row["ReferenceImage"].strip()
        if reference and not (ROOT / reference).exists():
            add_error(errors, f"Content/Design/WorldMapManifest.csv line {index}: missing reference image {reference}")
    return map_ids


def validate_world_assets(rows: list[dict[str, str]], map_ids: set[str], errors: list[str]) -> None:
    for index, row in enumerate(rows, start=2):
        map_id = row["MapId"].strip()
        if map_id not in map_ids:
            add_error(errors, f"Content/Design/WorldAssetManifest.csv line {index}: unknown MapId {map_id}")


def validate_objective_ids(errors: list[str]) -> None:
    source_path = ROOT / "Source" / "AbyssalEarth" / "ObjectiveSubsystem.cpp"
    objective_csv = DESIGN_DIR / "MainObjectiveArc.csv"
    if not source_path.exists() or not objective_csv.exists():
        return

    rows = read_csv(objective_csv, CSV_SPECS["MainObjectiveArc.csv"]["columns"], errors)
    csv_ids = {row["ObjectiveId"].strip() for row in rows}
    source_ids = set(re.findall(r'TEXT\("((?:OBJ_)[A-Z0-9_]+)"\)', source_path.read_text(encoding="utf-8")))

    for objective_id in sorted(source_ids - csv_ids):
        add_error(errors, f"ObjectiveSubsystem.cpp uses {objective_id}, but MainObjectiveArc.csv does not list it")
    for objective_id in sorted(csv_ids - source_ids):
        add_error(errors, f"MainObjectiveArc.csv lists {objective_id}, but ObjectiveSubsystem.cpp does not use it")


def validate_json(errors: list[str]) -> None:
    path = DESIGN_DIR / "AbyssalInterfaceContextSchema.json"
    if not path.exists():
        add_error(errors, f"Missing JSON: {path.relative_to(ROOT)}")
        return
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_error(errors, f"{path.relative_to(ROOT)} JSON parse error: {exc}")


def main() -> int:
    errors: list[str] = []
    csv_rows: dict[str, list[dict[str, str]]] = {}

    for filename, spec in CSV_SPECS.items():
        path = DESIGN_DIR / filename
        rows = read_csv(path, spec["columns"], errors)
        csv_rows[filename] = rows
        validate_required_values(path, rows, errors)
        validate_unique_ids(path, rows, spec["id"], errors)
        validate_priorities(path, rows, errors)

    validate_asset_manifest(DESIGN_DIR / "LuminousRiftAssetManifest.csv", csv_rows["LuminousRiftAssetManifest.csv"], errors)
    validate_asset_manifest(DESIGN_DIR / "WorldAssetManifest.csv", csv_rows["WorldAssetManifest.csv"], errors)
    validate_luminous_rift_import_checklist(csv_rows["LuminousRiftAssetImportChecklist.csv"], errors)
    map_ids = validate_world_maps(csv_rows["WorldMapManifest.csv"], errors)
    validate_world_assets(csv_rows["WorldAssetManifest.csv"], map_ids, errors)
    validate_objective_ids(errors)
    validate_json(errors)

    if errors:
        print("Design data validation failed:")
        for item in errors:
            print(f"- {item}")
        return 1

    checked_rows = sum(len(rows) for rows in csv_rows.values())
    print(f"Design data validation passed: {len(CSV_SPECS)} CSV files, {checked_rows} rows, and JSON schema checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
