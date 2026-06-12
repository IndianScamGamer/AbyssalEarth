"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_bedroll import build as build_sm_bedroll
from sm_cable_coil import build as build_sm_cable_coil
from sm_field_console import build as build_sm_field_console
from sm_portable_lamp import build as build_sm_portable_lamp
from sm_railing import build as build_sm_railing
from sm_survey_crate import build as build_sm_survey_crate
from sm_survey_platform import build as build_sm_survey_platform
from sm_tripod import build as build_sm_tripod


def run_all():
    build_sm_bedroll()
    build_sm_cable_coil()
    build_sm_field_console()
    build_sm_portable_lamp()
    build_sm_railing()
    build_sm_survey_crate()
    build_sm_survey_platform()
    build_sm_tripod()


if __name__ == "__main__":
    run_all()
