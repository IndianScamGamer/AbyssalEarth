"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_inner_sea_basalt_dock_a import build as build_sm_inner_sea_basalt_dock_a
from sm_inner_sea_broken_pier_a import build as build_sm_inner_sea_broken_pier_a
from sm_inner_sea_dock import build as build_sm_inner_sea_dock
from sm_inner_sea_submerged_ruin_a import build as build_sm_inner_sea_submerged_ruin_a
from sm_stalactite import build as build_sm_stalactite


def run_all():
    build_sm_inner_sea_basalt_dock_a()
    build_sm_inner_sea_broken_pier_a()
    build_sm_inner_sea_dock()
    build_sm_inner_sea_submerged_ruin_a()
    build_sm_stalactite()


if __name__ == "__main__":
    run_all()
