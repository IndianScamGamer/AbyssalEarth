"""
Abyssal Earth — Luminous Rift Machine Kit
Script 3/7: Ancient alien machine geometry

Run in Blender 4.x Scripting tab.
Exports to Content/ArtSourceExports/LuminousRift/

Assets generated:
  SM_Rift_HexCollector_Tile_A         — single hexagonal panel (gold frame, glass pane)
  SM_Rift_HexCollector_Cluster_A      — 7-tile flower arrangement
  SM_Rift_HexCollector_Cluster_B_Broken — broken cluster variant
  SM_Rift_OrbFrame_A                  — partial ring frame around central orb
  SM_Rift_OrbHub_A                    — central radial hub with beam arm sockets
  SM_Rift_BeamEmitterNode_A           — end-device for gold beam splines
  SM_Rift_AncientWall_Gate_A          — right-side gate wall structure
  SM_Rift_AncientWall_Panel_A/B       — modular wall panel sections
  SM_Rift_BridgeSpan_A                — full-length traversable bridge segment
  SM_Rift_BridgeSpan_B_Broken         — broken bridge segment
  SM_Rift_PlatformNode_A              — floating platform node
  SM_Rift_TowerSegment_A/B/C          — distant tower silhouette pieces
"""

import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix

EXPORT_ROOT = os.path.join(os.path.dirname(bpy.data.filepath),
                           "..", "..", "..",
                           "Content", "ArtSourceExports", "LuminousRift")
EXPORT_ROOT = os.path.normpath(EXPORT_ROOT)
os.makedirs(EXPORT_ROOT, exist_ok=True)

TAU = math.tau
PI  = math.pi


# ──────────── shared utils ────────────
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def new_mesh(name):
    mesh = bpy.data.meshes.new(name)
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj, bmesh.new()

def finalise(obj, bm):
    bm.to_mesh(obj.data)
    bm.free()
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

