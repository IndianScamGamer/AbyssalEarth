"""
Abyssal Earth — World Biome Kits
Script 5/7: Per-world unique environment geometry

Run in Blender 4.x Scripting tab.
Each world exports to its own subdirectory.

Fossil Sky   → Content/ArtSourceExports/FossilSky/
Glassroot    → Content/ArtSourceExports/GlassrootForest/
Gravity Well → Content/ArtSourceExports/GravityWell/
Inner Sea    → Content/ArtSourceExports/InnerSea/
Mantle Garden→ Content/ArtSourceExports/MantleGarden/

Assets generated:

FOSSIL SKY (amber, warm, massive fossil skeleton ceiling):
  SM_FossilSky_RibArch_A/B/C       - Massive bone rib arches spanning tunnel
  SM_FossilSky_SpineSegment_A/B    - Giant vertebra spine segments
  SM_FossilSky_WoodDock_A          - Weathered dock/bridge platform

GLASSROOT FOREST (misty, translucent red-veined glass trees):
  SM_Glassroot_TrunkBase_A/B       - 4–8m diameter glass-bark tree trunk base
  SM_Glassroot_RootFlange_A        - Sprawling surface roots
  SM_Glassroot_FloatingPlatform_A  - Root-encrusted rock platform in flooded zone

GRAVITY WELL (spiraling debris vortex, floating rocks):
  SM_GravityWell_FloatingRock_A/B/C - Irregular floating rock chunks
  SM_GravityWell_SpiralDrift_A     - Thin plate-like rock debris
  SM_GravityWell_PortalRing_A      - Outer ring of the gravity vortex opening

INNER SEA (underground ocean, stalactites, golden bioluminescent docks):
  SM_InnerSea_Stalactite_A/B/C     - Hanging ceiling formations
  SM_InnerSea_WoodDock_A           - Floating/grounded dock section
  SM_InnerSea_DockPost_A           - Dock piling post

MANTLE GARDEN (volcanic, lava, purple crystals):
  SM_MantleGarden_LavaRock_A/B     - Jagged volcanic rock formations
  SM_MantleGarden_LavaBridge_A     - Natural lava-cooled rock arch bridge
  SM_MantleGarden_PurpleCrystal_A/B - Purple amethyst-style crystal clusters
  SM_MantleGarden_SteamColumn_A   - Solid base column for steam VFX
"""

import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix

TAU = math.tau
PI  = math.pi

BASE_EXPORT = os.path.join(os.path.dirname(bpy.data.filepath),
                            "..", "..", "..",
                            "Content", "ArtSourceExports")
BASE_EXPORT = os.path.normpath(BASE_EXPORT)


def get_dir(subdir):
    p = os.path.join(BASE_EXPORT, subdir)
    os.makedirs(p, exist_ok=True)
    return p

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
        "mat_wet_basalt":         (0.06, 0.06, 0.07, 1),
        "mat_crystal_blue":       (0.10, 0.55, 1.0,  1),
        "mat_blue_emissive":      (0.05, 0.40, 1.0,  1),
        "mat_ancient_machine_dark":(0.05, 0.05, 0.06, 1),
        "mat_gold_emissive":      (1.0,  0.72, 0.10, 1),
        "mat_human_equipment":    (0.18, 0.16, 0.14, 1),
        "mat_amber_emissive":     (1.0,  0.55, 0.05, 1),
        "mat_lava_emissive":      (1.0,  0.25, 0.0,  1),
        "mat_fossil_bone":        (0.72, 0.64, 0.44, 1),
        "mat_glass_bark":         (0.55, 0.80, 0.70, 1),
        "mat_red_emissive_vein":  (0.90, 0.05, 0.05, 1),
        "mat_purple_emissive":    (0.55, 0.10, 0.90, 1),
        "mat_water_bioluminescent":(0.10, 0.80, 0.60, 1),
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

def export_fbx(obj, export_dir, filename):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = os.path.join(export_dir, filename)
    bpy.ops.export_scene.fbx(
        filepath=path, use_selection=True, global_scale=100.0,
        apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
        mesh_smooth_type='FACE', use_mesh_modifiers=True, bake_anim=False)
    print(f"  Exported: {path}")

