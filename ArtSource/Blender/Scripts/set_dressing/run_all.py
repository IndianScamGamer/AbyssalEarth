"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_ancient_rubble_a import build as build_sm_ancient_rubble_a
from sm_crystal_scatter_a import build as build_sm_crystal_scatter_a
from sm_kelp_strand_a import build as build_sm_kelp_strand_a
from sm_scatter_rock_l import build as build_sm_scatter_rock_l
from sm_scatter_rock_m import build as build_sm_scatter_rock_m
from sm_scatter_rock_s import build as build_sm_scatter_rock_s


def run_all():
    build_sm_ancient_rubble_a()
    build_sm_crystal_scatter_a()
    build_sm_kelp_strand_a()
    build_sm_scatter_rock_l()
    build_sm_scatter_rock_m()
    build_sm_scatter_rock_s()


if __name__ == "__main__":
    run_all()