def smart_uv(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

def add_mat_slots(obj, names):
    palette = {
        "mat_ancient_machine_dark": (0.05, 0.05, 0.06, 1),
        "mat_ancient_machine_edge_wear": (0.12, 0.10, 0.08, 1),
        "mat_gold_emissive":        (1.0,  0.72, 0.10, 1),
        "mat_blue_emissive":        (0.05, 0.40, 1.0,  1),
        "mat_collector_glass":      (0.55, 0.80, 1.0,  1),
        "mat_wet_basalt":           (0.06, 0.06, 0.07, 1),
        "mat_crystal_blue":         (0.10, 0.55, 1.0,  1),
        "mat_orb_energy":           (0.4,  0.8,  1.0,  1),
    }
    for name in names:
        if name not in bpy.data.materials:
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = palette.get(name, (0.5,0.5,0.5,1))
        obj.data.materials.append(bpy.data.materials[name])

def set_origin_bottom(obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    min_z = min((obj.matrix_world @ v.co).z for v in obj.data.vertices)
    bpy.context.scene.cursor.location = (obj.location.x, obj.location.y, min_z)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    obj.location = (0, 0, 0)

def export_fbx(obj, filename):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = os.path.join(EXPORT_ROOT, filename)
    bpy.ops.export_scene.fbx(
        filepath=path, use_selection=True, global_scale=100.0,
        apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
        mesh_smooth_type='FACE', use_mesh_modifiers=True, bake_anim=False)
    print(f"  Exported: {path}")


# ══════════════════════════════════════════════
#  HEX COLLECTOR TILE
# ══════════════════════════════════════════════
# Single hexagonal panel.  Gold outer frame, frosted inner pane,
# mechanical node at each corner where adjacent tiles share joints.
# Matches: AD-002 (Collector Panel — Single Tile Detail).

def hex_pts(cx, cy, r, z=0.0):
    return [(cx + math.cos(i*TAU/6 + PI/6)*r,
             cy + math.sin(i*TAU/6 + PI/6)*r, z)
            for i in range(6)]

def build_hex_tile(name="SM_Rift_HexCollector_Tile_A",
                   outer_r=2.0, frame_w=0.22, pane_depth=0.04):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)

    inner_r = outer_r - frame_w

    # ── outer hex frame (6 trapezoidal frame segments) ──
    outer_pts = hex_pts(0, 0, outer_r)
    inner_pts = hex_pts(0, 0, inner_r)

    for i in range(6):
        ni = (i+1)%6
        # front face of frame segment
        ov = [bm.verts.new((outer_pts[i][0], outer_pts[i][1], 0.0)),
              bm.verts.new((outer_pts[ni][0],outer_pts[ni][1], 0.0)),
              bm.verts.new((inner_pts[ni][0],inner_pts[ni][1], 0.0)),
              bm.verts.new((inner_pts[i][0], inner_pts[i][1], 0.0))]
        bm.faces.new(ov)
        # back face
        bv = [bm.verts.new((v.co.x, v.co.y, -frame_w*0.6)) for v in ov]
        bm.faces.new(list(reversed(bv)))
        # side faces
        for j in range(4):
            nj = (j+1)%4
            try:
                bm.faces.new([ov[j], ov[nj], bv[nj], bv[j]])
            except Exception:
                pass

    # ── frosted inner pane ──────────────────────
    pane_pts = hex_pts(0, 0, inner_r - 0.04)
    pane_f = [bm.verts.new((p[0], p[1], -0.008)) for p in pane_pts]
    pane_b = [bm.verts.new((p[0], p[1], -0.008 - pane_depth)) for p in pane_pts]
    bm.faces.new(pane_f)
    bm.faces.new(list(reversed(pane_b)))
    for i in range(6):
        ni = (i+1)%6
        try:
            bm.faces.new([pane_f[i], pane_f[ni], pane_b[ni], pane_b[i]])
        except Exception:
            pass

    # ── corner joint nodes ───────────────────────
    for ox, oy, _ in outer_pts:
        node = bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.12,
            matrix=Matrix.Translation(Vector((ox, oy, 0.0))))

    # ── bevelled centre-strut radials ────────────
    for i in range(6):
        angle = i * TAU/6 + PI/6
        mx = math.cos(angle) * (inner_r * 0.55)
        my = math.sin(angle) * (inner_r * 0.55)
        sv = [bm.verts.new((math.cos(angle + da)*0.04,
                            math.sin(angle + da)*0.04,
                            dz))
              for da, dz in [(-PI/2, 0),( PI/2, 0),
                              (PI/2, -0.03),(-PI/2,-0.03)]]
        ev = [bm.verts.new((mx + math.cos(angle + da)*0.04,
                            my + math.sin(angle + da)*0.04,
                            dz))
              for da, dz in [(-PI/2, 0),( PI/2, 0),
                              (PI/2, -0.03),(-PI/2,-0.03)]]
        try:
            bm.faces.new([sv[0],sv[1],ev[1],ev[0]])
            bm.faces.new([sv[2],sv[3],ev[3],ev[2]])
            bm.faces.new([sv[0],sv[3],ev[3],ev[0]])
            bm.faces.new([sv[1],sv[2],ev[2],ev[1]])
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_gold_emissive", "mat_collector_glass",
                        "mat_ancient_machine_dark"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  HEX COLLECTOR CLUSTER
# ══════════════════════════════════════════════
# 7-tile flower arrangement (1 centre + 6 surrounding).
# Centre connection node where all beam lines converge.
# Matches: Luminous Rift hero image, AD-002.

