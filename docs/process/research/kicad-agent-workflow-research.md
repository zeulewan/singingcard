# KiCad AI Agent Workflow Research

**Research Date:** December 30, 2025
**Objective:** Find the best tools and workflow for an AI agent (Claude Code) to work with KiCad for automated PCB design, including auto-routing, component selection, visual inspection, and automated ordering.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [MCP Servers for KiCad](#mcp-servers-for-kicad)
3. [KiCad Programmatic Control](#kicad-programmatic-control)
4. [Auto-Routing Solutions](#auto-routing-solutions)
5. [JLCPCB Integration](#jlcpcb-integration)
6. [Component Selection & Libraries](#component-selection--libraries)
7. [Visual Inspection Tools](#visual-inspection-tools)
8. [DRC/ERC Automation & Cleanup](#drcerc-automation--cleanup)
9. [Code-First Design Tools](#code-first-design-tools)
10. [CI/CD Automation](#cicd-automation)
11. [Recommended Agent Workflow](#recommended-agent-workflow)
12. [Tool Installation Summary](#tool-installation-summary)
13. [Sources](#sources)
14. [Component Placement Automation](#component-placement-automation)
15. [Interactive BOM Visualization](#interactive-bom-visualization)
16. [Alternative PCB Ordering APIs](#alternative-pcb-ordering-apis)
17. [Alternative EDA Tools](#alternative-eda-tools)
18. [Netlist Generation Tools](#netlist-generation-tools)
19. [Advanced Workflow: Complete Example](#advanced-workflow-complete-example)
20. [Limitations & Considerations](#limitations--considerations)

---

## Executive Summary

### Best Approach for Claude Code Agent

The optimal workflow combines several tools:

| Capability | Recommended Tool | Notes |
|------------|------------------|-------|
| **Primary Control** | [KiCad MCP Server](https://github.com/Finerestaurant/kicad-mcp-python) | Uses official IPC-API, most stable |
| **Auto-routing** | [FreeRouting](https://github.com/freerouting/freerouting) + CLI | Available via Plugin Manager |
| **Component Selection** | [easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py) + JLCPCB Tools | Access LCSC/JLCPCB library |
| **Visual Inspection** | `kicad-cli pcb render` + gerbv | Headless raytracing + Gerber rendering |
| **Fabrication Files** | [KiBot](https://github.com/INTI-CMNB/KiBot) | Complete CI/CD automation |
| **Ordering** | [JLCPCB API](https://api.jlcpcb.com/) | Programmatic ordering available |

**Key Requirement:** KiCad 9.0+ is essential for the IPC API and modern MCP server support.

---

## MCP Servers for KiCad

### 1. kicad-mcp-python (Recommended)

**Repository:** [github.com/Finerestaurant/kicad-mcp-python](https://github.com/Finerestaurant/kicad-mcp-python)

Uses KiCad's **official IPC-API** for the most stable and reliable interaction.

**Key Features:**
- Board analysis with screenshots via `get_board_status`
- Create, modify, and analyze PCB layouts
- Schematic manipulation
- Most stable due to official API usage

**Requirements:**
- KiCad 9.0+
- Python 3.8+
- IPC API enabled in KiCad Preferences > Plugins

---

### 2. KiCAD-MCP-Server by mixelpixx

**Repository:** [github.com/mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server)

**Features:**
- 59 tools organized into functional categories
- IPC-enabled commands: `route_trace`, `add_via`, `place_component`, `move_component`, `delete_component`, `add_copper_pour`, `refill_zones`, `add_board_outline`, `add_mounting_hole`
- Auto-detection in Claude Code

---

### 3. kicad-mcp by lamaalrajih

**Repository:** [github.com/lamaalrajih/kicad-mcp](https://github.com/lamaalrajih/kicad-mcp)

**Features:**
- Design Rule Checking via KiCad CLI
- PCB Visualization generation
- Circuit Pattern Recognition
- Works with Claude Desktop, VSCode Cline extension

---

## KiCad Programmatic Control

### Option 1: IPC API (KiCad 9.0+) - Recommended

The new IPC API is the future-proof approach:

```bash
pip install kicad-python
```

**Documentation:** [docs.kicad.org/kicad-python-main](https://docs.kicad.org/kicad-python-main/)

**Requirements:**
- KiCad must be running with API server enabled
- Uses Protocol Buffers + nng for IPC

**Deprecation Notice:** SWIG bindings deprecated in KiCad 9.0, removed in KiCad 10.0 (Feb 2026)

---

### Option 2: kicad-cli (Headless Operations)

```bash
# Run DRC
kicad-cli pcb drc --output drc_report.txt board.kicad_pcb

# Run ERC
kicad-cli sch erc --output erc_report.txt schematic.kicad_sch

# Export Gerbers
kicad-cli pcb export gerbers board.kicad_pcb

# Export 3D render (PNG/JPEG with raytracing)
kicad-cli pcb render --output render.png --width 1920 --height 1080 board.kicad_pcb

# Export SVG
kicad-cli pcb export svg board.kicad_pcb
kicad-cli sch export svg schematic.kicad_sch
```

**Documentation:** [docs.kicad.org/9.0/en/cli/cli.html](https://docs.kicad.org/9.0/en/cli/cli.html)

---

### Option 3: kigadgets (Cross-Version Support)

**Repository:** [github.com/atait/kicad-python](https://github.com/atait/kicad-python)

Works with KiCad 5.0 through 9.0, abstracts API differences.

```bash
pip install kigadgets
```

---

### Option 4: Direct S-Expression Manipulation

KiCad files use s-expression format. Libraries for direct file manipulation:

- **kicad-sch-api**: [forum.kicad.info/t/kicad-sch-api](https://forum.kicad.info/t/kicad-sch-api-python-library-for-kicad-schematic-manipulation/65363)
- No KiCad installation required
- Useful for batch operations

---

## Auto-Routing Solutions

### 1. FreeRouting (Primary Choice)

**Repository:** [github.com/freerouting/freerouting](https://github.com/freerouting/freerouting)

**Installation:** Available via KiCad Plugin and Content Manager

**Features:**
- Specctra/Electra DSN interface
- GUI, CLI, and API interfaces
- Exports .ses session files back to KiCad

**CLI Usage:**
```bash
java -jar freerouting.jar -de input.dsn -do output.ses
```

**Alternative Plugin:** [github.com/jharris2268/kicad-freerouting-plugin-alt](https://forum.kicad.info/t/an-alternative-freerouting-plugin/52736)
- Command-line only version
- Updates tracks in pcbnew as it runs

---

### 2. OrthoRoute (GPU-Accelerated)

**Website:** [bbenchoff.github.io/pages/OrthoRoute.html](https://bbenchoff.github.io/pages/OrthoRoute.html)

- GPU-accelerated using Manhattan lattice + PathFinder algorithm
- Built as KiCad plugin using IPC API
- Handles complex designs with thousands of nets
- Requires significant VRAM (tested on 80GB A100)

**Use Case:** Very large/complex boards where FreeRouting would take too long

---

### 3. Interactive Router (Built-in)

KiCad's native push-and-shove router can be controlled via Python API for semi-automated routing.

---

## JLCPCB Integration

### Plugin: kicad-jlcpcb-tools

**Repository:** [github.com/Bouni/kicad-jlcpcb-tools](https://github.com/Bouni/kicad-jlcpcb-tools)

**Features:**
- Generate BOM + CPL files for JLCPCB
- Assign LCSC part numbers directly from plugin
- Query JLCPCB parts database
- Lookup datasheets
- Outputs `GERBER-<project>.zip`, `BOM-<project>.csv`, `CPL-<project>.csv`

**Access:** Tools > External Plugins > JLCPCB Tools

---

### Plugin: Fabrication Toolkit

**Repository:** [github.com/bennymeg/Fabrication-Toolkit](https://github.com/bennymeg/Fabrication-Toolkit)

**CLI Support for Automation:**
```bash
python3 -m plugins.cli -p /myProject/myBoard.kicad_pcb \
  --additionalLayers \
  --autoTranslate \
  --autoFill \
  --excludeDNP
```

---

### JLCPCB API (Programmatic Ordering)

**API Portal:** [api.jlcpcb.com](https://api.jlcpcb.com/)

**Available APIs:**
| API | Capabilities |
|-----|--------------|
| PCB API | Real-time quotations, ordering, order lifecycle tracking |
| Stencil API | SMD stencil procurement, automatic quoting |
| 3D Printing API | Multi-material additive manufacturing |
| Components API | Access to millions of components, real-time pricing |

**Features:**
- File uploading
- Automatic pricing
- Ordering
- Order status tracking

**Requirements:**
- Apply for API access at api.jlcpcb.com
- Intended for companies with regular order volume

---

### KiKit (Automation Tool)

**Documentation:** [yaqwsx.github.io/KiKit/v1.4/fabrication/jlcpcb/](https://yaqwsx.github.io/KiKit/v1.4/fabrication/jlcpcb/)

```bash
pip install kikit
```

Panelization and JLCPCB fabrication file generation.

---

## Component Selection & Libraries

### JLCPCB KiCad Library

**Repository:** [github.com/CDFER/JLCPCB-Kicad-Library](https://github.com/CDFER/JLCPCB-Kicad-Library)

- Full KiCad library: schematic symbols, footprints, 3D STEP models
- Focused on JLCPCB basic/preferred parts (no extra setup costs)

---

### easyeda2kicad (Import Any LCSC Component)

**Repository:** [github.com/uPesy/easyeda2kicad.py](https://github.com/uPesy/easyeda2kicad.py)

```bash
pip install easyeda2kicad

# Full component (symbol + footprint + 3D)
easyeda2kicad --full --lcsc_id=C2040

# Individual exports
easyeda2kicad --symbol --lcsc_id=C2040
easyeda2kicad --footprint --lcsc_id=C2040
easyeda2kicad --3d --lcsc_id=C2040
```

**Output:**
- `easyeda2kicad.kicad_sym` - Symbol library
- `easyeda2kicad.pretty/` - Footprints
- `easyeda2kicad.3dshapes/` - 3D models (WRL + STEP)

**KiCad Plugin:** [github.com/rasmushauschild/easyeda2kicad_plugin](https://github.com/rasmushauschild/easyeda2kicad_plugin)

---

### JLC2KICAD_lib

Automatically generates component library from JLCPCB/EasyEDA.

**SQLite Database:** Automatically updated database of JLCPCB parts filtered to in-stock items.

---

## Visual Inspection Tools

### 1. kicad-cli pcb render (Recommended)

Built-in raytraced 3D rendering:

```bash
# Basic render
kicad-cli pcb render --output board.png board.kicad_pcb

# High-res with options
kicad-cli pcb render \
  --output board.png \
  --width 3840 \
  --height 2160 \
  --side top \
  --background opaque \
  --quality high \
  board.kicad_pcb
```

**Options:**
- `--side`: top, bottom, front, back, left, right
- `--perspective`: Enable perspective projection
- `--zoom`: Zoom factor
- `--rotate`: Custom rotation angles
- `--light-*`: Customize lighting

---

### 2. gerbv (Gerber Viewer)

**Website:** [gerbv.github.io](https://gerbv.github.io/)

Headless Gerber to image conversion:

```bash
gerbv -x png -o output.png -D 600 -a top.gbr bottom.gbr drill.drl

# Options:
# -x: export format (png/pdf/ps/svg)
# -o: output filename
# -D: DPI resolution
# -a: antialiasing
# -b: background color (hex)
# -f: foreground color (hex)
```

---

### 3. tracespace

**Repository:** [github.com/tracespace/tracespace](https://github.com/tracespace/tracespace)
**Online Viewer:** [tracespace.io/view](https://tracespace.io/view/)

- Generates beautiful SVG renders from Gerber/drill files
- Works in Node.js and browser
- Accepts ZIP files

---

### 4. KiCad 3D Viewer Export

From command line:
```bash
kicad-cli pcb export step --output model.step board.kicad_pcb
kicad-cli pcb export glb --output model.glb board.kicad_pcb
kicad-cli pcb export vrml --output model.wrl board.kicad_pcb
```

Can be rendered in external 3D software (Blender, Fusion 360).

---

### 5. SVG Export for Schematics

```bash
kicad-cli sch export svg --output schematic_output/ schematic.kicad_sch
```

Each sheet exports to its own SVG file.

---

### 6. KiCanvas (Browser-based Viewer)

**Website:** [kicanvas.org](https://kicanvas.org/)
**GitHub:** [github.com/theacodes/kicanvas](https://github.com/theacodes/kicanvas)

Interactive, browser-based KiCad viewer:

**Features:**
- Parse and display KiCad files directly in-browser
- Load local files or pull from GitHub
- Embeddable `<kicanvas-viewer>` element for documentation
- Written in TypeScript, uses Canvas/WebGL

**Use Cases:**
- Share designs without requiring KiCad installation
- Embed in documentation and tutorials
- Quick visual review from CI/CD pipelines

**Note:** Currently in early alpha, supports KiCad 7+ features.

---

## DRC/ERC Automation & Cleanup

### kicad-cli (Built-in)

```bash
# Run DRC with exit code on violations
kicad-cli pcb drc \
  --output drc_report.json \
  --format json \
  --exit-code-violations \
  board.kicad_pcb

# Run ERC
kicad-cli sch erc \
  --output erc_report.json \
  --format json \
  schematic.kicad_sch
```

---

### KiBot

**Repository:** [github.com/INTI-CMNB/KiBot](https://github.com/INTI-CMNB/KiBot)

```bash
pip install kibot
```

**Configuration (kibot.yaml):**
```yaml
preflight:
  run_erc: true
  run_drc: true
  check_zone_fills: true
  update_xml: true
```

---

### KiAuto

**Repository:** [github.com/INTI-CMNB/KiAuto](https://github.com/INTI-CMNB/KiAuto)

```bash
pip install kiauto

# Run DRC with filter file
pcbnew_do run_drc -f FILTER_FILE board.kicad_pcb output/
```

**Filter Files:** Use regex to exclude specific warnings/errors.

---

### KiPadCheck

**Repository:** [github.com/HiGregSmith/KiPadCheck](https://github.com/HiGregSmith/KiPadCheck)

Extra DRC checks for:
- Drill holes
- Pads
- Paste layers
- Silkscreen

---

### kicad-automation-scripts

**Repository:** [github.com/productize/kicad-automation-scripts](https://github.com/productize/kicad-automation-scripts)

Uses xdotool for UI automation when API is insufficient.

**Docker Available:** `docker run` for consistent environments.

---

## Code-First Design Tools

### SKiDL (Python)

**Repository:** [github.com/devbisme/skidl](https://github.com/devbisme/skidl)

```bash
pip install skidl
```

```python
from skidl import *

# Create circuit with code
r = Part('Device', 'R', value='10K', footprint='Resistor_SMD:R_0805_2012Metric')
c = Part('Device', 'C', value='100nF', footprint='Capacitor_SMD:C_0805_2012Metric')

# Connect
r[1] += Net('VCC')
r[2] += c[1]
c[2] += Net('GND')

# Generate netlist for KiCad
generate_netlist()

# Or directly to PCB
generate_pcb()
```

**Benefits:**
- Version control friendly
- Parametric designs
- Algorithmic circuit generation
- Built-in ERC

---

### atopile

**Website:** [atopile.io](https://atopile.io/)

```bash
pip install atopile
```

- Declarative `.ato` files
- Automatic parametric component picking
- Deep validation
- Native KiCad integration
- JLCPCB ordering from CI

**Example:**
```
module MyBoard:
    power = new PowerSupply(voltage=3.3V)
    mcu = new ESP32S3()
    mcu.vcc ~ power.output
```

---

### tscircuit (React/TypeScript)

**Website:** [tscircuit.com](https://tscircuit.com/)
**GitHub:** [github.com/tscircuit/tscircuit](https://github.com/tscircuit/tscircuit)

Design electronics using React components:

```tsx
import { Resistor, Capacitor, Led, Board } from "tscircuit"

export const MyCircuit = () => (
  <Board>
    <Resistor name="R1" value="330" footprint="0805" />
    <Led name="LED1" footprint="0805" />
    <trace from=".R1 > .2" to=".LED1 > .anode" />
  </Board>
)
```

**Features:**
- React/TypeScript syntax for circuit design
- Automatic autorouting and part selection
- KiCad import/export via CircuitJSON
- Export to Gerbers, BOM, Pick-and-Place
- JLC and PCBWay manufacturing export
- Visual schematic and PCB rendering in browser

**KiCad Integration:**
```bash
# Import KiCad footprints
footprint="kicad:Resistor_SMD/R_0402_1005Metric"
```

---

## CI/CD Automation

### KiBot (Comprehensive Solution)

**Repository:** [github.com/INTI-CMNB/KiBot](https://github.com/INTI-CMNB/KiBot)

**Docker Image:** `ghcr.io/inti-cmnb/kicad9_auto:latest`

**Example kibot.yaml:**
```yaml
kibot:
  version: 1

preflight:
  run_erc: true
  run_drc: true
  check_zone_fills: true

outputs:
  - name: gerbers
    type: gerber
    dir: gerbers
    layers:
      - F.Cu
      - B.Cu
      - F.SilkS
      - B.SilkS
      - F.Mask
      - B.Mask
      - Edge.Cuts

  - name: drill
    type: excellon
    dir: gerbers

  - name: bom
    type: bom
    dir: docs

  - name: 3d_render
    type: render_3d
    dir: images
```

---

### GitHub Actions Example

```yaml
name: KiCad CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    container: ghcr.io/inti-cmnb/kicad9_auto:latest

    steps:
      - uses: actions/checkout@v3

      - name: Run KiBot
        run: kibot -c kibot.yaml

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: fabrication-files
          path: |
            gerbers/
            docs/
            images/
```

---

### KDT Template (Professional)

**Repository:** [github.com/nguyen-v/KDT_Hierarchical_KiBot](https://github.com/nguyen-v/KDT_Hierarchical_KiBot)

Pre-configured template with:
- Stackup tables
- Fabrication notes
- Drill drawings
- Testpoint tables
- Assembly documents

---

## Recommended Agent Workflow

### Complete AI Agent Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE AGENT WORKFLOW                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. DESIGN CREATION                                              │
│     ├── Option A: SKiDL/atopile → Generate schematic via code   │
│     └── Option B: MCP Server → Create/modify KiCad project       │
│                                                                  │
│  2. COMPONENT SELECTION                                          │
│     ├── easyeda2kicad --full --lcsc_id=CXXXXX                   │
│     └── Query JLCPCB parts database for availability             │
│                                                                  │
│  3. SCHEMATIC VALIDATION                                         │
│     └── kicad-cli sch erc → Check for electrical errors          │
│                                                                  │
│  4. PCB LAYOUT                                                   │
│     ├── MCP Server → Place components                            │
│     └── kigadgets → Programmatic placement                       │
│                                                                  │
│  5. AUTO-ROUTING                                                 │
│     ├── Export DSN: kicad-cli pcb export dsn                    │
│     ├── Route: java -jar freerouting.jar -de in.dsn -do out.ses │
│     └── Import SES back to KiCad                                 │
│                                                                  │
│  6. DRC CHECK                                                    │
│     └── kicad-cli pcb drc --exit-code-violations                 │
│                                                                  │
│  7. VISUAL INSPECTION                                            │
│     ├── kicad-cli pcb render → 3D raytraced PNG                 │
│     ├── gerbv -x png → Gerber layer images                       │
│     └── AI reviews images for issues                             │
│                                                                  │
│  8. CLEANUP & FIXES                                              │
│     ├── MCP Server → Modify traces/components                    │
│     └── Repeat DRC/Visual until clean                            │
│                                                                  │
│  9. FABRICATION FILES                                            │
│     ├── KiBot → Generate all outputs                             │
│     └── kicad-jlcpcb-tools → JLCPCB-ready files                  │
│                                                                  │
│ 10. ORDERING (Optional)                                          │
│     └── JLCPCB API → Automated PCB order                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tool Installation Summary

### Essential Tools

```bash
# KiCad 9.0+ (required for IPC API)
# Install from: https://www.kicad.org/download/

# Python packages
pip install kicad-python      # Official IPC API bindings
pip install kigadgets         # Cross-version compatibility
pip install kibot             # CI/CD automation
pip install kiauto            # Automation scripts
pip install easyeda2kicad     # LCSC component import
pip install skidl             # Code-first design
pip install atopile           # Hardware design language

# FreeRouting
# Install via KiCad Plugin Manager or:
# Download from: https://github.com/freerouting/freerouting/releases

# Gerber viewer
brew install gerbv  # macOS
apt install gerbv   # Linux

# Node.js tools
npm install -g tracespace-cli
```

### KiCad Plugins (via Plugin Manager)

- FreeRouting
- JLCPCB Tools
- Fabrication Toolkit
- easyeda2kicad

### MCP Servers

```bash
# Clone and configure (example)
git clone https://github.com/Finerestaurant/kicad-mcp-python
cd kicad-mcp-python
pip install -r requirements.txt
```

---

## Sources

### MCP Servers
- [KiCAD-MCP-Server by mixelpixx](https://github.com/mixelpixx/KiCAD-MCP-Server)
- [kicad-mcp by lamaalrajih](https://github.com/lamaalrajih/kicad-mcp)
- [kicad-mcp-python by Finerestaurant](https://github.com/Finerestaurant/kicad-mcp-python)

### KiCad Documentation
- [KiCad CLI Documentation](https://docs.kicad.org/9.0/en/cli/cli.html)
- [KiCad IPC API Developer Docs](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/)
- [KiCad Python Bindings](https://docs.kicad.org/kicad-python-main/)

### Auto-routing
- [FreeRouting GitHub](https://github.com/freerouting/freerouting)
- [FreeRouting Plugin Guide](https://www.protoexpress.com/blog/how-to-autoroute-pcb-layout-in-kicad-using-freerouting-plugin/)
- [OrthoRoute](https://bbenchoff.github.io/pages/OrthoRoute.html)
- [Alternative FreeRouting Plugin](https://forum.kicad.info/t/an-alternative-freerouting-plugin/52736)

### JLCPCB Integration
- [kicad-jlcpcb-tools](https://github.com/Bouni/kicad-jlcpcb-tools)
- [Fabrication Toolkit](https://github.com/bennymeg/Fabrication-Toolkit)
- [JLCPCB API Platform](https://api.jlcpcb.com/)
- [JLCPCB KiCad Library](https://github.com/CDFER/JLCPCB-Kicad-Library)
- [KiKit JLC Fabrication](https://yaqwsx.github.io/KiKit/v1.4/fabrication/jlcpcb/)

### Component Libraries
- [easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py)
- [easyeda2kicad Plugin](https://github.com/rasmushauschild/easyeda2kicad_plugin)

### Visualization
- [gerbv](https://gerbv.github.io/)
- [tracespace](https://github.com/tracespace/tracespace)
- [KiCad 3D Viewer](https://www.kicad.org/discover/3dviewer/)

### Automation
- [KiBot](https://github.com/INTI-CMNB/KiBot)
- [KiAuto](https://github.com/INTI-CMNB/KiAuto)
- [kicad-automation-scripts](https://github.com/productize/kicad-automation-scripts)
- [KiCad 9 CI/CD Guide](https://sschueller.github.io/posts/ci-cd-with-kicad-2025/)

### Code-First Design
- [SKiDL](https://github.com/devbisme/skidl)
- [atopile](https://atopile.io/)
- [kigadgets](https://github.com/atait/kicad-python)
- [tscircuit](https://tscircuit.com/)

### Component Placement
- [kicad-parts-placer](https://github.com/snhobbs/kicad-parts-placer)
- [kicad_component_layout](https://github.com/mcbridejc/kicad_component_layout)
- [kicad-kbplacer](https://github.com/adamws/kicad-kbplacer)
- [Autocuro AI Routing](https://autocuro.com/blog/how-we-automate-kicad-pcb-routing)

### Visualization & Viewers
- [KiCanvas](https://kicanvas.org/)
- [InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom)

### Alternative EDA
- [pcb-rnd](http://repo.hu/projects/pcb-rnd/)

### PCB Ordering
- [JLCPCB API](https://api.jlcpcb.com/)
- [PCBWay API Cooperation](https://www.pcbway.com/api_cooperation.html)
- [OSH Park](https://oshpark.com/)

### KiCad Forum Discussions
- [KiCad 9.0 Python API Discussion](https://forum.kicad.info/t/kicad-9-0-python-api-ipc-api/57236)
- [KiCad MCP Server Discussion](https://forum.kicad.info/t/kicad-mcp-server/60704)

---

## Component Placement Automation

### kicad-parts-placer

**Repository:** [github.com/snhobbs/kicad-parts-placer](https://github.com/snhobbs/kicad-parts-placer)
**PyPI:** [pypi.org/project/kicad-parts-placer](https://pypi.org/project/kicad-parts-placer/)

```bash
pip install kicad-parts-placer
```

- Auto-place components from centroid file
- Useful for maintaining common board form factors
- Group components for batch positioning

---

### kicad_component_layout

**Repository:** [github.com/mcbridejc/kicad_component_layout](https://github.com/mcbridejc/kicad_component_layout)

Write a script to generate `layout.yaml`, then sync to PCB design:
- Change positions, rotation, flip status
- Modify footprints based on designators
- Works via KiCad plugin

---

### kicad-kbplacer (Keyboard-specific)

**Repository:** [github.com/adamws/kicad-kbplacer](https://github.com/adamws/kicad-kbplacer)

- Automatic keyboard key placement and routing
- Convex hull board edge generation
- Executable as Python module: `python -m kbplacer`

---

### Autocuro (AI-based)

**Website:** [autocuro.com](https://autocuro.com/blog/how-we-automate-kicad-pcb-routing)

- AI-driven placement and routing
- Works with KiCad 8 and 9
- Uses KiCad Python scripting

---

## Interactive BOM Visualization

### InteractiveHtmlBom

**Repository:** [github.com/openscopeproject/InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom)
**Demo:** [openscopeproject.org/InteractiveHtmlBomDemo](https://openscopeproject.org/InteractiveHtmlBomDemo/)

**Features:**
- Interactive HTML BOM for manual assembly
- Visual component highlighting on PCB image
- Reverse lookup by clicking footprints
- Net highlighting for troubleshooting
- Fully self-contained HTML (no internet needed)
- Supports KiCad, Eagle, Fusion360, Allegro, EasyEDA

**Installation:**
```bash
# Via pip (for script usage)
pip install interactivehtmlbom

# Via KiCad Plugin Manager
# Search for "Interactive Html Bom"
```

**CLI Usage:**
```bash
generate_interactive_bom --dest-dir output/ board.kicad_pcb
```

---

## Alternative PCB Ordering APIs

### PCBWay

**API Portal:** [pcbway.com/api_cooperation.html](https://www.pcbway.com/api_cooperation.html)

- API cooperation program available
- Contact required for API access
- Features: instant quotes, file upload, order tracking

---

### OSH Park

**Website:** [oshpark.com](https://oshpark.com/)

- Direct KiCad/Eagle file upload (no Gerber conversion needed)
- Project sharing for open hardware
- No public API for automated ordering
- Focus on quality (especially "After Dark" service)

---

### Comparison

| Vendor | API | Best For |
|--------|-----|----------|
| JLCPCB | Full REST API | Production, SMT assembly |
| PCBWay | Contact for access | Custom requirements |
| OSH Park | No public API | Prototypes, quality |

---

## Alternative EDA Tools

### pcb-rnd

**Website:** [repo.hu/projects/pcb-rnd](http://repo.hu/projects/pcb-rnd/)

Modular PCB layout editor optimized for automation:

**Features:**
- Command-line interface for batch processing
- Query language for design analysis
- Multiple file format support (Eagle, KiCad compatible)
- Scripting-first design philosophy
- Part of Ringdove EDA Suite (sch-rnd, camv-rnd, route-rnd)

**Use Case:** CI pipelines, research, custom automation workflows

**Version:** 3.1.7 (May 2025)

---

## Netlist Generation Tools

### nl2sch (Netlist to Schematic)

**Repository:** [github.com/tpecar/nl2sch](https://github.com/tpecar/nl2sch)

- Convert PCB netlist back to schematic
- Useful for reverse engineering or documentation
- Requires Python 3.9+

---

### SKiDL Output Formats

SKiDL supports multiple netlist/output formats:
- KiCad netlist (.net)
- XML for BOM generation
- Direct .kicad_pcb generation
- SVG schematics
- DOT graphs for documentation

---

## Advanced Workflow: Complete Example

### Automated PCB Design Script

```python
#!/usr/bin/env python3
"""
Complete agent workflow example
"""
import subprocess
import os

# Step 1: Create circuit with SKiDL
from skidl import *

@subcircuit
def create_led_driver():
    mcu = Part('MCU_Microchip_ATmega', 'ATmega328P-AU',
               footprint='Package_QFP:TQFP-32_7x7mm_P0.8mm')
    led = Part('Device', 'LED', footprint='LED_SMD:LED_0805_2012Metric')
    r = Part('Device', 'R', value='330', footprint='Resistor_SMD:R_0805_2012Metric')

    mcu['PB5'] += r[1]
    r[2] += led[1]
    led[2] += Net('GND')

    return mcu

circuit = create_led_driver()
generate_netlist()

# Step 2: Import components from JLCPCB
subprocess.run(['easyeda2kicad', '--full', '--lcsc_id=C14877'])  # ATmega328P

# Step 3: Run ERC
subprocess.run(['kicad-cli', 'sch', 'erc',
                '--output', 'erc_report.json',
                '--format', 'json',
                'project.kicad_sch'])

# Step 4: Export DSN for autorouting
subprocess.run(['kicad-cli', 'pcb', 'export', 'dsn',
                '--output', 'board.dsn',
                'project.kicad_pcb'])

# Step 5: Autoroute with FreeRouting
subprocess.run(['java', '-jar', 'freerouting.jar',
                '-de', 'board.dsn',
                '-do', 'board.ses'])

# Step 6: Import routed session
# (Done via MCP server or manually)

# Step 7: Run DRC
result = subprocess.run(['kicad-cli', 'pcb', 'drc',
                        '--output', 'drc_report.json',
                        '--format', 'json',
                        '--exit-code-violations',
                        'project.kicad_pcb'])

if result.returncode != 0:
    print("DRC violations found! Check drc_report.json")
    exit(1)

# Step 8: Generate visual inspection images
subprocess.run(['kicad-cli', 'pcb', 'render',
                '--output', 'render_top.png',
                '--side', 'top',
                '--width', '2048',
                '--height', '2048',
                'project.kicad_pcb'])

subprocess.run(['kicad-cli', 'pcb', 'render',
                '--output', 'render_bottom.png',
                '--side', 'bottom',
                'project.kicad_pcb'])

# Step 9: Generate fabrication files with KiBot
subprocess.run(['kibot', '-c', 'kibot.yaml'])

# Step 10: Generate interactive BOM
subprocess.run(['generate_interactive_bom',
                '--dest-dir', 'docs/',
                'project.kicad_pcb'])

print("Design complete! Files ready for ordering.")
```

---

## Next Steps for Implementation

1. **Install KiCad 9.0+** with IPC API enabled
2. **Set up MCP Server** (kicad-mcp-python recommended)
3. **Configure JLCPCB Tools** for component selection
4. **Install FreeRouting** for auto-routing
5. **Set up KiBot** for CI/CD automation
6. **Apply for JLCPCB API access** if automated ordering needed
7. **Test visual inspection pipeline** with `kicad-cli pcb render` and `gerbv`
8. **Install InteractiveHtmlBom** for assembly documentation
9. **Set up kicad-parts-placer** for component placement automation

---

## Limitations & Considerations

### What Works Well for AI Agents

- **Schematic creation** via SKiDL/atopile (code-first approach)
- **Component selection** from JLCPCB library (well-documented)
- **Auto-routing** with FreeRouting (predictable CLI interface)
- **DRC/ERC checking** via kicad-cli (reliable automation)
- **Visual inspection** via renders and screenshots
- **Fabrication file generation** via KiBot (comprehensive)

### Current Challenges

1. **Interactive editing**: MCP servers are improving but still maturing
2. **Complex placement**: AI may struggle with optimal component placement
3. **High-frequency/analog**: Auto-routing not suitable for RF/sensitive signals
4. **Custom requirements**: Some designs need human expertise
5. **JLCPCB API access**: Requires application and approval

### Recommendations

- Use **code-first design** (SKiDL/atopile) for repeatable circuits
- Keep **human review** in the loop for critical designs
- Start with **simple boards** to validate workflow
- Use **CI/CD** for regression testing design changes

---

*Last Updated: December 30, 2025*
