"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_rib_arch import build as build_sm_rib_arch
from sm_spine_segment import build as build_sm_spine_segment
from sm_floating_rock import build as build_sm_floating_rock
from sm_fossil_sky_giant_rib_a import build as build_sm_fossil_sky_giant_rib_a
from sm_fossil_sky_observation_walkway_a import build as build_sm_fossil_sky_observation_walkway_a
from sm_fossil_sky_ceiling_skeleton_hero_a import build as build_sm_fossil_sky_ceiling_skeleton_hero_a


def run_all():
    build_sm_rib_arch()  # SM_RIB_ARCH
    build_sm_spine_segment()  # SM_SPINE_SEGMENT
    build_sm_floating_rock()  # SM_FLOATING_ROCK
    build_sm_fossil_sky_giant_rib_a()  # SM_FossilSky_GiantRib_A
    build_sm_fossil_sky_observation_walkway_a()  # SM_FossilSky_ObservationWalkway_A
    build_sm_fossil_sky_ceiling_skeleton_hero_a()  # SM_FossilSky_CeilingSkeleton_Hero_A


if __name__ == "__main__":
    run_all()
