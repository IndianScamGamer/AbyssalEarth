"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_abyssal_creature import build as build_sm_abyssal_creature
from sm_collectible_items import build as build_sm_collectible_items
from sm_creature_pack import build as build_sm_creature_pack
from sm_diver import build as build_sm_diver
from sm_helios_detailed import build as build_sm_helios_detailed
from sm_rift_creature_a import build as build_sm_rift_creature_a
from sm_rift_creature_b import build as build_sm_rift_creature_b
from sm_rift_creature_c import build as build_sm_rift_creature_c


def run_all():
    build_sm_abyssal_creature()
    build_sm_collectible_items()
    build_sm_creature_pack()
    build_sm_diver()
    build_sm_helios_detailed()
    build_sm_rift_creature_a()
    build_sm_rift_creature_b()
    build_sm_rift_creature_c()


if __name__ == "__main__":
    run_all()
