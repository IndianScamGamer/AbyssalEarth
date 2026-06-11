"""
gen_characters.py  —  AbyssalEarth  Script 6/7
Generates character placeholder meshes: protagonist diver, Helios robot (detailed),
rift creature silhouettes, and collectible item meshes.

Export targets
  Content/ArtSourceExports/Characters/

Run inside Blender >= 3.6 (bpy):
  blender --background --python gen_characters.py

All units are in Blender metres; scale 100× on export → UE5 cm.
"""

import bpy
import bmesh
import math
import os
from mathutils import Matrix, Vector

# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

EXPORT_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))),
    "Content", "ArtSourceExports", "Characters"
)
os.makedirs(EXPORT_BASE, exist_ok=True)


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


def export_fbx(ob, filename):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    path = os.path.join(EXPORT_BASE, filename + ".fbx")
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
    print(f"[gen_characters] Exported {path}")


# ---------------------------------------------------------------------------
# 1. Protagonist Diver  —  SM_Diver_Protagonist_A
#    Full-body humanoid ~1.80 m tall. Inspired by concept art diver silhouette:
#    dive suit with shoulder tanks, wide visor helmet, utility belt, fin boots.
# ---------------------------------------------------------------------------

def build_diver():
    clear_scene()
    ob, me = new_mesh("SM_Diver_Protagonist_A")
    bm = bmesh.new()

    def add_cyl(r, h, segs, mat_i, z_offset=0.0, cap=True):
        bmesh.ops.create_cylinder(
            bm,
            cap_ends=cap,
            cap_tris=False,
            segments=segs,
            radius1=r,
            radius2=r * 0.85,
            depth=h,
            matrix=Matrix.Translation((0, 0, z_offset + h * 0.5)),
        )
        top = sorted(bm.verts, key=lambda v: v.co.z, reverse=True)[:segs * 2]
        return top

    def add_sphere(r, segs, z_off):
        result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r,
                                            matrix=Matrix.Translation((0, 0, z_off)))
        for v in result['verts']:
            v.co.z += 0
        return result['verts']

    # Legs (two cylinders offset laterally)
    for side in [-1, 1]:
        mat = Matrix.Translation((side * 0.14, 0, 0))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=10, radius1=0.085, radius2=0.07,
                                   depth=0.55, matrix=mat @ Matrix.Translation((0, 0, 0.275)))
        # Fin boot
        boot_mat = mat @ Matrix.Translation((0, 0.05, 0.10))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.10, radius2=0.08,
                                   depth=0.20, matrix=boot_mat)

    # Torso
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=12, radius1=0.175, radius2=0.16,
                               depth=0.52, matrix=Matrix.Translation((0, 0, 0.83)))

    # Shoulder tank pair
    for side in [-1, 1]:
        tank_mat = Matrix.Translation((side * 0.22, -0.08, 0.95))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.055, radius2=0.055,
                                   depth=0.36, matrix=tank_mat)

    # Arms
    for side in [-1, 1]:
        arm_mat = Matrix.Translation((side * 0.26, 0, 0.95))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.065, radius2=0.055,
                                   depth=0.42, matrix=arm_mat)
        # Glove
        glove_mat = Matrix.Translation((side * 0.26, 0, 0.72))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.06,
                                    matrix=glove_mat)

    # Neck
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius1=0.065, radius2=0.065,
                               depth=0.10, matrix=Matrix.Translation((0, 0, 1.12)))

    # Helmet (large sphere, visor notch)
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.165,
                                matrix=Matrix.Translation((0, 0, 1.31)))

    # Visor plate (flat disc forward)
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=12, radius1=0.10, radius2=0.10,
                               depth=0.03,
                               matrix=Matrix.Translation((0, 0.155, 1.31)))

    # Utility belt detail
    bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                               segments=14, radius1=0.18, radius2=0.18,
                               depth=0.06,
                               matrix=Matrix.Translation((0, 0, 0.73)))

    # Belt pouches
    for ang in [0, 60, -60, 180]:
        rad = math.radians(ang)
        px = 0.185 * math.sin(rad)
        py = 0.185 * math.cos(rad)
        bmesh.ops.create_cube(bm, size=0.07,
                               matrix=Matrix.Translation((px, py, 0.73)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_human_equipment", "mat_glass_bark"])
    set_origin_to_base(ob)
    export_fbx(ob, "SM_Diver_Protagonist_A")


# ---------------------------------------------------------------------------
# 2. Helios Robot — detailed  —  SM_HeliosRobot_Detailed_A
#    Humanoid AI ~1.85 m. Smooth-panelled form, oval glowing faceplate,
#    segmented limbs. Based on Figure 03 concept (sleek, non-threatening).
# ---------------------------------------------------------------------------

def build_helios_detailed():
    clear_scene()
    ob, me = new_mesh("SM_HeliosRobot_Detailed_A")
    bm = bmesh.new()

    # Legs
    for side in [-1, 1]:
        for seg_z, seg_r, seg_h in [(0.0, 0.09, 0.30), (0.32, 0.085, 0.28)]:
            mat = Matrix.Translation((side * 0.135, 0, seg_z + seg_h * 0.5))
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=10, radius1=seg_r, radius2=seg_r * 0.92,
                                       depth=seg_h, matrix=mat)
        # Foot block
        foot_mat = Matrix.Translation((side * 0.135, 0.03, 0.10))
        bmesh.ops.create_cube(bm, size=0.10,
                               matrix=foot_mat @ Matrix.Scale(1.0, 4, (1, 0, 0))
                               @ Matrix.Scale(0.55, 4, (0, 0, 1)))

    # Hip junction sphere
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.13,
                                matrix=Matrix.Translation((0, 0, 0.65)))

    # Torso — two tapered sections
    for z_off, r1, r2, h in [(0.65, 0.155, 0.18, 0.26), (0.91, 0.18, 0.155, 0.24)]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=12, radius1=r1, radius2=r2,
                                   depth=h, matrix=Matrix.Translation((0, 0, z_off + h * 0.5)))

    # Chest emissive panel
    bmesh.ops.create_cube(bm, size=0.12,
                           matrix=Matrix.Translation((0, 0.175, 1.0))
                           @ Matrix.Scale(1.4, 4, (1, 0, 0))
                           @ Matrix.Scale(0.18, 4, (0, 0, 1)))

    # Shoulder spheres
    for side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.075,
                                    matrix=Matrix.Translation((side * 0.245, 0, 1.13)))

    # Upper arms
    for side in [-1, 1]:
        for seg_z, seg_r, seg_h in [(0.78, 0.065, 0.25), (1.04, 0.058, 0.22)]:
            mat = Matrix.Translation((side * 0.295, 0, seg_z + seg_h * 0.5))
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=8, radius1=seg_r, radius2=seg_r * 0.90,
                                       depth=seg_h, matrix=mat)
        # Hand disc
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=8, radius1=0.06, radius2=0.06,
                                   depth=0.04,
                                   matrix=Matrix.Translation((side * 0.295, 0, 0.73)))

    # Neck cylinder
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius1=0.055, radius2=0.055,
                               depth=0.10, matrix=Matrix.Translation((0, 0, 1.19)))

    # Head — slightly flattened sphere
    head_r = 0.145
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=head_r,
                                         matrix=Matrix.Translation((0, 0, 1.365)))
    for v in result['verts']:
        if (v.co - Vector((0, 0, 1.365))).length < head_r + 0.001:
            v.co.y *= 0.78  # flatten front-back

    # Oval faceplate (forward)
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=14, radius1=0.09, radius2=0.09,
                               depth=0.025,
                               matrix=Matrix.Translation((0, 0.155, 1.365))
                               @ Matrix.Scale(0.7, 4, (1, 0, 0))
                               @ Matrix.Scale(1.15, 4, (0, 0, 1)))

    # Head side vents
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=0.05,
                               matrix=Matrix.Translation((side * 0.15, 0, 1.36))
                               @ Matrix.Scale(0.25, 4, (1, 0, 0))
                               @ Matrix.Scale(0.5, 4, (0, 0, 1)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_ancient_machine_dark", "mat_gold_emissive", "mat_blue_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, "SM_HeliosRobot_Detailed_A")


