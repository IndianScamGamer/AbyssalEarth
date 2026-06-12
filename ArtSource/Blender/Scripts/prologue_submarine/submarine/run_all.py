"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_airlock import build as build_sm_airlock
from sm_bulkhead_door import build as build_sm_bulkhead_door
from sm_bunk_room import build as build_sm_bunk_room
from sm_corridor_corner import build as build_sm_corridor_corner
from sm_corridor_straight import build as build_sm_corridor_straight
from sm_engine_room import build as build_sm_engine_room
from sm_pipe_bundle import build as build_sm_pipe_bundle


def run_all():
    build_sm_airlock()
    build_sm_bulkhead_door()
    build_sm_bunk_room()
    build_sm_corridor_corner()
    build_sm_corridor_straight()
    build_sm_engine_room()
    build_sm_pipe_bundle()


if __name__ == "__main__":
    run_all()
