"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_survey_platform import build as build_sm_survey_platform
from sm_survey_crate import build as build_sm_survey_crate
from sm_portable_lamp import build as build_sm_portable_lamp
from sm_cable_coil import build as build_sm_cable_coil
from sm_field_console import build as build_sm_field_console
from sm_railing import build as build_sm_railing
from sm_tripod import build as build_sm_tripod
from sm_bedroll import build as build_sm_bedroll


def run_all():
    build_sm_survey_platform()  # SM_Human_SurveyPlatform_A
    build_sm_survey_crate()  # SM_Human_SurveyCrate_A
    build_sm_portable_lamp()  # SM_Human_PortableLamp_A
    build_sm_cable_coil()  # SM_Human_CableCoil_A
    build_sm_field_console()  # SM_Human_FieldConsole_A
    build_sm_railing()  # SM_Human_TemporaryRailing_A
    build_sm_tripod()  # SM_Human_TripodScanner_A
    build_sm_bedroll()  # SM_Human_BedrollBundle_A


if __name__ == "__main__":
    run_all()