# ---------------------------------------------------------------------------
# 3. Rift Creature — Silhouette A  —  SM_RiftCreature_Silhouette_A
#    Long-bodied, 4 radial tentacle arms, central bioluminescent core.
#    Inspired by concept "rift_creature_silhouettes": fluid, deep-sea-like.
#    ~1.4 m long body + arm spans.
# ---------------------------------------------------------------------------

def build_rift_creature_a():
    clear_scene()
    ob, me = new_mesh("SM_RiftCreature_Silhouette_A")
    bm = bmesh.new()

    # Central body — elongated ellipsoid via scaled icosphere
    result = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=0.35,
                                         matrix=Matrix.Translation((0, 0, 0)))
    for v in result['verts']:
        v.co.z *= 2.2   # elongate vertically
        v.co.x *= 0.65
        v.co.y *= 0.65

    # Bioluminescent core orb (inner — will be separate slot)
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.12,
                                matrix=Matrix.Translation((0, 0, 0.05)))

    # 4 radial tentacle arms at 90° intervals
    for i in range(4):
        ang = math.radians(i * 90)
        cx = math.cos(ang) * 0.30
        cy = math.sin(ang) * 0.30
        # Arm root segment
        arm_mat = Matrix.Translation((cx * 0.6, cy * 0.6, 0.0))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=6, radius1=0.07, radius2=0.045,
                                   depth=0.40,
                                   matrix=arm_mat @ Matrix.Rotation(
                                       math.atan2(cy, cx), 4, 'Z')
                                   @ Matrix.Rotation(math.radians(90), 4, 'Y'))
        # Arm mid segment (angled down)
        mid_mat = Matrix.Translation((cx * 1.25, cy * 1.25, -0.15))
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius1=0.042, radius2=0.025,
                                   depth=0.38,
                                   matrix=mid_mat @ Matrix.Rotation(
                                       math.atan2(cy, cx), 4, 'Z')
                                   @ Matrix.Rotation(math.radians(80), 4, 'Y'))
        # Tip fingers (2 tapered)
        for j in [-1, 1]:
            tip_offset = Vector((cx * 1.95 + j * cy * 0.08,
                                  cy * 1.95 + j * cx * 0.08,
                                  -0.38))
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=4, radius1=0.020, radius2=0.004,
                                       depth=0.28,
                                       matrix=Matrix.Translation(tip_offset))

    # Head crest — fan of flat spines
    for i in range(5):
        ang = math.radians(-40 + i * 20)
        spine_x = math.sin(ang) * 0.22
        spine_z_top = 0.72 + 0.06 * math.cos(ang * 2)
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=3, radius1=0.012, radius2=0.002,
                                   depth=0.24,
                                   matrix=Matrix.Translation((spine_x, 0, spine_z_top))
                                   @ Matrix.Rotation(ang * 0.5, 4, 'Y'))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_water_bioluminescent", "mat_blue_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, "SM_RiftCreature_Silhouette_A")


