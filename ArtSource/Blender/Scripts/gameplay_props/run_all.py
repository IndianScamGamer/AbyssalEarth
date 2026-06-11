"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_fabricator import build as build_sm_fabricator
from sm_terminal import build as build_sm_terminal
from sm_crystal_cluster import build as build_sm_crystal_cluster
from sm_beacon import build as build_sm_beacon
from sm_checkpoint import build as build_sm_checkpoint
from sm_steam_vent import build as build_sm_steam_vent
from sm_magma_geyser import build as build_sm_magma_geyser
from sm_helios_robot import build as build_sm_helios_robot


def run_all():
    build_sm_fabricator()  # SM_FabricatorStation_A
    build_sm_terminal()  # SM_InterfaceTerminal_A
    build_sm_crystal_cluster()  # SM_CRYSTAL_CLUSTER
    build_sm_beacon()  # SM_Beacon_A
    build_sm_checkpoint()  # SM_CheckpointActor_A
    build_sm_steam_vent()  # SM_SteamVent_A
    build_sm_magma_geyser()  # SM_MagmaGeyser_A
    build_sm_helios_robot()  # SM_HeliosRobot_Static


if __name__ == "__main__":
    run_all()
