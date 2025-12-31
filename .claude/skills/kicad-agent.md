# KiCad Agent Skill

This skill guides autonomous PCB design from requirements to fabrication.

## Activation

Use this skill when user provides PCB project requirements.

## Workflow Overview (V-Model Systems Engineering Approach)

```
Requirements → Component Selection → Library Import → SCHEMATIC → ERC (0 errors) →
Update PCB from Schematic → Board Setup → Component Placement → Routing →
DRC (0 errors) → Visual Verification → Fabrication Export → Order
```

**CRITICAL PRINCIPLES:**

1. **Schematic FIRST, PCB Second** - The schematic is the source of truth. Never route a PCB without a proper schematic.
2. **ERC Must Pass (0 errors)** - Run Electrical Rules Check before proceeding to PCB.
3. **DRC Must Pass (0 errors)** - Run Design Rules Check before fabrication. ALL violations must be resolved.
4. **Always render and visually inspect** - Don't blindly trust generated files.

## V-Model Design Process

The V-Model ensures verification at each stage:

```
Design Specs ───────────────────────────── Final Validation
       ↘                                         ↗
   Component Selection ─────────────── Assembly Test
          ↘                               ↗
      Schematic + ERC ─────────── Functional Test
             ↘                       ↗
        PCB Layout ───────── Visual Inspection
               ↘               ↗
            Routing + DRC
```

Key insight: Early decisions propagate throughout the entire design. Spending time on proper schematic design prevents costly respins.

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

## Phase 3: Schematic Design

### 3.1 Understanding Schematics vs Netlists

**CRITICAL DISTINCTION:**
- **Schematic (.kicad_sch)**: Visual representation of the circuit with symbols, wires, and connections. Required for ERC.
- **Netlist (.net)**: Text file listing components and their connections. Used for PCB import.

Both are needed for a proper design workflow:
1. Schematic provides visual verification and ERC capability
2. Netlist/schematic provides connectivity data for PCB

### 3.2 Creating Proper KiCad Schematics

KiCad 8/9 schematics require:
1. **lib_symbols section**: Embedded symbol definitions for all components
2. **Component instances**: Placed symbols with properties (Reference, Value, Footprint)
3. **Wires and labels**: Connections between components
4. **Power symbols**: +3V3, GND, etc.

**Grid spacing**: Use 50 mils (1.27mm) for symbol and wire placement. Other grid sizes cause connectivity issues.

**Footprint assignment**: Every symbol MUST have a footprint assigned before PCB generation. Use `property "Footprint" "Library:Footprint"` in each symbol.

### 3.3 SKiDL for Netlist Generation

SKiDL provides a code-first approach for connectivity:

```python
from skidl import *
set_default_tool(KICAD8)
lib_search_paths[KICAD8].append('libs')

# Import custom parts from project library
mcu = Part('project', 'PartName', footprint='project:FootprintName', ref='U1')

# Connect power
mcu['VCC'] += Net('+3V')
mcu['GND'] += Net('GND')

# Generate netlist
generate_netlist(file_='project.net')
```

**IMPORTANT:** SKiDL generates netlists only, NOT KiCad 8 schematics.
For a complete design flow, you also need a proper schematic file.

### 3.4 Generating Proper Schematics

Options for schematic generation:
1. **Manual in KiCad**: Use Eeschema GUI to create schematic
2. **Python script**: Generate .kicad_sch file with embedded symbols (see create_schematic_v5.py)
3. **SKiDL + manual schematic**: Use SKiDL for netlist, create matching schematic manually

**Schematic file structure (KiCad 9):**
```
(kicad_sch
  (version 20250114)
  (generator "create_schematic_v5.py")
  (generator_version "9.0")
  (uuid "...")
  (paper "A4")  ; Use A4 for simple designs, A3 for complex
  (title_block ...)
  (lib_symbols
    ; ALL symbol definitions MUST be embedded here
    (symbol "Device:C" ...)
    (symbol "singingcard:ISD3900FYI" ...)
  )
  ; Component instances
  (symbol
    (lib_id "Device:C")
    (at X Y rotation)
    (property "Reference" "C1" ...)
    (property "Value" "100nF" ...)
    (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" ...)
    (instances
      (project "projectname"
        (path "/uuid" (reference "C1") (unit 1))
      )
    )
  )
  ; Wires connecting pins to labels
  (wire
    (pts (xy X1 Y1) (xy X2 Y2))
    (stroke (width 0) (type default))
    (uuid "...")
  )
  ; Global labels for net connections
  (global_label "NET_NAME"
    (shape bidirectional)
    (at X Y ANGLE)  ; ANGLE: 0=right, 90=down, 180=left, 270=up
    ...
  )
  ; No-connect flags for unused pins
  (no_connect (at X Y) (uuid "..."))
)
```

