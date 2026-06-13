"""
SM_HeliosRobot_Detailed_A — AbyssalEarth procedural mesh.
STANDALONE — no shared/ folder needed. Run from Blender text editor or:
  blender --background --python sm_helios_detailed.py

FBX exports to your Desktop in a folder called AbyssalEarth_FBX.
"""
import os
import math
import random
import bpy
import bmesh
from mathutils import Matrix, Vector

TAU = math.tau
PI  = math.pi

# --- Export destination (Desktop/AbyssalEarth_FBX) ---
EXPORT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "AbyssalEarth_FBX")
os.makedirs(EXPORT_DIR, exist_ok=True)

# ── inlined utils ────────────────────────────────────────────────────────────

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def new_mesh(name):
    mesh = bpy.data.meshes.new(name)
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm   = bmesh.new()
    return obj, bm


def finalise(obj, bm):
    bm.to_mesh(obj.data)
    bm.free()
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def smart_uv(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")


_MAT_COLORS = {
    "mat_ancient_machine_dark":      (0.05, 0.05, 0.06, 1),
    "mat_ancient_machine_edge_wear": (0.12, 0.11, 0.10, 1),
    "mat_gold_emissive":             (1.00, 0.72, 0.10, 1),
    "mat_blue_emissive":             (0.05, 0.45, 1.00, 1),
    "mat_collector_glass":           (0.60, 0.85, 1.00, 1),
    "mat_human_equipment":           (0.18, 0.16, 0.14, 1),
    "mat_pearl_stone":               (0.88, 0.85, 0.82, 1),
}

def add_mat_slots(obj, names):
    for name in names:
        col = _MAT_COLORS.get(name, (0.5, 0.5, 0.5, 1))
        if name not in bpy.data.materials:
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = col
        obj.data.materials.append(bpy.data.materials[name])


def set_origin_to_base(obj):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    min_z = min((obj.matrix_world @ v.co).z for v in obj.data.vertices)
    bpy.context.scene.cursor.location = (obj.location.x, obj.location.y, min_z)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    obj.location = (0, 0, 0)


def export_fbx(obj, export_dir, filename):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = os.path.join(export_dir, filename + ".fbx")
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        global_scale=100.0,
        apply_unit_scale=True,
        apply_scale_options="FBX_SCALE_ALL",
        mesh_smooth_type="FACE",
        use_mesh_modifiers=True,
        bake_anim=False,
    )
    print(f"  [export] {path}")


# ── build ────────────────────────────────────────────────────────────────────

