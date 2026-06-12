"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_ammonite_fossil import build as build_sm_ammonite_fossil
from sm_fossil_sky_ceiling_skeleton_hero_a import build as build_sm_fossil_sky_ceiling_skeleton_hero_a
from sm_fossil_sky_giant_rib_a import build as build_sm_fossil_sky_giant_rib_a
from sm_fossil_sky_observation_walkway_a import build as build_sm_fossil_sky_observation_walkway_a
from sm_grated_walkway import build as build_sm_grated_walkway
from sm_petrified_fish import build as build_sm_petrified_fish
from sm_rib_arch import build as build_sm_rib_arch
from sm_spine_segment import build as build_sm_spine_segment
from sm_whale_skeleton_wall import build as build_sm_whale_skeleton_wall
from sm_wood_dock import build as build_sm_wood_dock


def run_all():
    build_sm_ammonite_fossil()
    build_sm_fossil_sky_ceiling_skeleton_hero_a()
    build_sm_fossil_sky_giant_rib_a()
    build_sm_fossil_sky_observation_walkway_a()
    build_sm_grated_walkway()
    build_sm_petrified_fish()
    build_sm_rib_arch()
    build_sm_spine_segment()
    build_sm_whale_skeleton_wall()
    build_sm_wood_dock()


if __name__ == "__main__":
    run_all()
