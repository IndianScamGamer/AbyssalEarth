"""
gen_prologue_submarine.py  —  AbyssalEarth  Script 7/7
Generates modular submarine interior + elevator shaft kit.

All pieces tile together to build:
  - PRO_001 Submarine Interior (Bunk → Corridor → Engine → Airlock)
  - ACT1 / Later regions: crashed elevator shaft + mechanism

Export target: Content/ArtSourceExports/Prologue/
Export target: Content/ArtSourceExports/ElevatorShaft/

Run inside Blender >= 3.6:
  blender --background --python gen_prologue_submarine.py

All units: Blender metres → UE5 cm via global_scale=100.0
"""

import bpy
import bmesh
import math
import os
from mathutils import Matrix, Vector

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
PROLOGUE_DIR = os.path.join(REPO_ROOT, "Content", "ArtSourceExports", "Prologue")
ELEVATOR_DIR = os.path.join(REPO_ROOT, "Content", "ArtSourceExports", "ElevatorShaft")
for d in [PROLOGUE_DIR, ELEVATOR_DIR]:
    os.makedirs(d, exist_ok=True)


# ---------------------------------------------------------------------------
# Shared utils
# ---------------------------------------------------------------------------

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes) + list(bpy.data.materials):
        bpy.data.batch_remove(ids=[block])


def new_mesh(name):
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob, me


def finalise(ob, me, bm):
    bm.to_mesh(me)
    bm.free()
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)


def smart_uv(ob):
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')


def add_mat_slots(ob, slot_names):
    for name in slot_names:
        mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        ob.data.materials.append(mat)


def set_origin_to_base(ob):
    min_z = min((ob.matrix_world @ v.co).z for v in ob.data.vertices)
    bpy.context.scene.cursor.location = (0.0, 0.0, min_z)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    ob.location = (0, 0, 0)


def export_fbx(ob, export_dir, filename):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    path = os.path.join(export_dir, filename + ".fbx")
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        global_scale=100.0,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        mesh_smooth_type='FACE',
        bake_anim=False,
        axis_forward='-Z',
        axis_up='Y',
    )
    print(f"[gen_prologue_submarine] Exported {path}")


# ===========================================================================
# SUBMARINE INTERIOR KIT
# ===========================================================================

# ---------------------------------------------------------------------------
# SM_Sub_CorridorSection_Straight_A
#   Hollow tube: 3 m long × 3 m wide × 2.5 m tall.
#   Rounded rectangular cross-section (12-seg arch top).
#   Interior-facing normals. Bolt detail rings every 1 m.
# ---------------------------------------------------------------------------

