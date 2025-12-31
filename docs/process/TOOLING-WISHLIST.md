# Tooling Wishlist for PCB Development

Tools that would significantly improve Claude Code's ability to work with KiCad and PCB projects.

---

## Already Exists in KiCad 9 CLI

Reference these capabilities - they're already available!

### PCB Operations (`kicad-cli pcb`)

```bash
# 3D Rendering
kicad-cli pcb render --side front --output front.png project.kicad_pcb
kicad-cli pcb render --side back --width 1600 --height 1200 project.kicad_pcb

# Design Rules Check
kicad-cli pcb drc --output drc-report.json project.kicad_pcb

# Gerber Export
kicad-cli pcb export gerbers --output gerbers/ project.kicad_pcb

# Drill Files
kicad-cli pcb export drill --output gerbers/ --format excellon project.kicad_pcb

# Pick-and-Place / Position File
kicad-cli pcb export pos --output positions.csv --format csv project.kicad_pcb

# 3D Model Export
kicad-cli pcb export step --output board.step project.kicad_pcb
kicad-cli pcb export vrml --output board.wrl project.kicad_pcb
kicad-cli pcb export glb --output board.glb project.kicad_pcb

# 2D Exports
kicad-cli pcb export svg --layers F.Cu,B.Cu --output layers.svg project.kicad_pcb
kicad-cli pcb export pdf --layers F.Cu,B.Cu --output layers.pdf project.kicad_pcb
kicad-cli pcb export dxf --output board.dxf project.kicad_pcb

# Manufacturing Formats
kicad-cli pcb export ipc2581 --output board.xml project.kicad_pcb
kicad-cli pcb export odb --output odb_output/ project.kicad_pcb
```

### Schematic Operations (`kicad-cli sch`)

```bash
# Electrical Rules Check
kicad-cli sch erc --output erc-report.json project.kicad_sch

# Bill of Materials
kicad-cli sch export bom --output bom.csv project.kicad_sch

# Netlist Export
kicad-cli sch export netlist --output netlist.net project.kicad_sch

# PDF/SVG Export
kicad-cli sch export pdf --output schematic.pdf project.kicad_sch
kicad-cli sch export svg --output schematic.svg project.kicad_sch
```

### What's NOT in kicad-cli (gaps to fill)

| Capability | Status | Workaround |
|------------|--------|------------|
| Schematic 3D/image render | Missing | Export SVG/PDF |
| DSN export (autorouting) | Missing | Use KiCad Python |
| SES import (autorouting) | Missing | Use KiCad Python |
| Component placement | Missing | Edit .kicad_pcb directly |
| Net/component queries | Missing | Parse files or use Python |
| Symbol/footprint creation | Limited | Use fp/sym subcommands |

---

## High Priority

### 1. KiCad Python Bridge (MCP Server)

**Problem:** KiCad's Python API (`pcbnew`) only works inside KiCad's bundled Python, requiring complex subprocess calls.

**Desired Tool:** An MCP server that exposes KiCad's Python API.

```json
{
  "tool": "kicad_pcb",
  "action": "get_components",
  "file": "project.kicad_pcb"
}
```

**Capabilities:**
- Read/write PCB properties
- List components with positions
- Get net connections
- Run DRC programmatically
- Export DSN/import SES (for autorouting)
- Modify footprints
- Update 3D model paths

**Implementation:**
```python
# MCP Server using KiCad's Python
from mcp import Server
import pcbnew

@server.tool("kicad.get_components")
def get_components(pcb_path: str):
    board = pcbnew.LoadBoard(pcb_path)
    components = []
    for fp in board.GetFootprints():
        components.append({
            "ref": fp.GetReference(),
            "value": fp.GetValue(),
            "x": fp.GetPosition().x / 1e6,
            "y": fp.GetPosition().y / 1e6,
            "rotation": fp.GetOrientation().AsDegrees()
        })
    return components
```

---

### 2. JLCPCB Parts API Client

**Problem:** Have to manually search JLCPCB website for parts, check stock, verify compatibility.

**Desired Tool:** API client for JLCPCB/LCSC parts database.

```bash
jlcpcb-parts search "100nF 0603" --category basic --in-stock
jlcpcb-parts info C14663  # Get full part details
jlcpcb-parts check-bom bom.csv  # Validate all parts
```

