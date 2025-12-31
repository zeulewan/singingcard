# PCB Layout Design

Phase 7 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-layout, route pcb, pcb design, layout
- After schematic is complete

## Purpose

Create PCB layout from schematic with proper routing for JLCPCB manufacturing.

## Prerequisites

- Schematic complete with ERC clean
- Netlist generated
- Footprints assigned to all components

## JLCPCB Design Rules

### 2-Layer Board (1oz Copper) - Standard

| Parameter | Minimum | Recommended |
|-----------|---------|-------------|
| Trace width | 0.127mm (5mil) | 0.15mm (6mil) |
| Trace spacing | 0.127mm (5mil) | 0.15mm (6mil) |
| Via drill | 0.3mm | 0.3mm |
| Via pad | 0.6mm | 0.7mm |
| Via-to-trace | 0.127mm (5mil) | 0.15mm (6mil) |
| Hole-to-trace | 0.25mm | 0.3mm |
| Hole-to-hole | 0.25mm | 0.3mm |
| Annular ring | 0.15mm | 0.2mm |
| Copper-to-edge | 0.3mm | 0.5mm |
| Silkscreen width | 0.15mm | 0.2mm |
| Silkscreen height | 0.8mm | 1.0mm |

### 4-Layer Board (1oz Copper)

| Parameter | Minimum | Recommended |
|-----------|---------|-------------|
| Trace width | 0.09mm (3.5mil) | 0.1mm (4mil) |
| Trace spacing | 0.09mm (3.5mil) | 0.1mm (4mil) |
| Via drill | 0.2mm | 0.25mm |
| Via pad | 0.45mm | 0.5mm |

## Process

### Step 1: Board Setup

1. **Set board outline:**
   - Draw on Edge.Cuts layer
   - Closed polygon required
   - Consider mounting holes in corners
   - Consider enclosure fit

2. **Set design rules:**
   - File → Board Setup → Design Rules
   - Set clearance, track width, via size per JLCPCB specs
   - Add net classes for power (wider traces)

3. **Set stackup (if multilayer):**
   - File → Board Setup → Board Stackup
   - Standard 4-layer: Sig-GND-VCC-Sig

### Step 2: Component Placement

**Placement order:**
1. **Fixed items first:**
   - Connectors (USB, headers)
   - Mounting holes
   - Components with mechanical constraints

2. **Critical components:**
   - Main IC
   - Crystal/oscillator near IC
   - Decoupling caps near power pins

3. **Thermal considerations:**
   - High-power components away from edges
   - Heat-generating parts with clearance

4. **Signal flow:**
   - Input on one side, output on other
   - Minimize trace lengths

**Placement rules:**
- Keep related components close
- Align components in grid pattern
- Orient ICs consistently (pin 1 direction)
- Ensure reference designators visible
- Leave room for routing

### Step 3: Power Distribution

1. **Power planes or pours:**
   - 4-layer: Use internal layers for VCC/GND
   - 2-layer: Use copper pours on both layers

2. **Power trace sizing:**
   - Use net classes for power rails
   - Calculate trace width for current:
     - 1A @ 1oz: ~0.5mm trace (internal), ~0.3mm (external)
     - See IPC-2221 calculator

3. **Ground strategy:**
   - Single ground plane preferred
   - Star ground for analog/digital split
   - Avoid ground loops

### Step 4: Signal Routing

**Routing priority:**
1. Critical signals (clocks, high-speed)
2. Analog signals
3. Digital signals
4. Power connections

**Routing rules:**
- Avoid 90° angles (use 45° or curves)
- Match lengths for differential pairs
- Keep analog away from digital
- Cross signals at 90° on different layers
- Use vias to switch layers

**Routing strategies:**
- **Interactive routing:** Manual, highest control
- **Push-and-shove:** KiCad's smart routing
- **Autorouter:** FreeRouting for assistance

### Step 5: Autorouting (Optional)

