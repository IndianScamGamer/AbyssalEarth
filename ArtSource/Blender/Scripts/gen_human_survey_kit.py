"""
Abyssal Earth — Human Survey Kit
Script 4/7: Field-gear expedition props

Run in Blender 4.x Scripting tab.
Exports to Content/ArtSourceExports/Slice/

Assets generated:
  SM_Human_SurveyPlatform_A    - 10×10m elevated survey platform
  SM_Human_SurveyCrate_A       - weathered metal storage crate
  SM_Human_PortableLamp_A      - cylindrical survey lamp (warm-tone)
  SM_Human_CableCoil_A         - cable drum on stand
  SM_Human_FieldConsole_A      - portable field computer terminal
  SM_Human_TemporaryRailing_A  - 3m modular safety railing segment
  SM_Human_TripodScanner_A     - collapsed survey tripod + scanner head
  SM_Human_BedrollBundle_A     - rolled sleeping mat and bag bundle

Art direction: Practical worn modern field gear.  Simple readable shapes.
Small cyan status LEDs.  Contrast with ancient alien surroundings.
Matches: expedition_crates_props_concept.png, AD-005, HE-001 through HE-005
"""

import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix

EXPORT_ROOT = os.path.join(os.path.dirname(bpy.data.filepath),
                           "..", "..", "..",
                           "Content", "ArtSourceExports", "Slice")
EXPORT_ROOT = os.path.normpath(EXPORT_ROOT)
os.makedirs(EXPORT_ROOT, exist_ok=True)

TAU = math.tau
PI  = math.pi


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
        "mat_human_equipment": (0.18, 0.16, 0.14, 1),
        "mat_blue_emissive":   (0.05, 0.40, 1.0,  1),
        "mat_amber_emissive":  (1.0,  0.55, 0.05, 1),
        "mat_wet_basalt":      (0.06, 0.06, 0.07, 1),
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

def box_from_corners(bm, min_pt, max_pt):
    x0,y0,z0 = min_pt
    x1,y1,z1 = max_pt
    verts = [
        bm.verts.new((x0,y0,z0)), bm.verts.new((x1,y0,z0)),
        bm.verts.new((x1,y1,z0)), bm.verts.new((x0,y1,z0)),
        bm.verts.new((x0,y0,z1)), bm.verts.new((x1,y0,z1)),
        bm.verts.new((x1,y1,z1)), bm.verts.new((x0,y1,z1)),
    ]
    faces = [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    for f in faces:
        try:
            bm.faces.new([verts[i] for i in f])
        except Exception:
            pass
    return verts


# ══════════════════════════════════════════════
#  1. SURVEY PLATFORM
# ══════════════════════════════════════════════
# 10×10m modular elevated platform. Grid of square deck panels,
# perimeter safety rail channel, 4 support legs with cross-braces.
# Matches: expedition atmosphere of HE-001 through HE-005.

def build_survey_platform():
    print("Building SM_Human_SurveyPlatform_A …")
    obj, bm = new_mesh("SM_Human_SurveyPlatform_A")
    rng = random.Random(3)

    plat_w = 10.0
    deck_h = 0.18
    leg_h  = 1.8

    # ── deck panels (3×3 grid) ─────────────────────
    panel_w = plat_w / 3
    for gx in range(3):
        for gy in range(3):
            x0 = (gx * panel_w - plat_w/2) + 0.02
            x1 = x0 + panel_w - 0.04
            y0 = (gy * panel_w - plat_w/2) + 0.02
            y1 = y0 + panel_w - 0.04
            box_from_corners(bm, (x0, y0, 0), (x1, y1, deck_h))
            # anti-slip groove lines on top
            for sl in range(4):
                sx = x0 + (sl+1) * panel_w/5
                sv = [bm.verts.new((sx, y0 + 0.02, deck_h)),
                      bm.verts.new((sx, y1 - 0.02, deck_h))]
                gv = [bm.verts.new((sx, y0 + 0.02, deck_h - 0.012)),
                      bm.verts.new((sx, y1 - 0.02, deck_h - 0.012))]
                try:
                    bm.faces.new([sv[0], sv[1], gv[1], gv[0]])
                except Exception:
                    pass

    # ── perimeter rail channel ─────────────────────
    half = plat_w * 0.5
    for sx, sy, ex, ey in [(-half, -half, half, -half),
                            (half,  -half, half, half),
                            (half,   half,-half,  half),
                            (-half,  half,-half, -half)]:
        rv = [bm.verts.new((sx - 0.06 * (1 if ey != -half else 0),
                            sy, deck_h + 0.02)),
              bm.verts.new((ex, ey, deck_h + 0.02)),
              bm.verts.new((ex, ey, deck_h + 1.05)),
              bm.verts.new((sx - 0.06 * (1 if ey != -half else 0),
                            sy, deck_h + 1.05))]
        # top rail bar
        for z_off in (deck_h + 0.02, deck_h + 1.05):
            bm.verts.new((sx, sy, z_off))

    # ── 4 support legs ─────────────────────────────
    for lx, ly in [(-4.2,-4.2),(4.2,-4.2),(4.2,4.2),(-4.2,4.2)]:
        leg_verts = bmesh.ops.create_cylinder(
            bm, cap_ends=True, cap_tris=False, segments=6,
            radius=0.14, depth=leg_h,
            matrix=Matrix.Translation(Vector((lx, ly, -leg_h/2))))
        # cross-braces to adjacent legs
        for sign in (-1, 1):
            brace_pts = [
                bm.verts.new((lx, ly, -leg_h * 0.3)),
                bm.verts.new((lx + sign * 8.4 * 0.5, ly, -leg_h * 0.7)),
            ]

    # ── anchor feet ────────────────────────────────
    for lx, ly in [(-4.2,-4.2),(4.2,-4.2),(4.2,4.2),(-4.2,4.2)]:
        foot = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                        segments=8, radius=0.28)
        bmesh.ops.translate(bm, verts=foot['verts'],
                            vec=Vector((lx, ly, -leg_h - 0.02)))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  2. SURVEY CRATE
