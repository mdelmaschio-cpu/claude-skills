#!/usr/bin/env python3
"""MCP server that drives the FreeCAD -> photoreal-render pipeline.

Exposes 6 tools over stdio via the `mcp` Python SDK (FastMCP):

  export_freecad_scene   FreeCAD -> glTF/OBJ (+ optional 2D TechDraw SVG sheets)
  render_photoreal        exported scene -> Cycles render (local, works today)
  render_pipeline          the two steps above, chained
  coohom_status            report whether Coohom partner credentials/endpoints are configured
  coohom_call              call one configured, partner-documented Coohom endpoint

All heavy lifting shells out to `freecadcmd` / `blender`, which must be on
PATH (or pointed to via FREECAD_CMD / BLENDER_BIN), because the FreeCAD and
Blender Python APIs (App, Import, Mesh, TechDraw, bpy) only exist inside
those applications' own interpreters, not in the interpreter running this
MCP server.

Install: pip install mcp
Run:     python mcp_server.py
Add to Claude Code / Claude Desktop as a stdio MCP server pointing at this file.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Missing dependency: pip install mcp", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
FREECAD_CMD = os.environ.get("FREECAD_CMD", "freecadcmd")
BLENDER_BIN = os.environ.get("BLENDER_BIN", "blender")

mcp = FastMCP("freecad-render-pipeline")


def _last_json_line(stdout):
    """The export/render scripts print one JSON object as their last stdout
    line; earlier lines may be application warnings, so scan from the end."""
    for line in reversed(stdout.splitlines()):
        if not line.strip():
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    return None


def _run(cmd, timeout=600):
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return {"ok": False, "error": f"Executable not found: {cmd[0]}",
                "hint": "Install it or point FREECAD_CMD/BLENDER_BIN at the right binary."}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Timed out after {timeout}s running: {' '.join(cmd)}"}

    parsed = _last_json_line(proc.stdout)
    if proc.returncode != 0 and parsed is None:
        return {"ok": False, "error": f"Command exited {proc.returncode}", "stderr": proc.stderr[-2000:]}
    return parsed if parsed is not None else {"ok": proc.returncode == 0, "stdout": proc.stdout[-2000:]}


@mcp.tool()
def export_freecad_scene(
    input_path: str, output_path: str, fmt: str = "glb", output_2d_dir: str = ""
) -> dict:
    """Export a FreeCAD (.FCStd) 2D/BIM document to a render-ready 3D scene
    (glTF/GLB/OBJ), and optionally export its TechDraw sheets to SVG.

    Args:
        input_path: Path to the source .FCStd file.
        output_path: Path to write the 3D export to (extension should match fmt).
        fmt: One of gltf, glb, obj, stl, step, iges. Default glb.
        output_2d_dir: If set, also export every TechDraw page as SVG into this directory.

    Returns a dict with ok, document, 3d_export, objects_exported, and (if
    requested) 2d_sheets — or ok:false with an actionable error/hint.
    """
    cmd = [FREECAD_CMD, str(SCRIPT_DIR / "export_freecad_scene.py"), "--",
           "--input", input_path, "--output", output_path, "--format", fmt]
    if output_2d_dir:
        cmd += ["--output-2d", output_2d_dir]
    return _run(cmd)


@mcp.tool()
def render_photoreal(
    scene_path: str, output_path: str, samples: int = 128,
    width: int = 1920, height: int = 1080, hdri_path: str = ""
) -> dict:
    """Render an exported scene (glTF/GLB/OBJ/FBX) to a photorealistic image
    using Blender's Cycles path tracer, auto-framing a camera and lighting
    rig around the geometry (or using an HDRI environment if hdri_path is set).

    Args:
        scene_path: Path to the scene exported by export_freecad_scene.
        output_path: Path to write the rendered image (e.g. render.png).
        samples: Cycles sample count; higher = cleaner but slower. Default 128.
        width, height: Output resolution in pixels.
        hdri_path: Optional .hdr/.exr environment map for lighting/reflections.

    Returns ok, output, engine, samples, resolution — or ok:false with an
    actionable error (e.g. missing Blender binary).
    """
    cmd = [BLENDER_BIN, "--background", "--factory-startup", "--python",
           str(SCRIPT_DIR / "render_scene.py"), "--",
           "--input", scene_path, "--output", output_path,
           "--samples", str(samples), "--width", str(width), "--height", str(height)]
    if hdri_path:
        cmd += ["--hdri", hdri_path]
    return _run(cmd, timeout=1800)


@mcp.tool()
def render_pipeline(
    fcstd_path: str, render_output_path: str, fmt: str = "glb",
    samples: int = 128, width: int = 1920, height: int = 1080, hdri_path: str = ""
) -> dict:
    """Run the full local pipeline: FreeCAD (.FCStd) -> exported scene ->
    photorealistic Cycles render, in one call.

    Args:
        fcstd_path: Path to the source .FCStd file.
        render_output_path: Path to write the final rendered image.
        fmt, samples, width, height, hdri_path: see export_freecad_scene / render_photoreal.

    Returns the render_photoreal result, with an added 'export' key holding
    the export_freecad_scene result. Stops early (ok:false) if export fails.
    """
    scene_path = str(Path(render_output_path).with_suffix(f".{fmt}"))
    export_result = export_freecad_scene(fcstd_path, scene_path, fmt)
    if not export_result.get("ok"):
        return {"ok": False, "stage": "export", "export": export_result}
    render_result = render_photoreal(scene_path, render_output_path, samples, width, height, hdri_path)
    render_result["export"] = export_result
    return render_result


@mcp.tool()
def coohom_status(config_path: str = "coohom_endpoints.json") -> dict:
    """Check whether Coohom Open API partner credentials and endpoint paths
    are configured. Coohom's Open Platform is partner-gated (apply at
    https://www.coohom.com/b2b/api); this tool never fabricates a "connected"
    state — it reports exactly what is and is not filled in.

    Args:
        config_path: Path to the Coohom endpoints config (see
            coohom_endpoints.example.json in this skill for the shape).
    """
    return _run([sys.executable, str(SCRIPT_DIR / "coohom_client.py"), "status", "--config", config_path])


@mcp.tool()
def coohom_call(endpoint: str, body: dict, config_path: str = "coohom_endpoints.json",
                 method: str = "POST") -> dict:
    """Call one Coohom Open API endpoint that you have already filled into
    the config file from your partner documentation. This tool does not
    know Coohom's real endpoint paths or signing scheme on its own — call
    coohom_status first, and only proceed once every endpoint is filled in.

    Args:
        endpoint: Logical endpoint name as configured (e.g. create_design, upload_model, start_render, get_render_status).
        body: JSON-serializable request body.
        config_path: Path to the Coohom endpoints config.
        method: HTTP method, default POST.
    """
    return _run([sys.executable, str(SCRIPT_DIR / "coohom_client.py"), "call", endpoint,
                 "--config", config_path, "--body", json.dumps(body), "--method", method])


if __name__ == "__main__":
    mcp.run()
