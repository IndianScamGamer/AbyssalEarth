"""
Abyssal Earth — Luminous Rift Environment Kit
Script 2/7: Natural rock geometry for The Luminous Rift

Run in Blender 4.x Scripting tab.
Exports to Content/ArtSourceExports/LuminousRift/

Assets generated:
  SM_Rift_CrystalCluster_S_A/B/C     — small blue crystal clusters (3 variants)
  SM_Rift_CrystalCluster_M_A/B/C     — medium
  SM_Rift_CrystalCluster_L_A/B       — large
  SM_Rift_CrystalCluster_Hero_A      — hero centrepiece
  SM_Rift_ForegroundLedge_A          — main First Overlook viewing ledge
  SM_Rift_ForegroundLedge_B_Broken   — broken ledge variant
  SM_Rift_RockArch_A/B               — cavern framing arches
  SM_Rift_Overhang_A/B               — ceiling overhangs
  SM_Rift_HangingSlab_A/B/C          — suspended ceiling rocks
  SM_Rift_CavernWall_Large_A/B       — background cavern wall panels
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


# ──────────── shared utils (same as script 1) ────────────
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
        "mat_wet_basalt":      (0.06, 0.06, 0.07, 1),
        "mat_crystal_blue":    (0.10, 0.55, 1.0,  1),
        "mat_blue_emissive":   (0.05, 0.40, 1.0,  1),
        "mat_ancient_machine_dark": (0.05, 0.05, 0.06, 1),
        "mat_gold_emissive":   (1.0,  0.72, 0.10, 1),
    }
    for name in names:
        if name not in bpy.data.materials:
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = palette.get(name, (0.5,0.5,0.5,1))
        obj.data.materials.append(bpy.data.materials[name])

def set_origin_to_base(obj):
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

def jitter_verts(bm_verts, seed, scale=0.04):
    rng = random.Random(seed)
    for v in bm_verts:
        v.co.x += rng.uniform(-scale, scale)
        v.co.y += rng.uniform(-scale, scale)
        v.co.z += rng.uniform(-scale * 0.5, scale * 0.5)


# ══════════════════════════════════════════════
#  CRYSTAL CLUSTER BUILDER (core function)
# ══════════════════════════════════════════════
# Produces angular faceted prismatic spires from a rough basalt rock base.
# Three silhouette types are seeded by variant char: A=vertical spear,
# B=fan spread, C=low broken. Matches: blue_crystal_harvestable_concept.png,
# LR-001 through LR-018 (crystals visible throughout Luminous Rift shots).

def build_crystal_kit(name, seed, config):
    """
    config = {
      'base_r': float,          rock footprint radius (m)
      'rock_h': float,          max rock height
      'spires': [               list of spire defs
        { 'ox':float, 'oy':float, 'h':float, 'w':float,
          'tilt': (tx,ty), 'sides':int }
      ]
    }
    """
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    base_r = config['base_r']
    rock_h = config['rock_h']

    # ── rock base (deformed icosphere) ────────────
    res = bmesh.ops.create_icosphere(bm, subdivisions=3,
                                      radius=base_r * 0.85)
    for v in res['verts']:
        # flatten bottom
        if v.co.z < -base_r * 0.3:
            v.co.z = -base_r * 0.3
        elif v.co.z < 0:
            v.co.z *= 0.35
        # cap top to rock_h
        if v.co.z > rock_h:
            v.co.z = rock_h * rng.uniform(0.85, 1.0)
        # organic noise
        v.co += Vector((rng.uniform(-0.05,0.05)*base_r,
                        rng.uniform(-0.05,0.05)*base_r,
                        rng.uniform(-0.03,0.03)*base_r))

    # ── crystal spires ────────────────────────────
    for sp in config['spires']:
        ox, oy = sp['ox'], sp['oy']
        h, w   = sp['h'], sp['w']
        sides  = sp.get('sides', 5)
        tx, ty = sp.get('tilt', (rng.uniform(-0.15, 0.15),
                                  rng.uniform(-0.15, 0.15)))
        tilt   = Vector((tx, ty, 1)).normalized()
        base_z = rock_h * rng.uniform(0.05, 0.15)

        base_verts, top_verts = [], []
        for s in range(sides):
            a = s * TAU / sides + rng.uniform(-0.1, 0.1)
            bx = ox + math.cos(a) * w
            by = oy + math.sin(a) * w
            base_verts.append(bm.verts.new((bx, by, base_z)))
            tx2 = ox + math.cos(a) * w * 0.06 + tilt.x * h * 0.22
            ty2 = oy + math.sin(a) * w * 0.06 + tilt.y * h * 0.22
            top_verts.append(bm.verts.new((tx2, ty2, base_z + h)))

        tip = bm.verts.new((ox + tilt.x * h * 0.08,
                            oy + tilt.y * h * 0.08,
                            base_z + h * 1.04))

        try:
            bm.faces.new(list(reversed(base_verts)))
        except Exception:
            pass
        for s in range(sides):
            ns = (s+1)%sides
            try:
                bm.faces.new([base_verts[s], base_verts[ns],
                               top_verts[ns], top_verts[s]])
                bm.faces.new([top_verts[s], top_verts[ns], tip])
            except Exception:
                pass

    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    return obj


def make_spires_A_small(seed):
    """Vertical spear cluster — 3 spires, upright."""
    rng = random.Random(seed)
    return [{'ox': rng.uniform(-0.04,0.04), 'oy': rng.uniform(-0.04,0.04),
             'h': h, 'w': h*0.13, 'sides': 5,
             'tilt': (rng.uniform(-0.06,0.06), rng.uniform(-0.06,0.06))}
            for h in [rng.uniform(0.22,0.30), rng.uniform(0.16,0.22),
                      rng.uniform(0.18,0.26)]]

def make_spires_B_fan(seed):
    """Fan spread — 5 spires fanning outward."""
    rng = random.Random(seed)
    spires = []
    for i in range(5):
        angle  = i * TAU/5
        spread = rng.uniform(0.04, 0.10)
        h      = rng.uniform(0.18, 0.32)
        spires.append({'ox': math.cos(angle)*spread,
                       'oy': math.sin(angle)*spread,
                       'h': h, 'w': h*0.11, 'sides': 5,
                       'tilt': (math.cos(angle)*0.18, math.sin(angle)*0.18)})
    return spires

def make_spires_C_broken(seed):
    """Low broken — short stumps and shards, some horizontal lean."""
    rng = random.Random(seed)
    spires = []
    for _ in range(4):
        h = rng.uniform(0.08, 0.18)
        spires.append({'ox': rng.uniform(-0.06,0.06),
                       'oy': rng.uniform(-0.06,0.06),
                       'h': h, 'w': h*0.18, 'sides': 4,
                       'tilt': (rng.uniform(-0.3,0.3), rng.uniform(-0.3,0.3))})
    return spires


# ══════════════════════════════════════════════
#  FOREGROUND LEDGE
# ══════════════════════════════════════════════
# The First Overlook platform the player stands on.
# Uneven walkable top, jagged outer edges, layered basalt striations.
# Matches: AD-004 (rock arch framing view), ancient_bridge_platform_kit_concept.png

def build_foreground_ledge(name, broken=False, seed=7):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    # ── ledge top surface (irregular polygon) ─────
    # Base outline: roughly trapezoidal with organic bumps
    outline_pts = []
    n_pts = 14
    base_w = 5.0  # ~10m wide total (half = 5 in each direction)
    base_d = 8.0
    for i in range(n_pts):
        a = i * TAU / n_pts
        # trapezoid-ish base shape with noise
        bx = math.cos(a) * (base_w + rng.uniform(-0.8, 0.8))
        by = math.sin(a) * (base_d * 0.5 + rng.uniform(-1.0, 1.0))
        outline_pts.append((bx, by, rng.uniform(-0.15, 0.25)))

    # Create top surface
    top_verts = [bm.verts.new(p) for p in outline_pts]
    bm.faces.new(top_verts)

    # ── extrude down for thickness with layered striations ─
    depths = [0.6, 1.4, 2.8, 5.2]
    prev_ring = top_verts
    for depth in depths:
        new_ring = []
        for v in prev_ring:
            squeeze = 1.0 - depth * 0.04
            nx = v.co.x * squeeze + rng.uniform(-0.15, 0.15)
            ny = v.co.y * squeeze + rng.uniform(-0.15, 0.15)
            new_ring.append(bm.verts.new((nx, ny, -depth + rng.uniform(-0.1, 0.1))))
        for i in range(len(prev_ring)):
            ni = (i+1)%len(prev_ring)
            try:
                bm.faces.new([prev_ring[i], prev_ring[ni],
                               new_ring[ni], new_ring[i]])
            except Exception:
                pass
        prev_ring = new_ring

    # bottom cap
    try:
        bm.faces.new(list(reversed(prev_ring)))
    except Exception:
        pass

    # ── crystal sockets on underside/edges ────────
    crystal_positions = [(-2.5, -2.0, -1.5), (1.8, 1.5, -2.0),
                         (-0.5, 3.0, -1.2),   (3.0, -1.0, -3.0)]
    if not broken:
        for cx, cy, cz in crystal_positions:
            cv = [bm.verts.new((cx + math.cos(a*TAU/4)*0.12,
                                cy + math.sin(a*TAU/4)*0.12,
                                cz))
                  for a in range(4)]
            tip = bm.verts.new((cx, cy, cz + 0.45))
            try:
                bm.faces.new(cv)
                for i in range(4):
                    bm.faces.new([cv[i], cv[(i+1)%4], tip])
            except Exception:
                pass

    # ── broken variant: shear off one side ────────
    if broken:
        for v in bm.verts:
            if v.co.x > 2.0 and v.co.z > -1.5:
                v.co.z -= (v.co.x - 2.0) * 0.8
                v.co.x += rng.uniform(-0.3, 0.1)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  ROCK ARCH
# ══════════════════════════════════════════════
# Natural stone arch 30–60m span. Uneven sides, crystal sockets,
# strong silhouette for cavern framing. Matches: AD-004.

def build_rock_arch(name, span, height, thickness, seed=3):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs = 16  # arch segments
    half = span * 0.5

    # ── left pillar ───────────────────────────────
    for side, sx in [("left", -half), ("right", half)]:
        pillar_w = thickness * rng.uniform(0.8, 1.2)
        pillar_d = thickness * rng.uniform(0.9, 1.1)
        base_h   = height * rng.uniform(0.35, 0.50)

        # tapered pillar: wider at base
        for i, (fz, fw, fd) in enumerate([
                (0.0,     pillar_w*1.3, pillar_d*1.3),
                (base_h*0.3, pillar_w*1.1, pillar_d*1.1),
                (base_h,  pillar_w,     pillar_d)]):
            ring = [bm.verts.new((sx + math.cos(a*TAU/8)*fw + rng.uniform(-0.2,0.2),
                                  math.sin(a*TAU/8)*fd + rng.uniform(-0.2,0.2),
                                  fz))
                    for a in range(8)]
            if i > 0:
                prev = list(bm.verts)[-8 - 8 : -8]
                for j in range(8):
                    nj = (j+1)%8
                    try:
                        bm.faces.new([prev[j], prev[nj], ring[nj], ring[j]])
                    except Exception:
                        pass
            if i == 0:
                try:
                    bm.faces.new(list(reversed(ring)))
                except Exception:
                    pass

    # ── arch curve (tube following parabolic path) ─
    arch_verts_rings = []
    for seg in range(segs + 1):
        t = seg / segs
        ax = half * (1 - 2 * t)                   # -half to +half
        az = height * (1 - (2*t-1)**2) * 0.85     # parabola
        az += rng.uniform(-0.3, 0.3)
        ring_r = thickness * (0.7 + rng.uniform(0, 0.25))
        ring_pts = [bm.verts.new((ax + math.cos(a*TAU/8)*ring_r,
                                  math.sin(a*TAU/8)*ring_r,
                                  az))
                    for a in range(8)]
        arch_verts_rings.append(ring_pts)

    for ri in range(len(arch_verts_rings)-1):
        lo, hi = arch_verts_rings[ri], arch_verts_rings[ri+1]
        for j in range(8):
            nj = (j+1)%8
            try:
                bm.faces.new([lo[j], lo[nj], hi[nj], hi[j]])
            except Exception:
                pass
    # cap ends
    try:
        bm.faces.new(list(reversed(arch_verts_rings[0])))
        bm.faces.new(arch_verts_rings[-1])
    except Exception:
        pass

    # ── crystal clusters embedded in arch ─────────
    for cx, cz, ch in [(0, height*0.9, 0.35), (-half*0.5, height*0.7, 0.28),
                        (half*0.5, height*0.7, 0.28)]:
        cv = [bm.verts.new((cx + math.cos(a*TAU/5)*0.14,
                            rng.uniform(-0.10, 0.10),
                            cz + math.sin(a*TAU/5)*0.14))
              for a in range(5)]
        ctip = bm.verts.new((cx, 0, cz + ch))
        try:
            bm.faces.new(cv)
            for i in range(5):
                bm.faces.new([cv[i], cv[(i+1)%5], ctip])
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  CEILING OVERHANG
# ══════════════════════════════════════════════
# Dark rock overhangs that frame the top of the First Overlook composition.
# Matches: AD-004, LR-004, LR-009.

def build_overhang(name, width, depth, seed=15):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    n = 10
    # ── bottom face profile (irregular) ──────────
    bot_pts = []
    for i in range(n):
        t = i / (n - 1)
        bx = (t - 0.5) * width + rng.uniform(-0.5, 0.5)
        by = rng.uniform(-depth * 0.15, depth * 0.15)
        bot_pts.append(bm.verts.new((bx, by, 0.0)))

    top_pts = []
    for i, bv in enumerate(bot_pts):
        t = i / (n - 1)
        thk = rng.uniform(1.5, 4.0)
        ovh = depth * (0.5 + 0.5 * abs(1 - 2*t))  # deeper at edges
        top_pts.append(bm.verts.new((bv.co.x + rng.uniform(-0.3, 0.3),
                                     bv.co.y + ovh,
                                     thk + rng.uniform(-0.3, 0.3))))

    # faces
    try:
        bm.faces.new(list(reversed(bot_pts)))
        bm.faces.new(top_pts)
    except Exception:
        pass
    for i in range(n-1):
        try:
            bm.faces.new([bot_pts[i], bot_pts[i+1],
                          top_pts[i+1], top_pts[i]])
        except Exception:
            pass
    # side caps
    try:
        bm.faces.new([bot_pts[0], top_pts[0],
                      bm.verts.new((bot_pts[0].co.x - 0.3, top_pts[0].co.y, 0))])
        bm.faces.new([bot_pts[-1], top_pts[-1],
                      bm.verts.new((bot_pts[-1].co.x + 0.3, top_pts[-1].co.y, 0))])
    except Exception:
        pass

    # ── stalactite-style crystal drips ────────────
    for _ in range(rng.randint(3, 6)):
        cx = rng.uniform(-width*0.35, width*0.35)
        cy = rng.uniform(0, depth * 0.3)
        ch = rng.uniform(0.3, 0.8)
        cv = [bm.verts.new((cx + math.cos(a*TAU/4)*0.08,
                            cy + math.sin(a*TAU/4)*0.08,
                            rng.uniform(-0.2, 0.2)))
              for a in range(4)]
        ctip = bm.verts.new((cx, cy, -ch))
        try:
            bm.faces.new(list(reversed(cv)))
            for i in range(4):
                bm.faces.new([cv[i], cv[(i+1)%4], ctip])
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  HANGING SLAB
# ══════════════════════════════════════════════
# Large fractured rock slab suspended from the ceiling. Crystal clusters
# embedded on underside. Convincing fracture geometry at anchor.
# Matches: AD-006 (Hanging Slab — Ceiling Detail).

def build_hanging_slab(name, w, l, thickness, seed=42):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    n_w, n_l = 5, 8
    # ── slab top surface ──────────────────────────
    top_grid = []
    for gx in range(n_w):
        row = []
        for gy in range(n_l):
            tx = (gx / (n_w-1) - 0.5) * w + rng.uniform(-0.15, 0.15)
            ty = (gy / (n_l-1) - 0.5) * l + rng.uniform(-0.15, 0.15)
            tz = 0.0 + rng.uniform(-0.08, 0.08)
            row.append(bm.verts.new((tx, ty, tz)))
        top_grid.append(row)

    # ── slab bottom (slightly varied) ─────────────
    bot_grid = []
    for gx in range(n_w):
        row = []
        for gy in range(n_l):
            tv = top_grid[gx][gy]
            thk = thickness + rng.uniform(-0.2, 0.3)
            row.append(bm.verts.new((tv.co.x + rng.uniform(-0.12, 0.12),
                                     tv.co.y + rng.uniform(-0.12, 0.12),
                                     tv.co.z - thk)))
        bot_grid.append(row)

    # top faces
    for gx in range(n_w-1):
        for gy in range(n_l-1):
            try:
                bm.faces.new([top_grid[gx][gy],   top_grid[gx+1][gy],
                               top_grid[gx+1][gy+1], top_grid[gx][gy+1]])
            except Exception:
                pass

    # bottom faces
    for gx in range(n_w-1):
        for gy in range(n_l-1):
            try:
                bm.faces.new([bot_grid[gx][gy],   bot_grid[gx][gy+1],
                               bot_grid[gx+1][gy+1], bot_grid[gx+1][gy]])
            except Exception:
                pass

    # side edges
    for gy in range(n_l-1):
        for gx, gx2 in [(0,0), (n_w-1, n_w-1)]:
            try:
                bm.faces.new([top_grid[gx][gy],   top_grid[gx][gy+1],
                               bot_grid[gx2][gy+1], bot_grid[gx2][gy]])
            except Exception:
                pass
    for gx in range(n_w-1):
        for gy, gy2 in [(0,0), (n_l-1, n_l-1)]:
            try:
                bm.faces.new([top_grid[gx][gy],   top_grid[gx+1][gy],
                               bot_grid[gx+1][gy2], bot_grid[gx][gy2]])
            except Exception:
                pass

    # ── crystal clusters on underside ─────────────
    for cx, cy in [(0,0), (rng.uniform(-w*0.25, w*0.25),
                            rng.uniform(-l*0.25, l*0.25))]:
        cz_base = -thickness - 0.05
        for s in range(rng.randint(2, 4)):
            h = rng.uniform(0.25, 0.55)
            angle = s * TAU / 4 + rng.uniform(-0.3, 0.3)
            spx = cx + math.cos(angle) * rng.uniform(0.1, 0.25)
            spy = cy + math.sin(angle) * rng.uniform(0.1, 0.25)
            cv = [bm.verts.new((spx + math.cos(a*TAU/5)*0.06,
                                spy + math.sin(a*TAU/5)*0.06,
                                cz_base))
                  for a in range(5)]
            ctip = bm.verts.new((spx, spy, cz_base - h))
            try:
                bm.faces.new(list(reversed(cv)))
                for i in range(5):
                    bm.faces.new([cv[i], cv[(i+1)%5], ctip])
            except Exception:
                pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  CAVERN WALL
# ══════════════════════════════════════════════
# Large background wall tile ~50m wide.  World-aligned UV friendly,
# vertical striations, occasional crystal socket.

def build_cavern_wall(name, width, height, depth, seed=99):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    nx, nz = 8, 10
    verts = []
    for ix in range(nx):
        col = []
        for iz in range(nz):
            x = (ix / (nx-1) - 0.5) * width
            z = iz / (nz-1) * height
            # vertical striation noise (deeper in y = wall thickness)
            y_noise = math.sin(x * 0.8) * 0.8 + math.cos(x * 1.4) * 0.5
            y = -depth * 0.5 + y_noise + rng.uniform(-0.3, 0.3)
            z += rng.uniform(-0.15, 0.15)
            col.append(bm.verts.new((x, y, z)))
        verts.append(col)

    for ix in range(nx-1):
        for iz in range(nz-1):
            try:
                bm.faces.new([verts[ix][iz],   verts[ix+1][iz],
                               verts[ix+1][iz+1], verts[ix][iz+1]])
            except Exception:
                pass

    # ── crystal sockets ────────────────────────────
    for _ in range(rng.randint(2, 5)):
        cx = rng.uniform(-width*0.35, width*0.35)
        cz = rng.uniform(height*0.15, height*0.80)
        h  = rng.uniform(0.5, 1.5)
        cv = [bm.verts.new((cx + math.cos(a*TAU/5)*0.18,
                            rng.uniform(-depth*0.3, 0),
                            cz + math.sin(a*TAU/5)*0.18))
              for a in range(5)]
        ctip = bm.verts.new((cx, rng.uniform(0, depth*0.1), cz + h))
        try:
            bm.faces.new(cv)
            for i in range(5):
                bm.faces.new([cv[i], cv[(i+1)%5], ctip])
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════

def main():
    clear_scene()
    print(f"\n=== Abyssal Earth — Luminous Rift Env Kit (→ {EXPORT_ROOT}) ===\n")

    # Crystal cluster configs
    def cfg_S_A(): return {'base_r':0.22,'rock_h':0.12,
                           'spires':make_spires_A_small(1)}
    def cfg_S_B(): return {'base_r':0.22,'rock_h':0.10,
                           'spires':make_spires_B_fan(2)}
    def cfg_S_C(): return {'base_r':0.22,'rock_h':0.08,
                           'spires':make_spires_C_broken(3)}
    def cfg_M_A(): return {'base_r':0.36,'rock_h':0.20,
                           'spires':make_spires_A_small(4)*2}
    def cfg_M_B(): return {'base_r':0.36,'rock_h':0.18,
                           'spires':make_spires_B_fan(5)}
    def cfg_M_C(): return {'base_r':0.36,'rock_h':0.16,
                           'spires':make_spires_C_broken(6)*2}
    def cfg_L_A(): return {'base_r':0.55,'rock_h':0.30,
                           'spires':[
                               {'ox':0,'oy':0,'h':1.35,'w':0.14,'sides':5},
                               {'ox':-0.18,'oy':0.12,'h':1.05,'w':0.12,'sides':5,
                                'tilt':(-0.12, 0.05)},
                               {'ox':0.20,'oy':-0.10,'h':0.90,'w':0.11,'sides':5,
                                'tilt':(0.10,-0.08)},
                               {'ox':-0.08,'oy':-0.22,'h':0.60,'w':0.09,'sides':4,
                                'tilt':(-0.06,-0.15)},
                           ]}
    def cfg_L_B(): return {'base_r':0.55,'rock_h':0.28,
                           'spires':make_spires_B_fan(8) + make_spires_C_broken(9)}
    def cfg_Hero(): return {'base_r':0.90,'rock_h':0.45,
                            'spires':[
                                {'ox':0,'oy':0,'h':2.80,'w':0.22,'sides':6},
                                {'ox':-0.35,'oy':0.20,'h':2.10,'w':0.18,'sides':5,
                                 'tilt':(-0.10, 0.06)},
                                {'ox':0.38,'oy':-0.15,'h':1.85,'w':0.16,'sides':5,
                                 'tilt':(0.12,-0.06)},
                                {'ox':-0.20,'oy':-0.40,'h':1.40,'w':0.14,'sides':5,
                                 'tilt':(-0.08,-0.18)},
                                {'ox':0.25,'oy':0.38,'h':1.20,'w':0.13,'sides':4,
                                 'tilt':(0.08, 0.20)},
                                {'ox':-0.50,'oy':-0.10,'h':0.80,'w':0.10,'sides':4,
                                 'tilt':(-0.25,-0.05)},
                                {'ox':0.15,'oy':-0.52,'h':0.65,'w':0.09,'sides':4,
                                 'tilt':(0.04,-0.28)},
                            ]}

    assets = [
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_S_A",1,cfg_S_A()),
         "SM_Rift_CrystalCluster_S_A.fbx"),
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_S_B",2,cfg_S_B()),
         "SM_Rift_CrystalCluster_S_B.fbx"),
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_S_C",3,cfg_S_C()),
         "SM_Rift_CrystalCluster_S_C.fbx"),
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_M_A",4,cfg_M_A()),
         "SM_Rift_CrystalCluster_M_A.fbx"),
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_M_B",5,cfg_M_B()),
         "SM_Rift_CrystalCluster_M_B.fbx"),
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_M_C",6,cfg_M_C()),
         "SM_Rift_CrystalCluster_M_C.fbx"),
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_L_A",7,cfg_L_A()),
         "SM_Rift_CrystalCluster_L_A.fbx"),
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_L_B",8,cfg_L_B()),
         "SM_Rift_CrystalCluster_L_B.fbx"),
        (lambda: build_crystal_kit("SM_Rift_CrystalCluster_Hero_A",9,cfg_Hero()),
         "SM_Rift_CrystalCluster_Hero_A.fbx"),

        (lambda: build_foreground_ledge("SM_Rift_ForegroundLedge_A",False,7),
         "SM_Rift_ForegroundLedge_A.fbx"),
        (lambda: build_foreground_ledge("SM_Rift_ForegroundLedge_B_Broken",True,14),
         "SM_Rift_ForegroundLedge_B_Broken.fbx"),

        (lambda: build_rock_arch("SM_Rift_RockArch_A", 28,18,3.5, 3),
         "SM_Rift_RockArch_A.fbx"),
        (lambda: build_rock_arch("SM_Rift_RockArch_B", 42,25,5.0, 6),
         "SM_Rift_RockArch_B.fbx"),

        (lambda: build_overhang("SM_Rift_Overhang_A", 22, 12, 11),
         "SM_Rift_Overhang_A.fbx"),
        (lambda: build_overhang("SM_Rift_Overhang_B", 35, 18, 22),
         "SM_Rift_Overhang_B.fbx"),

        (lambda: build_hanging_slab("SM_Rift_HangingSlab_A", 12, 25, 2.5, 42),
         "SM_Rift_HangingSlab_A.fbx"),
        (lambda: build_hanging_slab("SM_Rift_HangingSlab_B",  8, 18, 3.5, 55),
         "SM_Rift_HangingSlab_B.fbx"),
        (lambda: build_hanging_slab("SM_Rift_HangingSlab_C", 20, 40, 4.0, 68),
         "SM_Rift_HangingSlab_C.fbx"),

        (lambda: build_cavern_wall("SM_Rift_CavernWall_Large_A", 40, 30, 5, 99),
         "SM_Rift_CavernWall_Large_A.fbx"),
        (lambda: build_cavern_wall("SM_Rift_CavernWall_Large_B", 60, 40, 8, 111),
         "SM_Rift_CavernWall_Large_B.fbx"),
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
    print("\n=== Script 2/7 complete ===")

main()