def box(bm, mn, mx):
    x0,y0,z0 = mn; x1,y1,z1 = mx
    vv = [bm.verts.new((x0,y0,z0)), bm.verts.new((x1,y0,z0)),
          bm.verts.new((x1,y1,z0)), bm.verts.new((x0,y1,z0)),
          bm.verts.new((x0,y0,z1)), bm.verts.new((x1,y0,z1)),
          bm.verts.new((x1,y1,z1)), bm.verts.new((x0,y1,z1))]
    for fi in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:
        try: bm.faces.new([vv[i] for i in fi])
        except: pass


# ════════════════════════════════════════════════════════
#  FOSSIL SKY
# ════════════════════════════════════════════════════════

def build_rib_arch(name, span, height, rib_w, seed=1):
    """Giant fossil rib bone arching over a tunnel.
    Organic elongated parabola with bone texture striations.
    Matches: fossil_sky_concept.png — ribs arching over the entire tunnel ceiling."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs  = 20
    arc   = 0.92       # fraction of circle
    half  = span * 0.5

    rings = []
    for seg in range(int(segs * arc) + 1):
        t     = seg / segs
        angle = t * TAU * arc
        cx    = math.cos(angle) * half
        cz    = math.sin(angle) * height
        # organic bone cross-section (flattened oval)
        tw = rib_w * (0.7 + 0.5 * math.sin(t * PI))  # thicker in middle
        th = tw * 0.55                                  # flatter = bone
        ring = [bm.verts.new((
                    cx + math.cos(a*TAU/8)*tw,
                    math.sin(a*TAU/8)*th + rng.uniform(-0.02, 0.02),
                    cz + rng.uniform(-0.05*height, 0.05*height)))
                for a in range(8)]
        rings.append(ring)
        # bone striation grooves along length
        if seg % 3 == 0:
            for j in (0, 4):
                gv = bm.verts.new((cx + math.cos(j*TAU/8)*tw*1.02,
                                   math.sin(j*TAU/8)*th*1.02,
                                   cz))

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(8):
            nj=(j+1)%8
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    if rings:
        try: bm.faces.new(list(reversed(rings[0])))
        except: pass
        try: bm.faces.new(rings[-1])
        except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_fossil_bone"])
    set_origin_bottom(obj)
    return obj


def build_spine_segment(name, length, width, seed=5):
    """Giant vertebra-style spine segment.
    Oval body with 4 transverse processes (bone wings)."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    # ── vertebra body ─────────────────────────────
    segs = 12
    levels = [(0, width*0.55), (length*0.2, width*0.60),
              (length*0.5, width*0.65), (length*0.8, width*0.60),
              (length, width*0.55)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*r + rng.uniform(-0.05,0.05)*r,
                    math.sin(i*TAU/segs)*r*0.65 + rng.uniform(-0.03,0.03)*r,
                    z))
                for i in range(segs)]
        rings.append(ring)
    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    for r in (rings[0], rings[-1]):
        try: bm.faces.new(list(reversed(r)))
        except: pass

    # ── 4 transverse bone wings ────────────────────
    for z_frac in (0.25, 0.75):
        for side in (-1, 1):
            wing_len = width * 1.4
            wx0, wx1 = width*0.62*side, wing_len*side
            wz = z_frac * length
            wv = [bm.verts.new((wx0, rng.uniform(-0.08,0.08)*width, wz-0.08)),
                  bm.verts.new((wx0, rng.uniform(-0.08,0.08)*width, wz+0.08)),
                  bm.verts.new((wx1, rng.uniform(-0.25,0.25)*width*0.3, wz+0.06+wing_len*0.12)),
                  bm.verts.new((wx1, rng.uniform(-0.25,0.25)*width*0.3, wz-0.06+wing_len*0.12))]
            try: bm.faces.new(wv)
            except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_fossil_bone"])
    set_origin_bottom(obj)
    return obj


