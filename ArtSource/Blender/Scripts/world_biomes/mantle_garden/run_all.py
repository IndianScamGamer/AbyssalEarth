"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_lava_bridge import build as build_sm_lava_bridge
from sm_lava_rock import build as build_sm_lava_rock
from sm_mantle_garden_mineral_flower_a import build as build_sm_mantle_garden_mineral_flower_a
from sm_mantle_garden_mineral_flower_patch import build as build_sm_mantle_garden_mineral_flower_patch
from sm_mantle_garden_obsidian_ridge_a import build as build_sm_mantle_garden_obsidian_ridge_a
from sm_mantle_garden_steam_vent_mesh_a import build as build_sm_mantle_garden_steam_vent_mesh_a
from sm_purple_crystal import build as build_sm_purple_crystal
from sm_steam_column import build as build_sm_steam_column


def run_all():
    build_sm_lava_bridge()
    build_sm_lava_rock()
    build_sm_mantle_garden_mineral_flower_a()
    build_sm_mantle_garden_mineral_flower_patch()
    build_sm_mantle_garden_obsidian_ridge_a()
    build_sm_mantle_garden_steam_vent_mesh_a()
    build_sm_purple_crystal()
    build_sm_steam_column()


if __name__ == "__main__":
    run_all()
