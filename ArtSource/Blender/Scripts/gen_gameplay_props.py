"""
Abyssal Earth — Gameplay Props Generator
Script 1/7: Slice-critical interactive actors

Run in Blender 4.x Scripting tab. Each mesh is exported as a separate FBX
into Content/ArtSourceExports/Slice/.

Assets generated:
  SM_FabricatorStation_A     - Ancient hex crafting station
  SM_InterfaceTerminal_A     - Ancient wall-mounted interface
  SM_HarvestableNode_S/M/L   - Blue crystal harvestable nodes (3 sizes)
  SM_Beacon_A                - Deployable expedition beacon stake
  SM_CheckpointActor_A       - Checkpoint pylon
  SM_SteamVent_A             - Steam vent floor grate + pipe stub
  SM_MagmaGeyser_A           - Volcanic geyser cone
  SM_HeliosRobot_Static       - Helios robot (slim humanoid, static placeholder)
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

# ──────────────────────────────────────────────
# CONFIG — adjust EXPORT_ROOT to your repo path
# ──────────────────────────────────────────────
EXPORT_ROOT = os.path.join(os.path.dirname(bpy.data.filepath), "..", "..", "..",
                           "Content", "ArtSourceExports", "Slice")
EXPORT_ROOT = os.path.normpath(EXPORT_ROOT)
os.makedirs(EXPORT_ROOT, exist_ok=True)

TAU = math.tau
PI  = math.pi


# ══════════════════════════════════════════════
#  UTILITY HELPERS
# ══════════════════════════════════════════════

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
    for name in names:
        if name not in bpy.data.materials:
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = mat_color(name)
        obj.data.materials.append(bpy.data.materials[name])

def mat_color(name):
    palette = {
        "mat_ancient_machine_dark": (0.05, 0.05, 0.06, 1),
        "mat_gold_emissive":        (1.0,  0.72, 0.1,  1),
        "mat_blue_emissive":        (0.05, 0.45, 1.0,  1),
        "mat_crystal_blue":         (0.1,  0.6,  1.0,  1),
        "mat_wet_basalt":           (0.08, 0.08, 0.09, 1),
        "mat_human_equipment":      (0.18, 0.16, 0.14, 1),
        "mat_orb_energy":           (0.4,  0.8,  1.0,  1),
        "mat_amber_emissive":       (1.0,  0.5,  0.05, 1),
        "mat_lava_emissive":        (1.0,  0.25, 0.0,  1),
    }
    return palette.get(name, (0.5, 0.5, 0.5, 1))

def set_origin_to_base(obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    # move cursor to bottom of bounds
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
        filepath=path,
        use_selection=True,
        global_scale=100.0,          # Blender meters → UE5 cm
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        mesh_smooth_type='FACE',
        use_mesh_modifiers=True,
        bake_anim=False,
    )
    print(f"  Exported: {path}")

def add_subdivision(obj, levels=1):
    mod = obj.modifiers.new("Subsurf", 'SUBSURF')
    mod.levels = levels
    mod.render_levels = levels

def extrude_region(bm, faces, dist, direction=None):
    if direction is None:
        direction = faces[0].normal.copy()
    geom = bmesh.ops.extrude_face_region(bm, geom=faces)
    verts = [e for e in geom['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts, vec=direction * dist)
    return [f for f in geom['geom'] if isinstance(f, bmesh.types.BMFace)]


# ══════════════════════════════════════════════
#  1. FABRICATOR STATION
# ══════════════════════════════════════════════
# Ancient circular crafting station. Heavy circular base, raised hex
# plinth at centre, 6 equidistant radial arms with node tips.
# Matches: ancient_fabricator_concept.png + ancient_terminal_concept.png

def build_fabricator():
    print("Building SM_FabricatorStation_A …")
    obj, bm = new_mesh("SM_FabricatorStation_A")

    # ── base disc ────────────────────────────────
    base_verts = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                          segments=32, radius=1.1)
    base_faces = [f for f in bm.faces if len(f.verts) > 4]
    extrude_region(bm, base_faces, 0.06, Vector((0, 0, -1)))
    extrude_region(bm, base_faces, 0.04)

    # ── inner recessed groove ring ────────────────
    groove = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                      segments=32, radius=0.9)
    gf = [f for f in bm.faces if f.calc_center_median().z > 0.08
          and f.calc_center_median().length < 0.95]
    bmesh.ops.translate(bm, verts=groove['verts'], vec=Vector((0, 0, 0.04)))

    # ── raised central hex plinth ──────────────────
    hex_verts = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                         segments=6, radius=0.42)
    bmesh.ops.translate(bm, verts=hex_verts['verts'], vec=Vector((0, 0, 0.10)))
    hf = [f for f in bm.faces
          if all(abs(v.co.z - 0.10) < 0.01 for v in f.verts) and
          f.calc_center_median().length < 0.45]
    if hf:
        extrude_region(bm, hf, 0.30)
        # bevel top
        top_faces = [f for f in bm.faces
                     if all(abs(v.co.z - 0.40) < 0.01 for v in f.verts)
                     and f.calc_center_median().length < 0.45]

    # ── 6 radial arms ─────────────────────────────
    for i in range(6):
        angle = i * TAU / 6
        dx, dy = math.cos(angle), math.sin(angle)
        # arm box: thin rectangular prism
        arm_verts = []
        w, h, l = 0.06, 0.06, 0.58          # width, height, length
        for sx in (-1, 1):
            for sy in (-1, 1):
                for sz in (0, 1):
                    lx = dx * (0.42 + sz * l) - dy * sx * w
                    ly = dy * (0.42 + sz * l) + dx * sx * w
                    lz = 0.10 + sy * h
                    arm_verts.append(bm.verts.new((lx, ly, lz)))
        bm.verts.ensure_lookup_table()
        # faces: 6 faces of box (skip for brevity — build as loop)
        v = arm_verts
        faces_idx = [(0,1,3,2),(4,5,7,6),(0,4,6,2),(1,5,7,3),
                     (0,1,5,4),(2,3,7,6)]
        for fi in faces_idx:
            try:
                bm.faces.new([v[j] for j in fi])
            except Exception:
                pass

        # node at tip: small sphere approximation (ico)
        cx = dx * (0.42 + 0.58 + 0.09)
        cy = dy * (0.42 + 0.58 + 0.09)
        node_verts = bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.09,
            matrix=Matrix.Translation(Vector((cx, cy, 0.16))))['verts']

    # ── central orb socket ─────────────────────────
    orb = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.14,
                                      matrix=Matrix.Translation(
                                          Vector((0, 0, 0.50))))
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_gold_emissive",
                        "mat_blue_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  2. INTERFACE TERMINAL
# ══════════════════════════════════════════════
# Wall-mounted ancient terminal. Thick backplate, central circular display
# with radial petal geometry, 4 small control nodes at cardinal directions.
# Matches: ancient_terminal_concept.png

def build_terminal():
    print("Building SM_InterfaceTerminal_A …")
    obj, bm = new_mesh("SM_InterfaceTerminal_A")

    # ── backplate ─────────────────────────────────
    bmesh.ops.create_grid(bm, x_segments=4, y_segments=6, size=1.0)
    bm.verts.ensure_lookup_table()
    # select all faces and extrude back
    back_faces = list(bm.faces)
    extrude_region(bm, back_faces, 0.12, Vector((0, -1, 0)))

    # ── display circle ring ───────────────────────
    outer = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=24, radius=0.44)
    bmesh.ops.translate(bm, verts=outer['verts'], vec=Vector((0, 0.14, 0.10)))
    inner = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=24, radius=0.28)
    bmesh.ops.translate(bm, verts=inner['verts'], vec=Vector((0, 0.14, 0.10)))

    # ── 8 petal segments around display ──────────
    for i in range(8):
        angle = i * TAU / 8 + TAU / 16
        r_in, r_out = 0.30, 0.42
        a0, a1 = angle - TAU/24, angle + TAU/24
        pts = [
            (math.cos(a0)*r_in,  0.16, 0.10 + math.sin(a0)*r_in),
            (math.cos(a1)*r_in,  0.16, 0.10 + math.sin(a1)*r_in),
            (math.cos(a1)*r_out, 0.16, 0.10 + math.sin(a1)*r_out),
            (math.cos(a0)*r_out, 0.16, 0.10 + math.sin(a0)*r_out),
        ]
        face_verts = [bm.verts.new(p) for p in pts]
        bm.faces.new(face_verts)
        # extrude petal slightly
        extrude_region(bm, [bm.faces[-1]], 0.02)

    # ── 4 control nodes ───────────────────────────
    for a in (0, PI/2, PI, 3*PI/2):
        cx = math.cos(a) * 0.58
        cz = 0.10 + math.sin(a) * 0.58
        bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.055,
            matrix=Matrix.Translation(Vector((cx, 0.16, cz))))

    # ── gold ring bezel ────────────────────────────
    bezel = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=32, radius=0.46)
    bmesh.ops.translate(bm, verts=bezel['verts'], vec=Vector((0, 0.15, 0.10)))
    bm.faces.ensure_lookup_table()
    ring_faces = [f for f in bm.faces
                  if abs(f.calc_center_median().y - 0.15) < 0.01
                  and 0.43 < f.calc_center_median().xz.length < 0.47]
    if ring_faces:
        extrude_region(bm, ring_faces, 0.025)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_ancient_machine_dark", "mat_blue_emissive",
                        "mat_gold_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  3. HARVESTABLE CRYSTAL NODES
# ══════════════════════════════════════════════
# Three sizes: S (~50cm), M (~90cm), L (~140cm)
# Dark basalt rock base with angular faceted crystal spires.
# Matches: blue_crystal_harvestable_concept.png

def build_crystal_cluster(name, base_r, crystal_count, heights, rock_r):
    print(f"Building {name} …")
    obj, bm = new_mesh(name)

    # ── basalt rock base ──────────────────────────
    rock = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=rock_r)
    # flatten bottom
    for v in rock['verts']:
        if v.co.z < -rock_r * 0.4:
            v.co.z = -rock_r * 0.4
        elif v.co.z < 0:
            v.co.z *= 0.4
    # add some rocky asymmetry
    import random; random.seed(hash(name) % 999)
    for v in rock['verts']:
        v.co += Vector((random.uniform(-0.03, 0.03)*rock_r,
                        random.uniform(-0.03, 0.03)*rock_r,
                        random.uniform(-0.02, 0.02)*rock_r))

    # ── crystal spires ────────────────────────────
    for i in range(crystal_count):
        angle  = i * TAU / crystal_count + random.uniform(-0.2, 0.2)
        spread = random.uniform(0.05, base_r * 0.6)
        cx     = math.cos(angle) * spread
        cy     = math.sin(angle) * spread
        h      = heights[i % len(heights)] * random.uniform(0.85, 1.15)
        w      = h * random.uniform(0.12, 0.18)
        tilt   = Vector((random.uniform(-0.15,0.15), random.uniform(-0.15,0.15),1)).normalized()

        # crystal = tapered prism with 5 sides (pentagon cross-section)
        sides = 5
        base_pts, top_pts = [], []
        for s in range(sides):
            a2 = s * TAU / sides + random.uniform(-0.1, 0.1)
            bx = cx + math.cos(a2) * w
            by = cy + math.sin(a2) * w
            base_pts.append(bm.verts.new((bx, by, 0.0)))
            tx = cx + math.cos(a2) * w * 0.07 + tilt.x * h * 0.25
            ty = cy + math.sin(a2) * w * 0.07 + tilt.y * h * 0.25
            top_pts.append(bm.verts.new((tx, ty, h)))

        # tip
        tip = bm.verts.new((cx + tilt.x*h*0.1, cy + tilt.y*h*0.1, h*1.05))

        # build faces
        bm.faces.new(list(reversed(base_pts)))       # base cap
        for s in range(sides):
            ns = (s + 1) % sides
            bm.faces.new([base_pts[s], base_pts[ns],
                          top_pts[ns],  top_pts[s]])  # side quad
        for s in range(sides):
            ns = (s + 1) % sides
            bm.faces.new([top_pts[s], top_pts[ns], tip])  # tip tris

    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_crystal_blue", "mat_blue_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  4. DEPLOYABLE BEACON
# ══════════════════════════════════════════════
# Compact expedition stake. 50cm stake, ring light band at mid-point,
# small base disc with grip teeth, top emitter dome.
# Matches: Regenerated/Beacon/deployable_beacon_prop_concept.png

def build_beacon():
    print("Building SM_Beacon_A …")
    obj, bm = new_mesh("SM_Beacon_A")

    # ── main stake body ───────────────────────────
    stake = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=12, radius=0.025, depth=0.46)
    bmesh.ops.translate(bm, verts=stake['verts'], vec=Vector((0, 0, 0.23)))

    # ── pointed bottom spike ──────────────────────
    spike_base = [bm.verts.new((math.cos(a*TAU/8)*0.022,
                                math.sin(a*TAU/8)*0.022, 0.02))
                  for a in range(8)]
    spike_tip  = bm.verts.new((0, 0, -0.055))
    bm.faces.new(list(reversed(spike_base)))
    for i in range(8):
        bm.faces.new([spike_base[i], spike_base[(i+1)%8], spike_tip])

    # ── emissive light ring band ──────────────────
    ring_segs = 20
    for r_mult, z_off in [(1.0, 0.28), (1.0, 0.30)]:
        rv = [bm.verts.new((math.cos(a*TAU/ring_segs)*0.038*r_mult,
                            math.sin(a*TAU/ring_segs)*0.038*r_mult,
                            z_off))
              for a in range(ring_segs)]
        for i in range(ring_segs):
            pass   # ring verts exist; face bridging below

    ring_lo = [bm.verts.new((math.cos(a*TAU/16)*0.038,
                             math.sin(a*TAU/16)*0.038, 0.27))
               for a in range(16)]
    ring_hi = [bm.verts.new((math.cos(a*TAU/16)*0.038,
                             math.sin(a*TAU/16)*0.038, 0.31))
               for a in range(16)]
    for i in range(16):
        ni = (i+1)%16
        bm.faces.new([ring_lo[i], ring_lo[ni], ring_hi[ni], ring_hi[i]])

    # ── top emitter dome cap ──────────────────────
    cap = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035,
                                      matrix=Matrix.Translation(
                                          Vector((0, 0, 0.50))))
    # flatten bottom half of dome
    for v in cap['verts']:
        if v.co.z < 0.50:
            v.co.z = 0.50

    # ── base disc with grip notches ───────────────
    base_disc = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                         segments=8, radius=0.06)
    bmesh.ops.translate(bm, verts=base_disc['verts'],
                        vec=Vector((0, 0, 0.01)))
    base_f = [f for f in bm.faces
              if all(v.co.z < 0.02 for v in f.verts)
              and f.calc_center_median().length < 0.07]
    if base_f:
        extrude_region(bm, base_f, 0.015, Vector((0, 0, -1)))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  5. CHECKPOINT PYLON
# ══════════════════════════════════════════════
# 150cm exploration waypoint marker. Tapered octagonal pylon, wide at
# base, emissive ring band at 80cm, glowing disc top cap.

def build_checkpoint():
    print("Building SM_CheckpointActor_A …")
    obj, bm = new_mesh("SM_CheckpointActor_A")

    segs = 8
    # ── tapered pylon body (wider at base) ────────
    levels = [
        (0.00, 0.14),   # z, radius
        (0.05, 0.13),
        (0.10, 0.11),
        (0.80, 0.075),
        (1.40, 0.055),
        (1.48, 0.045),
    ]
    rings = []
    for z, r in levels:
        ring = [bm.verts.new((math.cos(i*TAU/segs)*r,
                              math.sin(i*TAU/segs)*r, z))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(segs):
            ni = (i+1)%segs
            bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])

    # base cap
    bm.faces.new(list(reversed(rings[0])))

    # ── emissive ring at 80cm ─────────────────────
    ring_z0, ring_z1 = 0.76, 0.84
    band_r = 0.085
    blo = [bm.verts.new((math.cos(i*TAU/16)*band_r,
                         math.sin(i*TAU/16)*band_r, ring_z0))
           for i in range(16)]
    bhi = [bm.verts.new((math.cos(i*TAU/16)*band_r,
                         math.sin(i*TAU/16)*band_r, ring_z1))
           for i in range(16)]
    for i in range(16):
        ni = (i+1)%16
        bm.faces.new([blo[i], blo[ni], bhi[ni], bhi[i]])

    # ── top disc cap ──────────────────────────────
    top = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                   segments=16, radius=0.06)
    bmesh.ops.translate(bm, verts=top['verts'], vec=Vector((0, 0, 1.48)))
    top_f = [f for f in bm.faces
             if all(abs(v.co.z - 1.48) < 0.01 for v in f.verts)
             and f.calc_center_median().length < 0.07]
    if top_f:
        extrude_region(bm, top_f, 0.018)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_blue_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  6. STEAM VENT
# ══════════════════════════════════════════════
# Floor grate 80cm diameter with square openings, short 20cm pipe stub.
# VFX from the BP handles the steam column.

def build_steam_vent():
    print("Building SM_SteamVent_A …")
    obj, bm = new_mesh("SM_SteamVent_A")

    # ── outer octagonal grate ring ────────────────
    outer = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                     segments=8, radius=0.42)
    bmesh.ops.translate(bm, verts=outer['verts'], vec=Vector((0, 0, 0.04)))
    of = [f for f in bm.faces if f.calc_center_median().length < 0.43
          and abs(f.calc_center_median().z - 0.04) < 0.01]
    if of:
        extrude_region(bm, of, 0.04, Vector((0, 0, -1)))

    # ── 4×4 square grate openings ─────────────────
    for gx in range(-1, 2):
        for gy in range(-1, 2):
            if abs(gx) + abs(gy) > 2:
                continue
            cx, cy = gx * 0.20, gy * 0.20
            hw = 0.065
            gv = [bm.verts.new((cx+dx*hw, cy+dy*hw, 0.04))
                  for dx, dy in ((-1,-1),(1,-1),(1,1),(-1,1))]
            bm.faces.new(gv)
            extrude_region(bm, [bm.faces[-1]], 0.05, Vector((0, 0, -1)))

    # ── central pipe stub ─────────────────────────
    pipe = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                      segments=10, radius=0.09, depth=0.20)
    bmesh.ops.translate(bm, verts=pipe['verts'], vec=Vector((0, 0, -0.20)))

    # ── bolted flange lip ─────────────────────────
    flange = bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False,
                                      segments=8, radius=0.14)
    bmesh.ops.translate(bm, verts=flange['verts'], vec=Vector((0, 0, 0.0)))
    ff = [f for f in bm.faces
          if all(abs(v.co.z) < 0.01 for v in f.verts)
          and f.calc_center_median().length < 0.15]
    if ff:
        extrude_region(bm, ff, 0.025)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  7. MAGMA GEYSER
# ══════════════════════════════════════════════
# Rocky cone ~180cm tall, split fissures on sides that glow lava-orange.
# VFX handles the eruption column.

def build_magma_geyser():
    print("Building SM_MagmaGeyser_A …")
    obj, bm = new_mesh("SM_MagmaGeyser_A")

    # ── main cone body ────────────────────────────
    segs = 10
    levels = [(0, 0.55), (0.2, 0.52), (0.5, 0.46), (0.85, 0.38),
              (1.1, 0.28), (1.4, 0.18), (1.75, 0.08), (1.82, 0.04)]
    rings = []
    import random; random.seed(12)
    for z, r in levels:
        ring = [bm.verts.new((
                    math.cos(i*TAU/segs)*r * random.uniform(0.88, 1.12),
                    math.sin(i*TAU/segs)*r * random.uniform(0.88, 1.12),
                    z + random.uniform(-0.03, 0.03)))
                for i in range(segs)]
        rings.append(ring)

    for ri in range(len(rings)-1):
        lo, hi = rings[ri], rings[ri+1]
        for i in range(segs):
            ni = (i+1)%segs
            bm.faces.new([lo[i], lo[ni], hi[ni], hi[i]])
    bm.faces.new(list(reversed(rings[0])))  # base cap

    # ── 3 fissure cracks (indented wedges) ────────
    for i in range(3):
        angle = i * TAU/3 + TAU/6
        for lvl_z, lvl_r in [(0.3, 0.50), (0.7, 0.42), (1.1, 0.30)]:
            crack_v = [
                bm.verts.new((
                    math.cos(angle + da) * (lvl_r - 0.04),
                    math.sin(angle + da) * (lvl_r - 0.04),
                    lvl_z + dz))
                for da, dz in ((-0.12, -0.05),(0.12, -0.05),(0.0, 0.08))
            ]
            bm.faces.new(crack_v)

    # ── vent opening at top ────────────────────────
    top_ring = [bm.verts.new((math.cos(i*TAU/8)*0.05,
                              math.sin(i*TAU/8)*0.05, 1.82))
                for i in range(8)]
    bm.faces.new(top_ring)

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_wet_basalt", "mat_lava_emissive"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  8. HELIOS ROBOT (STATIC MESH PLACEHOLDER)
# ══════════════════════════════════════════════
# Figure 03 inspired: smooth white humanoid, ~175cm. Oval black faceplate,
# black joints (shoulders/elbows/hips/knees), slim torso.
# Matches: helios_figure03_style_fullbody_concept.png

def build_helios_robot():
    print("Building SM_HeliosRobot_Static …")
    obj, bm = new_mesh("SM_HeliosRobot_Static")

    def sphere(cx, cy, cz, r, subdiv=1):
        return bmesh.ops.create_icosphere(
            bm, subdivisions=subdiv, radius=r,
            matrix=Matrix.Translation(Vector((cx, cy, cz))))['verts']

    def cyl(cx, cy, cz, r, h, segs=10):
        return bmesh.ops.create_cylinder(
            bm, cap_ends=True, cap_tris=False, segments=segs,
            radius=r, depth=h,
            matrix=Matrix.Translation(Vector((cx, cy, cz + h/2))))['verts']

    # ── pelvis ─────────────────────────────────────
    sphere(0, 0, 0.88, 0.12, 2)

    # ── torso ──────────────────────────────────────
    cyl(0, 0, 0.94, 0.16, 0.40)                    # lower torso
    cyl(0, 0, 1.32, 0.17, 0.14)                    # chest
    sphere(0, 0, 1.50, 0.155, 2)                   # shoulder yoke

    # ── neck + head ────────────────────────────────
    cyl(0, 0, 1.52, 0.04, 0.07)                    # neck
    sphere(0, 0, 1.64, 0.095, 2)                   # head
    # faceplate (oval inset — flattened sphere)
    fv = sphere(0.0, -0.10, 1.64, 0.070, 1)
    for v in fv:
        v.co.y += 0.04
        v.co.z = 1.64 + (v.co.z - 1.64) * 0.55    # squash

    # ── left arm ──────────────────────────────────
    sphere(-0.22, 0, 1.50, 0.055)                  # shoulder joint (black)
    cyl(-0.22, 0, 1.20, 0.042, 0.30)               # upper arm
    sphere(-0.22, 0, 1.18, 0.048)                  # elbow joint (black)
    cyl(-0.22, 0, 0.90, 0.036, 0.28)               # lower arm
    sphere(-0.22, 0, 0.88, 0.04)                   # wrist
    cyl(-0.22, 0, 0.76, 0.035, 0.12, 8)            # hand

    # ── right arm (mirror) ─────────────────────────
    sphere(0.22, 0, 1.50, 0.055)
    cyl(0.22, 0, 1.20, 0.042, 0.30)
    sphere(0.22, 0, 1.18, 0.048)
    cyl(0.22, 0, 0.90, 0.036, 0.28)
    sphere(0.22, 0, 0.88, 0.04)
    cyl(0.22, 0, 0.76, 0.035, 0.12, 8)

    # ── left leg ──────────────────────────────────
    sphere(-0.10, 0, 0.88, 0.052)                  # hip joint
    cyl(-0.10, 0, 0.56, 0.055, 0.32)               # thigh
    sphere(-0.10, 0, 0.54, 0.052)                  # knee
    cyl(-0.10, 0, 0.24, 0.046, 0.30)               # shin
    # foot
    fv = [bm.verts.new((-0.10 + dx*0.05, dy*0.04, 0.04))
          for dx in (-1.4, -0.4, 0.6, 1.0) for dy in (-1, 1)]
    bm.faces.new([fv[0],fv[2],fv[4],fv[6]])
    bm.faces.new([fv[1],fv[3],fv[5],fv[7]])

    # ── right leg (mirror) ─────────────────────────
    sphere(0.10, 0, 0.88, 0.052)
    cyl(0.10, 0, 0.56, 0.055, 0.32)
    sphere(0.10, 0, 0.54, 0.052)
    cyl(0.10, 0, 0.24, 0.046, 0.30)
    rfv = [bm.verts.new((0.10 + dx*0.05, dy*0.04, 0.04))
           for dx in (-1.4, -0.4, 0.6, 1.0) for dy in (-1, 1)]
    bm.faces.new([rfv[0],rfv[2],rfv[4],rfv[6]])
    bm.faces.new([rfv[1],rfv[3],rfv[5],rfv[7]])

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, ["mat_human_equipment", "mat_ancient_machine_dark"])
    set_origin_to_base(obj)
    return obj


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════

def main():
    clear_scene()
    print(f"\n=== Abyssal Earth — Gameplay Props (export → {EXPORT_ROOT}) ===\n")

    assets = [
        (build_fabricator,    "SM_FabricatorStation_A.fbx"),
        (build_terminal,      "SM_InterfaceTerminal_A.fbx"),
        (lambda: build_crystal_cluster("SM_HarvestableNode_S", 0.18, 3,
                                       [0.28, 0.22, 0.32], 0.16),
                              "SM_HarvestableNode_S.fbx"),
        (lambda: build_crystal_cluster("SM_HarvestableNode_M", 0.28, 5,
                                       [0.55, 0.40, 0.65, 0.45, 0.50], 0.24),
                              "SM_HarvestableNode_M.fbx"),
        (lambda: build_crystal_cluster("SM_HarvestableNode_L", 0.40, 7,
                                       [0.90, 0.75, 1.05, 0.80, 0.70, 0.95, 0.85], 0.34),
                              "SM_HarvestableNode_L.fbx"),
        (build_beacon,        "SM_Beacon_A.fbx"),
        (build_checkpoint,    "SM_CheckpointActor_A.fbx"),
        (build_steam_vent,    "SM_SteamVent_A.fbx"),
        (build_magma_geyser,  "SM_MagmaGeyser_A.fbx"),
        (build_helios_robot,  "SM_HeliosRobot_Static.fbx"),
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
    print("\n=== Script 1/7 complete ===")

main()