**Features:**
- Search by parameters (value, package, category)
- Filter by Basic/Extended parts
- Real-time stock levels
- Price at quantity breaks
- Footprint/symbol availability
- Datasheet links
- Alternative part suggestions

**Implementation Notes:**
- LCSC has an unofficial API
- Could scrape JLCPCB parts library
- Cache results locally

---

### 3. Schematic Generator Library

**Problem:** Creating schematics programmatically requires understanding KiCad's complex S-expression format.

**Desired Tool:** High-level Python library for schematic generation.

```python
from kicad_schematic import Schematic, Component, Wire, Label

sch = Schematic("project.kicad_sch")

# Add component with automatic symbol lookup
mcu = sch.add_component("ATtiny85", ref="U1", pos=(100, 100))

# Connect pins with automatic wire routing
sch.connect(mcu.pin("VCC"), sch.power("+3V3"))
sch.connect(mcu.pin("GND"), sch.power("GND"))

# Add decoupling cap near power pins
cap = sch.add_component("100nF", ref="C1", near=mcu.pin("VCC"))
sch.connect(cap.pin(1), mcu.pin("VCC"))
sch.connect(cap.pin(2), sch.power("GND"))

sch.save()
```

**Features:**
- Component placement with collision avoidance
- Automatic wire routing
- Symbol library integration
- Hierarchical sheet support
- Net label management
- ERC pre-validation

---

### 4. Gerber Analyzer/Validator

**Problem:** Cannot verify Gerber files without external viewer.

**Desired Tool:** CLI tool to analyze and validate Gerbers.

```bash
gerber-check output/gerbers/ --rules jlcpcb
```

**Output:**
```
Gerber Analysis Report
======================
Board size: 50.0 x 40.0 mm
Layers: 6 (F.Cu, B.Cu, F.Mask, B.Mask, F.Silk, Edge.Cuts)
Drill holes: 45 (min: 0.3mm, max: 3.2mm)

JLCPCB Compatibility:
[PASS] Board size within limits
[PASS] Minimum trace width: 0.15mm (min: 0.127mm)
[PASS] Minimum spacing: 0.15mm (min: 0.127mm)
[PASS] Minimum drill: 0.3mm (min: 0.3mm)
[WARN] Via count: 45 (consider reducing for cost)
[PASS] All layers present

Estimated cost: $2.00 (5 pcs) + $3.00 assembly setup
```

**Features:**
- Parse all Gerber/Excellon formats
- Check against manufacturer DFM rules
- Generate visual diff between versions
- Estimate manufacturing cost
- Detect common issues (acid traps, slivers)

---

## Medium Priority

### 5. Component Footprint Validator

**Problem:** Footprints from various sources may not match actual component dimensions.

**Desired Tool:** Validate footprints against datasheets.

```bash
footprint-check SOIC-8.kicad_mod --datasheet W25Q16JV.pdf
```

**Features:**
- Parse datasheet PDF for package dimensions
- Compare against footprint pads
- Check recommended land pattern
- Verify 3D model alignment
- Generate correction suggestions

---

### 6. BOM Intelligence Tool

**Problem:** Manual effort to find equivalent parts, check lifecycle, verify specs.

**Desired Tool:** Smart BOM analysis and optimization.

```bash
bom-intel analyze bom.csv --optimize cost --constraints jlcpcb-basic
```

**Features:**
- Find cheaper equivalent parts
- Check component lifecycle (active, NRND, obsolete)
- Verify specifications meet requirements
- Suggest Basic parts to replace Extended
- Multi-source availability check
- Risk assessment (single source, low stock)

---

### 7. PCB Diff Tool

**Problem:** Hard to see what changed between PCB versions.

**Desired Tool:** Visual and text diff for KiCad files.

```bash
pcb-diff v1.0/project.kicad_pcb v1.1/project.kicad_pcb --output diff.html
```

**Features:**
- Layer-by-layer visual diff
- Component movement highlighting
- Net changes summary
- New/removed components
- Copper pour differences
- Generate change report

---

### 8. Design Rule Generator

**Problem:** Manually setting up design rules for each manufacturer.

**Desired Tool:** Import manufacturer capabilities as KiCad design rules.

