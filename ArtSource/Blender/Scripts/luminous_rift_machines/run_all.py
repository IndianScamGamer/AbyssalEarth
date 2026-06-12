"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from sm_beam_emitter import build as build_sm_beam_emitter
from sm_bridge_span import build as build_sm_bridge_span
from sm_gate_wall import build as build_sm_gate_wall
from sm_hanging_platform import build as build_sm_hanging_platform
from sm_hex_arm_joint import build as build_sm_hex_arm_joint
from sm_hex_cluster import build as build_sm_hex_cluster
from sm_hex_tile import build as build_sm_hex_tile
from sm_orb_frame import build as build_sm_orb_frame
from sm_orb_hub import build as build_sm_orb_hub
from sm_platform_node import build as build_sm_platform_node
from sm_rope_railing import build as build_sm_rope_railing
from sm_stair_ramp import build as build_sm_stair_ramp
from sm_tower import build as build_sm_tower


def run_all():
    build_sm_beam_emitter()
    build_sm_bridge_span()
    build_sm_gate_wall()
    build_sm_hanging_platform()
    build_sm_hex_arm_joint()
    build_sm_hex_cluster()
    build_sm_hex_tile()
    build_sm_orb_frame()
    build_sm_orb_hub()
    build_sm_platform_node()
    build_sm_rope_railing()
    build_sm_stair_ramp()
    build_sm_tower()


if __name__ == "__main__":
    run_all()
