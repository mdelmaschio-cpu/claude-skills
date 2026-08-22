# freecad-render-pipeline

Turn FreeCAD 2D drawings and BIM/Arch models into photorealistic renders.

## Two paths, one export

1. **Local (works today, no account needed):** FreeCAD (`freecadcmd`) exports
   geometry to glTF/OBJ → Blender (`blender --background`) renders it with
   Cycles, auto-framing a camera and a three-point lighting rig (or an HDRI
   environment) around the imported scene.
2. **Coohom cloud (scaffolded, needs your partner credentials):** a thin
   Python client for Coohom's Open API — the cloud interior-design/render
   platform often typed "Cohoom." Coohom's real endpoint paths and signing
   scheme are partner-gated (apply at coohom.com/b2b/api); this client
   refuses to fabricate a working connection and instead reports exactly
   which credentials/endpoints are still unfilled.

## What's in here

| Component | Where | What |
|---|---|---|
| FreeCAD exporter | `skills/freecad-render-pipeline/scripts/export_freecad_scene.py` | `.FCStd` → glTF/OBJ (+ optional TechDraw SVG sheets) |
| Blender renderer | `skills/freecad-render-pipeline/scripts/render_scene.py` | exported scene → Cycles photoreal image |
| Coohom client | `skills/freecad-render-pipeline/scripts/coohom_client.py` | config-driven, partner-gated Open API calls |
| MCP server | `skills/freecad-render-pipeline/scripts/mcp_server.py` | exposes all of the above as MCP tools (`pip install mcp`) |
| References | `skills/freecad-render-pipeline/references/` | FreeCAD/Blender API notes, Coohom API facts, MCP architecture |
| Persona agent | `agents/cs-freecad-render.md` | prerequisite + parameter forcing-question gate |
| Slash command | `commands/cs-render-freecad.md` | `/cs:render-freecad <file.FCStd>` |

## Quick start

```bash
freecadcmd skills/freecad-render-pipeline/scripts/export_freecad_scene.py -- \
  --input plan.FCStd --output scene.glb

blender --background --factory-startup --python skills/freecad-render-pipeline/scripts/render_scene.py -- \
  --input scene.glb --output render.png --samples 256
```

Full details, prerequisites, and the MCP client config snippet: see
[`skills/freecad-render-pipeline/SKILL.md`](skills/freecad-render-pipeline/SKILL.md).

## License

MIT.