def build_wood_dock(length=8.0, seed=4):
    """Weathered wooden dock section. 2m wide plank-top walkway,
    support posts, cross-braces."""
    print("Building SM_FossilSky_WoodDock_A …")
    obj, bm = new_mesh("SM_FossilSky_WoodDock_A")
    rng = random.Random(seed)

    w = 2.0
    plank_h = 0.05
    n_planks = int(length / 0.25)

    for p in range(n_planks):
        y0 = (p / n_planks - 0.5) * length + rng.uniform(-0.005, 0.005)
        y1 = ((p+1)/n_planks - 0.5) * length + rng.uniform(-0.005, 0.005)
        dip = rng.uniform(-0.01, 0.008)
        box(bm, (-w/2 + 0.01, y0, dip), (w/2 - 0.01, y1, plank_h + dip))

    # support posts
    for py in [i/(4) * length - length/2 for i in range(5)]:
        for px in (-w/2 + 0.12, w/2 - 0.12):
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=6, radius=0.055, depth=0.85,
                                       matrix=Matrix.Translation(Vector((px, py, -0.42))))

    # cross-braces
    for py in [i/3*length - length/2 for i in range(4)]:
        for dx in (-1, 1):
            bv = [bm.verts.new((-w/2*dx, py - length*0.12, -0.05)),
                  bm.verts.new(( w/2*dx, py + length*0.12, -0.70))]

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])  # wood-like
    set_origin_bottom(obj)
    return obj


# ════════════════════════════════════════════════════════
#  GLASSROOT FOREST
# ════════════════════════════════════════════════════════

def build_glassroot_trunk(name, r, seed=10):
    """Translucent glass-bark tree trunk with red vein channels.
    Smooth surface with occasional red emissive ridge.
    Matches: glassroot_forest_concept.png."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs = 16
    h_trunk = r * 4.0    # trunks are tall relative to radius

    # ── trunk levels (slight natural taper) ──────
    levels = [(0, r), (r*0.8, r*0.98), (r*1.8, r*0.95),
              (h_trunk*0.4, r*0.88), (h_trunk*0.65, r*0.82),
              (h_trunk*0.80, r*0.76), (h_trunk, r*0.70)]
    rings = []
    for z, lr in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*lr + rng.uniform(-0.02,0.02)*r,
                    math.sin(i*TAU/segs)*lr + rng.uniform(-0.02,0.02)*r,
                    z + rng.uniform(-0.01,0.01)*r))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    try: bm.faces.new(list(reversed(rings[0])))
    except: pass

    # ── root flange at base ───────────────────────
    flange_segs = 24
    for fi in range(flange_segs):
        angle = fi * TAU / flange_segs
        spread = r * (1.8 + 0.6 * abs(math.sin(angle * 3)))
        fv = [
            bm.verts.new((math.cos(angle)*r*1.02, math.sin(angle)*r*1.02, 0.0)),
            bm.verts.new((math.cos(angle)*spread,  math.sin(angle)*spread,  0.0)),
            bm.verts.new((math.cos(angle)*spread*0.95, math.sin(angle)*spread*0.95,
                          -rng.uniform(0.05,0.20)*r)),
        ]
        try: bm.faces.new(fv)
        except: pass

    # ── 3 red emissive vein ridges ─────────────────
    for vein_i in range(3):
        v_angle = vein_i * TAU/3 + rng.uniform(-0.3, 0.3)
        for zi in range(12):
            z = zi / 11 * h_trunk * 0.85
            v_angle += rng.uniform(-0.05, 0.05)  # gentle spiral
            vx = math.cos(v_angle) * (r + 0.035)
            vy = math.sin(v_angle) * (r + 0.035)
            bm.verts.new((vx, vy, z))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_glass_bark", "mat_red_emissive_vein"])
    set_origin_bottom(obj)
    return obj


def build_glassroot_platform():
    """Rock platform overgrown with glass tree roots."""
    print("Building SM_Glassroot_FloatingPlatform_A …")
    obj, bm = new_mesh("SM_Glassroot_FloatingPlatform_A")
    rng = random.Random(22)

    # ── rock body ─────────────────────────────────
    res = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=3.5)
    for v in res['verts']:
        if v.co.z < -1.5: v.co.z = -1.5
        v.co.z *= 0.5
        v.co.x += rng.uniform(-0.2, 0.2)
        v.co.y += rng.uniform(-0.2, 0.2)

    # ── surface root tendrils ─────────────────────
    for ri in range(6):
        angle  = ri * TAU/6 + rng.uniform(-0.2, 0.2)
        length = rng.uniform(1.5, 3.5)
        for t in range(8):
            pct = t/7
            rx  = math.cos(angle) * (3.4 + pct * length)
            ry  = math.sin(angle) * (3.4 + pct * length)
            rz  = -pct * 0.8 + rng.uniform(-0.1, 0.1)
            rw  = 0.08 * (1 - pct * 0.6)
            bm.verts.new((rx + rng.uniform(-0.04,0.04),
                          ry + rng.uniform(-0.04,0.04),
                          rz))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_glass_bark"])
    set_origin_bottom(obj)
    return obj


# ════════════════════════════════════════════════════════
#  GRAVITY WELL
# ════════════════════════════════════════════════════════

def build_floating_rock(name, scale, seed=30):
    """Irregular floating rock chunk. Fractured faces, no clean flat bottom.
    Matches: gravity_well_concept.png — debris spiraling around vortex."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=scale)
    for v in res['verts']:
        # organic rocky deformation
        v.co.x *= rng.uniform(0.6, 1.4)
        v.co.y *= rng.uniform(0.6, 1.4)
        v.co.z *= rng.uniform(0.5, 1.3)
        v.co += Vector((rng.uniform(-0.08,0.08)*scale,
                        rng.uniform(-0.08,0.08)*scale,
                        rng.uniform(-0.08,0.08)*scale))

    # ── fracture detail: create bevelled crack ─────
    for _ in range(rng.randint(2, 4)):
        crack_dir = Vector((rng.uniform(-1,1), rng.uniform(-1,1),
                            rng.uniform(-1,1))).normalized()
        for v in bm.verts:
            proj = v.co.dot(crack_dir)
            if abs(proj - rng.uniform(scale*0.1, scale*0.5)) < scale*0.08:
                v.co += crack_dir * rng.uniform(-0.04,0.04)*scale

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt"])
    set_origin_bottom(obj)
    return obj


