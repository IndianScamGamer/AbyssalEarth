"""run_all_assets.py — master runner for ALL AbyssalEarth assets.

Usage:
    blender --background --python run_all_assets.py
"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from characters.run_all import run_all as run_characters
from gameplay_props.run_all import run_all as run_gameplay_props
from human_survey_kit.run_all import run_all as run_human_survey_kit
from items.run_all import run_all as run_items
from luminous_rift_env.run_all import run_all as run_luminous_rift_env
from luminous_rift_machines.run_all import run_all as run_luminous_rift_machines
from prologue_submarine.run_all import run_all as run_prologue_submarine
from set_dressing.run_all import run_all as run_set_dressing
from vfx_support.run_all import run_all as run_vfx_support
from world_biomes.run_all import run_all as run_world_biomes


def main():
    print("=== AbyssalEarth Full Asset Generation ===")
    print()
    print('--- characters ---')
    run_characters()
    print()
    print('--- gameplay_props ---')
    run_gameplay_props()
    print()
    print('--- human_survey_kit ---')
    run_human_survey_kit()
    print()
    print('--- items ---')
    run_items()
    print()
    print('--- luminous_rift_env ---')
    run_luminous_rift_env()
    print()
    print('--- luminous_rift_machines ---')
    run_luminous_rift_machines()
    print()
    print('--- prologue_submarine ---')
    run_prologue_submarine()
    print()
    print('--- set_dressing ---')
    run_set_dressing()
    print()
    print('--- vfx_support ---')
    run_vfx_support()
    print()
    print('--- world_biomes ---')
    run_world_biomes()
    print()
    print("=== ALL ASSETS COMPLETE ===")


if __name__ == "__main__":
    main()