**Global Label Orientation:**
Labels should be placed offset from pins with wires connecting them.

Key concepts:
- **Pin angle** indicates direction wire goes FROM pin AWAY from component body
  - 0: wire goes right (left-side pin)
  - 180: wire goes left (right-side pin)
  - 90: wire goes up (bottom pin) - note: standard math convention
  - 270: wire goes down (top pin)
- **KiCad Y-axis** increases downward (screen coordinates)
- **Label position** should be offset IN the direction of the pin angle (away from component)
- **Label arrow** should point TOWARD the pin (opposite of pin angle)

```python
def create_global_label_with_wire(net_name, x, y, angle):
    offset = 5.08  # mm

    # Offset in direction of pin angle (away from component)
    # Note: Y formula has minus because KiCad Y is inverted vs standard math
    label_x = x + offset * math.cos(math.radians(angle))
    label_y = y - offset * math.sin(math.radians(angle))

    # Label arrow points toward pin (opposite of pin angle)
    label_angle = (angle + 180) % 360

    # Wire from pin to label
    wire = f'(wire (pts (xy {x} {y}) (xy {label_x} {label_y})) ...)'

    # Label with arrow pointing back toward pin
    label = f'(global_label "{net_name}" (at {label_x} {label_y} {label_angle}) ...)'

    return wire + label
```

**Common mistake:** Using `y + offset * sin(angle)` instead of `y - offset * sin(angle)`. This causes labels to be placed toward the component instead of away from it, making them overlap with pins.

### 3.5 Run ERC (Electrical Rules Check)

**BEFORE proceeding to PCB, ERC must pass with 0 errors:**

```bash
kicad-cli sch erc project.kicad_sch --output erc-report.json --format json --severity-all
```

Check results:
```bash
cat erc-report.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
errors = [v for v in d.get('violations',[]) if v.get('severity')=='error']
warnings = [v for v in d.get('violations',[]) if v.get('severity')=='warning']
print(f'Errors: {len(errors)}, Warnings: {len(warnings)}')
if errors:
    for e in errors[:5]:
        print(f'  - {e.get(\"description\",\"\")}')
"
```

**Common ERC violations:**
- Floating pins: Unconnected inputs
- Power pin issues: Power flags missing
- Duplicate references: Same ref designator used twice
- Global label issues: Labels used only once
- `lib_symbol_issues`: Library not configured (warning, not blocking)
- `footprint_link_issues`: Footprint library not found (warning, not blocking)

**Note on warnings vs errors:**
- **Errors** must be fixed - they indicate real electrical issues
- **Warnings** about library configuration can be ignored if symbols/footprints are embedded
- `footprint_link_issues` warnings occur when CLI can't find global KiCad libraries - this is normal when running from command line

**Fix ALL ERC errors before proceeding to PCB.** Warnings about library paths are acceptable if footprints are embedded in the PCB file.

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

### 5.1 Export DSN for auto-routing

```bash
python export_dsn.py  # Creates project.dsn
```

**CRITICAL: DSN must include actual pad sizes!**

The `export_dsn.py` script MUST export actual pad dimensions from each footprint, NOT use a fixed size.
If all pads use the same padstack (e.g., 600x600um), FreeRouting will route traces through larger pads
causing shorts and clearance violations.

Example of correct padstack generation:
```python
# Collect unique pad sizes from all footprints
pad_sizes = set()
for comp in components:
    for pad in comp['pads']:
        sx = round(pad['size_x'] * 1000)  # mm to um
        sy = round(pad['size_y'] * 1000)
        pad_sizes.add((sx, sy))

# Generate padstack for each size
for sx, sy in pad_sizes:
    half_x, half_y = sx // 2, sy // 2
    dsn.append(f'(padstack "Rect[T]Pad_{sx}x{sy}_um"')
    dsn.append(f'  (shape (rect F.Cu -{half_x} -{half_y} {half_x} {half_y}))')
```

### 5.2 Run FreeRouting

```bash
# Download FreeRouting if not present
curl -L -o freerouting.jar "https://github.com/freerouting/freerouting/releases/download/v2.0.1/freerouting-2.0.1.jar"

# IMPORTANT: FreeRouting 2.0.1 requires Java 21
# On macOS: brew install openjdk@21
# Then use: /opt/homebrew/opt/openjdk@21/bin/java -jar freerouting.jar

# Auto-route (headless mode, single-threaded for best results)
java -jar freerouting.jar -de project.dsn -do project.ses -mt 1
```

