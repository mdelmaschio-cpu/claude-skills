#!/usr/bin/env python3
"""Photorealistic Cycles render of a glTF/OBJ scene exported from FreeCAD.

Runs inside Blender's own Python (bpy is only importable there):

    blender --background --factory-startup --python render_scene.py -- \\
        --input scene.glb --output render.png --samples 128 \\
        --width 1920 --height 1080 [--hdri studio.hdr]

FreeCAD's glTF/OBJ export carries geometry and materials but no camera,
lights, or environment, so this script auto-frames a camera on the
imported scene's bounding box and lights it with a three-point rig (or an
HDRI environment if --hdri is given) before rendering with Cycles.

Reference: https://docs.blender.org/api/current/bpy.ops.import_scene.html
           https://docs.blender.org/api/current/bpy.types.CyclesRenderSettings.html
"""
import argparse
import json
import math
import os
import sys


def _args_after_dashdash():
    argv = sys.argv
    return argv[argv.index("--") + 1:] if "--" in argv else argv[1:]


def _import_obj(path):
    # wm.obj_import ships from Blender 3.x+; fall back to the legacy
    # import_scene.obj operator on older builds.
    importer = bpy.ops.wm.obj_import if hasattr(bpy.ops.wm, "obj_import") else bpy.ops.import_scene.obj
    importer(filepath=path)


_IMPORTERS = {
    ".glb": lambda path: bpy.ops.import_scene.gltf(filepath=path),
    ".gltf": lambda path: bpy.ops.import_scene.gltf(filepath=path),
    ".obj": _import_obj,
    ".fbx": lambda path: bpy.ops.import_scene.fbx(filepath=path),
}


def import_scene(path):
    ext = os.path.splitext(path)[1].lower()
    importer = _IMPORTERS.get(ext)
    if importer is None:
        raise ValueError(f"Unsupported scene format: {ext} (use .glb, .gltf, .obj, or .fbx)")
    importer(path)


def scene_bounds(objects):
    xs, ys, zs = [], [], []
    for obj in objects:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            world = obj.matrix_world @ mathutils.Vector(corner)
            xs.append(world.x)
            ys.append(world.y)
            zs.append(world.z)
    if not xs:
        return None
    return (min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs))


def auto_frame_camera(objects):
    bounds = scene_bounds(objects)
    if bounds is None:
        return None
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = bounds
    center = mathutils.Vector(((xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2))
    radius = max(xmax - xmin, ymax - ymin, zmax - zmin, 1.0)

    cam_data = bpy.data.cameras.new("AutoCamera")
    cam_obj = bpy.data.objects.new("AutoCamera", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)

    distance = radius * 1.8
    cam_obj.location = center + mathutils.Vector((distance, -distance, distance * 0.7))
    direction = center - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam_obj
    return center, radius


def add_three_point_lighting(center, radius):
    specs = [
        ("KeyLight", (radius * 2.0, -radius * 2.0, radius * 2.5), 1200),
        ("FillLight", (-radius * 2.2, -radius * 1.2, radius * 1.5), 500),
        ("RimLight", (0, radius * 2.5, radius * 1.8), 700),
    ]
    for name, offset, power in specs:
        light_data = bpy.data.lights.new(name, type="AREA")
        light_data.energy = power
        light_data.size = radius * 0.5
        light_obj = bpy.data.objects.new(name, light_data)
        light_obj.location = mathutils.Vector(center) + mathutils.Vector(offset)
        bpy.context.scene.collection.objects.link(light_obj)


def set_hdri_environment(hdri_path):
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()
    bg = nodes.new("ShaderNodeBackground")
    env = nodes.new("ShaderNodeTexEnvironment")
    out = nodes.new("ShaderNodeOutputWorld")
    env.image = bpy.data.images.load(hdri_path)
    links.new(env.outputs["Color"], bg.inputs["Color"])
    links.new(bg.outputs["Background"], out.inputs["Surface"])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--samples", type=int, default=128)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--hdri", default=None, help="Path to an .hdr/.exr environment map")
    parser.add_argument("--denoise", action="store_true", default=True)
    args = parser.parse_args(_args_after_dashdash())

    if not os.path.isfile(args.input):
        print(json.dumps({"ok": False, "error": f"Input scene not found: {args.input}"}))
        sys.exit(1)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    import_scene(args.input)

    mesh_objects = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not mesh_objects:
        print(json.dumps({"ok": False, "error": "Imported scene contains no mesh objects to render."}))
        sys.exit(1)

    center, radius = auto_frame_camera(mesh_objects) or ((0, 0, 0), 1.0)

    if args.hdri:
        set_hdri_environment(args.hdri)
    else:
        add_three_point_lighting(center, radius)

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = args.denoise
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.filepath = args.output

    bpy.ops.render.render(write_still=True)
    result = {
        "ok": True, "output": args.output, "engine": "CYCLES",
        "samples": args.samples, "resolution": [args.width, args.height],
    }
    print(json.dumps(result))


if __name__ == "__main__":
    try:
        import bpy
        import mathutils
    except ImportError:
        print(json.dumps({
            "ok": False,
            "error": "bpy is not importable outside Blender.",
            "hint": "Run with: blender --background --factory-startup --python render_scene.py -- <args>",
        }))
        sys.exit(1)
    main()