# ---------------------------------------------------------------------------
# 4. Rift Creature — Silhouette B  —  SM_RiftCreature_Silhouette_B
#    Manta-like: broad flat mantle, twin trailing tails, upper ridge spines.
# ---------------------------------------------------------------------------

def build_rift_creature_b():
    clear_scene()
    ob, me = new_mesh("SM_RiftCreature_Silhouette_B")
    bm = bmesh.new()

    # Flat mantle — wide subdivided plane, extruded to give volume
    verts_raw = []
    for i in range(9):
        ang = math.radians(i * 40 - 160)  # 320° sweep leaving trailing gap
        r = 1.10 + 0.18 * math.cos(math.radians(i * 80))
        verts_raw.append(bm.verts.new((math.cos(ang) * r,
                                        math.sin(ang) * r * 0.42,
                                        0.0)))
    bm.verts.ensure_lookup_table()
    # Centre
    cv = bm.verts.new((0, 0, 0))
    for i in range(len(verts_raw) - 1):
        bm.faces.new([verts_raw[i], verts_raw[i + 1], cv])
    # Thicken via extrude
    for v in bm.verts:
        dup = bm.verts.new(v.co + Vector((0, 0, 0.12)))

    # Body ridge (dorsal spine row)
    for i in range(7):
        t = i / 6.0
        px = (t - 0.5) * 1.6
        pz = 0.18 + 0.12 * math.sin(math.pi * t)
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=3, radius1=0.025, radius2=0.005,
                                   depth=0.20,
                                   matrix=Matrix.Translation((px, 0, pz)))

    # Twin trailing tails
    for side in [-1, 1]:
        for seg, (tz, tr, tlen) in enumerate([(0, 0.055, 0.60), (-0.20, 0.040, 0.50), (-0.42, 0.020, 0.35)]):
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=6, radius1=tr, radius2=tr * 0.75,
                                       depth=tlen,
                                       matrix=Matrix.Translation(
                                           (side * 0.22, -1.05 - seg * 0.5, tz + tlen * 0.5 - 0.3)))

    # Cephalic lobes (head end)
    for side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.16,
                                    matrix=Matrix.Translation((side * 0.30, 0.85, 0.05)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_water_bioluminescent", "mat_purple_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, "SM_RiftCreature_Silhouette_B")


