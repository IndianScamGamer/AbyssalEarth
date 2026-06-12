"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_floating_rock import build as build_sm_floating_rock
from sm_gravity_well_curved_tower_a import build as build_sm_gravity_well_curved_tower_a
from sm_gravity_well_floating_platform_a import build as build_sm_gravity_well_floating_platform_a
from sm_portal_ring import build as build_sm_portal_ring


def run_all():
    build_sm_floating_rock()
    build_sm_gravity_well_curved_tower_a()
    build_sm_gravity_well_floating_platform_a()
    build_sm_portal_ring()


if __name__ == "__main__":
    run_all()