**FreeRouting Tips:**
- Use `-mt 1` for single-threaded mode (avoids clearance violation bugs)
- Routing typically completes in 1-5 seconds for simple boards
- If routing fails, check DSN pad sizes first

### 5.3 Import SES back into KiCad

Use `import_ses.py` script to parse SES and add tracks/vias to PCB:
```bash
python import_ses.py
cp singingcard_routed.kicad_pcb singingcard.kicad_pcb
```

### 5.4 Visual Verification

**CRITICAL: Always render and check after routing:**
```bash
kicad-cli pcb render --output renders/top_routed.png --side top --width 2048 --height 1536 project.kicad_pcb
kicad-cli pcb render --output renders/bottom_routed.png --side bottom --width 2048 --height 1536 project.kicad_pcb
```

Review renders:
- Check all nets are connected (no ratsnest lines)
- Look for routing issues (traces crossing pads)
- Verify power traces are wide enough
- Check both layers if using 2-layer board

## Phase 6: Design Rule Check (MUST PASS WITH 0 ERRORS)

**CRITICAL: DRC must have 0 violations before fabrication.**

```bash
kicad-cli pcb drc --output drc.json --format json --severity-all project.kicad_pcb
```

Parse and verify:
```bash
cat drc.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
violations = d.get('violations', [])
unconnected = d.get('unconnected_items', [])
print(f'Violations: {len(violations)}')
print(f'Unconnected: {len(unconnected)}')
if violations:
    by_type = {}
    for v in violations:
        t = v.get('type', 'unknown')
        by_type[t] = by_type.get(t, 0) + 1
    for t, count in sorted(by_type.items()):
        print(f'  {t}: {count}')
"
```

**DRC issue priority:**

| Violation Type | Severity | Action |
|----------------|----------|--------|
| `unconnected` | **CRITICAL** | Must fix - board won't work |
| `clearance` | **CRITICAL** | Must fix - shorts possible |
| `track_width` | **CRITICAL** | Must fix - traces may burn |
| `drill_out_of_range` | **CRITICAL** | Must fix - fab will fail |
| `silk_over_copper` | Warning | Cosmetic - may hide soldermask issues |
| `silk_overlap` | Warning | Cosmetic - readability issue |
| `lib_footprint_issues` | Warning | Library config - OK if footprints embedded |
| `lib_footprint_mismatch` | Warning | Version difference - usually OK |

**Acceptable for fabrication:**
- 0 unconnected items (all nets routed)
- 0 clearance/track width errors
- Warnings about library configuration are OK when running from CLI
- Silkscreen warnings are cosmetic but ideally should be fixed

**Do NOT proceed to fabrication with clearance errors or unconnected items.**

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

**Routes causing shorts/clearance violations:**
→ First check: DSN padstack sizes must match actual footprint pad sizes
→ If all padstacks are same size (e.g., 600x600um), the export_dsn.py needs fixing
→ Regenerate DSN with correct pad sizes, then re-route
→ If still failing: adjust component placement to give more routing room

**Components too close together:**
→ Adjust positions in create_pcb.py placement dictionary
→ Spread components at least 5mm apart for easy routing
→ Put connectors on board edges, ICs in center
→ Keep bypass caps near their associated IC power pins

**3D models not showing:**
→ Check model paths are relative to project
→ Use ${KIPRJMOD}/ prefix for project-relative paths
→ Verify .wrl/.step files exist

**3D models offset from footprint:**
→ Common with easyeda2kicad imported footprints
→ Check the (model ...) section in the .kicad_mod file
→ Set offset to (xyz 0 0 0) if model appears misaligned
→ Verify by rendering: `kicad-cli pcb render --perspective ...`

Example fix in .kicad_mod file:
```
(model "${KIPRJMOD}/libs/project.3dshapes/Part.wrl"
    (offset (xyz 0 0 0))      ; Fix: set to 0,0,0
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
)
```

## Best Practices

1. **Always render after algorithmic changes** - Don't blindly trust generated files
2. **Commit frequently** - Save working states before major changes
3. **Document decisions** - Update design-log.md with rationale
4. **Verify LCSC availability early** - Avoid redesign later
5. **Keep skill file updated** - Document new learnings and workarounds
6. **Use screenshots for debugging** - Visual inspection catches many issues
