"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_beacon import build as build_sm_beacon
from sm_checkpoint import build as build_sm_checkpoint
from sm_crystal_cluster import build as build_sm_crystal_cluster
from sm_discovery_marker import build as build_sm_discovery_marker
from sm_ember_vent import build as build_sm_ember_vent
from sm_fabricator import build as build_sm_fabricator
from sm_gravity_shear_emitter import build as build_sm_gravity_shear_emitter
from sm_helios_robot import build as build_sm_helios_robot
from sm_magma_geyser import build as build_sm_magma_geyser
from sm_power_node import build as build_sm_power_node
from sm_rift_core import build as build_sm_rift_core
from sm_steam_vent import build as build_sm_steam_vent
from sm_structural_debris import build as build_sm_structural_debris
from sm_terminal import build as build_sm_terminal


def run_all():
    build_sm_beacon()
    build_sm_checkpoint()
    build_sm_crystal_cluster()
    build_sm_discovery_marker()
    build_sm_ember_vent()
    build_sm_fabricator()
    build_sm_gravity_shear_emitter()
    build_sm_helios_robot()
    build_sm_magma_geyser()
    build_sm_power_node()
    build_sm_rift_core()
    build_sm_steam_vent()
    build_sm_structural_debris()
    build_sm_terminal()


if __name__ == "__main__":
    run_all()
