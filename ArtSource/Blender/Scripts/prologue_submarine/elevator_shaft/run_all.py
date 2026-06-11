"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_shaft_section import build as build_sm_shaft_section
from sm_elevator_car import build as build_sm_elevator_car
from sm_crashed_car import build as build_sm_crashed_car
from sm_elevator_mechanism import build as build_sm_elevator_mechanism
from sm_shaft_debris import build as build_sm_shaft_debris


def run_all():
    build_sm_shaft_section()  # SM_Elevator_ShaftSection_A
    build_sm_elevator_car()  # SM_Elevator_Car_A
    build_sm_crashed_car()  # SM_Elevator_CrashedCar_A
    build_sm_elevator_mechanism()  # SM_Elevator_Mechanism_A
    build_sm_shaft_debris()  # SM_Elevator_ShaftDebris_A


if __name__ == "__main__":
    run_all()
