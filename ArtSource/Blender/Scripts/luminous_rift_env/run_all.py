"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_crystal_kit import build as build_sm_crystal_kit
from sm_foreground_ledge import build as build_sm_foreground_ledge
from sm_rock_arch import build as build_sm_rock_arch
from sm_overhang import build as build_sm_overhang
from sm_hanging_slab import build as build_sm_hanging_slab
from sm_cavern_wall import build as build_sm_cavern_wall


def run_all():
    build_sm_crystal_kit()  # SM_CRYSTAL_KIT
    build_sm_foreground_ledge()  # SM_FOREGROUND_LEDGE
    build_sm_rock_arch()  # SM_ROCK_ARCH
    build_sm_overhang()  # SM_OVERHANG
    build_sm_hanging_slab()  # SM_HANGING_SLAB
    build_sm_cavern_wall()  # SM_CAVERN_WALL


if __name__ == "__main__":
    run_all()
