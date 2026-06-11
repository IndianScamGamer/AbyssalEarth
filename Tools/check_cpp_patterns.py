#!/usr/bin/env python3
"""
Static guard for AbyssalEarth C++ sources.

Fails the build when a known-bad API pattern reappears. Each entry encodes a
bug class that previously shipped and was fixed in the tick-24 QA pass — this
keeps them from regressing without needing an engine build in CI.

Run from the repo root: python Tools/check_cpp_patterns.py
"""

import re
import sys
from pathlib import Path

SOURCE_DIR = Path("Source/AbyssalEarth")

# (compiled regex, explanation shown on failure)
BANNED_PATTERNS = [
    (
        re.compile(r"\.(AddLambda|AddUObject|AddRaw|AddSP)\("),
        "Dynamic multicast delegates only support AddDynamic/RemoveDynamic with "
        "UFUNCTION handlers. If this is a non-dynamic delegate, rename it so the "
        "distinction is obvious and add an exception below.",
    ),
    (
        re.compile(r"\bFDelegateHandle\b"),
        "FDelegateHandle is only valid for non-dynamic delegates; all gameplay "
        "delegates in this project are dynamic.",
    ),
    (
        re.compile(r"\b(GetInteractPrompt|OnFocusBegin|OnFocusEnd)\b"),
        "IAbyssalInteractable declares GetInteractionPrompt / OnBeginFocus / "
        "OnEndFocus. These older names do not exist.",
    ),
    (
        re.compile(r"\b(bAutoActivate\b.*Hazard|ActivateHazard|On\w+PhaseBegin)"),
        "AAbyssalHazardBase exposes bStartActive / SetHazardActive() / "
        "OnPhaseChanged(EHazardPhase). The matched API never existed.",
    ),
    (
        re.compile(r"\bResetOxygen\b"),
        "UOxygenComponent's real API is RefillOxygen().",
    ),
    (
        re.compile(r"EAutomationTestFlags::ApplicationContextMask"),
        "Removed in UE 5.4+ (enum class migration). Use "
        "EAutomationTestFlags_ApplicationContextMask.",
    ),
    (
        re.compile(r"EAbyssalItemCategory::(Material|Tool|Upgrade|Quest)\b"),
        "EAbyssalItemCategory only defines Resource/Crafting/Equipment/Consumable.",
    ),
]


def main() -> int:
    if not SOURCE_DIR.is_dir():
        print(f"ERROR: {SOURCE_DIR} not found — run from the repo root.")
        return 2

    failures = 0
    for path in sorted(SOURCE_DIR.rglob("*")):
        if path.suffix not in (".h", ".cpp", ".inl"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.lstrip()
            if stripped.startswith("//") or stripped.startswith("*"):
                continue  # comments may legitimately mention old names
            for pattern, why in BANNED_PATTERNS:
                if pattern.search(line):
                    failures += 1
                    print(f"{path}:{lineno}: banned pattern {pattern.pattern!r}")
                    print(f"    {line.strip()}")
                    print(f"    → {why}")

    if failures:
        print(f"\nFAILED: {failures} banned API usage(s) found.")
        return 1

    print("C++ pattern guard passed — no banned API usage found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
