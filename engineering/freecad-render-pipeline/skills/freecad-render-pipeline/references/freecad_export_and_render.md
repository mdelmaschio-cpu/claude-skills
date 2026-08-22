# FreeCAD export + Blender render — API notes

## Why export instead of scripting FreeCAD's own Render workbench

FreeCAD ships a Render workbench (originally by Yorik van Havre, who also
authored the BIM Workbench) that can drive external renderers — Appleseed,
Blender/Cycles, LuxCoreRender, OSPRay, POV-Ray — directly from inside
FreeCAD. Its Python scripting surface has changed across FreeCAD releases
(0.20 → 0.21 → 1.0), so this skill instead uses the smaller, far more
stable surface: FreeCAD exports geometry, Blender renders it. That split
also means the render step doesn't require a FreeCAD install at all —
only the exported file.

- FreeCAD Render workbench: https://wiki.freecad.org/Render_Workbench
- FreeCAD BIM Workbench: https://wiki.freecad.org/BIM_Workbench
- FreeCAD Import/Export module: https://wiki.freecad.org/Import_Export
- FreeCAD TechDraw Workbench (2D sheets): https://wiki.freecad.org/TechDraw_Workbench

## Why export works the same for plain Part geometry and BIM/IFC

FreeCAD's BIM Workbench uses IfcOpenShell to read `.ifc` files and convert
each IFC entity into a native FreeCAD `Arch`/`BIM` object (wall, window,
slab, ...). Once loaded, every one of those objects exposes the same
`.Shape` property that a plain `Part::Feature` does — so `Import.export()`
and `Mesh.export()` (both called on a list of document objects, not on
IFC data directly) work uniformly regardless of whether the geometry
originated from a 2D sketch, a solid, or an imported IFC building model.
This is also why the export script in this skill never needs
IFC-specific branches.

## Format choice

- **glTF/GLB** (default): best material/color fidelity into Blender via
  the built-in glTF importer; added to FreeCAD's `Import` module export
  dispatcher in recent releases. If your FreeCAD build's `Import.export`
  can't write glTF, the export script automatically falls back to `Mesh.export`
  producing an `.obj` next to the intended output — check the script's
  JSON output for a `3d_export_fallback` key when this happens.
- **OBJ/STL**: safe, universal fallback (mesh only, weaker material
  fidelity), always available via the `Mesh` module.
- **STEP/IGES**: for round-tripping into other CAD tools, not for
  rendering.

## TechDraw (2D) sheets

`TechDraw.writeSVGPage(page, path)` exports a `TechDraw::DrawPage` object
to SVG without the GUI. The exact scripting surface (function name and
signature) has shifted between FreeCAD releases; the export script wraps
the call in a try/except and points to the TechDraw wiki page above if it
raises `AttributeError` on your version, rather than failing silently.

## Units: the one gotcha that produces "blank" renders

FreeCAD's internal unit is millimeters; Blender's default scene unit is
meters. A 6-meter-wide FreeCAD wall exports as `6000` in whatever linear
unit the glTF/OBJ exporter writes (glTF's spec unit is meters, so a
correct glTF exporter already converts — OBJ has no unit convention and
often round-trips raw FreeCAD numbers). If a render comes back
apparently empty, check the imported mesh's dimensions in Blender
(`N` panel → Item → Dimensions) against the model's real-world size
before assuming the pipeline is broken — the auto-framing camera in
`render_scene.py` computes its distance from the *imported* bounding box,
so a 1000x-too-large import still gets framed, just absurdly far from
anything that looks intentional.

## Blender API surface used by `render_scene.py`

- `bpy.ops.import_scene.gltf` / `bpy.ops.wm.obj_import` (Blender 3.x+) /
  legacy `bpy.ops.import_scene.obj`: https://docs.blender.org/api/current/bpy.ops.import_scene.html
- `bpy.types.CyclesRenderSettings` (`scene.cycles.samples`,
  `use_denoising`): https://docs.blender.org/api/current/bpy.types.CyclesRenderSettings.html
- World shader nodes for HDRI environments (`ShaderNodeBackground` +
  `ShaderNodeTexEnvironment` + `ShaderNodeOutputWorld`):
  https://docs.blender.org/api/current/bpy.types.ShaderNodeTexEnvironment.html
- Headless invocation flags (`--background`, `--factory-startup`,
  `--python`, args after `--`): https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html

## Alternative render engine: LuxCoreRender

LuxCoreRender is available inside Blender via the third-party BlendLuxCore
add-on and is one of the renderers FreeCAD's own Render workbench also
supports. This skill implements Cycles only (it ships with every Blender
install, so `render_scene.py` works with zero extra setup); switching the
`scene.render.engine` value to `"LUXCORE"` after installing BlendLuxCore
is a reasonable extension, but this skill does not implement it because
the add-on's material/node conventions are not part of Blender core and
vary by add-on version. See https://wiki.freecad.org/Render_Workbench for
FreeCAD's own LuxCoreRender integration if you'd rather stay inside
FreeCAD for that path.
