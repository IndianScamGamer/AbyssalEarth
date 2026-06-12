"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_cable_vines import build as build_sm_cable_vines
from sm_crashed_car import build as build_sm_crashed_car
from sm_elevator_car import build as build_sm_elevator_car
from sm_elevator_mechanism import build as build_sm_elevator_mechanism
from sm_emergency_strip import build as build_sm_emergency_strip
from sm_shaft_debris import build as build_sm_shaft_debris
from sm_shaft_section import build as build_sm_shaft_section
from sm_torn_hull_frame import build as build_sm_torn_hull_frame
from sm_wrecked_panel import build as build_sm_wrecked_panel


def run_all():
    build_sm_cable_vines()
    build_sm_crashed_car()
    build_sm_elevator_car()
    build_sm_elevator_mechanism()
    build_sm_emergency_strip()
    build_sm_shaft_debris()
    build_sm_shaft_section()
    build_sm_torn_hull_frame()
    build_sm_wrecked_panel()


if __name__ == "__main__":
    run_all()
