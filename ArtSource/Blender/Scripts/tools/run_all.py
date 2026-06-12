"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_tool_battery_case import build as build_sm_tool_battery_case
from sm_tool_data_tablet import build as build_sm_tool_data_tablet
from sm_tool_dome_beacon import build as build_sm_tool_dome_beacon
from sm_tool_flare import build as build_sm_tool_flare
from sm_tool_hand_scanner import build as build_sm_tool_hand_scanner
from sm_tool_multitool import build as build_sm_tool_multitool
from sm_tool_plasma_drill import build as build_sm_tool_plasma_drill


def run_all():
    build_sm_tool_battery_case()
    build_sm_tool_data_tablet()
    build_sm_tool_dome_beacon()
    build_sm_tool_flare()
    build_sm_tool_hand_scanner()
    build_sm_tool_multitool()
    build_sm_tool_plasma_drill()


if __name__ == "__main__":
    run_all()
