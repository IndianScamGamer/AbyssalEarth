"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_lava_rock import build as build_sm_lava_rock
from sm_purple_crystal import build as build_sm_purple_crystal
from sm_lava_bridge import build as build_sm_lava_bridge
from sm_steam_column import build as build_sm_steam_column
from sm_mantle_garden_obsidian_ridge_a import build as build_sm_mantle_garden_obsidian_ridge_a
from sm_mantle_garden_steam_vent_mesh_a import build as build_sm_mantle_garden_steam_vent_mesh_a
from sm_mantle_garden_mineral_flower_a import build as build_sm_mantle_garden_mineral_flower_a


def run_all():
    build_sm_lava_rock()  # SM_LAVA_ROCK
    build_sm_purple_crystal()  # SM_PURPLE_CRYSTAL
    build_sm_lava_bridge()  # SM_MantleGarden_LavaBridge_A
    build_sm_steam_column()  # SM_MantleGarden_SteamColumn_A
    build_sm_mantle_garden_obsidian_ridge_a()  # SM_MantleGarden_ObsidianRidge_A
    build_sm_mantle_garden_steam_vent_mesh_a()  # SM_MantleGarden_SteamVent_Mesh_A
    build_sm_mantle_garden_mineral_flower_a()  # SM_MantleGarden_MineralFlower_A


if __name__ == "__main__":
    run_all()