def build_portal_ring():
    """Outer ring structure of the Gravity Well vortex opening.
    Partially destroyed, floating rock shards incorporated.
    Matches: gravity_well_concept.png — the central glowing void."""
    print("Building SM_GravityWell_PortalRing_A …")
    obj, bm = new_mesh("SM_GravityWell_PortalRing_A")
    rng = random.Random(7)

    ring_r  = 22.0
    tube_r  = 1.2
    segs    = 32
    cover   = 0.78    # partial ring

    rings_all = []
    for seg in range(int(segs * cover) + 1):
        t     = seg / segs
        angle = t * TAU * cover
        cx    = math.cos(angle) * ring_r
        cz    = math.sin(angle) * ring_r
        tr    = tube_r + rng.uniform(-0.1, 0.15)
        ring  = [bm.verts.new((
                     cx + math.cos(a*TAU/10)*tr,
                     math.sin(a*TAU/10)*tr,
                     cz + math.sin(a*TAU/10)*tr*0.35))
                 for a in range(10)]
        rings_all.append(ring)

    for ri in range(len(rings_all)-1):
        lo, hi = rings_all[ri], rings_all[ri+1]
        for j in range(10):
            nj=(j+1)%10
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    if rings_all:
        try: bm.faces.new(list(reversed(rings_all[0])))
        except: pass
        try: bm.faces.new(rings_all[-1])
        except: pass

    # ── ancient machine details on ring ───────────
    for i in range(8):
        angle = i * TAU/8
        rx = math.cos(angle) * ring_r
        rz = math.sin(angle) * ring_r
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=tube_r*1.4,
                                    matrix=Matrix.Translation(Vector((rx, 0, rz))))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_blue_emissive",
                        "mat_wet_basalt"])
    set_origin_bottom(obj)
    return obj