def build_corridor_straight():
    clear_scene()
    ob, me = new_mesh("SM_Sub_CorridorSection_Straight_A")
    bm = bmesh.new()

    W, H, L = 1.5, 1.25, 3.0   # half-width, half-height, full length
    SEGS = 10                   # arch segments per side

    def profile_verts(bm_ref, z_off):
        """Generate cross-section verts at z_off: arch top + flat walls + flat floor."""
        verts = []
        # Left wall bottom
        verts.append(bm_ref.verts.new((-W, z_off, 0.0)))
        # Left arch
        for i in range(SEGS + 1):
            t = i / SEGS
            ang = math.radians(180 + t * 180)
            vx = math.cos(ang) * W
            vy = H + math.sin(ang) * H * 0.35
            verts.append(bm_ref.verts.new((vx, z_off, vy)))
        # Right wall bottom
        verts.append(bm_ref.verts.new((W, z_off, 0.0)))
        return verts

    front = profile_verts(bm, 0.0)
    back  = profile_verts(bm, L)
    bm.verts.ensure_lookup_table()

    n = len(front)
    # Side walls
    for i in range(n - 1):
        bm.faces.new([front[i], front[i + 1], back[i + 1], back[i]])
    # End caps
    bm.faces.new(front)
    bm.faces.new(list(reversed(back)))
    # Floor
    bm.faces.new([front[0], back[0], back[-1], front[-1]])

    # Bolt rings at 0.5 m intervals
    for ring_z in [0.5, 1.0, 1.5, 2.0, 2.5]:
        for i, v in enumerate(front):
            lv = bm.verts.new(v.co + Vector((0, ring_z, 0)))
            rv = bm.verts.new(v.co + Vector((0.015 * (1 if v.co.x > 0 else -1),
                                              ring_z, 0.015)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, PROLOGUE_DIR, "SM_Sub_CorridorSection_Straight_A")


# ---------------------------------------------------------------------------
# SM_Sub_CorridorSection_Corner_A
#   90° L-bend corridor. Two 2 m arms meeting at rounded interior corner.
# ---------------------------------------------------------------------------

def build_corridor_corner():
    clear_scene()
    ob, me = new_mesh("SM_Sub_CorridorSection_Corner_A")
    bm = bmesh.new()

    W, H = 1.4, 1.2
    ARM = 2.0  # arm length

    # Arm along +Y (forward)
    for z in [0.0, ARM]:
        for (x, y) in [(-W, z), (W, z)]:
            bm.verts.new((x, y, 0))
            bm.verts.new((x, y, H))

    # Arm along +X (right)
    for x in [ARM, ARM + ARM]:
        for (xi, y) in [(x, 0), (x, W)]:
            bm.verts.new((xi, y, 0))
            bm.verts.new((xi, y, H))

    # Connect with simple quads (simplified box corridors)
    bm.verts.ensure_lookup_table()
    v = bm.verts

    # Y-arm floor & ceiling quad
    bm.faces.new([v[0], v[2], v[6], v[4]])   # floor
    bm.faces.new([v[1], v[3], v[7], v[5]])   # ceiling
    # Left wall
    bm.faces.new([v[0], v[1], v[5], v[4]])
    # Right wall segment
    bm.faces.new([v[2], v[3], v[7], v[6]])

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, PROLOGUE_DIR, "SM_Sub_CorridorSection_Corner_A")


# ---------------------------------------------------------------------------
# SM_Sub_BulkheadDoor_A
#   Oval pressure door in frame.  Frame is 2.4 × 2.8 m wall segment.
#   Door oval: 1.0 × 1.8 m. Locking wheel handle. Hinge bolts.
# ---------------------------------------------------------------------------

def build_bulkhead_door():
    clear_scene()
    ob, me = new_mesh("SM_Sub_BulkheadDoor_A")
    bm = bmesh.new()

    # Frame wall panel
    for corner in [(-1.2, 0), (1.2, 0), (1.2, 2.8), (-1.2, 2.8)]:
        bm.verts.new((corner[0], 0.0, corner[1]))
        bm.verts.new((corner[0], 0.06, corner[1]))
    bm.verts.ensure_lookup_table()
    v = bm.verts
    bm.faces.new([v[0], v[2], v[4], v[6]])   # front face
    bm.faces.new([v[1], v[3], v[5], v[7]])   # back face
    bm.faces.new([v[0], v[1], v[3], v[2]])   # bottom
    bm.faces.new([v[4], v[5], v[7], v[6]])   # top
    bm.faces.new([v[0], v[1], v[5], v[4]])   # left
    bm.faces.new([v[2], v[3], v[7], v[6]])   # right

    # Door oval (12 segs)
    SEGS = 14
    for i in range(SEGS):
        ang = math.radians(i * 360 / SEGS)
        x = math.cos(ang) * 0.52
        z = math.sin(ang) * 0.90 + 1.10  # centred at z=1.1
        bm.verts.new((x, -0.04, z))
        bm.verts.new((x, -0.10, z))
    bm.verts.ensure_lookup_table()
    # Door faces
    base = 16
    for i in range(SEGS):
        ni = (i + 1) % SEGS
        bm.faces.new([v[base + i*2], v[base + i*2 + 1],
                       v[base + ni*2 + 1], v[base + ni*2]])

    # Wheel handle
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=12, radius1=0.28, radius2=0.28,
                               depth=0.04,
                               matrix=Matrix.Translation((0, -0.14, 1.10)))
    # Spokes
    for i in range(4):
        ang = math.radians(i * 45)
        sx = math.cos(ang) * 0.22
        sz = math.sin(ang) * 0.22
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=4, radius1=0.018, radius2=0.018,
                                   depth=0.44,
                                   matrix=Matrix.Translation((0, -0.16, 1.10))
                                   @ Matrix.Rotation(ang, 4, 'Y'))

    # Hinge bolts
    for bz in [0.35, 1.10, 1.85]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.04,
                                    matrix=Matrix.Translation((-0.56, -0.10, bz)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, PROLOGUE_DIR, "SM_Sub_BulkheadDoor_A")