def build():
    """Helios android — 1.75m humanoid robot, white shell + gold joints + blue visor."""
    random.seed(42)
    obj, bm = new_mesh("SM_HeliosRobot_Detailed_A")

    # ── Legs ──────────────────────────────────────────────────────────────
    for side in [-1, 1]:
        # Upper leg
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=10,
            radius1=0.09, radius2=0.08, depth=0.30,
            matrix=Matrix.Translation((side * 0.135, 0, 0.15)))
        # Knee sphere
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.06,
            matrix=Matrix.Translation((side * 0.135, 0, 0.32)))
        # Lower leg
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=10,
            radius1=0.075, radius2=0.065, depth=0.28,
            matrix=Matrix.Translation((side * 0.135, 0, 0.46)))
        # Ankle disc
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=10,
            radius1=0.072, radius2=0.072, depth=0.03,
            matrix=Matrix.Translation((side * 0.135, 0, 0.615)))
        # Foot
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side * 0.135, 0.025, 0.065))
            @ Matrix.Scale(0.14, 4, (1, 0, 0))
            @ Matrix.Scale(0.22, 4, (0, 1, 0))
            @ Matrix.Scale(0.10, 4, (0, 0, 1)))
        # Toe ridge
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side * 0.135, 0.085, 0.058))
            @ Matrix.Scale(0.10, 4, (1, 0, 0))
            @ Matrix.Scale(0.05, 4, (0, 1, 0))
            @ Matrix.Scale(0.025, 4, (0, 0, 1)))

    # ── Pelvis / hip ──────────────────────────────────────────────────────
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0, 0.64))
        @ Matrix.Scale(0.32, 4, (1, 0, 0))
        @ Matrix.Scale(0.20, 4, (0, 1, 0))
        @ Matrix.Scale(0.10, 4, (0, 0, 1)))
    # Hip ball joints
    for side in [-1, 1]:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.055,
            matrix=Matrix.Translation((side * 0.135, 0, 0.64)))

    # ── Torso ─────────────────────────────────────────────────────────────
    # Lower torso
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=12,
        radius1=0.155, radius2=0.175, depth=0.22,
        matrix=Matrix.Translation((0, 0, 0.80)))
    # Upper torso
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=12,
        radius1=0.175, radius2=0.155, depth=0.22,
        matrix=Matrix.Translation((0, 0, 1.02)))
    # Chest emissive stripe (gold line across chest)
    bmesh.ops.create_cube(bm, size=1,
        matrix=Matrix.Translation((0, 0.175, 1.06))
        @ Matrix.Scale(0.28, 4, (1, 0, 0))
        @ Matrix.Scale(0.02, 4, (0, 1, 0))
        @ Matrix.Scale(0.06, 4, (0, 0, 1)))
    # Chest logo diamond
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.028,
        matrix=Matrix.Translation((0, 0.178, 1.06))
        @ Matrix.Scale(1.0, 4, (1, 0, 0))
        @ Matrix.Scale(0.3, 4, (0, 1, 0))
        @ Matrix.Scale(1.5, 4, (0, 0, 1)))
    # Side chest panels
    for side in [-1, 1]:
        bmesh.ops.create_cube(bm, size=1,
            matrix=Matrix.Translation((side * 0.16, 0.10, 1.02))
            @ Matrix.Scale(0.06, 4, (1, 0, 0))
            @ Matrix.Scale(0.14, 4, (0, 1, 0))
            @ Matrix.Scale(0.20, 4, (0, 0, 1)))

    # ── Shoulders ─────────────────────────────────────────────────────────
    for side in [-1, 1]:
        # Shoulder pauldron
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.09,
            matrix=Matrix.Translation((side * 0.255, 0, 1.14))
            @ Matrix.Scale(1.0, 4, (1, 0, 0))
            @ Matrix.Scale(0.85, 4, (0, 1, 0))
            @ Matrix.Scale(0.85, 4, (0, 0, 1)))
        # Shoulder seam ring
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=12,
            radius1=0.07, radius2=0.07, depth=0.015,
            matrix=Matrix.Translation((side * 0.255, 0, 1.14))
            @ Matrix.Rotation(TAU / 4, 4, 'Y'))

    # ── Arms ──────────────────────────────────────────────────────────────
    for side in [-1, 1]:
        # Upper arm
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=8,
            radius1=0.065, radius2=0.058, depth=0.26,
            matrix=Matrix.Translation((side * 0.31, 0, 1.00)))
        # Elbow sphere
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.048,
            matrix=Matrix.Translation((side * 0.31, 0, 0.86)))
        # Lower arm
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=8,
            radius1=0.055, radius2=0.048, depth=0.22,
            matrix=Matrix.Translation((side * 0.31, 0, 0.73)))
        # Wrist ring
        bmesh.ops.create_cylinder(bm, cap_ends=False, segments=10,
            radius1=0.052, radius2=0.052, depth=0.025,
            matrix=Matrix.Translation((side * 0.31, 0, 0.625)))
        # Palm disc
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=8,
            radius1=0.055, radius2=0.042, depth=0.04,
            matrix=Matrix.Translation((side * 0.31, 0, 0.595)))
        # Fingers — 4 stubby cylinders
        for fi in range(4):
            fa = -0.04 + fi * 0.028
            bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=6,
                radius1=0.012, radius2=0.009, depth=0.055,
                matrix=Matrix.Translation((side * 0.31 + fa, 0.04, 0.558)))

    # ── Neck ──────────────────────────────────────────────────────────────
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=8,
        radius1=0.055, radius2=0.060, depth=0.09,
        matrix=Matrix.Translation((0, 0, 1.19)))

    # ── Head ──────────────────────────────────────────────────────────────
    # Main head shell (slightly flattened front-back)
    head_res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.145,
        matrix=Matrix.Translation((0, 0, 1.365)))
    for v in head_res['verts']:
        local = v.co - Vector((0, 0, 1.365))
        if local.length < 0.150:
            v.co.y *= 0.78

    # Visor — oval blue panel
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=16,
        radius1=0.088, radius2=0.088, depth=0.018,
        matrix=Matrix.Translation((0, 0.155, 1.370))
        @ Matrix.Scale(0.65, 4, (1, 0, 0))
        @ Matrix.Scale(1.0, 4, (0, 0, 1))
        @ Matrix.Rotation(TAU / 4, 4, 'X'))

    # Gold trim ring around visor
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=16,
        radius1=0.095, radius2=0.095, depth=0.008,
        matrix=Matrix.Translation((0, 0.150, 1.370))
        @ Matrix.Scale(0.65, 4, (1, 0, 0))
        @ Matrix.Scale(1.0, 4, (0, 0, 1))
        @ Matrix.Rotation(TAU / 4, 4, 'X'))

    # Side vents (3 slots each side)
    for side in [-1, 1]:
        for vi in range(3):
            vz = 1.32 + vi * 0.030
            bmesh.ops.create_cube(bm, size=1,
                matrix=Matrix.Translation((side * 0.145, 0, vz))
                @ Matrix.Scale(0.02, 4, (1, 0, 0))
                @ Matrix.Scale(0.06, 4, (0, 1, 0))
                @ Matrix.Scale(0.018, 4, (0, 0, 1)))

    # Crown ridge (gold band across top)
    bmesh.ops.create_cylinder(bm, cap_ends=False, segments=14,
        radius1=0.148, radius2=0.148, depth=0.012,
        matrix=Matrix.Translation((0, 0, 1.43)))

    # ── Spine detail (back) ───────────────────────────────────────────────
    for si in range(5):
        sz = 0.72 + si * 0.07
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.018,
            matrix=Matrix.Translation((0, -0.175, sz)))

    finalise(obj, bm)
    smart_uv(obj)
    add_mat_slots(obj, [
        "mat_ancient_machine_dark",
        "mat_gold_emissive",
        "mat_blue_emissive",
        "mat_ancient_machine_edge_wear",
        "mat_pearl_stone",
    ])
    set_origin_to_base(obj)
    export_fbx(obj, EXPORT_DIR, "SM_HeliosRobot_Detailed_A")
    return obj


if __name__ == "__main__":
    clear_scene()
    build()
    print("  ✓ SM_HeliosRobot_Detailed_A  →  Desktop/AbyssalEarth_FBX/")
