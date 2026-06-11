"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_glassroot_trunk import build as build_sm_glassroot_trunk
from sm_glassroot_platform import build as build_sm_glassroot_platform
from sm_glassroot_root_column_s import build as build_sm_glassroot_root_column_s
from sm_glassroot_root_column_m import build as build_sm_glassroot_root_column_m
from sm_glassroot_root_column_hero import build as build_sm_glassroot_root_column_hero
from sm_glassroot_terrace_pearl_stone_a import build as build_sm_glassroot_terrace_pearl_stone_a
from sm_glassroot_root_bridge_a import build as build_sm_glassroot_root_bridge_a


def run_all():
    build_sm_glassroot_trunk()  # SM_GLASSROOT_TRUNK
    build_sm_glassroot_platform()  # SM_Glassroot_FloatingPlatform_A
    build_sm_glassroot_root_column_s()  # SM_Glassroot_RootColumn_S
    build_sm_glassroot_root_column_m()  # SM_Glassroot_RootColumn_M
    build_sm_glassroot_root_column_hero()  # SM_Glassroot_RootColumn_Hero
    build_sm_glassroot_terrace_pearl_stone_a()  # SM_Glassroot_Terrace_PearlStone_A
    build_sm_glassroot_root_bridge_a()  # SM_Glassroot_RootBridge_A


if __name__ == "__main__":
    run_all()
