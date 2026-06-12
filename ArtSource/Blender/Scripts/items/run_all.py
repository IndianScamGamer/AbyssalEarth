"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_item_abyssal_core import build as build_sm_item_abyssal_core
from sm_item_air_canister import build as build_sm_item_air_canister
from sm_item_armor_plating import build as build_sm_item_armor_plating
from sm_item_fossil_shard import build as build_sm_item_fossil_shard
from sm_item_gravity_crystal import build as build_sm_item_gravity_crystal
from sm_item_heat_shield_cell import build as build_sm_item_heat_shield_cell
from sm_item_magma_residue import build as build_sm_item_magma_residue
from sm_item_pressure_liner import build as build_sm_item_pressure_liner
from sm_item_rebreather_mod import build as build_sm_item_rebreather_mod
from sm_item_rift_stabiliser import build as build_sm_item_rift_stabiliser
from sm_item_suit_patch import build as build_sm_item_suit_patch
from sm_item_thermal_weave import build as build_sm_item_thermal_weave


def run_all():
    build_sm_item_abyssal_core()
    build_sm_item_air_canister()
    build_sm_item_armor_plating()
    build_sm_item_fossil_shard()
    build_sm_item_gravity_crystal()
    build_sm_item_heat_shield_cell()
    build_sm_item_magma_residue()
    build_sm_item_pressure_liner()
    build_sm_item_rebreather_mod()
    build_sm_item_rift_stabiliser()
    build_sm_item_suit_patch()
    build_sm_item_thermal_weave()


if __name__ == "__main__":
    run_all()
