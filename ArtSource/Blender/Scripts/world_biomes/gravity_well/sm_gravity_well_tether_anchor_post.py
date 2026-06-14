"""
SM_GravityWell_TetherAnchorPost — AbyssalEarth procedural mesh.
Concept: GW-002, GW-004

Heavy iron anchor post driven into cave stone — the fixed wall anchor point that the
tether rock chains attach to. A square cross-section iron column is expansion-bolted
into a thick base plate; a forged tether ring tops the post for chain attachment.
A side arm at mid-height carries an amber lamp globe, doubling as an expedition
wayfinding beacon for players navigating the Gravity Well approach corridor.

Run standalone:  blender --background --python <this_file>.py
"""
import sys, os, math, random
import bpy, bmesh
from mathutils import Matrix, Vector

_HERE         = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                           add_mat_slots, set_origin_to_base, export_fbx,
                           get_export_dir, TAU, PI)

EXPORT_DIR = get_export_dir('GravityWell')

POST_W       = 0.18   # square post cross-section width
POST_H       = 1.35   # post height
BASE_W       = 0.38   # base plate width
BASE_H       = 0.06   # base plate height
BOLT_R       = 0.028  # expansion bolt radius
BOLT_H       = 0.08   # bolt protrusion height
N_BOLTS      = 4      # corner bolts
RING_R       = 0.16   # tether ring outer radius
RING_TUBE    = 0.028  # ring tube radius
ARM_L        = 0.35   # lamp arm length
LAMP_R       = 0.10   # lamp globe radius