# ---------------------------------------------------------------------------
# SM_Sub_BunkRoom_Shell_A
#   Room shell: 5 × 4 × 2.5 m box, no floor (sits on ground).
#   Interior bunk alcoves each side (2 per side, stacked).
#   Riveted panel detail on walls.
# ---------------------------------------------------------------------------

def build_bunk_room():
    clear_scene()
    ob, me = new_mesh("SM_Sub_BunkRoom_Shell_A")
    bm = bmesh.new()

    W, D, H = 2.5, 4.0, 2.5

    # Outer shell (open-top box for interior)
    verts_box = [
        bm.verts.new((-W, 0, 0)),    # 0
        bm.verts.new(( W, 0, 0)),    # 1
        bm.verts.new(( W, D, 0)),    # 2
        bm.verts.new((-W, D, 0)),    # 3
        bm.verts.new((-W, 0, H)),    # 4
        bm.verts.new(( W, 0, H)),    # 5
        bm.verts.new(( W, D, H)),    # 6
        bm.verts.new((-W, D, H)),    # 7
    ]
    bm.faces.new([verts_box[0], verts_box[1], verts_box[2], verts_box[3]])  # floor
    bm.faces.new([verts_box[4], verts_box[5], verts_box[6], verts_box[7]])  # ceiling
    bm.faces.new([verts_box[0], verts_box[1], verts_box[5], verts_box[4]])  # front
    bm.faces.new([verts_box[2], verts_box[3], verts_box[7], verts_box[6]])  # back
    bm.faces.new([verts_box[0], verts_box[3], verts_box[7], verts_box[4]])  # left
    bm.faces.new([verts_box[1], verts_box[2], verts_box[6], verts_box[5]])  # right

    # Bunk alcoves left wall
    for row in range(2):
        bz = 0.30 + row * 1.10
        bmesh.ops.create_cube(bm, size=0.8,
                               matrix=Matrix.Translation((-W + 0.45, D * 0.3 + row * 0.2, bz + 0.4))
                               @ Matrix.Scale(1.05, 4, (0, 1, 0))
                               @ Matrix.Scale(0.28, 4, (1, 0, 0))
                               @ Matrix.Scale(0.55, 4, (0, 0, 1)))
        bmesh.ops.create_cube(bm, size=0.8,
                               matrix=Matrix.Translation((-W + 0.45, D * 0.65 - row * 0.2, bz + 0.4))
                               @ Matrix.Scale(1.05, 4, (0, 1, 0))
                               @ Matrix.Scale(0.28, 4, (1, 0, 0))
                               @ Matrix.Scale(0.55, 4, (0, 0, 1)))

    # Riveted panel lines — horizontal strips
    for i in range(5):
        strip_z = 0.5 * (i + 1)
        bmesh.ops.create_cube(bm, size=0.04,
                               matrix=Matrix.Translation((0, D * 0.5, strip_z))
                               @ Matrix.Scale(W * 2 / 0.04, 4, (1, 0, 0))
                               @ Matrix.Scale(0.5, 4, (0, 0, 1)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, PROLOGUE_DIR, "SM_Sub_BunkRoom_Shell_A")


# ---------------------------------------------------------------------------
# SM_Sub_EngineRoom_Shell_A
#   6 × 6 × 3.5 m.  Central engine block (2 turbine cylinders side by side).
#   Conduit bundles on ceiling. Pressure gauge array.
# ---------------------------------------------------------------------------

def build_engine_room():
    clear_scene()
    ob, me = new_mesh("SM_Sub_EngineRoom_Shell_A")
    bm = bmesh.new()

    W, D, H = 3.0, 6.0, 3.5

    # Room shell
    for corner, is_top in [
        ((-W, 0, 0), False), ((W, 0, 0), False),
        ((W, D, 0), False), ((-W, D, 0), False),
        ((-W, 0, H), True), ((W, 0, H), True),
        ((W, D, H), True), ((-W, D, H), True),
    ]:
        bm.verts.new(corner)

    bm.verts.ensure_lookup_table()
    v = bm.verts
    bm.faces.new([v[0], v[1], v[2], v[3]])   # floor
    bm.faces.new([v[4], v[5], v[6], v[7]])   # ceiling
    bm.faces.new([v[0], v[1], v[5], v[4]])   # front
    bm.faces.new([v[2], v[3], v[7], v[6]])   # back
    bm.faces.new([v[0], v[3], v[7], v[4]])   # left
    bm.faces.new([v[1], v[2], v[6], v[5]])   # right

    # Engine turbines
    for side in [-0.9, 0.9]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=16, radius1=0.55, radius2=0.55,
                                   depth=2.0,
                                   matrix=Matrix.Translation((side, D * 0.45, 1.0))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))
        # Turbine front intake cowl
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=16, radius1=0.65, radius2=0.45,
                                   depth=0.35,
                                   matrix=Matrix.Translation((side, D * 0.45 - 1.17, 1.0))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))
        # Turbine exhaust port
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=12, radius1=0.40, radius2=0.55,
                                   depth=0.28,
                                   matrix=Matrix.Translation((side, D * 0.45 + 1.14, 1.0))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Central drive shaft
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius1=0.12, radius2=0.12,
                               depth=D * 0.7,
                               matrix=Matrix.Translation((0, D * 0.45, 0.65))
                               @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Conduit bundle ceiling
    for cx in [-1.5, -0.5, 0.5, 1.5]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius1=0.06, radius2=0.06,
                                   depth=D,
                                   matrix=Matrix.Translation((cx, D * 0.5, H - 0.20))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Pressure gauge array panel
    bmesh.ops.create_cube(bm, size=1.0,
                           matrix=Matrix.Translation((0, 0.06, 1.8))
                           @ Matrix.Scale(2.4, 4, (1, 0, 0))
                           @ Matrix.Scale(0.06, 4, (0, 1, 0))
                           @ Matrix.Scale(1.2, 4, (0, 0, 1)))
    for gx in [-0.80, -0.26, 0.26, 0.80]:
        for gz in [1.3, 1.85]:
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=12, radius1=0.10, radius2=0.10,
                                       depth=0.05,
                                       matrix=Matrix.Translation((gx, 0.10, gz)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt", "mat_gold_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, PROLOGUE_DIR, "SM_Sub_EngineRoom_Shell_A")


