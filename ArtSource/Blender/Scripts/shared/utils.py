"""
shared/utils.py — Common helpers for all AbyssalEarth Blender asset scripts.
Import with:
    from shared.utils import (clear_scene, new_mesh, finalise, smart_uv,
                               add_mat_slots, set_origin_to_base, export_fbx,
                               get_export_dir, mat_color, extrude_region)
"""
import bpy
import bmesh
import math
import os
from mathutils import Matrix, Vector

TAU = math.tau
PI  = math.pi


def _get_repo_root():
    """Walk up from this file to find the directory containing Content/."""
    path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isdir(os.path.join(path, "Content")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    raise RuntimeError("Cannot find repo root (no Content/ directory found)")


def get_export_dir(subpath):
    """Return and create Content/ArtSourceExports/<subpath>."""
    d = os.path.join(_get_repo_root(), "Content", "ArtSourceExports", subpath)
    os.makedirs(d, exist_ok=True)
    return d


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
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
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")


_MATERIAL_COLORS = {
    "mat_ancient_machine_dark":   (0.05, 0.05, 0.06, 1),
    "mat_ancient_machine_edge_wear": (0.12, 0.11, 0.10, 1),
    "mat_gold_emissive":          (1.00, 0.72, 0.10, 1),
    "mat_blue_emissive":          (0.05, 0.45, 1.00, 1),
    "mat_crystal_blue":           (0.10, 0.60, 1.00, 1),
    "mat_wet_basalt":             (0.08, 0.08, 0.09, 1),
    "mat_human_equipment":        (0.18, 0.16, 0.14, 1),
    "mat_collector_glass":        (0.60, 0.85, 1.00, 1),
    "mat_orb_energy":             (0.40, 0.80, 1.00, 1),
    "mat_lava_emissive":          (1.00, 0.25, 0.00, 1),
    "mat_purple_emissive":        (0.55, 0.10, 1.00, 1),
    "mat_red_emissive_vein":      (1.00, 0.05, 0.05, 1),
    "mat_glass_bark":             (0.60, 0.90, 0.80, 1),
    "mat_water_bioluminescent":   (0.00, 0.55, 0.65, 1),
    # Biome-specific
    "mat_bone_stone":             (0.82, 0.78, 0.70, 1),
    "mat_cyan_fossil_vein":       (0.00, 0.80, 0.75, 1),
    "mat_glassroot_translucent":  (0.55, 0.90, 0.75, 1),
    "mat_red_sap":                (0.70, 0.08, 0.05, 1),
    "mat_pearl_stone":            (0.88, 0.85, 0.82, 1),
    "mat_wet_edge":               (0.10, 0.12, 0.14, 1),
    "mat_dark_basalt":            (0.06, 0.06, 0.07, 1),
    "mat_amber_stabilizer":       (1.00, 0.60, 0.10, 1),
    "mat_obsidian":               (0.04, 0.03, 0.04, 1),
    "mat_heat_crack":             (1.00, 0.35, 0.00, 1),
    "mat_heat_bloom":             (1.00, 0.50, 0.10, 1),
    "mat_magenta_mineral":        (0.85, 0.10, 0.65, 1),
    "mat_fossil_bone":            (0.80, 0.76, 0.68, 1),
}


def mat_color(name):
    return _MATERIAL_COLORS.get(name, (0.50, 0.50, 0.50, 1))


def add_mat_slots(obj, names):
    for name in names:
        if name not in bpy.data.materials:
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = mat_color(name)
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
    """Export obj as FBX.  filename should NOT include .fbx extension."""
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


def add_subdivision(obj, levels=1):
    mod = obj.modifiers.new("Subsurf", "SUBSURF")
    mod.levels = levels
    mod.render_levels = levels


def extrude_region(bm, faces, dist, direction=None):
    if direction is None:
        direction = faces[0].normal.copy()
    geom = bmesh.ops.extrude_face_region(bm, geom=faces)
    verts = [e for e in geom["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts, vec=direction * dist)
    return [f for f in geom["geom"] if isinstance(f, bmesh.types.BMFace)]
