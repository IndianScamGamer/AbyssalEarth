"""run_all.py — build all assets in this folder."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)
from shared.utils import clear_scene

from sm_hex_tile import build as build_sm_hex_tile
from sm_hex_cluster import build as build_sm_hex_cluster
from sm_orb_frame import build as build_sm_orb_frame
from sm_orb_hub import build as build_sm_orb_hub
from sm_beam_emitter import build as build_sm_beam_emitter
from sm_bridge_span import build as build_sm_bridge_span
from sm_platform_node import build as build_sm_platform_node
from sm_gate_wall import build as build_sm_gate_wall
from sm_tower import build as build_sm_tower


def run_all():
    build_sm_hex_tile()  # SM_HEX_TILE
    build_sm_hex_cluster()  # SM_HEX_CLUSTER
    build_sm_orb_frame()  # SM_Rift_OrbFrame_A
    build_sm_orb_hub()  # SM_Rift_OrbHub_A
    build_sm_beam_emitter()  # SM_Rift_BeamEmitterNode_A
    build_sm_bridge_span()  # SM_BRIDGE_SPAN
    build_sm_platform_node()  # SM_Rift_PlatformNode_A
    build_sm_gate_wall()  # SM_Rift_AncientWall_Gate_A
    build_sm_tower()  # SM_TOWER


if __name__ == "__main__":
    run_all()