# ---------------------------------------------------------------------------
# SM_Sub_AirlockChamber_A
#   4 × 4 × 3 m octagonal room with outer hatch (open bottom for water entry).
#   Inner door frame + outer circular hatch ring. Warning stripes on floor.
# ---------------------------------------------------------------------------

def build_airlock():
    clear_scene()
    ob, me = new_mesh("SM_Sub_AirlockChamber_A")
    bm = bmesh.new()

    R = 2.0   # inscribed radius
    H = 3.0
    SEGS = 8

    for z in [0.0, H]:
        for i in range(SEGS):
            ang = math.radians(i * 360 / SEGS + 22.5)
            bm.verts.new((math.cos(ang) * R, math.sin(ang) * R, z))

    bm.verts.ensure_lookup_table()
    v = bm.verts
    # Walls
    for i in range(SEGS):
        ni = (i + 1) % SEGS
        bm.faces.new([v[i], v[ni], v[SEGS + ni], v[SEGS + i]])
    # Ceiling
    ceil_verts = [v[SEGS + i] for i in range(SEGS)]
    bm.faces.new(ceil_verts)

    # Outer hatch ring
    bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                               segments=20, radius1=0.82, radius2=0.82,
                               depth=0.12,
                               matrix=Matrix.Translation((0, -R + 0.05, 0.80)))
    # Hatch dogs (locking lugs)
    for i in range(6):
        ang = math.radians(i * 60)
        bmesh.ops.create_cube(bm, size=0.08,
                               matrix=Matrix.Translation(
                                   (math.cos(ang) * 0.90, -R + 0.05 + math.sin(ang) * 0.90, 0.80))
                               @ Matrix.Scale(0.5, 4, (0, 0, 1)))

    # Warning stripe ring on floor
    bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                               segments=20, radius1=1.65, radius2=1.65,
                               depth=0.02,
                               matrix=Matrix.Translation((0, 0, 0.01)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, PROLOGUE_DIR, "SM_Sub_AirlockChamber_A")


