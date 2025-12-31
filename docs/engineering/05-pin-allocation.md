# PCB Pin Allocation & Datasheet Analysis

Phase 3.5 of PCB Systems Engineering Lifecycle - between component selection and schematic design.

## Activation
- User says: /pcb-pin-allocation, pin allocation, datasheet analysis, chip research
- After component selection, before schematic design

## Purpose

Thoroughly analyze all component datasheets and create a complete pin connection map before starting schematic design.

## Prerequisites

- Component selection complete (BOM exists)
- LCSC/JLCPCB part numbers identified

## Critical Rules

**DO NOT start schematic design until this phase is complete.**

1. **Read EVERY datasheet** - No exceptions
2. **Understand EVERY pin** - Know what each pin does
3. **Document EVERY connection** - In PIN-CONNECTIONS.md
4. **NEVER GUESS** - Each pin function MUST come from the datasheet

**If you cannot access a datasheet, you CANNOT proceed with that component.**

KiCad symbols are NOT authoritative - they may have errors or be incomplete. The datasheet is the single source of truth.

## Process

### Step 1: Create Datasheets Directory

```bash
mkdir -p docs/datasheets
```

### Step 2: Download All Datasheets

For each component in BOM:

1. **ICs (Critical):** Download full datasheet from manufacturer
2. **Passives:** Note values, tolerances, voltage ratings
3. **Connectors:** Download mechanical drawings
4. **Specialty:** Sensors, speakers, displays - full datasheets

**Datasheet Sources:**
- LCSC product page → Datasheet link
- Manufacturer website (preferred - most current)
- Octopart/Findchips for alternatives

**Naming Convention:**
```
docs/datasheets/
├── ISD3900_datasheet.pdf
├── W25Q16JV_datasheet.pdf
├── AMS1117-3.3_datasheet.pdf
├── KLJ-01304T_speaker_datasheet.pdf
└── GL5528_LDR_datasheet.pdf
```

### Step 3: Read Each Datasheet - Extract Key Information

For each IC, document:

#### 3.1 Power Requirements
```markdown
## [Part Number] Power

| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| VCC | 2.7 | 3.0 | 3.6 | V |
| ICC (active) | - | 15 | 25 | mA |
| ICC (standby) | - | 1 | 5 | µA |

**Power Pins:**
- VCC: pins 5, 17, 28
- GND: pins 6, 18, 29
- AVCC (analog): pin 12

**Decoupling Required:**
- 100nF on each VCC/GND pair
- 10µF bulk on main supply
```

#### 3.2 Pin Functions
```markdown
## [Part Number] Pin Functions

| Pin | Name | Type | Description |
|-----|------|------|-------------|
| 1 | RESET | Input | Active low reset |
| 2 | XTAL1 | Input | Crystal input |
| 3 | XTAL2 | Output | Crystal output |
| ... | ... | ... | ... |

**Pin Types:**
- Power: VCC, GND, AVCC, AGND
- Input: Digital input, analog input
- Output: Digital output, open-drain, push-pull
- I/O: Bidirectional
- NC: No connect (leave floating or tie to GND per datasheet)
```

#### 3.3 Interface Requirements
```markdown
## [Part Number] Interfaces

### SPI Interface
| Signal | Pin | Notes |
|--------|-----|-------|
| MOSI | 15 | Master Out, Slave In |
| MISO | 16 | Master In, Slave Out |
| SCK | 17 | Clock, max 10MHz |
| CS | 18 | Active low chip select |

**SPI Mode:** Mode 0 (CPOL=0, CPHA=0)
**Max Clock:** 10 MHz
**Bit Order:** MSB first

### I2C Interface
| Signal | Pin | Notes |
|--------|-----|-------|
| SDA | 20 | Needs 4.7k pull-up |
| SCL | 21 | Needs 4.7k pull-up |

**Address:** 0x50 (7-bit)
**Max Clock:** 400 kHz
```

#### 3.4 Application Circuit
```markdown
## [Part Number] Application Circuit

From datasheet Figure X, page Y:

**Required External Components:**
- C1: 100nF ceramic, VCC to GND
- C2: 10µF electrolytic, VCC to GND
- R1: 10k pull-up on RESET
- Y1: 12MHz crystal
- C3, C4: 22pF load capacitors for crystal

**Optional Components:**
- LED on status pin (with 330R series)
- External EEPROM on I2C bus
```

#### 3.5 Absolute Maximum Ratings
```markdown
## [Part Number] Absolute Maximums

| Parameter | Value | Notes |
|-----------|-------|-------|
| VCC | 4.0V | Destroy above this |
| Input voltage | VCC + 0.5V | ESD clamp |
| Output current | 25mA | Per pin |
| Total power | 500mW | With derating |
| Storage temp | -40 to +85°C | |
```

### Step 4: Create Pin Connection Matrix

Create `docs/PIN-CONNECTIONS.md`:

```markdown
# Pin Connections

## System Overview

[Block diagram of connections]

## Net List

| Net Name | Source | Destination(s) | Notes |
|----------|--------|----------------|-------|
| +3V3 | U3.OUT | U1.VCC, U2.VCC, C1+ | Main 3.3V rail |
| GND | Battery- | All GND pins | Star ground |
| SPI_MOSI | U1.MOSI | U2.DI | SPI data out |
| SPI_MISO | U2.DO | U1.MISO | SPI data in |
| SPI_SCK | U1.SCK | U2.CLK | SPI clock |
| SPI_CS | U1.GPIO5 | U2./CS | Chip select |

## Component Pin Assignments

### U1: [Main IC]

| Pin | Name | Net | Connection | Notes |
|-----|------|-----|------------|-------|
| 1 | VCC | +3V3 | Power rail | 100nF to GND |
| 2 | GND | GND | Ground | |
| 3 | MOSI | SPI_MOSI | U2.DI | |
| 4 | MISO | SPI_MISO | U2.DO | |
| ... | ... | ... | ... | ... |

### U2: [Flash Memory]

| Pin | Name | Net | Connection | Notes |
|-----|------|-----|------------|-------|
| 1 | /CS | SPI_CS | U1.GPIO5 | Active low |
| 2 | DO | SPI_MISO | U1.MISO | |
| 3 | /WP | +3V3 | Pull high | Disable write protect |
| 4 | GND | GND | Ground | |
| 5 | DI | SPI_MOSI | U1.MOSI | |
| 6 | CLK | SPI_SCK | U1.SCK | |
| 7 | /HOLD | +3V3 | Pull high | Disable hold |
| 8 | VCC | +3V3 | Power | 100nF to GND |

### Passive Components

| Ref | Value | Net 1 | Net 2 | Purpose |
|-----|-------|-------|-------|---------|
| C1 | 100nF | +3V3 | GND | U1 decoupling |
| C2 | 100nF | +3V3 | GND | U2 decoupling |
| C3 | 10µF | +3V3 | GND | Bulk capacitor |
| R1 | 10k | TRIGGER | GND | Pull-down |

## Power Distribution

```
Battery (+3V)
    │
    ├──[Polarity Protection]──┬── VCC_RAW
    │                         │
    │                    [LDO 3.3V]
    │                         │
    │                         ├── +3V3
    │                         │    ├── U1.VCC (100nF)
    │                         │    ├── U2.VCC (100nF)
    │                         │    └── 10µF bulk
    │                         │
    └─────────────────────────┴── GND
```

## Signal Routing Priority

1. **Power:** Wide traces, short paths
2. **Clock/Crystal:** Short, away from noisy signals
3. **SPI:** Keep together, matched lengths if >10MHz
4. **Audio:** Away from digital, ground shield if possible
5. **GPIO:** Flexible routing

## Open Questions

- [ ] Does U1 need external crystal or internal oscillator OK?
- [ ] What pull-up value for I2C? (Depends on bus capacitance)
- [ ] Speaker connection: single-ended or differential?
```

### Step 5: Verify Completeness

Checklist before proceeding to schematic:

```markdown
## Pre-Schematic Checklist

### Datasheets Downloaded
- [ ] U1: [part] - datasheet.pdf
- [ ] U2: [part] - datasheet.pdf
- [ ] All ICs have datasheets

### Power Analysis
- [ ] All power pins identified
- [ ] Current budget calculated
- [ ] Decoupling requirements noted

### Pin Allocation
- [ ] All IC pins have assignments
- [ ] No pin conflicts
- [ ] All interfaces defined

### External Components
- [ ] All required passives identified
- [ ] Values match datasheet recommendations
- [ ] Voltage ratings adequate

### Questions Resolved
- [ ] All "Open Questions" answered
- [ ] Ambiguities clarified with datasheets or research
```

## Output

After completing this phase:

```
docs/
├── datasheets/
│   ├── ISD3900_datasheet.pdf
│   ├── W25Q16JV_datasheet.pdf
│   └── ...
├── PIN-CONNECTIONS.md      # Complete pin map
└── research/
    └── chip-notes.md       # Detailed notes from datasheets
```

## Datasheet Sources and Fallbacks

**Primary Sources (in order):**
1. Manufacturer website (most current, most reliable)
2. LCSC product page → Datasheet link
3. Octopart/Findchips
4. Mouser/DigiKey product pages

**Cross-Reference: KiCad Symbol Files**
After reading datasheets, verify KiCad symbols match:
- `kicad/libs/*.kicad_sym` - Compare pin names/numbers against datasheet
- Flag any discrepancies for correction

```bash
# List pin definitions from symbol file for verification
grep -A2 "pin " kicad/libs/project.kicad_sym
```

**If Datasheet Unavailable:**
- Try alternative sources (Mouser, DigiKey, Octopart)
- Contact manufacturer directly
- **DO NOT proceed with component if datasheet cannot be obtained**
- Consider selecting an alternative component with available documentation

**Web Fetch Limitations:**
- Some manufacturer sites block automated downloads
- Chinese datasheets may have encoding issues
- Large PDFs may timeout
- Solution: Have user manually download and place in `docs/datasheets/`

## Common Mistakes to Avoid

1. **Skipping datasheet reading** - "I'll figure it out in schematic" → errors
2. **Ignoring NC pins** - Some must be grounded, some must float
3. **Missing decoupling** - Every IC power pin needs capacitor
4. **Wrong pull-up/down** - Check if internal exists, correct value
5. **Voltage level mismatch** - 3.3V IC connected to 5V signal
6. **Forgetting analog ground** - AGND vs DGND separation

## Success Criteria

- [ ] All datasheets downloaded
- [ ] All datasheets read and understood
- [ ] PIN-CONNECTIONS.md complete
- [ ] All pins assigned
- [ ] No conflicts or ambiguities
- [ ] Ready for schematic design
