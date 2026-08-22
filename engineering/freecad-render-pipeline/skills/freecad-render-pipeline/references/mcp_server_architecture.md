# MCP server architecture — `scripts/mcp_server.py`

## Why an MCP server on top of the CLI scripts

`export_freecad_scene.py` and `render_scene.py` are standalone CLI tools
you can run by hand. `mcp_server.py` wraps them (and `coohom_client.py`)
as MCP tools so an agent — Claude Code, Claude Desktop, Claude Cowork, or
any other MCP client — can call them directly as part of a conversation,
without the user having to shell out commands themselves.

- MCP specification: https://modelcontextprotocol.io/specification/draft.md
- Python SDK (FastMCP): https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md

## Design choices

- **stdio transport, not HTTP.** Everything here runs against files and
  binaries on the same machine (FreeCAD, Blender). stdio is the
  documented transport for local MCP servers; there is no reason to add
  network exposure for a tool that only touches the local filesystem and
  local applications.
- **Subprocess boundary, not in-process imports.** `mcp_server.py` never
  imports `FreeCAD`, `bpy`, or `Import`/`Mesh`/`TechDraw` directly — those
  modules only exist inside FreeCAD's and Blender's own bundled Python
  interpreters, which are usually a different Python build than whatever
  runs the MCP server. Each tool instead shells out to `freecadcmd` or
  `blender --background --python ...` and parses the last JSON line of
  stdout, matching how both applications are actually meant to be
  scripted headlessly.
- **Every tool returns structured JSON**, always including `ok`, per this
  skill's error-handling convention (from the mcp-builder guide's
  actionable-error-message guidance): a failure carries `error` and often
  `hint` naming the concrete fix (missing binary, wrong Python, unfilled
  Coohom config) rather than a bare traceback.
- **`render_pipeline` composes the other two tools** as a convenience,
  because "FreeCAD file in, rendered image out" is the common case; the
  individual `export_freecad_scene`/`render_photoreal` tools stay
  available separately for anyone who wants to export once and try
  several render settings, or inspect the intermediate glTF/OBJ.
- **`coohom_status` / `coohom_call` never fabricate connectivity.** They
  are thin wrappers around `coohom_client.py`'s config-driven design (see
  [coohom_open_api.md](coohom_open_api.md)) — an agent calling
  `coohom_call` before `coohom_status` reports `configured: true` gets a
  clear `CoohomConfigError` message, not a silent failure or an invented
  response.

## Adding this server to an MCP client

Most MCP clients (including Claude Code) take a stdio server as a command
+ args entry, e.g.:

```json
{
  "mcpServers": {
    "freecad-render-pipeline": {
      "command": "python",
      "args": ["/absolute/path/to/scripts/mcp_server.py"],
      "env": {
        "FREECAD_CMD": "/usr/bin/freecadcmd",
        "BLENDER_BIN": "/usr/bin/blender"
      }
    }
  }
}
```

Set `FREECAD_CMD`/`BLENDER_BIN` explicitly if either binary isn't on the
PATH the MCP client's process inherits (common on macOS app bundles and
some sandboxed environments).

## Tool inventory

| Tool | Wraps | Read-only? |
|---|---|---|
| `export_freecad_scene` | `export_freecad_scene.py` via `freecadcmd` | No — writes files |
| `render_photoreal` | `render_scene.py` via `blender --background` | No — writes an image |
| `render_pipeline` | both of the above, chained | No |
| `coohom_status` | `coohom_client.py status` | Yes |
| `coohom_call` | `coohom_client.py call` | No, once real endpoints are filled in |