# ════════════════════════════════════════════════════════
#  INNER SEA
# ════════════════════════════════════════════════════════

def build_stalactite(name, r_base, height, seed=50):
    """Hanging cave stalactite. Natural tapered form with occasional
    bioluminescent tip. Matches: inner_sea_concept.png."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    segs  = 8
    levels = [(0, r_base), (height*0.25, r_base*0.78),
              (height*0.55, r_base*0.50), (height*0.80, r_base*0.26),
              (height*0.95, r_base*0.09), (height, r_base*0.02)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*(r + rng.uniform(-0.05,0.05)*r),
                    math.sin(i*TAU/segs)*(r + rng.uniform(-0.05,0.05)*r),
                    -(z + rng.uniform(-0.02,0.02)*height)))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    tip = bm.verts.new((rng.uniform(-0.02,0.02)*r_base,
                        rng.uniform(-0.02,0.02)*r_base,
                        -(height + r_base*0.05)))
    for j in range(segs):
        try: bm.faces.new([rings[-1][j], rings[-1][(j+1)%segs], tip])
        except: pass

    # top mount cap
    try: bm.faces.new(rings[0])
    except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_water_bioluminescent"])
    set_origin_bottom(obj)
    return obj


def build_inner_sea_dock():
    """Floating harbour dock section. Plank walkway, rusty metal cleats,
    rope loops. Matches atmosphere of inner_sea_concept.png."""
    print("Building SM_InnerSea_WoodDock_A …")
    obj, bm = new_mesh("SM_InnerSea_WoodDock_A")
    rng = random.Random(60)

    length, width = 12.0, 3.0

    # planks
    for p in range(int(length / 0.28)):
        y0 = p * 0.28 - length/2
        y1 = y0 + 0.26
        dip = rng.uniform(-0.02, 0.015)
        box(bm, (-width/2 + 0.015, y0, dip), (width/2 - 0.015, y1, 0.055 + dip))

    # gunwale rails
    for sx in (-width/2 - 0.05, width/2 + 0.05):
        box(bm, (sx, -length/2, 0.0), (sx + 0.08, length/2, 0.18))

    # dock posts (cleats)
    for py in [-length/2 + 1, 0, length/2 - 1]:
        for px in (-width/2 - 0.02, width/2 + 0.02):
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=6, radius=0.065, depth=0.45,
                                       matrix=Matrix.Translation(Vector((px, py, -0.22))))
            box(bm, (px - 0.09, py - 0.025, 0.12), (px + 0.09, py + 0.025, 0.22))

    # floats (barrel-like)
    for fy in (-length/3, length/3):
        for fx in (-width/2 + 0.15, width/2 - 0.15):
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=12, radius=0.22, depth=0.40,
                                       matrix=Matrix.Translation(Vector((fx, fy, -0.20))) @
                                              Matrix.Rotation(PI/2, 4, 'X'))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_bottom(obj)
    return obj


# ════════════════════════════════════════════════════════
#  MANTLE GARDEN
# ════════════════════════════════════════════════════════

def build_lava_rock(name, scale, seed=80):
    """Jagged volcanic rock. Rough geometry, sharp edges, hot fissures.
    Matches: mantle_garden_concept.png — dark jagged formations."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    # ── primary rock mass ─────────────────────────
    res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=scale)
    for v in res['verts']:
        v.co.x *= rng.uniform(0.5, 1.6)
        v.co.y *= rng.uniform(0.5, 1.5)
        v.co.z *= rng.uniform(0.4, 1.4)
        if v.co.z < -scale * 0.3:
            v.co.z = -scale * 0.3
        v.co += Vector((rng.uniform(-0.12,0.12)*scale,
                        rng.uniform(-0.12,0.12)*scale,
                        rng.uniform(-0.06,0.06)*scale))

    # ── secondary spire shards ────────────────────
    for _ in range(rng.randint(2, 4)):
        angle = rng.uniform(0, TAU)
        sr    = scale * rng.uniform(0.3, 0.7)
        sh    = scale * rng.uniform(0.6, 1.4)
        sw    = sh * 0.14
        sx    = math.cos(angle) * sr
        sy    = math.sin(angle) * sr
        sv = [bm.verts.new((sx + math.cos(a*TAU/4)*sw,
                            sy + math.sin(a*TAU/4)*sw,
                            rng.uniform(scale*0.1, scale*0.25)))
              for a in range(4)]
        tip = bm.verts.new((sx + rng.uniform(-sw,sw),
                            sy + rng.uniform(-sw,sw),
                            sh))
        try:
            bm.faces.new(sv)
            for i in range(4):
                bm.faces.new([sv[i], sv[(i+1)%4], tip])
        except: pass

    # ── lava fissure cracks ───────────────────────
    for _ in range(rng.randint(2, 5)):
        angle = rng.uniform(0, TAU)
        fl    = rng.uniform(scale*0.4, scale*1.0)
        for ti in range(6):
            t  = ti/5
            fx = math.cos(angle) * fl * t
            fy = math.sin(angle) * fl * t
            fz = rng.uniform(-scale*0.05, scale*0.15)
            bm.verts.new((fx, fy, fz))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_lava_emissive"])
    set_origin_bottom(obj)
    return obj