# ══════════════════════════════════════════════
# Weathered metal storage crate with corner reinforcements,
# latch detail, and stencil emboss. Matches: expedition_crates_props_concept.png

def build_survey_crate():
    print("Building SM_Human_SurveyCrate_A …")
    obj, bm = new_mesh("SM_Human_SurveyCrate_A")
    rng = random.Random(7)

    # ── main body ─────────────────────────────────
    box_from_corners(bm, (-0.45, -0.30, 0), (0.45, 0.30, 0.32))

    # ── corner edge reinforcements ─────────────────
    corners = [(-0.45,-0.30),(0.45,-0.30),(0.45,0.30),(-0.45,0.30)]
    for cx, cy in corners:
        for z_range in [(0.0, 0.05), (0.27, 0.32)]:
            z0, z1 = z_range
            brace_w = 0.06
            # horizontal brace
            bx = cx + (brace_w if cx < 0 else -brace_w)
            by = cy + (brace_w if cy < 0 else -brace_w)
            box_from_corners(bm, (min(cx, bx), min(cy, by), z0),
                                 (max(cx, bx), max(cy, by), z1))

    # ── lid lip ───────────────────────────────────
    box_from_corners(bm, (-0.44,-0.29, 0.30), (0.44, 0.29, 0.34))

    # ── 2 latch details ───────────────────────────
    for lx in (-0.15, 0.15):
        box_from_corners(bm, (lx - 0.04, -0.32, 0.15),
                              (lx + 0.04, -0.31, 0.22))
        latch_arm = [bm.verts.new((lx - 0.025, -0.31, 0.15)),
                     bm.verts.new((lx + 0.025, -0.31, 0.15)),
                     bm.verts.new((lx + 0.025, -0.34, 0.17)),
                     bm.verts.new((lx - 0.025, -0.34, 0.17))]
        try:
            bm.faces.new(latch_arm)
        except Exception:
            pass

    # ── carry handle ──────────────────────────────
    for hx in (-0.18, 0.18):
        box_from_corners(bm, (hx - 0.02, -0.02, 0.34),
                              (hx + 0.02,  0.02, 0.40))
    box_from_corners(bm, (-0.18, -0.02, 0.38), (0.18, 0.02, 0.41))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  3. PORTABLE LAMP