def build_hex_cluster(name, broken=False, seed=1):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    tile_r   = 2.0
    gap      = 0.18
    spacing  = (tile_r + gap) * math.sqrt(3)

    tile_positions = [(0, 0, 0)]
    for i in range(6):
        angle  = i * TAU/6
        tx     = math.cos(angle) * spacing
        ty     = math.sin(angle) * spacing
        tilt_z = rng.uniform(-0.06, 0.06) if not broken else rng.uniform(-0.4, 0.4)
        tile_positions.append((tx, ty, tilt_z))

    skip_tiles = {3, 5} if broken else set()
    frame_w = 0.22

    for idx, (tx, ty, tz) in enumerate(tile_positions):
        if idx in skip_tiles:
            continue

        outer_pts = hex_pts(tx, ty, tile_r)
        inner_pts = hex_pts(tx, ty, tile_r - frame_w)

        # frame
        for i in range(6):
            ni = (i+1)%6
            rot_z = tz + (rng.uniform(-0.12,0.12) if broken else 0)
            ov = [bm.verts.new((outer_pts[i][0], outer_pts[i][1], tz)),
                  bm.verts.new((outer_pts[ni][0],outer_pts[ni][1], tz)),
                  bm.verts.new((inner_pts[ni][0],inner_pts[ni][1], tz)),
                  bm.verts.new((inner_pts[i][0], inner_pts[i][1], tz))]
            try:
                bm.faces.new(ov)
                bv = [bm.verts.new((v.co.x, v.co.y, tz - 0.14)) for v in ov]
                bm.faces.new(list(reversed(bv)))
                for j in range(4):
                    nj=(j+1)%4
                    bm.faces.new([ov[j],ov[nj],bv[nj],bv[j]])
            except Exception:
                pass

        # pane
        pane_pts = hex_pts(tx, ty, tile_r - frame_w - 0.04)
        pf = [bm.verts.new((p[0],p[1], tz - 0.01)) for p in pane_pts]
        try:
            bm.faces.new(pf)
        except Exception:
            pass

    # central hub node
    hub = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.55,
                                      matrix=Matrix.Translation(Vector((0,0,0.3))))
    # ring around hub
    for r_off in [0.65, 0.72]:
        rv = [bm.verts.new((math.cos(i*TAU/24)*r_off,
                            math.sin(i*TAU/24)*r_off,
                            0.08 + (r_off-0.65)*3))
              for i in range(24)]
        for i in range(24):
            ni=(i+1)%24
            try:
                bv = [bm.verts.new((rv[i].co.x, rv[i].co.y, rv[i].co.z-0.06)),
                      bm.verts.new((rv[ni].co.x,rv[ni].co.y,rv[ni].co.z-0.06))]
                bm.faces.new([rv[i], rv[ni], bv[1], bv[0]])
            except Exception:
                pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_gold_emissive", "mat_collector_glass",
                        "mat_ancient_machine_dark", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  ORB FRAME
# ══════════════════════════════════════════════
# Massive partial ring frame (~30m diameter) around the central orb.
# Not a perfect circle — asymmetric, damaged, with beam arm attachment
# points. Matches: AD-001 (Orb Apparatus — Mechanical Hub).

def build_orb_frame():
    print("Building SM_Rift_OrbFrame_A …")
    obj, bm = new_mesh("SM_Rift_OrbFrame_A")

    ring_r = 15.0        # frame ring radius
    tube_r = 0.85        # frame cross-section
    segs   = 28          # ring segments (we leave a gap)
    arc    = 0.82        # fraction of full circle (leaves ~65° gap)

    rng = random.Random(7)
    rings_verts = []
    for seg in range(int(segs * arc) + 1):
        t     = seg / segs
        angle = t * TAU * arc - PI/2
        cx    = math.cos(angle) * ring_r
        cz    = math.sin(angle) * ring_r
        tr    = tube_r + rng.uniform(-0.08, 0.12)

        ring = [bm.verts.new((
                    cx + math.cos(a*TAU/10) * tr,
                    math.sin(a*TAU/10) * tr,
                    cz + math.cos(a*TAU/10) * tr * 0.3))
                for a in range(10)]
        rings_verts.append((cx, cz, ring))

    for ri in range(len(rings_verts)-1):
        _, _, lo = rings_verts[ri]
        _, _, hi = rings_verts[ri+1]
        for j in range(10):
            nj=(j+1)%10
            try:
                bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except Exception:
                pass
    # end caps
    if rings_verts:
        bm.faces.new(list(reversed(rings_verts[0][2])))
        bm.faces.new(rings_verts[-1][2])

    # ── 8 beam arm attachment sockets ─────────────
    for i in range(8):
        angle = i * TAU/8
        arm_x = math.cos(angle) * ring_r * 0.85
        arm_z = math.sin(angle) * ring_r * 0.85
        sock  = bmesh.ops.create_cylinder(
            bm, cap_ends=True, cap_tris=False, segments=8,
            radius=0.60, depth=1.2,
            matrix=Matrix.Translation(Vector((arm_x, 0, arm_z))) @
                   Matrix.Rotation(PI/2, 4, 'X'))

    # ── structural cross-brace at 120° intervals ──
    for i in range(3):
        angle = i * TAU/3
        for sign in (-1, 1):
            x0 = math.cos(angle) * 1.5
            z0 = math.sin(angle) * 1.5
            x1 = math.cos(angle) * (ring_r - 1.0)
            z1 = math.sin(angle) * (ring_r - 1.0)
            bv = [bm.verts.new((x0 + math.cos(a*TAU/6)*0.22 * sign,
                                math.sin(a*TAU/6)*0.22,
                                z0 + math.sin(a*TAU/6)*0.22 * sign))
                  for a in range(6)]
            ev = [bm.verts.new((x1 + math.cos(a*TAU/6)*0.22 * sign,
                                math.sin(a*TAU/6)*0.22,
                                z1 + math.sin(a*TAU/6)*0.22 * sign))
                  for a in range(6)]
            for j in range(6):
                nj=(j+1)%6
                try:
                    bm.faces.new([bv[j],bv[nj],ev[nj],ev[j]])
                except Exception:
                    pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark",
                        "mat_ancient_machine_edge_wear",
                        "mat_gold_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  ORB HUB