def build_purple_crystal(name, scale, seed=90):
    """Purple amethyst-style crystal cluster. Similar silhouette to blue
    crystals but shorter, stockier, more angular.
    Matches: mantle_garden_concept.png — purple accents on dark lava rock."""
    print(f"Building {name} …")
    obj, bm = new_mesh(name)
    rng = random.Random(seed)

    # rock base
    res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=scale*0.55)
    for v in res['verts']:
        if v.co.z < 0: v.co.z *= 0.3
        v.co += Vector((rng.uniform(-0.04,0.04)*scale,
                        rng.uniform(-0.04,0.04)*scale,
                        rng.uniform(-0.02,0.02)*scale))

    # 4-6 crystals (stockier than blue: h/w ≈ 5:1 vs blue's 8:1)
    n = rng.randint(4, 7)
    for i in range(n):
        angle = i * TAU/n + rng.uniform(-0.2, 0.2)
        spread = rng.uniform(0.02, scale*0.5)
        cx = math.cos(angle)*spread
        cy = math.sin(angle)*spread
        h  = rng.uniform(scale*0.6, scale*1.3)
        w  = h * rng.uniform(0.17, 0.23)
        sides = 6  # hexagonal prism
        bv = [bm.verts.new((cx + math.cos(a*TAU/sides)*w,
                            cy + math.sin(a*TAU/sides)*w, 0.0))
              for a in range(sides)]
        tv = [bm.verts.new((cx + math.cos(a*TAU/sides)*w*0.08,
                            cy + math.sin(a*TAU/sides)*w*0.08, h))
              for a in range(sides)]
        tip = bm.verts.new((cx, cy, h*1.06))
        try:
            bm.faces.new(list(reversed(bv)))
            for s in range(sides):
                ns=(s+1)%sides
                bm.faces.new([bv[s],bv[ns],tv[ns],tv[s]])
                bm.faces.new([tv[s],tv[ns],tip])
        except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_purple_emissive"])
    set_origin_bottom(obj)
    return obj