# ══════════════════════════════════════════════
# Cylindrical survey lantern. 20cm dia × 30cm tall.
# Warm amber glow ring, weighted base, side cable connector.
# Matches: AD-005 (Human Survey Lamp — Close-Up).

def build_portable_lamp():
    print("Building SM_Human_PortableLamp_A …")
    obj, bm = new_mesh("SM_Human_PortableLamp_A")

    segs = 16

    # ── main cylinder body ────────────────────────
    body = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                      segments=segs, radius=0.10, depth=0.28,
                                      matrix=Matrix.Translation(Vector((0,0,0.14))))

    # ── weighted base disc ─────────────────────────
    base = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                      segments=segs, radius=0.13, depth=0.04,
                                      matrix=Matrix.Translation(Vector((0,0,0.02))))

    # ── amber glow ring band ──────────────────────
    ring_lo = [bm.verts.new((math.cos(i*TAU/segs)*0.105,
                             math.sin(i*TAU/segs)*0.105, 0.18))
               for i in range(segs)]
    ring_hi = [bm.verts.new((math.cos(i*TAU/segs)*0.105,
                             math.sin(i*TAU/segs)*0.105, 0.22))
               for i in range(segs)]
    for i in range(segs):
        ni=(i+1)%segs
        try:
            bm.faces.new([ring_lo[i], ring_lo[ni], ring_hi[ni], ring_hi[i]])
        except Exception:
            pass

    # ── top diffuser cap ──────────────────────────
    top_cap = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                         segments=segs, radius=0.08, depth=0.06,
                                         matrix=Matrix.Translation(Vector((0,0,0.31))))

    # ── side panel emboss ──────────────────────────
    box_from_corners(bm, (-0.055, 0.10, 0.08), (0.055, 0.104, 0.16))
    box_from_corners(bm, (-0.020, 0.10, 0.23), (0.020, 0.104, 0.27))

    # ── cable stub ────────────────────────────────
    cable_segs = 6
    cable_dir  = [bm.verts.new((0.10 + t*0.12,
                                -0.02 + math.sin(t*PI)*0.04,
                                0.10)) for t in [i/5 for i in range(6)]]

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive",
                        "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  4. CABLE COIL
# ══════════════════════════════════════════════
# Drum reel on a stand, partially unwound cable visible.
# Matches: expedition_crates_props_concept.png (cable reel item).

def build_cable_coil():
    print("Building SM_Human_CableCoil_A …")
    obj, bm = new_mesh("SM_Human_CableCoil_A")

    # ── stand frame ───────────────────────────────
    # 2 vertical posts
    for sx in (-0.28, 0.28):
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius=0.04, depth=0.55,
                                   matrix=Matrix.Translation(Vector((sx, 0, 0.275))))
    # horizontal axle
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius=0.035, depth=0.58,
                               matrix=Matrix.Translation(Vector((0, 0, 0.42))) @
                                      Matrix.Rotation(PI/2, 4, 'Y'))
    # base cross-bar
    box_from_corners(bm, (-0.32, -0.14, 0), (0.32, 0.14, 0.06))

    # ── drum ──────────────────────────────────────
    drum_r = 0.18
    for offset, r in [(0.0, drum_r), (0.0, drum_r * 1.25)]:
        disc = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                        segments=20, radius=r)
        for bv in (-0.26, 0.26):
            bmesh.ops.translate(bm, verts=disc['verts'],
                                vec=Vector((bv, 0, 0.42)))
            disc2 = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                             segments=20, radius=r)
            bmesh.ops.translate(bm, verts=disc2['verts'],
                                vec=Vector((bv + 0.04 if bv < 0 else bv - 0.04,
                                            0, 0.42)))

    # ── cable windings (helix tube) ────────────────
    n_coils = 8
    for t_i in range(n_coils * 12):
        t   = t_i / (n_coils * 12)
        angle = t * n_coils * TAU
        r_c = drum_r * 1.1
        cx  = r_c * math.cos(angle)
        cy  = r_c * math.sin(angle)
        cz  = 0.42 + (t - 0.5) * 0.45
        if abs(cz - 0.42) < 0.22:
            bm.verts.new((cx, cy, cz))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  5. FIELD CONSOLE