# ---------------------------------------------------------------------------
# SM_Sub_DecorPipes_Bundle_A   (4 m straight pipe bundle)
# ---------------------------------------------------------------------------

def build_pipe_bundle():
    clear_scene()
    ob, me = new_mesh("SM_Sub_DecorPipes_Bundle_A")
    bm = bmesh.new()

    layout = [(-0.08, 0.00, 0.055), (0.08, 0.00, 0.055),
              (0.00, -0.08, 0.055), (0.00, 0.08, 0.055),
              (-0.04, -0.04, 0.035)]

    for px, py, pr in layout:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=pr, radius2=pr,
                                   depth=4.0,
                                   matrix=Matrix.Translation((px, py, 2.0))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Clamp bands every 1 m
    for cz in [0.5, 1.5, 2.5, 3.5]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                                   segments=10, radius1=0.145, radius2=0.145,
                                   depth=0.06,
                                   matrix=Matrix.Translation((0, 0, cz)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, PROLOGUE_DIR, "SM_Sub_DecorPipes_Bundle_A")


# ===========================================================================
# ELEVATOR SHAFT KIT
# ===========================================================================

# ---------------------------------------------------------------------------
# SM_Elevator_ShaftSection_A   (10 m shaft segment, square 4 × 4 m interior)
#   Guide rail channels on all 4 walls, cable run on back wall,
#   grating floor panel, bolt rings every 2 m.
# ---------------------------------------------------------------------------

def build_shaft_section():
    clear_scene()
    ob, me = new_mesh("SM_Elevator_ShaftSection_A")
    bm = bmesh.new()

    W = 2.0   # half-width
    H = 10.0

    # Four walls
    walls = [
        ((-W, -W), (W, -W)),   # front
        ((W, -W),  (W,  W)),   # right
        ((W,  W),  (-W, W)),   # back
        ((-W, W),  (-W, -W)),  # left
    ]
    for (ax, ay), (bx, by) in walls:
        v0 = bm.verts.new((ax, ay, 0))
        v1 = bm.verts.new((bx, by, 0))
        v2 = bm.verts.new((bx, by, H))
        v3 = bm.verts.new((ax, ay, H))
        bm.faces.new([v0, v1, v2, v3])

    # Guide rail channels (front-left and front-right)
    for rx in [-W + 0.15, W - 0.15]:
        bmesh.ops.create_cube(bm, size=0.10,
                               matrix=Matrix.Translation((rx, -W, H * 0.5))
                               @ Matrix.Scale(0.6, 4, (1, 0, 0))
                               @ Matrix.Scale(H / 0.10, 4, (0, 0, 1)))

    # Cable run — back wall
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=6, radius1=0.045, radius2=0.045,
                               depth=H,
                               matrix=Matrix.Translation((0, W - 0.12, H * 0.5)))

    # Bolt rings
    for bz in [0.0, 2.5, 5.0, 7.5, 10.0]:
        for (ax, ay), (bx, by) in walls:
            v0 = bm.verts.new((ax * 1.015, ay * 1.015, bz))
            v1 = bm.verts.new((bx * 1.015, by * 1.015, bz))
            v2 = bm.verts.new((bx * 1.015, by * 1.015, bz + 0.06))
            v3 = bm.verts.new((ax * 1.015, ay * 1.015, bz + 0.06))
            bm.faces.new([v0, v1, v2, v3])

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_ancient_machine_dark", "mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, ELEVATOR_DIR, "SM_Elevator_ShaftSection_A")


# ---------------------------------------------------------------------------
# SM_Elevator_Car_A  (the elevator cabin, 3.5 × 3.5 × 3 m)
#   Open top, three solid walls, one grate front.
#   Floor: diamond-plate pattern. Speed indicator panel.
# ---------------------------------------------------------------------------

