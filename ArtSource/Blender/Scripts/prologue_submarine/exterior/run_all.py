"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_rov_drone import build as build_sm_rov_drone
from sm_shaft_rim_segment import build as build_sm_shaft_rim_segment
from sm_submarine_exterior import build as build_sm_submarine_exterior
from sm_work_light_post import build as build_sm_work_light_post


def run_all():
    build_sm_rov_drone()
    build_sm_shaft_rim_segment()
    build_sm_submarine_exterior()
    build_sm_work_light_post()


if __name__ == "__main__":
    run_all()