# ---------------------------------------------------------------------------
# 5. Rift Creature — Silhouette C  —  SM_RiftCreature_Silhouette_C
#    Vertical serpentine: coiled body column ~3 m tall, frilled neck collar.
# ---------------------------------------------------------------------------

def build_rift_creature_c():
    clear_scene()
    ob, me = new_mesh("SM_RiftCreature_Silhouette_C")
    bm = bmesh.new()

    # Spine helix — stack of spheres along sinusoidal path
    segments = 18
    for i in range(segments):
        t = i / (segments - 1)
        z = t * 2.8
        x = math.sin(t * math.pi * 2.5) * 0.18
        y = math.cos(t * math.pi * 2.5) * 0.12
        r = 0.14 - t * 0.06  # taper toward tail
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r,
                                    matrix=Matrix.Translation((x, y, z)))

    # Neck frill — ring of flat petals at z≈2.4
    frill_z = 2.40
    for i in range(8):
        ang = math.radians(i * 45)
        fx = math.cos(ang) * 0.28
        fy = math.sin(ang) * 0.28
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=4, radius1=0.03, radius2=0.005,
                                   depth=0.32,
                                   matrix=Matrix.Translation((fx, fy, frill_z + 0.16))
                                   @ Matrix.Rotation(ang, 4, 'Z')
                                   @ Matrix.Rotation(math.radians(90), 4, 'X'))

    # Head — elongated snout
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.18,
                                matrix=Matrix.Translation((0, 0, 2.95)))
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                               segments=8, radius1=0.06, radius2=0.03,
                               depth=0.30,
                               matrix=Matrix.Translation((0, 0.28, 2.95)))

    # Eye lights
    for side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.03,
                                    matrix=Matrix.Translation((side * 0.09, 0.16, 3.04)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_water_bioluminescent", "mat_blue_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, "SM_RiftCreature_Silhouette_C")


# ---------------------------------------------------------------------------
# 6. AbyssalCreature (patrol enemy)  —  SM_AbyssalCreature_Patrol_A
#    Crab/isopod hybrid: wide armoured carapace, 6 legs, two pincer arms,
#    head stalks with sensor orbs. Low to ground, ~1 m wide.
# ---------------------------------------------------------------------------

def build_abyssal_creature():
    clear_scene()
    ob, me = new_mesh("SM_AbyssalCreature_Patrol_A")
    bm = bmesh.new()

    # Carapace — scaled icosphere
    result = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.40,
                                         matrix=Matrix.Translation((0, 0, 0.25)))
    for v in result['verts']:
        v.co.x *= 1.35
        v.co.y *= 0.90
        v.co.z *= 0.58

    # Segmented abdomen plates (3 bands)
    for i in range(3):
        az = 0.12 + i * 0.06
        bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                                   segments=12, radius1=0.36 - i * 0.04,
                                   radius2=0.36 - i * 0.04,
                                   depth=0.03,
                                   matrix=Matrix.Translation((0, -0.20 - i * 0.12, az)))

    # 6 legs (3 per side)
    for side in [-1, 1]:
        for j in range(3):
            lx = side * 0.42
            ly = (j - 1) * 0.22
            # Upper segment
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=6, radius1=0.035, radius2=0.028,
                                       depth=0.28,
                                       matrix=Matrix.Translation(
                                           (lx + side * 0.12, ly, 0.22))
                                       @ Matrix.Rotation(math.radians(30 * side), 4, 'Z'))
            # Lower segment
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=5, radius1=0.025, radius2=0.015,
                                       depth=0.28,
                                       matrix=Matrix.Translation(
                                           (lx + side * 0.30, ly, 0.08))
                                       @ Matrix.Rotation(math.radians(-10 * side), 4, 'Z'))

    # Two pincer arms
    for side in [-1, 1]:
        # Arm
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=7, radius1=0.055, radius2=0.042,
                                   depth=0.45,
                                   matrix=Matrix.Translation(
                                       (side * 0.38, 0.32, 0.30))
                                   @ Matrix.Rotation(math.radians(20), 4, 'X'))
        # Pincer outer
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=4, radius1=0.04, radius2=0.008,
                                   depth=0.25,
                                   matrix=Matrix.Translation(
                                       (side * 0.40 + side * 0.05, 0.65, 0.38)))
        # Pincer inner (smaller)
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=4, radius1=0.030, radius2=0.005,
                                   depth=0.18,
                                   matrix=Matrix.Translation(
                                       (side * 0.40 - side * 0.04, 0.62, 0.35)))

    # Head stalks with sensor orbs
    for side in [-1, 1]:
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                   segments=5, radius1=0.018, radius2=0.015,
                                   depth=0.22,
                                   matrix=Matrix.Translation(
                                       (side * 0.12, 0.44, 0.42)))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.04,
                                    matrix=Matrix.Translation(
                                        (side * 0.12, 0.44, 0.58)))

    finalise(ob, me, bm)
    smart_uv(ob)
    add_mat_slots(ob, ["mat_wet_basalt", "mat_blue_emissive"])
    set_origin_to_base(ob)
    export_fbx(ob, "SM_AbyssalCreature_Patrol_A")