def build_elevator_car():
    clear_scene()
    ob, me = new_mesh("SM_Elevator_Car_A")
    bm = bmesh.new()

    W, D, H = 1.75, 1.75, 3.0

    # Floor
    bm.faces.new([bm.verts.new(c) for c in
                   [(-W, -D, 0), (W, -D, 0), (W, D, 0), (-W, D, 0)]])
    # Three solid walls
    for ax, ay, bx, by in [
        (-W, -D, W, -D),   # front (grate) — solid placeholder
        (W, -D,  W,  D),   # right
        (-W, D, -W, -D),   # left
    ]:
        v0 = bm.verts.new((ax, ay, 0))
        v1 = bm.verts.new((bx, by, 0))
        v2 = bm.verts.new((bx, by, H))
        v3 = bm.verts.new((ax, ay, H))
        bm.faces.new([v0, v1, v2, v3])
    # Back wall
    v0 = bm.verts.new((-W, D, 0))
    v1 = bm.verts.new(( W, D, 0))
    v2 = bm.verts.new(( W, D, H))
    v3 = bm.verts.new((-W, D, H))
    bm.faces.new([v0, v1, v2, v3])

    # Diamond plate rows on floor
    for row in range(6):
        for col in range(6):
            cx = -W + 0.28 + col * 0.50
            cy = -D + 0.28 + row * 0.55
            bmesh.ops.create_cube(bm, size=0.10,
                                   matrix=Matrix.Translation((cx, cy, 0.02))
                                   @ Matrix.Rotation(math.radians(45), 4, 'Z')
                                   @ Matrix.Scale(0.20, 4, (0, 0, 1)))

    # Grate front (4×3 grid of openings as bars)
    for gx in range(5):
        bmesh.ops.create_cube(bm, size=0.08,
                               matrix=Matrix.Translation((-W + 0.35 + gx * 0.70, -D, H * 0.5))
                               @ Matrix.Scale(0.25, 4, (1, 0, 0))
                               @ Matrix.Scale(H / 0.08, 4, (0, 0, 1)))

    # Speed indicator panel
    bmesh.ops.create_cube(bm, size=0.35,
                           matrix=Matrix.Translation((W - 0.18, D - 0.04, 1.5))
                           @ Matrix.Scale(0.5, 4, (1, 0, 0))
                           @ Matrix.Scale(0.10, 4, (0, 1, 0))
                           @ Matrix.Scale(1.2, 4, (0, 0, 1)))
    # LED depth counter strip
    bmesh.ops.create_cube(bm, size=0.12,
                           matrix=Matrix.Translation((W - 0.18, D - 0.08, 1.5))
                           @ Matrix.Scale(0.35, 4, (1, 0, 0))
                           @ Matrix.Scale(0.04, 4, (0, 1, 0))
                           @ Matrix.Scale(0.6, 4, (0, 0, 1)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_ancient_machine_dark", "mat_gold_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, ELEVATOR_DIR, "SM_Elevator_Car_A")


# ---------------------------------------------------------------------------
# SM_Elevator_CrashedCar_A   (same cabin, crumpled lower half)
# ---------------------------------------------------------------------------

def build_crashed_car():
    clear_scene()
    ob, me = new_mesh("SM_Elevator_CrashedCar_A")
    bm = bmesh.new()

    W, D, H = 1.75, 1.75, 3.0

    # Intact upper half
    for ax, ay, bx, by in [
        (-W, -D, W, -D),
        (W, -D,  W,  D),
        (-W, D, -W, -D),
    ]:
        v0 = bm.verts.new((ax, ay, H * 0.5))
        v1 = bm.verts.new((bx, by, H * 0.5))
        v2 = bm.verts.new((bx, by, H))
        v3 = bm.verts.new((ax, ay, H))
        bm.faces.new([v0, v1, v2, v3])

    # Crumpled lower half — irregular verts
    import random
    random.seed(42)
    for ax, ay, bx, by in [
        (-W, -D, W, -D),
        (W, -D,  W,  D),
        (-W, D, -W, -D),
    ]:
        for step in range(5):
            t = step / 4.0
            t2 = (step + 1) / 4.0
            rx1 = random.uniform(-0.15, 0.15)
            rz1 = random.uniform(-0.08, 0.08)
            rx2 = random.uniform(-0.15, 0.15)
            rz2 = random.uniform(-0.08, 0.08)
            v0 = bm.verts.new((ax + (bx - ax) * t + rx1, ay + (by - ay) * t + rx1, H * 0.5 * t + rz1))
            v1 = bm.verts.new((ax + (bx - ax) * t2 + rx2, ay + (by - ay) * t2 + rx2, H * 0.5 * t2 + rz2))
            v2 = bm.verts.new((ax + (bx - ax) * t2 + rx2, ay + (by - ay) * t2 + rx2, H * 0.5 * (t2 - 0.25) + rz2))
            v3 = bm.verts.new((ax + (bx - ax) * t + rx1, ay + (by - ay) * t + rx1, H * 0.5 * (t - 0.25) + rz1))
            try:
                bm.faces.new([v0, v1, v2, v3])
            except Exception:
                pass

    # Debris slab (floor panel broken, tilted)
    bmesh.ops.create_cube(bm, size=1.0,
                           matrix=Matrix.Translation((0.3, 0.2, 0.15))
                           @ Matrix.Rotation(math.radians(22), 4, 'X')
                           @ Matrix.Rotation(math.radians(15), 4, 'Z')
                           @ Matrix.Scale(W * 1.4, 4, (1, 0, 0))
                           @ Matrix.Scale(D * 1.4, 4, (0, 1, 0))
                           @ Matrix.Scale(0.08, 4, (0, 0, 1)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_wet_basalt"])
    set_origin_to_base(ob)
    export_fbx(ob, ELEVATOR_DIR, "SM_Elevator_CrashedCar_A")


# ---------------------------------------------------------------------------
# SM_Elevator_Mechanism_A
#   Large counterweight + pulley block at top of shaft, 6 × 6 × 4 m.
#   Ancient machine aesthetic: arched frame, huge gear wheels, chain loops.
# ---------------------------------------------------------------------------

def build_elevator_mechanism():
    clear_scene()
    ob, me = new_mesh("SM_Elevator_Mechanism_A")
    bm = bmesh.new()

    # Structural arch frame (two vertical pillars + cross beam)
    for sx in [-2.2, 2.2]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.22, radius2=0.22,
                                   depth=4.0,
                                   matrix=Matrix.Translation((sx, 0, 2.0)))
    # Cross beam
    bmesh.ops.create_cube(bm, size=0.40,
                           matrix=Matrix.Translation((0, 0, 4.20))
                           @ Matrix.Scale(4.4 / 0.40, 4, (1, 0, 0))
                           @ Matrix.Scale(0.8, 4, (0, 1, 0)))

    # Two large gear wheels
    for gx in [-1.2, 1.2]:
        GEAR_SEGS = 16
        for i in range(GEAR_SEGS):
            ang = math.radians(i * 360 / GEAR_SEGS)
            next_ang = math.radians((i + 1) * 360 / GEAR_SEGS)
            bmesh.ops.create_cube(bm, size=0.18,
                                   matrix=Matrix.Translation(
                                       (gx + math.cos(ang) * 0.72,
                                        math.sin(ang) * 0.12,
                                        3.50 + math.sin(ang) * 0.72))
                                   @ Matrix.Rotation(ang, 4, 'X')
                                   @ Matrix.Scale(0.5, 4, (0, 1, 0))
                                   @ Matrix.Scale(2.0, 4, (0, 0, 1)))
        # Gear hub
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=16, radius1=0.60, radius2=0.60,
                                   depth=0.18,
                                   matrix=Matrix.Translation((gx, 0, 3.50))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.18, radius2=0.18,
                                   depth=0.24,
                                   matrix=Matrix.Translation((gx, 0, 3.50))
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Counterweight block
    bmesh.ops.create_cube(bm, size=1.0,
                           matrix=Matrix.Translation((0, -1.60, 1.80))
                           @ Matrix.Scale(1.4, 4, (1, 0, 0))
                           @ Matrix.Scale(0.80, 4, (0, 1, 0))
                           @ Matrix.Scale(2.2, 4, (0, 0, 1)))
    # Weight detail bands
    for wz in [0.70, 1.20, 1.70, 2.20, 2.70]:
        bmesh.ops.create_cube(bm, size=0.05,
                               matrix=Matrix.Translation((0, -1.60, wz))
                               @ Matrix.Scale(1.5 / 0.05, 4, (1, 0, 0))
                               @ Matrix.Scale(0.85 / 0.05, 4, (0, 1, 0)))

    # Cable (twin cylinders from counterweight to gears)
    for cx in [-0.30, 0.30]:
        bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                                   segments=5, radius1=0.025, radius2=0.025,
                                   depth=2.60,
                                   matrix=Matrix.Translation((cx, -1.60, 3.10)))

    # Ancient machine emissive nodes on beam
    for nx in [-1.8, -0.6, 0.6, 1.8]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.09,
                                    matrix=Matrix.Translation((nx, 0, 4.28)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_ancient_machine_dark", "mat_gold_emissive", "mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, ELEVATOR_DIR, "SM_Elevator_Mechanism_A")


# ---------------------------------------------------------------------------
# SM_Elevator_ShaftDebris_A   (rubble pile + bent rail section)
# ---------------------------------------------------------------------------

def build_shaft_debris():
    clear_scene()
    ob, me = new_mesh("SM_Elevator_ShaftDebris_A")
    bm = bmesh.new()

    import random
    random.seed(77)

    # Rock chunks
    for i in range(8):
        px = random.uniform(-1.2, 1.2)
        py = random.uniform(-1.2, 1.2)
        rs = random.uniform(0.15, 0.45)
        result = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=rs,
                                             matrix=Matrix.Translation((px, py, rs * 0.5)))
        for v in result['verts']:
            v.co += Vector((random.uniform(-0.05, 0.05),
                            random.uniform(-0.05, 0.05),
                            random.uniform(-0.04, 0.04)))

    # Bent rail section
    for i in range(8):
        t = i / 7.0
        seg_x = -1.0 + t * 2.0
        seg_z = math.sin(t * math.pi) * 0.4 + 0.05
        bmesh.ops.create_cube(bm, size=0.08,
                               matrix=Matrix.Translation((seg_x, 0, seg_z))
                               @ Matrix.Scale(0.35, 4, (1, 0, 0))
                               @ Matrix.Scale(0.5, 4, (0, 0, 1)))

    # Torn cable coil
    CABLE_SEGS = 12
    for i in range(CABLE_SEGS):
        t = i / (CABLE_SEGS - 1)
        ang = t * math.pi * 3
        cx = math.cos(ang) * (0.35 - t * 0.1)
        cy = math.sin(ang) * (0.35 - t * 0.1)
        cz = t * 0.5
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius1=0.022, radius2=0.022,
                                   depth=0.18,
                                   matrix=Matrix.Translation((cx, cy, cz)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_wet_basalt", "mat_human_equipment"])
    set_origin_to_base(ob)
    export_fbx(ob, ELEVATOR_DIR, "SM_Elevator_ShaftDebris_A")


# ===========================================================================
# Main
# ===========================================================================

if __name__ == "__main__":
    print("=== gen_prologue_submarine.py ===")

    print("[Sub 1/6] SM_Sub_CorridorSection_Straight_A ...")
    build_corridor_straight()

    print("[Sub 2/6] SM_Sub_CorridorSection_Corner_A ...")
    build_corridor_corner()

    print("[Sub 3/6] SM_Sub_BulkheadDoor_A ...")
    build_bulkhead_door()

    print("[Sub 4/6] SM_Sub_BunkRoom_Shell_A ...")
    build_bunk_room()

    print("[Sub 5/6] SM_Sub_EngineRoom_Shell_A ...")
    build_engine_room()

    print("[Sub 6/6] SM_Sub_AirlockChamber_A ...")
    build_airlock()

    print("[Sub Decor] SM_Sub_DecorPipes_Bundle_A ...")
    build_pipe_bundle()

    print("[Elev 1/4] SM_Elevator_ShaftSection_A ...")
    build_shaft_section()

    print("[Elev 2/4] SM_Elevator_Car_A ...")
    build_elevator_car()

    print("[Elev 3/4] SM_Elevator_CrashedCar_A ...")
    build_crashed_car()

    print("[Elev 4/4] SM_Elevator_Mechanism_A ...")
    build_elevator_mechanism()

    print("[Elev Debris] SM_Elevator_ShaftDebris_A ...")
    build_shaft_debris()

    print("=== gen_prologue_submarine.py COMPLETE ===")
    print(f"Prologue → {PROLOGUE_DIR}")
    print(f"Elevator → {ELEVATOR_DIR}")
