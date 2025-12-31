# Tool Setup

Last Updated: December 30, 2025

## KiCad

- **Version:** 9.0.6
- **Location:** `/usr/local/bin/kicad-cli`
- **IPC API:** Enabled (required for MCP server)

## Python Virtual Environment

All Python packages installed in `venv/`:

```bash
source venv/bin/activate
```

### Installed Packages

| Package | Version | Purpose |
|---------|---------|---------|
| kicad-python | 0.5.0 | Official IPC API bindings |
| kigadgets | 0.5.1 | Cross-version KiCad compatibility |
| skidl | 2.2.1 | Code-first schematic design |
| kibot | 1.8.5 | CI/CD automation, fabrication files |
| kiauto | 2.3.5 | KiCad automation scripts |
| easyeda2kicad | 0.8.0 | Import LCSC/EasyEDA components |
| interactivehtmlbom | 2.10.0 | Interactive assembly BOM |
| kicad-parts-placer | 0.1.4 | Component placement from centroid |

## System Tools

| Tool | Version | Purpose |
|------|---------|---------|
| gerbv | 2.10.0 | Gerber file viewer/export |

## Not Yet Installed

- [ ] FreeRouting JAR (auto-router) - Download from GitHub releases
- [ ] kicad-mcp-python (MCP server) - Clone and configure

## Tool Locations

```
venv/bin/
├── python3           # Python interpreter
├── pip               # Package installer
├── kibot             # KiBot CLI
├── easyeda2kicad     # Component importer
├── generate_interactive_bom  # Interactive BOM
└── ...

/usr/local/bin/
└── kicad-cli         # KiCad CLI

/opt/homebrew/bin/
└── gerbv             # Gerber viewer
```

## Activation

```bash
cd /Users/zeul/GIT/singingcard
source venv/bin/activate
```