**Using FreeRouting:**

1. Export DSN from KiCad:
```python
# Via KiCad Python console
import pcbnew
board = pcbnew.LoadBoard("project.kicad_pcb")
pcbnew.ExportSpecctraDSN(board, "project.dsn")
```

2. Run FreeRouting:
```bash
/opt/homebrew/opt/openjdk@21/bin/java -jar freerouting.jar
```

3. Import SES back:
```python
pcbnew.ImportSpecctraSES(board, "project.ses")
pcbnew.SaveBoard("project.kicad_pcb", board)
```

**Note:** Manual cleanup usually required after autorouting.

### Step 6: Copper Pours

1. **Add ground pour:**
   - Select both layers for 2-layer
   - Set net to GND
   - Set clearance per design rules
   - Use solid fill (not hatched)

2. **Add power pour (if needed):**
   - Typically smaller area
   - Connect to power traces

3. **Fill zones:**
   - Edit → Fill All Zones (B)
   - Check for isolated copper islands
   - Remove islands or add stitching vias

### Step 7: Silkscreen

- [ ] Reference designators visible and not overlapping pads
- [ ] Pin 1/polarity markings visible
- [ ] Board name and revision
- [ ] Date or version indicator
- [ ] Company/project logo (optional)
- [ ] Important warnings (ESD, polarity)

### Step 8: Design Rules Check (DRC)

Run DRC and fix all errors:

| Error | Cause | Fix |
|-------|-------|-----|
| Clearance violation | Traces too close | Reroute with more space |
| Track too thin | Below minimum | Widen trace |
| Unconnected net | Missing connection | Route or via |
| Annular ring too small | Via too small | Increase pad size |
| Copper-to-edge | Too close to board edge | Move copper in |

**DRC must show 0 errors before proceeding.**

### Step 9: 3D Model Review

1. View 3D model: View → 3D Viewer
2. Check:
   - [ ] Components fit without overlap
   - [ ] Correct component heights
   - [ ] Connectors accessible
   - [ ] Mounting holes clear
3. Export renders to `tmp/` for inspection

### Step 10: Output Summary

```
## PCB Layout Complete

### Board Statistics
- Size: [X] x [Y] mm
- Layers: [count]
- Components: [count]
- Vias: [count]
- Traces: [length]

### DRC Results
- Errors: 0
- Warnings: [count] (all reviewed)
- Unconnected nets: 0

### Files Updated
- kicad/[project].kicad_pcb

### Next Steps
1. Review 3D model in tmp/
2. Run /pcb-dfm for manufacturing check
```

## Layer Usage (2-Layer)

| Layer | Purpose |
|-------|---------|
| F.Cu | Top copper - most routing |
| B.Cu | Bottom copper - ground pour, some routing |
| F.Silkscreen | Top silkscreen - designators, labels |
| B.Silkscreen | Bottom silkscreen - if needed |
| F.Mask | Top solder mask (auto) |
| B.Mask | Bottom solder mask (auto) |
| F.Paste | Top solder paste (auto) |
| B.Paste | Bottom solder paste (auto) |
| Edge.Cuts | Board outline |
| F.Courtyard | Component keepout |
| F.Fab | Fabrication notes |

## Common Mistakes

1. **Forgetting decoupling caps near IC**
   - Place 100nF within 3mm of power pins

2. **Traces too close to edge**
   - Minimum 0.3mm, prefer 0.5mm

3. **Silkscreen on pads**
   - Enable "Subtract soldermask from silkscreen"

4. **Floating copper**
   - Connect or remove isolated copper islands

5. **Via under component**
   - Avoid unless needed for thermal

## Success Criteria

- [ ] All nets routed (0 unconnected)
- [ ] DRC passes with 0 errors
- [ ] 3D model reviewed
- [ ] Component placement verified
- [ ] Silkscreen readable
- [ ] Ground pour complete