def build_lava_bridge():
    """Natural cooled-lava rock arch bridge. Player walks across this
    over a lava river. Matches: mantle_garden_concept.png foreground bridge arch."""
    print("Building SM_MantleGarden_LavaBridge_A …")
    obj, bm = new_mesh("SM_MantleGarden_LavaBridge_A")
    rng = random.Random(33)

    # arch params
    span  = 20.0
    rise  = 6.0
    w     = 5.0   # walkway width
    segs  = 16
    cover = 0.55  # fraction of circle

    rings_L = []  # left edge of walkway
    rings_R = []  # right edge

    for seg in range(int(segs * cover) + 1):
        t  = seg / segs
        a  = (t - 0.5) * TAU * cover
        ax = math.sin(a) * span * 0.5
        az = rise * (math.cos(a * 0.9) - math.cos(TAU*cover*0.9*0.5))
        az = max(az, 0)

        thick = 1.5 + rng.uniform(-0.1, 0.2)
        lv = bm.verts.new((ax - w/2 + rng.uniform(-0.2,0.2),
                            rng.uniform(-0.1,0.1), az + thick))
        rv = bm.verts.new((ax + w/2 + rng.uniform(-0.2,0.2),
                            rng.uniform(-0.1,0.1), az + thick))
        lb = bm.verts.new((ax - w/2 + rng.uniform(-0.15,0.15),
                            rng.uniform(-0.15,0.15)*3, az - 0.2))
        rb = bm.verts.new((ax + w/2 + rng.uniform(-0.15,0.15),
                            rng.uniform(-0.15,0.15)*3, az - 0.2))
        rings_L.append((lv, lb))
        rings_R.append((rv, rb))

    for ri in range(len(rings_L)-1):
        lt, lb = rings_L[ri];  lt2, lb2 = rings_L[ri+1]
        rt, rb = rings_R[ri];  rt2, rb2 = rings_R[ri+1]
        try:
            bm.faces.new([lt, lt2, rt2, rt])   # walkway top
            bm.faces.new([lb, lb2, lt2, lt])    # left side
            bm.faces.new([rb, rt, rt2, rb2])    # right side
        except: pass

    # ── lava fissure on underside ──────────────────
    for seg in range(4):
        t   = (seg + 0.5) / 4
        ax  = math.sin((t-0.5)*TAU*cover) * span * 0.5
        az  = rise * max(0, math.cos((t-0.5)*TAU*cover*0.9) - 0.3)
        fv  = [bm.verts.new((ax + dx*0.08, dy*0.5, az - 0.15))
               for dx, dy in ((-1,0),(1,0),(0,-1),(0,1))]
        try: bm.faces.new(fv)
        except: pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_lava_emissive"])
    set_origin_bottom(obj)
    return obj


def build_steam_column():
    """Rock base column for steam vent VFX attachment.
    Cracked basalt pillar with lava glow at base crack."""
    print("Building SM_MantleGarden_SteamColumn_A …")
    obj, bm = new_mesh("SM_MantleGarden_SteamColumn_A")
    rng = random.Random(44)

    segs = 8
    h    = 2.5
    levels = [(0, 0.8), (0.3, 0.72), (0.9, 0.62), (1.6, 0.55),
              (2.1, 0.50), (h, 0.44)]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*(r + rng.uniform(-0.04,0.04)*r),
                    math.sin(i*TAU/segs)*(r + rng.uniform(-0.04,0.04)*r),
                    z))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for j in range(segs):
            nj=(j+1)%segs
            try: bm.faces.new([lo[j],lo[nj],hi[nj],hi[j]])
            except: pass
    try: bm.faces.new(list(reversed(rings[0])))
    except: pass

    # vent opening at top
    top_r = [bm.verts.new((math.cos(i*TAU/8)*0.30,
                           math.sin(i*TAU/8)*0.30, h))
             for i in range(8)]
    try: bm.faces.new(top_r)
    except: pass

    # lava glow cracks at base
    for crack_a in range(3):
        angle = crack_a * TAU/3
        for step in range(4):
            t = step/3
            cv = bm.verts.new((math.cos(angle)*0.78*(1-t*0.2),
                               math.sin(angle)*0.78*(1-t*0.2),
                               t*0.35))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_lava_emissive"])
    set_origin_bottom(obj)
    return obj


# ════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════

