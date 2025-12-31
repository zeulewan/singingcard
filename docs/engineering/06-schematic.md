# PCB Schematic Design

Phase 5 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-schematic, create schematic, design schematic
- After PDR gate passes

## Purpose

Create KiCad schematic from component selection and requirements.

## Prerequisites

- PDR complete (component selection approved)
- BOM draft exists
- Datasheets available for key components

## Process

### Step 1: Gather Design Information

From datasheets, extract for each IC:
- Typical application circuit
- Required external components (caps, resistors)
- Power supply requirements
- Pin connections

### Step 2: Create/Verify Symbols

For each component:

**If symbol exists in KiCad library:**
- Verify pin count matches datasheet
- Verify pin names match datasheet
- Verify pin types (power, input, output, bidirectional)

**If custom symbol needed:**
Create using Python script or KiCad:

```python
# Symbol creation pattern
symbol = {
    'name': 'PART_NUMBER',
    'pins': [
        {'num': '1', 'name': 'VCC', 'type': 'power_in'},
        {'num': '2', 'name': 'GND', 'type': 'power_in'},
        # ... all pins from datasheet
    ]
}
```

Save to `kicad/libs/[project].kicad_sym`

### Step 3: Schematic Organization

Use hierarchical sheets for complex designs:

```
Main Sheet
├── Power Supply
├── Microcontroller
├── Audio Section
├── User Interface
└── Connectors
```

For simple designs (< 20 components), single sheet is fine.

### Step 4: Place Components

**Order of placement:**
1. Main IC (center of functional block)
2. Power input/output
3. Decoupling capacitors (near power pins)
4. External components (per application circuit)
5. Connectors

**Placement rules:**
- Group related components
- Signal flow left-to-right or top-to-bottom
- Keep power and ground clear
- Leave room for labels

### Step 5: Wire Connections

**Connection methods:**
1. **Direct wires** - For short, local connections
2. **Net labels** - For connections across the sheet
3. **Global labels** - For connections between sheets
4. **Power symbols** - For power rails (VCC, GND, +3V3)

**Net naming conventions:**
- Power rails: `+3V3`, `+5V`, `GND`, `VBAT`
- SPI: `SPI_MOSI`, `SPI_MISO`, `SPI_SCK`, `SPI_CS`
- I2C: `I2C_SDA`, `I2C_SCL`
- Audio: `AUDIO_OUT`, `SP+`, `SP-`
- General: `TRIGGER`, `STATUS_LED`

### Step 6: Add Required Elements

- [ ] Power input protection (TVS, polyfuse if needed)
- [ ] Decoupling capacitors (100nF per power pin, 10uF bulk)
- [ ] Pull-up/pull-down resistors where needed
- [ ] Test points for debugging
- [ ] Mounting holes (mechanical symbols)
- [ ] Fiducials (if needed for assembly)

### Step 7: Annotation

Run annotation to assign reference designators:
- Resistors: R1, R2, R3...
- Capacitors: C1, C2, C3...
- ICs: U1, U2...
- Connectors: J1, J2...
- Switches: SW1, SW2...
- LEDs: D1, D2... or LED1, LED2...
- Speakers: LS1, LS2...

### Step 8: Electrical Rules Check (ERC)

Run ERC and resolve all errors:

**Common ERC errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| Unconnected pin | Pin not wired | Connect or mark "no connect" |
| Power pin not driven | No power source | Add power symbol |
| Conflicting outputs | Two outputs connected | Check design, add buffer |
| Input not driven | Floating input | Add pull-up/down or connect |

**Acceptable warnings:**
- Power flags on power input connectors
- Bidirectional pins connected to each other

### Step 9: Design Review Checklist

```markdown
### Schematic Review Checklist

**Power:**
- [ ] All power pins connected to appropriate rail
- [ ] Decoupling caps on every IC power pin
- [ ] Bulk capacitor at power input
- [ ] Power-on sequence correct (if multiple rails)

**Signals:**
- [ ] All signals have defined logic levels
- [ ] Pull-ups on open-drain outputs
- [ ] Series resistors on high-speed lines if needed
- [ ] ESD protection on external connections

**Mechanical:**
- [ ] Mounting holes included
- [ ] Connector pinouts match external devices
- [ ] Test points accessible

**Documentation:**
- [ ] All components have values
- [ ] All nets have meaningful names
- [ ] Title block filled in
- [ ] Revision number set
```

### Step 10: Export and Document

1. Export PDF: `kicad/output/[project]_schematic.pdf`
2. Export netlist for PCB
3. Save ERC report

### Step 11: Output Summary

```
## Schematic Design Complete

### Statistics
- Components: [count]
- Nets: [count]
- Sheets: [count]

### ERC Results
- Errors: 0
- Warnings: [count] (all reviewed)

### Files Created
- kicad/[project].kicad_sch
- kicad/output/[project]_schematic.pdf

### Next Steps
1. Review schematic PDF
2. Verify against datasheets
3. Run /pcb-layout to start PCB design
```

## KiCad Global Label Orientation Rules

**CRITICAL: Label orientation depends on `justify` property, not angle:**

| Wire Direction | Angle | Justify | Result |
|----------------|-------|---------|--------|
| Left (←) | 180 | right | Text reads left-to-right |
| Right (→) | 0 | left | Text reads left-to-right |
| Up (↑) | 270 | left | Text reads bottom-to-top |
| Down (↓) | 90 | right | Text reads top-to-bottom |

**Rule:** Labels pointing left or down use `justify right`, others use `justify left`

## Common Application Circuits

### LDO Regulator (e.g., AMS1117)
```
VIN ─┬─[C1 10uF]─┬─ GND
     │           │
     └─[LDO]─────┴─ VOUT ─┬─[C2 10uF]─ GND
         │                 │
        GND               LOAD
```

### Flash Memory (SPI)
```
MCU                    FLASH
MOSI ──────────────── DI
MISO ──────────────── DO
SCK  ──────────────── CLK
CS   ──────────────── /CS
3V3  ──────┬───────── VCC, /WP, /HOLD
           └─[100nF]─ GND
```

### Audio Output
```
DAC_OUT ─[C 10uF]─┬─ SP+
                  │
                 [SPEAKER]
                  │
                  └─ SP- ─ GND (or diff output)
```

## Success Criteria

- [ ] All components placed and wired
- [ ] ERC passes with 0 errors
- [ ] All warnings reviewed and acceptable
- [ ] Schematic PDF exported
- [ ] Design matches datasheets
- [ ] User approved