```bash
design-rules import jlcpcb --layers 2 --copper 1oz > project.kicad_dru
```

**Features:**
- Preset rules for common manufacturers (JLCPCB, PCBWay, OSHPark)
- Layer-count aware rules
- Copper weight adjustments
- Via-in-pad rules
- Impedance control rules
- Export as KiCad design rules file

---

### 9. Autorouter Integration

**Problem:** FreeRouting requires Java, manual file conversion, GUI interaction.

**Desired Tool:** Seamless autorouter integration.

```bash
autoroute project.kicad_pcb --engine freerouting --passes 10
```

**Features:**
- Direct PCB file input/output
- Multiple engine support (FreeRouting, others)
- Configurable routing parameters
- Partial routing (specific nets only)
- Progress reporting
- Quality metrics

---

## Lower Priority (Nice to Have)

### 10. 3D Model Fetcher

**Problem:** Finding and placing 3D models is tedious.

**Desired Tool:** Automatically fetch 3D models for components.

```bash
model-fetch --bom bom.csv --output libs/3dmodels/
```

**Sources:**
- SnapEDA
- Ultra Librarian
- Component manufacturer websites
- GrabCAD

---

### 11. Test Point Suggester

**Problem:** Forgetting to add test points for debugging.

**Desired Tool:** Analyze design and suggest test points.

```bash
testpoint-suggest project.kicad_sch --output suggestions.md
```

**Suggestions:**
- Power rails (VCC, GND)
- Clock signals
- Communication buses (SPI, I2C)
- Analog signals
- Reset lines

---

### 12. Power Integrity Analyzer

**Problem:** Can't easily verify power distribution is adequate.

**Desired Tool:** Analyze power delivery network.

```bash
power-check project.kicad_pcb --load-profile loads.csv
```

**Analysis:**
- DC IR drop estimation
- Decoupling capacitor placement
- Via current capacity
- Trace width vs current
- Thermal hotspots

---

### 13. Interactive Component Placer

**Problem:** Component placement is done blind when generating PCB programmatically.

**Desired Tool:** Web-based component placement assistant.

```bash
place-assist project.kicad_pcb --serve 8080
```

**Features:**
- Drag-and-drop in browser
- Real-time DRC feedback
- Ratsnest visualization
- Save back to KiCad file
- Placement suggestions based on schematic

---

## Implementation Priorities

If building these tools, recommended order:

1. **KiCad Python Bridge (MCP)** - Unlocks DSN/SES export, component queries, everything pcbnew can do
2. **JLCPCB Parts API** - Critical for component selection phase, stock checking
3. **Gerber Validator** - DFM checking against manufacturer rules (kicad-cli has DRC, but not manufacturer-specific)
4. **Schematic Generator** - High-level API for creating schematics programmatically

**Note:** Headless rendering already exists via `kicad-cli pcb render`

---

## Existing Tools to Leverage

| Need | Existing Tool | Gap |
|------|---------------|-----|
| PCB rendering | `kicad-cli pcb render` | Works great! |
| DRC | `kicad-cli pcb drc` | No manufacturer-specific rules |
| ERC | `kicad-cli sch erc` | Works great! |
| Gerber export | `kicad-cli pcb export gerbers` | Works great! |
| Gerber viewing | gerbv, KiCad viewer | No CLI DFM analysis |
| Autorouting | FreeRouting | Java dependency, no direct CLI integration |
| 3D models | KiCad libraries | Incomplete coverage |
| Parts search | Octopart API | Not JLCPCB-specific |
| Schematic gen | skidl, pykicad | Limited, outdated |
| DSN/SES export | KiCad Python (pcbnew) | Not in kicad-cli |

---

## Notes for Implementation

**Tech Stack Suggestions:**
- Python for most tools (matches KiCad ecosystem)
- Rust for performance-critical (Gerber parsing)
- TypeScript for web-based tools
- Docker for isolation and reproducibility

**MCP Server Architecture:**
```
Claude Code <──> MCP Protocol <──> KiCad MCP Server
                                        │
                                        ├── pcbnew module
                                        ├── eeschema module
                                        └── render service
```

**Packaging:**
- Homebrew formula for macOS
- pip package for Python tools
- npm package for web tools
- Single binary with Nix for all platforms