def build():
    obj, bm = new_mesh("SM_GravityWell_TetherAnchorPost")

    # 1. Base plate — flat rectangular slab centered at origin
    hbw = BASE_W / 2
    bp0 = bm.verts.new((-hbw, -hbw, 0.0))
    bp1 = bm.verts.new(( hbw, -hbw, 0.0))
    bp2 = bm.verts.new(( hbw,  hbw, 0.0))
    bp3 = bm.verts.new((-hbw,  hbw, 0.0))
    bp4 = bm.verts.new((-hbw, -hbw, BASE_H))
    bp5 = bm.verts.new(( hbw, -hbw, BASE_H))
    bp6 = bm.verts.new(( hbw,  hbw, BASE_H))
    bp7 = bm.verts.new((-hbw,  hbw, BASE_H))
    bm.faces.new([bp0, bp3, bp2, bp1])          # bottom
    bm.faces.new([bp4, bp5, bp6, bp7])          # top
    bm.faces.new([bp0, bp1, bp5, bp4])          # front
    bm.faces.new([bp1, bp2, bp6, bp5])          # right
    bm.faces.new([bp2, bp3, bp7, bp6])          # back
    bm.faces.new([bp3, bp0, bp4, bp7])          # left

    # 2. Expansion bolts at plate corners
    bolt_inset = BASE_W / 2 - 0.05
    bolt_positions = [
        ( bolt_inset,  bolt_inset),
        (-bolt_inset,  bolt_inset),
        ( bolt_inset, -bolt_inset),
        (-bolt_inset, -bolt_inset),
    ]
    for (bx, by) in bolt_positions:
        # Bolt shaft
        bolt_mat = Matrix.Translation(Vector((bx, by, BASE_H + BOLT_H / 2)))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
                              radius1=BOLT_R, radius2=BOLT_R * 0.6,
                              depth=BOLT_H, matrix=bolt_mat)
        # Hex head on top of bolt
        hex_mat = Matrix.Translation(Vector((bx, by, BASE_H + BOLT_H + 0.01)))
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
                              radius1=BOLT_R * 1.4, radius2=BOLT_R * 1.4,
                              depth=0.02, matrix=hex_mat)

    # 3. Main post — square cross-section lofted column
    # 3 rings at z = BASE_H, BASE_H + POST_H*0.5, BASE_H + POST_H
    # Slight taper: bottom half-width = POST_W/2, top = POST_W/2 * 0.88
    hw_bot = POST_W / 2
    hw_top = POST_W / 2 * 0.88
    post_zs = [BASE_H, BASE_H + POST_H * 0.5, BASE_H + POST_H]
    post_hws = [hw_bot, (hw_bot + hw_top) / 2, hw_top]

    def post_ring(hw, z):
        return [
            bm.verts.new((-hw, -hw, z)),
            bm.verts.new(( hw, -hw, z)),
            bm.verts.new(( hw,  hw, z)),
            bm.verts.new((-hw,  hw, z)),
        ]

    post_rings = [post_ring(post_hws[k], post_zs[k]) for k in range(3)]

    # Cap the bottom
    bm.faces.new(post_rings[0])
    # Side faces between rings
    for ri in range(2):
        lo = post_rings[ri]
        hi = post_rings[ri + 1]
        n = len(lo)
        for si in range(n):
            ni = (si + 1) % n
            bm.faces.new([lo[si], lo[ni], hi[ni], hi[si]])
    # Cap the top
    bm.faces.new(list(reversed(post_rings[2])))

    # 2 decorative horizontal grooves as thin rings inset into the post sides
    for groove_z in (0.30, 0.80):
        hw_g = hw_bot - (hw_bot - hw_top) * (groove_z - BASE_H) / POST_H
        hw_gi = hw_g * 1.02  # slightly outside post surface for visibility
        # Each groove: 4-sided ring of inset faces (thin quad strip)
        groove_ring_outer = [
            bm.verts.new((-hw_gi, -hw_gi, groove_z - 0.012)),
            bm.verts.new(( hw_gi, -hw_gi, groove_z - 0.012)),
            bm.verts.new(( hw_gi,  hw_gi, groove_z - 0.012)),
            bm.verts.new((-hw_gi,  hw_gi, groove_z - 0.012)),
        ]
        groove_ring_inner = [
            bm.verts.new((-hw_gi, -hw_gi, groove_z + 0.012)),
            bm.verts.new(( hw_gi, -hw_gi, groove_z + 0.012)),
            bm.verts.new(( hw_gi,  hw_gi, groove_z + 0.012)),
            bm.verts.new((-hw_gi,  hw_gi, groove_z + 0.012)),
        ]
        for si in range(4):
            ni = (si + 1) % 4
            try:
                bm.faces.new([groove_ring_outer[si], groove_ring_outer[ni],
                               groove_ring_inner[ni], groove_ring_inner[si]])
            except Exception:
                pass

    # 4. Tether ring at post top — lofted torus
    ring_top_z = BASE_H + POST_H + RING_R
    N_MAIN_R = 12
    N_TUBE_R = 8
    t_rings = []
    for i in range(N_MAIN_R):
        a = i * TAU / N_MAIN_R
        cx = math.cos(a) * RING_R
        cy = math.sin(a) * RING_R
        ring_verts = []
        for j in range(N_TUBE_R):
            angle2 = j * TAU / N_TUBE_R
            tube_x = cx + math.cos(a) * math.cos(angle2) * RING_TUBE
            tube_y = cy + math.sin(a) * math.cos(angle2) * RING_TUBE
            tube_z = ring_top_z + math.sin(angle2) * RING_TUBE
            ring_verts.append(bm.verts.new((tube_x, tube_y, tube_z)))
        t_rings.append(ring_verts)
    for i in range(N_MAIN_R):
        lo = t_rings[i]
        hi = t_rings[(i + 1) % N_MAIN_R]
        for j in range(N_TUBE_R):
            nj = (j + 1) % N_TUBE_R
            try:
                bm.faces.new([lo[j], lo[nj], hi[nj], hi[j]])
            except Exception:
                pass

    # 5. Lamp arm — horizontal 4-sided box beam at mid-height, extending +Y
    arm_z = BASE_H + POST_H * 0.55
    arm_hw = 0.02  # half cross-section: 0.04 × 0.04 beam
    arm_verts_base = [
        bm.verts.new((-arm_hw, 0.0,       arm_z - arm_hw)),
        bm.verts.new(( arm_hw, 0.0,       arm_z - arm_hw)),
        bm.verts.new(( arm_hw, 0.0,       arm_z + arm_hw)),
        bm.verts.new((-arm_hw, 0.0,       arm_z + arm_hw)),
    ]
    arm_verts_tip = [
        bm.verts.new((-arm_hw, ARM_L, arm_z - arm_hw)),
        bm.verts.new(( arm_hw, ARM_L, arm_z - arm_hw)),
        bm.verts.new(( arm_hw, ARM_L, arm_z + arm_hw)),
        bm.verts.new((-arm_hw, ARM_L, arm_z + arm_hw)),
    ]
    # 4 side faces of the beam
    arm_pairs = [(arm_verts_base, arm_verts_tip)]
    for (a_lo, a_hi) in arm_pairs:
        for si in range(4):
            ni = (si + 1) % 4
            try:
                bm.faces.new([a_lo[si], a_lo[ni], a_hi[ni], a_hi[si]])
            except Exception:
                pass
    # End cap flange at arm tip (3-segment disc)
    flange_mat = Matrix.Translation(Vector((0.0, ARM_L, arm_z)))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8,
                          radius1=0.05, radius2=0.05, depth=0.01, matrix=flange_mat)

    # 6. Lamp globe at arm tip
    lamp_mat = Matrix.Translation(Vector((0.0, ARM_L, arm_z)))
    lamp_result = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=LAMP_R,
                                             matrix=lamp_mat)
    for v in lamp_result['verts']:
        v.co.z = arm_z + (v.co.z - arm_z) * 0.88

    # Cage ring around lamp equator — thin torus
    cage_R = LAMP_R + 0.015
    cage_T = 0.012
    N_CAGE_M = 16
    N_CAGE_T = 6
    cage_rings = []
    for i in range(N_CAGE_M):
        a = i * TAU / N_CAGE_M
        cx = 0.0 + math.cos(a) * cage_R
        cy = ARM_L + math.sin(a) * cage_R
        ring_verts = []
        for j in range(N_CAGE_T):
            angle2 = j * TAU / N_CAGE_T
            tube_x = cx + math.cos(a) * math.cos(angle2) * cage_T
            tube_y = cy + math.sin(a) * math.cos(angle2) * cage_T
            tube_z = arm_z + math.sin(angle2) * cage_T
            ring_verts.append(bm.verts.new((tube_x, tube_y, tube_z)))
        cage_rings.append(ring_verts)
    for i in range(N_CAGE_M):
        lo = cage_rings[i]
        hi = cage_rings[(i + 1) % N_CAGE_M]
        for j in range(N_CAGE_T):
            nj = (j + 1) % N_CAGE_T
            try:
                bm.faces.new([lo[j], lo[nj], hi[nj], hi[j]])
            except Exception:
                pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_amber_stabilizer",
                        "mat_ancient_machine_edge_wear"])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_GravityWell_TetherAnchorPost")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_GravityWell_TetherAnchorPost")
