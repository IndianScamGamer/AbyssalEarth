"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_glassroot_platform import build as build_sm_glassroot_platform
from sm_glassroot_root_bridge_a import build as build_sm_glassroot_root_bridge_a
from sm_glassroot_root_column_hero import build as build_sm_glassroot_root_column_hero
from sm_glassroot_root_column_m import build as build_sm_glassroot_root_column_m
from sm_glassroot_root_column_s import build as build_sm_glassroot_root_column_s
from sm_glassroot_terrace_pearl_stone_a import build as build_sm_glassroot_terrace_pearl_stone_a
from sm_glassroot_trunk import build as build_sm_glassroot_trunk


def run_all():
    build_sm_glassroot_platform()
    build_sm_glassroot_root_bridge_a()
    build_sm_glassroot_root_column_hero()
    build_sm_glassroot_root_column_m()
    build_sm_glassroot_root_column_s()
    build_sm_glassroot_terrace_pearl_stone_a()
    build_sm_glassroot_trunk()


if __name__ == "__main__":
    run_all()