# ══════════════════════════════════════════════
# Portable rugged field computer. 1.5×0.8m form factor on folding legs.
# Angled keyboard area, raised screen section, cyan status strip.
# Matches: expedition_crates_props_concept.png console item.

def build_field_console():
    print("Building SM_Human_FieldConsole_A …")
    obj, bm = new_mesh("SM_Human_FieldConsole_A")

    # ── main chassis ──────────────────────────────
    box_from_corners(bm, (-0.70, -0.38, 0.68), (0.70, 0.38, 1.05))

    # ── angled keyboard tray ──────────────────────
    kbd_pts = [
        bm.verts.new((-0.65, -0.36, 0.68)),
        bm.verts.new(( 0.65, -0.36, 0.68)),
        bm.verts.new(( 0.65, -0.36, 0.72)),
        bm.verts.new((-0.65, -0.36, 0.72)),
        bm.verts.new((-0.65, 0.05, 0.84)),
        bm.verts.new(( 0.65, 0.05, 0.84)),
        bm.verts.new(( 0.65, 0.05, 0.88)),
        bm.verts.new((-0.65, 0.05, 0.88)),
    ]
    for fi in [(0,1,2,3),(4,5,6,7),(0,4,7,3),(1,5,4,0),(2,6,5,1),(3,7,6,2)]:
        try:
            bm.faces.new([kbd_pts[i] for i in fi])
        except Exception:
            pass

    # ── raised screen panel ───────────────────────
    box_from_corners(bm, (-0.62, 0.08, 0.88), (0.62, 0.10, 1.46))
    # screen face
    box_from_corners(bm, (-0.56, 0.09, 0.92), (0.56, 0.11, 1.42))

    # ── status LED strip ──────────────────────────
    box_from_corners(bm, (-0.60, -0.39, 0.70), (0.60, -0.38, 0.72))

    # ── 4 folding legs ────────────────────────────
    for lx, ly in [(-0.55, -0.30), (0.55, -0.30),
                   (0.55,  0.30),  (-0.55, 0.30)]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius=0.025, depth=0.68,
                                   matrix=Matrix.Translation(Vector((lx, ly, 0.34))))

    # ── rubber foot pads ──────────────────────────
    for lx, ly in [(-0.55,-0.30),(0.55,-0.30),(0.55,0.30),(-0.55,0.30)]:
        box_from_corners(bm, (lx-0.04, ly-0.04, 0), (lx+0.04, ly+0.04, 0.04))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  6. TEMPORARY RAILING
# ══════════════════════════════════════════════
# 3m modular safety railing segment. Two horizontal rails,
# vertical balusters every 60cm, end snap-connectors.
# Snaps end-to-end for arbitrary path lengths.

def build_railing():
    print("Building SM_Human_TemporaryRailing_A …")
    obj, bm = new_mesh("SM_Human_TemporaryRailing_A")

    length = 3.0
    height = 1.05
    post_r = 0.022

    # ── 2 end posts ────────────────────────────────
    for px in (0, length):
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius=post_r*1.4, depth=height,
                                   matrix=Matrix.Translation(Vector((px, 0, height/2))))
        # snap connector
        box_from_corners(bm, (px-0.04, -0.03, -0.04), (px+0.04, 0.03, 0.04))
        box_from_corners(bm, (px-0.04, -0.03, height-0.04), (px+0.04, 0.03, height+0.04))

    # ── 4 intermediate balusters ────────────────────
    for bx in (0.60, 1.20, 1.80, 2.40):
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius=post_r, depth=height,
                                   matrix=Matrix.Translation(Vector((bx, 0, height/2))))

    # ── 2 horizontal rail bars ──────────────────────
    for rz in (0.35, height):
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius=post_r, depth=length,
                                   matrix=Matrix.Translation(Vector((length/2, 0, rz))) @
                                          Matrix.Rotation(PI/2, 4, 'Y'))

    # ── reflective warning strip on top rail ───────
    box_from_corners(bm, (-0.01, -0.025, height-0.01),
                          (length+0.01, 0.025, height+0.01))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_amber_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  7. TRIPOD SCANNER
# ══════════════════════════════════════════════
# Survey tripod with box scanner head. Extended legs, cable tether.

