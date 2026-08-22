---
name: "cs-render-freecad"
description: "/cs:render-freecad <path-to.FCStd> — Export a FreeCAD 2D/BIM document and render it photorealistically with Blender/Cycles (local, works today), or drive it through Coohom's partner-gated Open API once configured. Use when the user wants a photoreal render from a FreeCAD file."
---

# /cs:render-freecad — FreeCAD-to-Photoreal Forcing Questions

**Command:** `/cs:render-freecad <path-to.FCStd>`

## The Forcing Questions

### 1. Local Cycles render, or Coohom cloud?
**Local works immediately; Coohom needs a partner account.**
- Default to local unless the user explicitly has Coohom partner credentials
- Run `coohom_status` first if Coohom is requested — never assume it's configured

### 2. Are `freecadcmd` and `blender` actually on PATH?
```bash
freecadcmd --version
blender --version
```
- If either is missing, stop and get the binary path (or `FREECAD_CMD`/`BLENDER_BIN` env vars) before running anything else

### 3. Which export format?
- `glb` (default): best material fidelity into Blender
- `obj`/`stl`: safe fallback, weaker materials
- Check the exporter's JSON output for a `3d_export_fallback` key — if present, `Import.export` couldn't write glTF on this FreeCAD build and it silently fell back; tell the user

### 4. Preview or final pass?
- Preview: `--samples 64`, default resolution — fast iteration on framing/lighting
- Final: `--samples 256`+ , full target resolution, consider `--hdri` for realistic lighting instead of the built-in three-point rig

### 5. Does the render look wrong (blank/black/tiny)?
- Check `objects_exported` in the export JSON — 0 means nothing to render
- Check imported mesh dimensions in Blender against the model's real-world size — FreeCAD is mm-internal, a bad export can be 1000x too large or small (see the reference doc's units section)

### 6. If Coohom: is every endpoint actually filled in?
```bash
python scripts/coohom_client.py status --config coohom_endpoints.json
```
- Must report `configured: true` before any `coohom_call` — otherwise get the user to their partner docs at https://developer.coohom.com/reference first

## Workflow

```bash
# 1. Prerequisites
freecadcmd --version && blender --version

# 2. Export
freecadcmd scripts/export_freecad_scene.py -- --input plan.FCStd --output scene.glb --output-2d sheets/

# 3. Render
blender --background --factory-startup --python scripts/render_scene.py -- \
  --input scene.glb --output render.png --samples 256 --width 1920 --height 1080

# 4. (Optional, gated) Coohom
python scripts/coohom_client.py status --config coohom_endpoints.json
```

## Output Format

```markdown
# FreeCAD Render: <file>
**Date:** YYYY-MM-DD

## Path Chosen
[local-cycles | coohom-cloud]

## Prerequisites
- freecadcmd: present/missing (version)
- blender: present/missing (version)
- Coohom config: configured/not-configured (if cloud path)

## Export Result
- objects_exported: N
- format: glb/obj/...
- fallback triggered: yes/no

## Render Result
- output: path
- samples / resolution: N / WxH
- ok: true/false (+ error/hint if false)

## Verdict
🟢 RENDERED | 🟡 RENDERED-WITH-FALLBACK | 🔴 BLOCKED

## Top 3 Actions (if not green)
[3 concrete fixes with the exact hint text from the failing tool]
```

## Routing

- `/cs:write-a-skill` — if the user wants to extend this skill itself
- `/cs:karpathy-check` — for code-quality concerns in `scripts/`

## Related

- Agent: [`cs-freecad-render`](../agents/cs-freecad-render.md)
- Skill: [`freecad-render-pipeline`](../skills/freecad-render-pipeline/SKILL.md)

---

**Version:** 1.0.0