# ══════════════════════════════════════════════
# Central hub with 8 radial beam arms. The orb itself is a VFX sphere
# in-engine; this is only the mechanical hub structure.
# Matches: AD-001 top-down view.

def build_orb_hub():
    print("Building SM_Rift_OrbHub_A …")
    obj, bm = new_mesh("SM_Rift_OrbHub_A")

    # ── central sphere structure ──────────────────
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=2.8)

    # ── concentric ring bands ─────────────────────
    for r_off in [3.2, 3.8, 4.4]:
        rv = [bm.verts.new((math.cos(i*TAU/32)*r_off,
                            math.sin(i*TAU/32)*r_off,
                            0.0))
              for i in range(32)]
        for i in range(32):
            ni=(i+1)%32
            bv = [bm.verts.new((rv[i].co.x, rv[i].co.y, -0.35)),
                  bm.verts.new((rv[ni].co.x,rv[ni].co.y, -0.35))]
            try:
                bm.faces.new([rv[i], rv[ni], bv[1], bv[0]])
            except Exception:
                pass

    # ── 8 radial beam arms (tapered, ~10m each) ───
    n_arms = 8
    for i in range(n_arms):
        angle = i * TAU/n_arms
        for t in range(16):
            pct = t / 15
            cx  = math.cos(angle) * (3.0 + pct * 10.0)
            cz  = math.sin(angle) * (3.0 + pct * 10.0)
            arm_r = 0.38 * (1 - pct * 0.55)
            if t == 0:
                prev = [bm.verts.new((
                            cx + math.cos(a*TAU/8)*arm_r,
                            math.sin(a*TAU/8)*arm_r,
                            cz + math.sin(a*TAU/8)*arm_r*0.4))
                        for a in range(8)]
            else:
                curr = [bm.verts.new((
                            cx + math.cos(a*TAU/8)*arm_r,
                            math.sin(a*TAU/8)*arm_r,
                            cz + math.sin(a*TAU/8)*arm_r*0.4))
                        for a in range(8)]
                for j in range(8):
                    nj=(j+1)%8
                    try:
                        bm.faces.new([prev[j],prev[nj],curr[nj],curr[j]])
                    except Exception:
                        pass
                prev = curr

        # emitter node at tip
        tip_cx = math.cos(angle) * 13.5
        tip_cz = math.sin(angle) * 13.5
        bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.55,
            matrix=Matrix.Translation(Vector((tip_cx, 0, tip_cz))))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive",
                        "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  BEAM EMITTER NODE
# ══════════════════════════════════════════════
# End-device at collector array. 2–3m diameter disc with concave
# emitter face, mounting flange, gold emissive ring.