def build_tripod():
    print("Building SM_Human_TripodScanner_A …")
    obj, bm = new_mesh("SM_Human_TripodScanner_A")

    leg_h = 1.30
    # ── 3 legs ────────────────────────────────────
    for i in range(3):
        angle = i * TAU/3
        tx = math.cos(angle) * 0.45
        ty = math.sin(angle) * 0.45
        # leg as thin box
        bv = [bm.verts.new((0, 0, leg_h)),
              bm.verts.new((tx, ty, 0.04))]
        # thin cylinder leg
        leg_dir = Vector((tx, ty, 0.04 - leg_h)).normalized()
        for j in range(8):
            pass  # simplified: just thin cylinder
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius=0.018, depth=leg_h,
                                   matrix=(Matrix.Translation(Vector((tx/2, ty/2, leg_h/2))) @
                                           Matrix.Rotation(-math.atan2(math.sqrt(tx**2+ty**2),
                                                                         leg_h-0.04), 4, 'X') @
                                           Matrix.Rotation(angle, 4, 'Z')))
        # foot
        box_from_corners(bm, (tx-0.06, ty-0.06, 0), (tx+0.06, ty+0.06, 0.04))

    # ── centre column ─────────────────────────────
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=6, radius=0.025, depth=0.40,
                               matrix=Matrix.Translation(Vector((0, 0, leg_h + 0.20))))

    # ── scanner head box ──────────────────────────
    box_from_corners(bm, (-0.14, -0.09, leg_h+0.38), (0.14, 0.09, leg_h+0.58))
    # optic lens
    bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                             segments=12, radius=0.06)
    for v in bm.verts:
        if abs(v.co.z) < 0.01 and v.co.length < 0.07:
            v.co.z = leg_h + 0.48
            v.co.y = 0.10

    # ── cyan status ring ──────────────────────────
    for status_z in (leg_h+0.40, leg_h+0.56):
        sv = [bm.verts.new((math.cos(a*TAU/12)*0.15,
                            math.sin(a*TAU/12)*0.09,
                            status_z))
              for a in range(12)]
        try:
            bm.faces.new(sv)
        except Exception:
            pass

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  8. BEDROLL BUNDLE
# ══════════════════════════════════════════════
# Rolled sleeping mat + bag strapped with webbing.

def build_bedroll():
    print("Building SM_Human_BedrollBundle_A …")
    obj, bm = new_mesh("SM_Human_BedrollBundle_A")

    # ── outer roll cylinder ────────────────────────
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=20, radius=0.16, depth=0.62,
                               matrix=Matrix.Translation(Vector((0, 0, 0.31))) @
                                      Matrix.Rotation(PI/2, 4, 'X'))

    # ── 3 webbing straps ───────────────────────────
    for sy in (-0.18, 0, 0.18):
        strap = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                         segments=20, radius=0.165)
        bmesh.ops.translate(bm, verts=strap['verts'], vec=Vector((0, sy, 0.31)))
        for sv in strap['verts']:
            sv.co.x *= 0.15   # flatten strap

    # ── compression bag attached on back ──────────
    box_from_corners(bm, (-0.08, 0.14, 0.14), (0.08, 0.28, 0.48))
    # buckle
    box_from_corners(bm, (-0.03, 0.27, 0.28), (0.03, 0.30, 0.34))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment"])
    set_origin_bottom(obj)
    return obj


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════

def main():
    clear_scene()
    print(f"\n=== Abyssal Earth — Human Survey Kit (→ {EXPORT_ROOT}) ===\n")

    assets = [
        (build_survey_platform, "SM_Human_SurveyPlatform_A.fbx"),
        (build_survey_crate,    "SM_Human_SurveyCrate_A.fbx"),
        (build_portable_lamp,   "SM_Human_PortableLamp_A.fbx"),
        (build_cable_coil,      "SM_Human_CableCoil_A.fbx"),
        (build_field_console,   "SM_Human_FieldConsole_A.fbx"),
        (build_railing,         "SM_Human_TemporaryRailing_A.fbx"),
        (build_tripod,          "SM_Human_TripodScanner_A.fbx"),
        (build_bedroll,         "SM_Human_BedrollBundle_A.fbx"),
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
    print("\n=== Script 4/7 complete ===")

main()