# ---------------------------------------------------------------------------
# 7. Collectible item meshes — small props spawned as world pickups
# ---------------------------------------------------------------------------

def build_collectible_items():
    """Batch: crystal shard, data chip, ancient coin, fabricator core."""

    items = [
        ("SM_Item_CrystalShard_A", "mat_crystal_blue"),
        ("SM_Item_DataChip_A",     "mat_human_equipment"),
        ("SM_Item_AncientCoin_A",  "mat_gold_emissive"),
        ("SM_Item_FabricatorCore_A","mat_blue_emissive"),
    ]

    for idx, (name, mat_name) in enumerate(items):
        clear_scene()
        ob, me = new_mesh(name)
        bm = bmesh.new()

        if "Crystal" in name:
            # Hexagonal prism shard — faceted top
            result = bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                                segments=6, radius1=0.06, radius2=0.015,
                                                depth=0.18,
                                                matrix=Matrix.Translation((0, 0, 0.09)))
            for v in bm.verts:
                if v.co.z > 0.12:
                    v.co.z += 0.05 * (v.co.z - 0.12) * 3

        elif "DataChip" in name:
            # Thin rectangular chip with notch
            bmesh.ops.create_cube(bm, size=0.10,
                                   matrix=Matrix.Scale(1.0, 4) @ Matrix.Translation((0, 0, 0.015))
                                   @ Matrix.Scale(0.12, 4, (0, 0, 1)))
            # Notch corner
            bmesh.ops.create_cube(bm, size=0.025,
                                   matrix=Matrix.Translation((0.04, 0.04, 0.015)))

        elif "AncientCoin" in name:
            # Disc with radial grooves
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False,
                                       segments=16, radius1=0.065, radius2=0.065,
                                       depth=0.012,
                                       matrix=Matrix.Translation((0, 0, 0.006)))
            # Inner ring detail
            bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                                       segments=16, radius1=0.042, radius2=0.042,
                                       depth=0.013,
                                       matrix=Matrix.Translation((0, 0, 0.006)))

        elif "FabricatorCore" in name:
            # Small dodecahedron-ish: scaled icosphere
            result = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.07,
                                                 matrix=Matrix.Translation((0, 0, 0.07)))
            # Equatorial band
            bmesh.ops.create_cylinder(bm, cap_ends=False, cap_tris=False,
                                       segments=12, radius1=0.075, radius2=0.075,
                                       depth=0.018,
                                       matrix=Matrix.Translation((0, 0, 0.07)))

        finalise(ob, me, bm)
        smart_uv(ob)
        add_mat_slots(ob, [mat_name])
        set_origin_to_base(ob)
        export_fbx(ob, name)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== gen_characters.py ===")

    print("[1/7] Building SM_Diver_Protagonist_A ...")
    build_diver()

    print("[2/7] Building SM_HeliosRobot_Detailed_A ...")
    build_helios_detailed()

    print("[3/7] Building SM_RiftCreature_Silhouette_A ...")
    build_rift_creature_a()

    print("[4/7] Building SM_RiftCreature_Silhouette_B ...")
    build_rift_creature_b()

    print("[5/7] Building SM_RiftCreature_Silhouette_C ...")
    build_rift_creature_c()

    print("[6/7] Building SM_AbyssalCreature_Patrol_A ...")
    build_abyssal_creature()

    print("[7/7] Building collectible item meshes ...")
    build_collectible_items()

    print("=== gen_characters.py COMPLETE ===")
    print(f"Output: {EXPORT_BASE}")