def build_beam_emitter():
    print("Building SM_Rift_BeamEmitterNode_A …")
    obj, bm = new_mesh("SM_Rift_BeamEmitterNode_A")

    segs = 20
    # ── mounting disc ─────────────────────────────
    disc = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                    segments=segs, radius=1.1)
    bmesh.ops.translate(bm, verts=disc['verts'], vec=Vector((0, 0, 0)))
    df = [f for f in bm.faces if f.calc_center_median().length < 1.15
          and abs(f.calc_center_median().z) < 0.01]
    if df:
        back = bmesh.ops.extrude_face_region(bm, geom=df)
        bverts = [v for v in back['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=bverts, vec=Vector((0, 0, -0.35)))

    # ── concave emitter face ──────────────────────
    inner = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=segs, radius=0.70)
    bmesh.ops.translate(bm, verts=inner['verts'], vec=Vector((0, 0, 0.12)))
    emf = [f for f in bm.faces if f.calc_center_median().length < 0.72
           and abs(f.calc_center_median().z - 0.12) < 0.01]
    if emf:
        em_back = bmesh.ops.extrude_face_region(bm, geom=emf)
        emverts = [v for v in em_back['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=emverts, vec=Vector((0, 0, -0.22)))

    # ── gold emissive ring ─────────────────────────
    for r_off in [0.80, 0.90]:
        rv = [bm.verts.new((math.cos(i*TAU/segs)*r_off,
                            math.sin(i*TAU/segs)*r_off, 0.06))
              for i in range(segs)]
        for i in range(segs):
            ni=(i+1)%segs
            bv = [bm.verts.new((rv[i].co.x, rv[i].co.y, -0.01)),
                  bm.verts.new((rv[ni].co.x,rv[ni].co.y,-0.01))]
            try:
                bm.faces.new([rv[i],rv[ni],bv[1],bv[0]])
            except Exception:
                pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive",
                        "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  BRIDGE SPAN
# ══════════════════════════════════════════════
# Layered slab construction, 24m long × 8m wide. Circular insets, blue strips,
# exposed broken undersides on variant B. Matches: ancient_bridge_platform_kit_concept.png

def build_bridge_span(name, length=24.0, broken=False, seed=3):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    w, l, h = 8.0, length, 0.9
    nx, ny = 6, 12

    # ── top walkable surface ───────────────────────
    top = []
    for ix in range(nx):
        row = []
        for iy in range(ny):
            x = (ix/(nx-1) - 0.5) * w + rng.uniform(-0.08, 0.08)
            y = (iy/(ny-1) - 0.5) * l + rng.uniform(-0.05, 0.05)
            z = rng.uniform(-0.04, 0.04)
            if broken and iy > ny*0.65 and ix > nx*0.5:
                z -= (iy - ny*0.65) * 0.25 * (ix - nx*0.5) * 0.3
            row.append(bm.verts.new((x, y, z)))
        top.append(row)

    for ix in range(nx-1):
        for iy in range(ny-1):
            try:
                bm.faces.new([top[ix][iy], top[ix+1][iy],
                               top[ix+1][iy+1], top[ix][iy+1]])
            except Exception:
                pass

    # ── underside (thicker slabs) ─────────────────
    bot = []
    for ix in range(nx):
        row = []
        for iy in range(ny):
            tv = top[ix][iy]
            depth = h + rng.uniform(-0.05, 0.15)
            row.append(bm.verts.new((tv.co.x + rng.uniform(-0.05, 0.05),
                                     tv.co.y + rng.uniform(-0.05, 0.05),
                                     tv.co.z - depth)))
        bot.append(row)

    for ix in range(nx-1):
        for iy in range(ny-1):
            try:
                bm.faces.new([bot[ix][iy], bot[ix][iy+1],
                               bot[ix+1][iy+1], bot[ix+1][iy]])
            except Exception:
                pass

    # side walls
    for iy in range(ny-1):
        try:
            bm.faces.new([top[0][iy], top[0][iy+1],
                          bot[0][iy+1], bot[0][iy]])
            bm.faces.new([top[nx-1][iy], top[nx-1][iy+1],
                          bot[nx-1][iy+1], bot[nx-1][iy]])
        except Exception:
            pass
    for ix in range(nx-1):
        try:
            bm.faces.new([top[ix][0], top[ix+1][0],
                          bot[ix+1][0], bot[ix][0]])
            bm.faces.new([top[ix][ny-1], top[ix+1][ny-1],
                          bot[ix+1][ny-1], bot[ix][ny-1]])
        except Exception:
            pass

    # ── circular inset details ─────────────────────
    for iy in range(2, ny-2, 3):
        cy = (iy/(ny-1) - 0.5) * l
        for cx_off in (-w*0.25, w*0.25):
            rv = [bm.verts.new((cx_off + math.cos(a*TAU/12)*0.55,
                                cy + math.sin(a*TAU/12)*0.55,
                                0.02))
                  for a in range(12)]
            try:
                bm.faces.new(rv)
            except Exception:
                pass

    # ── blue emissive channel strips ──────────────
    for side in (-1, 1):
        sv = [bm.verts.new((side * (w*0.5 - 0.20), (iy/(ny-1)-0.5)*l, 0.01))
              for iy in range(ny)]
        for i in range(len(sv)-1):
            bv = [bm.verts.new((sv[i].co.x, sv[i].co.y, -0.04)),
                  bm.verts.new((sv[i+1].co.x, sv[i+1].co.y, -0.04))]
            try:
                bm.faces.new([sv[i], sv[i+1], bv[1], bv[0]])
            except Exception:
                pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_blue_emissive",
                        "mat_ancient_machine_edge_wear", "mat_wet_basalt"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  PLATFORM NODE
# ══════════════════════════════════════════════
# Floating circular platform ~18m diameter, layered slab underside,
# ancient machine surface detail.

def build_platform_node():
    print("Building SM_Rift_PlatformNode_A …")
    obj, bm = new_mesh("SM_Rift_PlatformNode_A")

    r = 9.0
    segs = 24

    # ── top surface (irregular circle) ───────────
    rng = random.Random(5)
    top_verts = [bm.verts.new((
                     math.cos(i*TAU/segs) * (r + rng.uniform(-0.5, 0.5)),
                     math.sin(i*TAU/segs) * (r + rng.uniform(-0.5, 0.5)),
                     rng.uniform(-0.12, 0.12)))
                 for i in range(segs)]
    try:
        bm.faces.new(top_verts)
    except Exception:
        pass

    # ── underslab steps (3 tiers) ─────────────────
    prev = top_verts
    for tier, (depth, squeeze) in enumerate([(0.5, 0.88), (1.4, 0.74), (2.8, 0.60)]):
        curr = [bm.verts.new((v.co.x * squeeze + rng.uniform(-0.15,0.15),
                              v.co.y * squeeze + rng.uniform(-0.15,0.15),
                              -depth))
                for v in prev]
        for j in range(segs):
            nj=(j+1)%segs
            try:
                bm.faces.new([prev[j], prev[nj], curr[nj], curr[j]])
            except Exception:
                pass
        prev = curr
    # bottom cap
    try:
        bm.faces.new(list(reversed(prev)))
    except Exception:
        pass

    # ── surface hex-grid inset detail ─────────────
    for hr in range(3):
        for hangle_i in range(6 if hr > 0 else 1):
            hangle = hangle_i * TAU/6
            hr_r   = hr * 3.5
            hcx    = math.cos(hangle) * hr_r
            hcy    = math.sin(hangle) * hr_r
            for s in range(6):
                a0 = s * TAU/6
                a1 = (s+1)*TAU/6
                pv = [bm.verts.new((hcx + math.cos(a)*1.6, hcy + math.sin(a)*1.6, 0.02))
                      for a in (a0, a1, a1, a0)]
                try:
                    bm.faces.new(pv)
                except Exception:
                    pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_blue_emissive",
                        "mat_ancient_machine_edge_wear"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  ANCIENT GATE WALL
# ══════════════════════════════════════════════
# Right-side gate wall structure. 50m wide × 100m tall.
# Two large circular sockets with blue emissive centres,
# nested rings, radial grooves, rock intrusions at base.
# Matches: concept art gate wall visible in Luminous Rift shots.

def build_gate_wall():
    print("Building SM_Rift_AncientWall_Gate_A …")
    obj, bm = new_mesh("SM_Rift_AncientWall_Gate_A")

    rng = random.Random(17)
    w, h, d = 25.0, 50.0, 6.0

    # ── main wall body ────────────────────────────
    nx, nz = 8, 12
    verts = []
    for ix in range(nx):
        col = []
        for iz in range(nz):
            x = (ix/(nx-1) - 0.5) * w + rng.uniform(-0.3, 0.3)
            z =  iz/(nz-1)       * h + rng.uniform(-0.2, 0.2)
            y = -d * 0.5 + math.sin(x*0.3)*1.2 + math.cos(z*0.15)*0.8
            col.append(bm.verts.new((x, y, z)))
        verts.append(col)

    for ix in range(nx-1):
        for iz in range(nz-1):
            try:
                bm.faces.new([verts[ix][iz], verts[ix+1][iz],
                               verts[ix+1][iz+1], verts[ix][iz+1]])
            except Exception:
                pass

    # ── two large circular socket features ────────
    for sock_cx, sock_cz in [(-6.0, 20.0), (5.0, 38.0)]:
        sock_r = rng.uniform(4.5, 6.0)
        # outer ring
        for r_off in [sock_r, sock_r-0.8, sock_r-2.2]:
            rv = [bm.verts.new((
                     sock_cx + math.cos(a*TAU/24)*r_off,
                     0.2 + (r_off - sock_r)*0.15,
                     sock_cz + math.sin(a*TAU/24)*r_off))
                  for a in range(24)]
            for i in range(24):
                ni=(i+1)%24
                bv = [bm.verts.new((rv[i].co.x, rv[i].co.y-0.35, rv[i].co.z)),
                      bm.verts.new((rv[ni].co.x,rv[ni].co.y-0.35,rv[ni].co.z))]
                try:
                    bm.faces.new([rv[i], rv[ni], bv[1], bv[0]])
                except Exception:
                    pass

        # emissive centre disc
        cv = [bm.verts.new((sock_cx + math.cos(a*TAU/12)*(sock_r-2.5),
                            0.25,
                            sock_cz + math.sin(a*TAU/12)*(sock_r-2.5)))
              for a in range(12)]
        try:
            bm.faces.new(cv)
        except Exception:
            pass

    # ── 4 radial groove lines ─────────────────────
    for gx in (-9.0, -3.0, 3.0, 9.0):
        for iz in range(nz):
            z0 = iz/(nz-1) * h
            z1 = (iz+1)/(nz-1) * h if iz < nz-1 else h
            gv = [bm.verts.new((gx - 0.12, -0.08, z0)),
                  bm.verts.new((gx + 0.12, -0.08, z0)),
                  bm.verts.new((gx + 0.12, -0.08, z1)),
                  bm.verts.new((gx - 0.12, -0.08, z1))]
            try:
                bm.faces.new(gv)
            except Exception:
                pass

    # ── rock intrusion base ───────────────────────
    for rx, rr in [(-10, 3.5), (8, 2.8), (0, 4.2)]:
        res = bmesh.ops.create_icosphere(bm, subdivisions=2,
                                          radius=rr)
        for v in res['verts']:
            v.co.x += rx
            v.co.y -= d * 0.3
            if v.co.z < 0:
                v.co.z *= 0.25

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark",
                        "mat_ancient_machine_edge_wear",
                        "mat_blue_emissive", "mat_wet_basalt"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  TOWER SEGMENTS
# ══════════════════════════════════════════════
# Distant silhouette towers. Vertical grooves, cyan emissive strips,
# broken tops. Matches: AD-003 (Tower Segment — Distant Structure).

def build_tower(name, width, height, seed=2):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs = 8
    levels_r = [(0, width*0.6), (height*0.15, width*0.55),
                (height*0.40, width*0.50), (height*0.65, width*0.46),
                (height*0.85, width*0.44), (height*0.95, width*0.40)]

    # ── tapered tower body ─────────────────────────
    rings = []
    for z, r in levels_r:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*(r + rng.uniform(-0.05,0.05)*width),
                    math.sin(i*TAU/segs)*(r + rng.uniform(-0.05,0.05)*width),
                    z + rng.uniform(-0.08, 0.08)*height*0.01))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try:
                bm.faces.new([lo[j], lo[nj], hi[nj], hi[j]])
            except Exception:
                pass
    bm.faces.new(list(reversed(rings[0])))

    # ── broken top (ragged edge) ──────────────────
    top_ring = rings[-1]
    for j in range(segs):
        top_h = height + rng.uniform(-height*0.08, height*0.04)
        bm.verts.new((top_ring[j].co.x, top_ring[j].co.y, top_h))

    # ── vertical groove cutouts ───────────────────
    for j in range(segs):
        angle = j * TAU/segs
        gx = math.cos(angle) * (width * 0.52)
        gy = math.sin(angle) * (width * 0.52)
        for seg_i in range(5):
            z0 = height * 0.15 + seg_i * height * 0.15
            z1 = z0 + height * 0.08
            gv = [bm.verts.new((gx + math.cos(angle+da)*0.04,
                                gy + math.sin(angle+da)*0.04,
                                z))
                  for da, z in [(-0.25,z0),(0.25,z0),(0.25,z1),(-0.25,z1)]]
            try:
                bm.faces.new(list(reversed(gv)))
            except Exception:
                pass

    # ── cyan emissive vertical strip ──────────────
    for _ in range(2):
        angle = rng.uniform(0, TAU)
        sx = math.cos(angle) * width * 0.51
        sy = math.sin(angle) * width * 0.51
        sv = [bm.verts.new((sx + math.cos(angle)*da, sy + math.sin(angle)*da,
                            z * height))
              for da, z in [(-0.04, 0.12), (0.04, 0.12),
                             (0.04, 0.88), (-0.04, 0.88)]]
        try:
            bm.faces.new(sv)
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_wet_basalt",
                        "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════

def main():
    clear_scene()
    print(f"\n=== Abyssal Earth — Luminous Rift Machines (→ {EXPORT_ROOT}) ===\n")

    assets = [
        (build_hex_tile,                         "SM_Rift_HexCollector_Tile_A.fbx"),
        (lambda: build_hex_cluster("SM_Rift_HexCollector_Cluster_A",  False, 1),
                                                 "SM_Rift_HexCollector_Cluster_A.fbx"),
        (lambda: build_hex_cluster("SM_Rift_HexCollector_Cluster_B_Broken", True, 2),
                                                 "SM_Rift_HexCollector_Cluster_B_Broken.fbx"),
        (build_orb_frame,                        "SM_Rift_OrbFrame_A.fbx"),
        (build_orb_hub,                          "SM_Rift_OrbHub_A.fbx"),
        (build_beam_emitter,                     "SM_Rift_BeamEmitterNode_A.fbx"),
        (build_gate_wall,                        "SM_Rift_AncientWall_Gate_A.fbx"),
        (lambda: build_bridge_span("SM_Rift_BridgeSpan_A", 24, False, 3),
                                                 "SM_Rift_BridgeSpan_A.fbx"),
        (lambda: build_bridge_span("SM_Rift_BridgeSpan_B_Broken", 24, True, 6),
                                                 "SM_Rift_BridgeSpan_B_Broken.fbx"),
        (build_platform_node,                    "SM_Rift_PlatformNode_A.fbx"),
        (lambda: build_tower("SM_Rift_TowerSegment_A",  6,  40, 2),
                                                 "SM_Rift_TowerSegment_A.fbx"),
        (lambda: build_tower("SM_Rift_TowerSegment_B", 10,  70, 5),
                                                 "SM_Rift_TowerSegment_B.fbx"),
        (lambda: build_tower("SM_Rift_TowerSegment_C", 14, 100, 8),
                                                 "SM_Rift_TowerSegment_C.fbx"),
    ]

    for builder, filename in assets:
        clear_scene()
        try:
            obj = builder()
            export_fbx(obj, filename)
            print(f"  ✓ {filename}")
        except Exception as e:
            print(f"  ✗ {filename}: {e}")
            import traceback; traceback.print_exc()

    clear_scene()
    print("\n=== Script 3/7 complete ===")

main()
