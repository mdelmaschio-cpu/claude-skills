#!/usr/bin/env python3
"""Export a FreeCAD document (2D TechDraw sheets and/or 3D/BIM geometry) to
render-ready formats. Run inside FreeCAD's own Python (freecadcmd), because
the FreeCAD, Import, Mesh, and TechDraw modules are only importable there:

    freecadcmd export_freecad_scene.py -- --input plan.FCStd --output scene.glb
    freecadcmd export_freecad_scene.py -- --input plan.FCStd --output scene.obj --format obj
    freecadcmd export_freecad_scene.py -- --input plan.FCStd --output-2d sheets/ --skip-3d

Works uniformly on plain Part/Sketch geometry and on BIM/Arch objects
(Wall, Window, IfcDocument, ...) because both expose a standard .Shape
that Import.export / Mesh.export already know how to serialize. This is
also why a document imported from IFC does not need special-casing here:
FreeCAD's BIM Workbench already converted it into native shapes.

Reference: https://wiki.freecad.org/Import_Export
           https://wiki.freecad.org/TechDraw_Workbench
"""
import argparse
import json
import os
import sys


def _fail(message, hint=None):
    payload = {"ok": False, "error": message}
    if hint:
        payload["hint"] = hint
    print(json.dumps(payload))
    sys.exit(1)


def export_3d(doc, output_path, fmt):
    """Export all visible, shape-bearing objects to gltf/glb/obj/stl."""
    objs = [o for o in doc.Objects if hasattr(o, "Shape") and getattr(o, "Visibility", True)]
    if not objs:
        objs = [o for o in doc.Objects if hasattr(o, "Shape")]
    if not objs:
        _fail("No shape-bearing objects found in the document.",
              "Confirm the FCStd file actually contains Part/BIM geometry, not just a spreadsheet or drawing.")

    ext = fmt.lower()
    if ext in ("gltf", "glb"):
        try:
            import Import
            Import.export(objs, output_path)
            return len(objs)
        except Exception as exc:  # noqa: BLE001 - version-dependent API, fall through to mesh export
            print(json.dumps({"warning": f"Import.export glTF failed ({exc}); falling back to mesh export"}),
                  file=sys.stderr)
            fallback = os.path.splitext(output_path)[0] + ".obj"
            import Mesh
            Mesh.export(objs, fallback)
            return fallback
    elif ext in ("obj", "stl", "step", "iges"):
        import Mesh
        if ext in ("obj", "stl"):
            Mesh.export(objs, output_path)
        else:
            import Import
            Import.export(objs, output_path)
        return len(objs)
    else:
        _fail(f"Unsupported 3D export format: {fmt}", "Use one of: gltf, glb, obj, stl, step, iges")


def export_2d(doc, output_dir):
    """Export every TechDraw page (2D plan/section/elevation sheet) to SVG."""
    pages = doc.findObjects("TechDraw::DrawPage")
    if not pages:
        return []
    os.makedirs(output_dir, exist_ok=True)
    written = []
    try:
        import TechDraw
    except ImportError:
        _fail("TechDraw module not available in this FreeCAD build.",
              "Install/enable the TechDraw workbench, or drop --output-2d if you only need the 3D model.")
    for page in pages:
        target = os.path.join(output_dir, f"{page.Name}.svg")
        try:
            TechDraw.writeSVGPage(page, target)
            written.append(target)
        except AttributeError:
            _fail("TechDraw.writeSVGPage is not available in this FreeCAD version.",
                  "See https://wiki.freecad.org/TechDraw_Workbench for the scripting API on your version, "
                  "or export the page manually from the GUI (File > Export > SVG).")
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="Path to the .FCStd source file")
    parser.add_argument("--output", help="Path for the 3D export (e.g. scene.glb)")
    parser.add_argument("--format", default="glb", help="3D export format: gltf, glb, obj, stl, step, iges (default: glb)")
    parser.add_argument("--output-2d", help="Directory to write TechDraw 2D sheets (SVG) into")
    parser.add_argument("--skip-3d", action="store_true", help="Skip the 3D export, only export 2D sheets")
    args = parser.parse_args()

    if not args.skip_3d and not args.output:
        parser.error("--output is required unless --skip-3d is set")

    try:
        import FreeCAD as App
    except ImportError:
        _fail("Could not import the FreeCAD module.",
              "Run this script with 'freecadcmd export_freecad_scene.py -- <args>', "
              "not the system 'python3'.")

    if not os.path.isfile(args.input):
        _fail(f"Input file not found: {args.input}")

    doc = App.openDocument(args.input)

    result = {"ok": True, "document": doc.Name}

    if not args.skip_3d:
        count_or_path = export_3d(doc, args.output, args.format)
        result["3d_export"] = args.output
        result["objects_exported"] = count_or_path if isinstance(count_or_path, int) else None
        if isinstance(count_or_path, str):
            result["3d_export_fallback"] = count_or_path

    if args.output_2d:
        result["2d_sheets"] = export_2d(doc, args.output_2d)

    App.closeDocument(doc.Name)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
