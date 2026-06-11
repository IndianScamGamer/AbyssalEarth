"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_wood_dock import build as build_sm_wood_dock
from sm_stalactite import build as build_sm_stalactite
from sm_inner_sea_dock import build as build_sm_inner_sea_dock
from sm_inner_sea_basalt_dock_a import build as build_sm_inner_sea_basalt_dock_a
from sm_inner_sea_broken_pier_a import build as build_sm_inner_sea_broken_pier_a
from sm_inner_sea_submerged_ruin_a import build as build_sm_inner_sea_submerged_ruin_a


def run_all():
    build_sm_wood_dock()  # SM_FossilSky_WoodDock_A
    build_sm_stalactite()  # SM_STALACTITE
    build_sm_inner_sea_dock()  # SM_InnerSea_WoodDock_A
    build_sm_inner_sea_basalt_dock_a()  # SM_InnerSea_BasaltDock_A
    build_sm_inner_sea_broken_pier_a()  # SM_InnerSea_BrokenPier_A
    build_sm_inner_sea_submerged_ruin_a()  # SM_InnerSea_SubmergedRuin_A


if __name__ == "__main__":
    run_all()