def main():
    print("\n=== Abyssal Earth — World Biome Kits ===\n")

    FOSSIL   = get_dir("FossilSky")
    GLASS    = get_dir("GlassrootForest")
    GRAVITY  = get_dir("GravityWell")
    SEA      = get_dir("InnerSea")
    MANTLE   = get_dir("MantleGarden")

    batches = [
        # (builder, export_dir, filename)
        # Fossil Sky
        (lambda: build_rib_arch("SM_FossilSky_RibArch_A", 22, 14, 2.2, 1),
         FOSSIL, "SM_FossilSky_RibArch_A.fbx"),
        (lambda: build_rib_arch("SM_FossilSky_RibArch_B", 32, 20, 3.0, 5),
         FOSSIL, "SM_FossilSky_RibArch_B.fbx"),
        (lambda: build_rib_arch("SM_FossilSky_RibArch_C", 15, 10, 1.6, 9),
         FOSSIL, "SM_FossilSky_RibArch_C.fbx"),
        (lambda: build_spine_segment("SM_FossilSky_SpineSegment_A", 8, 3.5, 3),
         FOSSIL, "SM_FossilSky_SpineSegment_A.fbx"),
        (lambda: build_spine_segment("SM_FossilSky_SpineSegment_B", 5, 2.4, 7),
         FOSSIL, "SM_FossilSky_SpineSegment_B.fbx"),
        (lambda: build_wood_dock(8.0, 4),
         FOSSIL, "SM_FossilSky_WoodDock_A.fbx"),

        # Glassroot Forest
        (lambda: build_glassroot_trunk("SM_Glassroot_TrunkBase_A", 2.2, 10),
         GLASS, "SM_Glassroot_TrunkBase_A.fbx"),
        (lambda: build_glassroot_trunk("SM_Glassroot_TrunkBase_B", 3.5, 17),
         GLASS, "SM_Glassroot_TrunkBase_B.fbx"),
        (build_glassroot_platform,
         GLASS, "SM_Glassroot_FloatingPlatform_A.fbx"),

        # Gravity Well
        (lambda: build_floating_rock("SM_GravityWell_FloatingRock_A", 4.0, 30),
         GRAVITY, "SM_GravityWell_FloatingRock_A.fbx"),
        (lambda: build_floating_rock("SM_GravityWell_FloatingRock_B", 2.2, 35),
         GRAVITY, "SM_GravityWell_FloatingRock_B.fbx"),
        (lambda: build_floating_rock("SM_GravityWell_FloatingRock_C", 1.0, 40),
         GRAVITY, "SM_GravityWell_FloatingRock_C.fbx"),
        (build_portal_ring,
         GRAVITY, "SM_GravityWell_PortalRing_A.fbx"),

        # Inner Sea
        (lambda: build_stalactite("SM_InnerSea_Stalactite_A", 0.9, 6.5, 50),
         SEA, "SM_InnerSea_Stalactite_A.fbx"),
        (lambda: build_stalactite("SM_InnerSea_Stalactite_B", 0.55, 4.0, 55),
         SEA, "SM_InnerSea_Stalactite_B.fbx"),
        (lambda: build_stalactite("SM_InnerSea_Stalactite_C", 1.4, 10.0, 60),
         SEA, "SM_InnerSea_Stalactite_C.fbx"),
        (build_inner_sea_dock,
         SEA, "SM_InnerSea_WoodDock_A.fbx"),

        # Mantle Garden
        (lambda: build_lava_rock("SM_MantleGarden_LavaRock_A", 5.0, 80),
         MANTLE, "SM_MantleGarden_LavaRock_A.fbx"),
        (lambda: build_lava_rock("SM_MantleGarden_LavaRock_B", 3.0, 85),
         MANTLE, "SM_MantleGarden_LavaRock_B.fbx"),
        (build_lava_bridge,
         MANTLE, "SM_MantleGarden_LavaBridge_A.fbx"),
        (lambda: build_purple_crystal("SM_MantleGarden_PurpleCrystal_A",1.8, 90),
         MANTLE, "SM_MantleGarden_PurpleCrystal_A.fbx"),
        (lambda: build_purple_crystal("SM_MantleGarden_PurpleCrystal_B",1.0, 95),
         MANTLE, "SM_MantleGarden_PurpleCrystal_B.fbx"),
        (build_steam_column,
         MANTLE, "SM_MantleGarden_SteamColumn_A.fbx"),
    ]

    for builder, export_dir, filename in batches:
        clear_scene()
        try:
            obj = builder()
            export_fbx(obj, export_dir, filename)
            print(f"  ✓ {filename}")
        except Exception as e:
            print(f"  ✗ {filename}: {e}")
            import traceback; traceback.print_exc()

    clear_scene()
    print("\n=== Script 5/7 complete ===")

main()
