# KiCad Agent Skill

This skill guides autonomous PCB design from requirements to fabrication.

## Activation

Use this skill when user provides PCB project requirements.

## Workflow Overview

```
Requirements → Component Selection → Library Import → Schematic → Layout → Routing → DRC → Export → Order
```

## Phase 1: Requirements Gathering

When user provides project requirements, capture in `kicad/specs.md`:

**Required info:**
- Project name/purpose
- Key components (MCU, sensors, connectors)
- Power requirements (voltage, current)
- I/O requirements

**Ask user if not specified:**
- Board dimensions (or "optimize for size")
- Layer count (default: 2)
- Surface finish (default: HASL lead-free)
- Solder mask color (default: green)
- Silkscreen color (default: white)
- PCB thickness (default: 1.6mm)
- Assembly by JLCPCB? (default: yes, SMT only)

## Phase 2: Component Selection

For each required component:

1. **Search LCSC** for parts:
   - Use WebFetch or Perplexity to find LCSC C-numbers
   - Check stock levels and pricing
   - Verify voltage/current specs match requirements

2. Document in `kicad/component-selection.md`:
   - LCSC part number (C-number)
   - Manufacturer part number
   - Package/footprint
   - Key specs (voltage, current, pins)
   - Price and stock status
   - JLCPCB assembly type (basic/extended)

3. **CRITICAL:** Verify JLCPCB assembly availability:
   - Basic parts: no extra fee
   - Extended parts: $3 setup fee per unique part
   - If out of stock: find alternative

**Common Issue:** Many specialty chips (e.g., MH2024K, WT2003S, JQ6500) are NOT on LCSC.
Always verify availability before committing to a design.

## Phase 2.5: Library Import with easyeda2kicad

Import LCSC components with symbols, footprints, and 3D models:

```bash
# Setup
mkdir -p kicad/libs kicad/3dmodels
cd kicad
source ../venv/bin/activate

# Import component (creates symbol, footprint, and 3D model)
easyeda2kicad --lcsc_id CXXXXXX --full --output libs/project.kicad_sym
```

**What gets created:**
- `libs/project.kicad_sym` - Symbol library
- `libs/project.pretty/` - Footprint library folder
- `libs/project.3dshapes/` - 3D models (.wrl and .step)

**Important notes:**
- Each `--full` call adds to the same library file
- Some parts may fail to import (no EasyEDA data)
- For generic parts (passives, connectors), use KiCad built-in libraries
- Symbols include LCSC Part property for BOM generation

**Verify imports:**
```bash
grep "symbol \"" libs/project.kicad_sym  # List symbols
ls libs/project.pretty/                   # List footprints
ls libs/project.3dshapes/                 # List 3D models
```

## Phase 3: Schematic Design

Using SKiDL (code-first approach):

```python
from skidl import *

# Example structure
mcu = Part('MCU_Microchip_ATmega', 'ATmega328P-AU',
           footprint='Package_QFP:TQFP-32_7x7mm_P0.8mm')

# Connect power
mcu['VCC'] += Net('VCC')
mcu['GND'] += Net('GND')

# Generate netlist
generate_netlist(file_='project.net')
```

**Verification:**
1. Run ERC: `kicad-cli sch erc --output erc.json --format json project.kicad_sch`
2. Review and fix any errors

## Phase 4: PCB Layout

1. Set board outline based on user dimensions
2. Place components:
   - MCU/main IC in center
   - Connectors on edges
   - Decoupling caps near IC power pins
   - Keep sensitive analog away from digital
3. Document placement decisions in `kicad/design-log.md`

## Phase 5: Routing

1. Export DSN for auto-routing:
```bash
kicad-cli pcb export dsn --output board.dsn project.kicad_pcb
```

2. Run FreeRouting (if installed):
```bash
java -jar freerouting.jar -de board.dsn -do board.ses
```

3. Import SES back into KiCad

4. Manual cleanup if needed

## Phase 6: Design Rule Check

```bash
kicad-cli pcb drc --output drc.json --format json --exit-code-violations project.kicad_pcb
```

**Fix common issues:**
- Clearance violations: adjust trace spacing
- Unconnected nets: complete routing
- Silk overlap: move silkscreen text

## Phase 7: Visual Verification

Generate renders for inspection:

```bash
# Top view
kicad-cli pcb render --output kicad/renders/top.png --side top --width 2048 --height 2048 project.kicad_pcb

# Bottom view
kicad-cli pcb render --output kicad/renders/bottom.png --side bottom --width 2048 --height 2048 project.kicad_pcb
```

**Check:**
- Component placement looks correct
- Silkscreen readable
- No obvious routing issues

## Phase 8: Fabrication Export

Using KiBot (recommended):

```bash
kibot -c kibot.yaml -b project.kicad_pcb
```

Output files for JLCPCB:
- Gerber files (all layers)
- Drill files
- BOM (CSV format)
- CPL/Pick-and-Place (CSV format)

## Phase 9: Ordering

**JLCPCB Requirements:**
- Gerber ZIP file
- BOM CSV with columns: Designator, Qty, LCSC Part Number
- CPL CSV with columns: Designator, Mid X, Mid Y, Rotation, Layer

**Ask user before ordering:**
- Quantity
- Delivery address (or use saved)
- Shipping method
- Total cost confirmation

## File Locations

```
kicad/
├── specs.md              # Project requirements
├── component-selection.md # Selected parts
├── design-log.md         # Design decisions
├── project.kicad_pro     # KiCad project
├── project.kicad_sch     # Schematic
├── project.kicad_pcb     # PCB layout
├── kibot.yaml            # KiBot config
├── output/               # Generated files
│   ├── gerbers/          # Gerber files
│   ├── bom.csv           # Bill of materials
│   └── cpl.csv           # Pick and place
└── renders/              # Visual inspection
    ├── top.png
    └── bottom.png
```

## Error Recovery

**Component out of stock:**
→ Search for pin-compatible alternative
→ Update component-selection.md
→ Re-run schematic

**DRC failures:**
→ Read error details from JSON
→ Fix in PCB editor
→ Re-run DRC until clean

**Routing incomplete:**
→ Try different FreeRouting settings
→ Or route manually via MCP server

## Context Management

This is a long project. To maintain context:
- Keep `specs.md` updated with current requirements
- Log decisions in `design-log.md`
- Reference `workflow-reference.md` for commands
- Check `tool-setup.md` for tool versions
