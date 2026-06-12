"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_cavern_wall import build as build_sm_cavern_wall
from sm_crystal_kit import build as build_sm_crystal_kit
from sm_foreground_ledge import build as build_sm_foreground_ledge
from sm_hanging_slab import build as build_sm_hanging_slab
from sm_overhang import build as build_sm_overhang
from sm_rock_arch import build as build_sm_rock_arch


def run_all():
    build_sm_cavern_wall()
    build_sm_crystal_kit()
    build_sm_foreground_ledge()
    build_sm_hanging_slab()
    build_sm_overhang()
    build_sm_rock_arch()


if __name__ == "__main__":
    run_all()
