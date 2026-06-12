"""run_all.py — build all sub-folder assets."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from prologue_submarine.elevator_shaft.run_all import run_all as run_elevator_shaft
from prologue_submarine.exterior.run_all import run_all as run_exterior
from prologue_submarine.submarine.run_all import run_all as run_submarine


def run_all():
    run_elevator_shaft()
    run_exterior()
    run_submarine()


if __name__ == "__main__":
    run_all()
