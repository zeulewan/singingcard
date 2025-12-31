# KiCad Agent Skill

This skill guides autonomous PCB design from requirements to fabrication.

## Activation

Use this skill when user provides PCB project requirements.

## Workflow Overview

```
Requirements → Component Selection → Library Import → Schematic (Netlist) → PCB Creation →
Visual Check → Manual Fix → Auto-Route → Visual Check → Manual Fix → DRC → Export → Order
```

**Key Principle:** Always render and visually inspect after algorithmic steps, then fix manually as needed.

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

**Common Issue:** Many specialty chips (e.g., MH2024K, WT2003S, JQ6500, ISD1820) are NOT on LCSC.
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

**IMPORTANT: Upgrade footprints to KiCad 8/9 format:**
```bash
kicad-cli fp upgrade --force libs/project.pretty
```

**Important notes:**
- Each `--full` call adds to the same library file
- Some parts may fail to import (no EasyEDA data)
- For generic parts (passives, connectors), use KiCad built-in libraries
- Symbols include LCSC Part property for BOM generation
- easyeda2kicad outputs older format - MUST upgrade with kicad-cli

**Verify imports:**
```bash
grep "symbol \"" libs/project.kicad_sym  # List symbols
ls libs/project.pretty/                   # List footprints
ls libs/project.3dshapes/                 # List 3D models
```

## Phase 3: Schematic Design with SKiDL

Using SKiDL (code-first approach) to generate netlist:

```python
from skidl import *
set_default_tool(KICAD8)
lib_search_paths[KICAD8].append('libs')

# Import custom parts from project library
mcu = Part('project', 'PartName', footprint='project:FootprintName', ref='U1')

# Connect power
mcu['VCC'] += Net('+3V')
mcu['GND'] += Net('GND')

# Generate netlist (SKiDL doesn't support KiCad 8 schematic generation)
generate_netlist(file_='project.net')
```

**IMPORTANT:** SKiDL does NOT generate KiCad 8 schematics - only netlists.
The netlist contains all connectivity info needed for PCB generation.

## Phase 4: PCB Creation from Netlist

Use custom Python script to create PCB from netlist:

1. Parse netlist for components, footprints, and nets
2. Load footprints from library files
3. Place components algorithmically:
   - Main ICs in center
   - Connectors on edges
   - Decoupling caps near IC power pins
   - Keep sensitive analog away from digital
4. Assign nets to pads
5. Write KiCad PCB file

**CRITICAL: Visual verification after placement:**
```bash
kicad-cli pcb render --output renders/top.png --side top --width 2048 --height 1536 --quality high project.kicad_pcb
kicad-cli pcb render --output renders/perspective.png --perspective --rotate "45,0,45" --zoom 1.5 --quality high project.kicad_pcb
```

Review renders:
- Check component placement makes sense
- Verify all components are present
- Check for overlapping footprints
- Verify 3D models are loading

If issues found, manually adjust positions in `create_pcb.py` and regenerate.

## Phase 5: Routing

**Note:** kicad-cli does NOT have DSN export. Use custom `export_dsn.py` script.

1. Export DSN for auto-routing:
```bash
python export_dsn.py  # Creates project.dsn
```

2. Run FreeRouting:
```bash
# Download FreeRouting if not present
curl -L -o freerouting.jar "https://github.com/freerouting/freerouting/releases/download/v2.0.1/freerouting-2.0.1.jar"

# Auto-route (headless mode)
java -jar freerouting.jar -de project.dsn -do project.ses
```

3. Import SES back into KiCad (requires custom script or manual import)

4. **CRITICAL: Visual verification after routing:**
```bash
kicad-cli pcb render --output renders/top_routed.png --side top --width 2048 --height 1536 project.kicad_pcb
```

Review renders:
- Check all nets are connected
- Look for routing issues
- Verify power traces are wide enough

## Phase 6: Design Rule Check

```bash
kicad-cli pcb drc --output drc.json --format json project.kicad_pcb
```

Parse results:
```bash
cat drc.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Violations: {len(d.get(\"violations\",[]))}'); print(f'Unconnected: {len(d.get(\"unconnected_items\",[]))}')"
```

**Common DRC issues:**
- `lib_footprint_issues`: Footprint library paths - usually cosmetic, ignore if footprints are embedded
- `silk_over_copper`: Silkscreen clipped - minor cosmetic issue
- `silk_overlap`: Text overlap - move silkscreen elements
- Unconnected items: Need to complete routing

## Phase 7: Final Visual Verification

Generate comprehensive renders:

```bash
# All views
kicad-cli pcb render --output renders/top.png --side top --width 2048 --height 1536 --quality high project.kicad_pcb
kicad-cli pcb render --output renders/bottom.png --side bottom --width 2048 --height 1536 --quality high project.kicad_pcb
kicad-cli pcb render --output renders/perspective.png --perspective --rotate "45,0,45" --zoom 1.5 --quality high project.kicad_pcb
```

## Phase 8: Fabrication Export

Using KiBot (recommended):

```bash
kibot -c kibot.yaml -b project.kicad_pcb
```

Or use kicad-cli directly:
```bash
# Gerbers
kicad-cli pcb export gerbers --output output/gerbers/ project.kicad_pcb

# Drill files
kicad-cli pcb export drill --output output/ project.kicad_pcb

# Position file (for assembly)
kicad-cli pcb export pos --output output/project-pos.csv project.kicad_pcb
```

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

## File Structure

```
project/
├── venv/                     # Python virtual environment
├── freerouting.jar           # Auto-routing tool
├── .claude/skills/
│   └── kicad-agent.md       # This skill file
├── kicad/
│   ├── specs.md             # Project requirements
│   ├── component-selection.md # Selected parts
│   ├── schematic-design.md  # Schematic documentation
│   ├── design-log.md        # Design decisions
│   ├── libs/
│   │   ├── project.kicad_sym     # Symbol library
│   │   ├── project.pretty/       # Footprint library
│   │   └── project.3dshapes/     # 3D models
│   ├── create_pcb.py        # PCB generation script
│   ├── export_dsn.py        # DSN export script
│   ├── project.net          # SKiDL netlist
│   ├── project.dsn          # Specctra DSN for routing
│   ├── project.ses          # Routed session file
│   ├── project.kicad_pro    # KiCad project
│   ├── project.kicad_sch    # Schematic (may be minimal)
│   ├── project.kicad_pcb    # PCB layout
│   ├── drc-report.json      # DRC results
│   ├── renders/             # Visual inspection images
│   └── output/              # Fabrication files
```

## Error Recovery

**Component out of stock:**
→ Search for pin-compatible alternative
→ Update component-selection.md
→ Re-run schematic generation

**DRC failures:**
→ Parse JSON for specific issues
→ Fix in PCB generation script
→ Regenerate PCB
→ Re-run DRC until clean

**Routing incomplete:**
→ Check DSN export captured all nets
→ Try different FreeRouting settings
→ Manual routing may be needed for complex sections

**3D models not showing:**
→ Check model paths are relative to project
→ Use ${KIPRJMOD}/ prefix for project-relative paths
→ Verify .wrl/.step files exist

## Best Practices

1. **Always render after algorithmic changes** - Don't blindly trust generated files
2. **Commit frequently** - Save working states before major changes
3. **Document decisions** - Update design-log.md with rationale
4. **Verify LCSC availability early** - Avoid redesign later
5. **Keep skill file updated** - Document new learnings and workarounds
6. **Use screenshots for debugging** - Visual inspection catches many issues
