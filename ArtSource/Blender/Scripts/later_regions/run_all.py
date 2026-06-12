"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_later_ash_dune import build as build_sm_later_ash_dune
from sm_later_buried_machine_slab import build as build_sm_later_buried_machine_slab
from sm_later_cathedral_column import build as build_sm_later_cathedral_column


def run_all():
    build_sm_later_ash_dune()
    build_sm_later_buried_machine_slab()
    build_sm_later_cathedral_column()


if __name__ == "__main__":
    run_all()
