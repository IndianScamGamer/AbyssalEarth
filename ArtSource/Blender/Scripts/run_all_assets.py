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
from luminous_rift_env.run_all import run_all as run_luminous_rift_env
from luminous_rift_machines.run_all import run_all as run_luminous_rift_machines
from prologue_submarine.run_all import run_all as run_prologue_submarine
from world_biomes.run_all import run_all as run_world_biomes


def main():
    print("=== AbyssalEarth Full Asset Generation ===")
    print(f'\n--- characters ---'); run_characters()
    print(f'\n--- gameplay_props ---'); run_gameplay_props()
    print(f'\n--- human_survey_kit ---'); run_human_survey_kit()
    print(f'\n--- luminous_rift_env ---'); run_luminous_rift_env()
    print(f'\n--- luminous_rift_machines ---'); run_luminous_rift_machines()
    print(f'\n--- prologue_submarine ---'); run_prologue_submarine()
    print(f'\n--- world_biomes ---'); run_world_biomes()
    print("\n=== ALL ASSETS COMPLETE ===")


if __name__ == "__main__":
    main()
