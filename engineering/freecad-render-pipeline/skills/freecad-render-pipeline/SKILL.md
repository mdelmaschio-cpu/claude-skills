---
name: freecad-render-pipeline
description: Turn FreeCAD 2D drawings and BIM/Arch models into photorealistic renders, via a local Blender/Cycles pipeline that works today and an MCP server that also exposes a partner-gated Coohom (cloud interior-design/render platform) API client. Use when the user wants to render FreeCAD, BIM, or IFC geometry photorealistically, or asks to drive Cohoom/Coohom from Python or an MCP server.
license: MIT
metadata:
  version: 1.0.0
---

# FreeCAD Render Pipeline

Two render paths from the same FreeCAD export, exposed as both CLI scripts and MCP tools:

1. **Local (works today, no account needed):** FreeCAD → glTF/OBJ export → Blender Cycles photoreal render.
2. **Coohom cloud (scaffolded, needs your partner credentials):** thin, honest client for Coohom's partner-gated Open API — see [references/coohom_open_api.md](references/coohom_open_api.md) for why the exact endpoints can't be hardcoded here.

> Note: the user-facing name is commonly typed "Cohoom" — the actual product is **Coohom** (coohom.com / open.coohom.com).

## Prerequisites

- **FreeCAD** with `freecadcmd` on PATH (ships with any FreeCAD install; used for export, not rendering).
- **Blender** (4.x+) with `blender` on PATH — Cycles ships built in, no extra install.
- `pip install mcp` if you want the MCP server (`scripts/mcp_server.py`); the export/render scripts themselves are stdlib-only.
- Optional: a Coohom Open API partner account (apply at coohom.com/b2b/api) if you also want the cloud path.

## Quick start — local pipeline

```bash
# 1. Export the FreeCAD document to a render-ready scene (+ optional 2D sheets)
freecadcmd scripts/export_freecad_scene.py -- \
  --input plan.FCStd --output scene.glb --output-2d sheets/

# 2. Render it photorealistically with Blender/Cycles
blender --background --factory-startup --python scripts/render_scene.py -- \
  --input scene.glb --output render.png --samples 256 --width 1920 --height 1080
```

Works on plain Part/Sketch geometry and on BIM/Arch objects (walls, windows, IFC-derived elements) alike, because both expose the standard `.Shape` that FreeCAD's export APIs already know how to serialize — see [references/freecad_export_and_render.md](references/freecad_export_and_render.md).

## Quick start — MCP server

```bash
pip install mcp
python scripts/mcp_server.py   # stdio MCP server; add it in Claude Code / Claude Desktop's MCP config
```

Tools exposed: `export_freecad_scene`, `render_photoreal`, `render_pipeline` (both steps chained), `coohom_status`, `coohom_call`. See [references/mcp_server_architecture.md](references/mcp_server_architecture.md).

## Coohom (cloud) path

Coohom's Open API is **partner-gated**: real endpoint paths and the signing scheme are only published to approved partners. `scripts/coohom_client.py` will never claim a fake success — `coohom_status` reports exactly which credentials/endpoints are still unfilled, and `coohom_call` refuses to run against a placeholder endpoint. Fill in `scripts/coohom_endpoints.example.json` from your own partner reference once you have access; details in [references/coohom_open_api.md](references/coohom_open_api.md).

## Workflow

1. Confirm prerequisites (`freecadcmd --version`, `blender --version`).
2. Export: pick `--format glb` (default, best material fidelity) unless you need `obj`/`step`/`iges` for another tool.
3. Render: start with `--samples 128` for a fast preview, raise to 256-512 for a final photoreal pass; pass `--hdri` for realistic outdoor/interior lighting instead of the built-in three-point rig.
4. If the render looks unlit or blown out, check `render.png`'s auto-framed camera distance against your model's actual scale (FreeCAD units vs. Blender's meter default can differ — see the reference doc).
5. Only reach for `coohom_call` once `coohom_status` reports `configured: true`.

## Troubleshooting

- `ModuleNotFoundError: No module named 'FreeCAD'` → you ran the export script with system `python3` instead of `freecadcmd`.
- `bpy is not importable outside Blender` → same issue, for the render script and `blender --python`.
- Render is a blank/black image → the mesh import produced 0 mesh objects (check the exporter's `objects_exported` count) or the scene scale is far outside the auto-framed camera's range.

---

**Version:** 1.0.0
