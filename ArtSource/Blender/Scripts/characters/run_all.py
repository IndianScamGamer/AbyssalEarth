"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_diver import build as build_sm_diver
from sm_helios_detailed import build as build_sm_helios_detailed
from sm_rift_creature_a import build as build_sm_rift_creature_a
from sm_rift_creature_b import build as build_sm_rift_creature_b
from sm_rift_creature_c import build as build_sm_rift_creature_c
from sm_abyssal_creature import build as build_sm_abyssal_creature
from sm_collectible_items import build as build_sm_collectible_items


def run_all():
    build_sm_diver()  # SM_Diver_Protagonist_A
    build_sm_helios_detailed()  # SM_HeliosRobot_Detailed_A
    build_sm_rift_creature_a()  # SM_RiftCreature_Silhouette_A
    build_sm_rift_creature_b()  # SM_RiftCreature_Silhouette_B
    build_sm_rift_creature_c()  # SM_RiftCreature_Silhouette_C
    build_sm_abyssal_creature()  # SM_AbyssalCreature_Patrol_A
    build_sm_collectible_items()  # SM_COLLECTIBLE_ITEMS


if __name__ == "__main__":
    run_all()
