# PCB System Design

Phase 2 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-system-design, system design, icd, block diagram
- After requirements are complete

## Purpose

Create system architecture, block diagram, and Interface Control Document.

## Prerequisites

- `requirements/PRD.md` complete
- `requirements/ConOps.md` complete
- Requirements decomposed with IDs

## Process

### Step 1: Create System Block Diagram

Identify major functional blocks from requirements:

**Common PCB Functional Blocks:**
- Power Management (input, regulation, distribution)
- Processing (MCU, DSP, FPGA)
- Memory (Flash, RAM, EEPROM)
- Sensors (analog, digital)
- Actuators (motors, speakers, LEDs)
- Communication (wired, wireless)
- User Interface (buttons, displays)
- Protection (ESD, overvoltage, reverse polarity)

**Block Diagram Elements:**
```
┌─────────────────────────────────────────────────────────┐
│                    SYSTEM BOUNDARY                       │
│                                                          │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐           │
│  │  Power  │────►│   MCU   │────►│ Output  │           │
│  │ Supply  │     │         │     │         │           │
│  └─────────┘     └────┬────┘     └─────────┘           │
│                       │                                  │
│                  ┌────▼────┐                            │
│                  │ Memory  │                            │
│                  └─────────┘                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
     ▲                 ▲                    │
     │                 │                    ▼
  [POWER]           [TRIGGER]           [OUTPUT]
  Battery           Button/Sensor       Speaker/LED
```

### Step 2: Define Interfaces

For each connection between blocks and external world:

**Interface Definition Table:**
| Interface ID | From | To | Type | Description |
|--------------|------|----|----|-------------|
| IF-001 | Battery | Power Supply | Power | 3V CR2032 |
| IF-002 | Power Supply | MCU | Power | 3.0V regulated |
| IF-003 | MCU | Flash | SPI | 4-wire SPI @ 10MHz |
| IF-004 | MCU | Speaker | Analog | PWM audio output |
| IF-005 | Button | MCU | Digital | Active-low input |

### Step 3: Create Interface Control Document

Write `requirements/ICD.md`:

```markdown
# Interface Control Document: [Project Name]

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [date] | [name] | Initial |

## 1. Scope
This document defines all interfaces for [Project Name].

## 2. External Interfaces

### 2.1 Power Interface (IF-001)
| Parameter | Value | Tolerance |
|-----------|-------|-----------|
| Connector | N/A (coin cell holder) | |
| Voltage | 3.0V | 2.0V - 3.3V |
| Current (peak) | [X] mA | |
| Current (avg) | [X] mA | |

### 2.2 User Interface - Trigger (IF-005)
| Parameter | Value |
|-----------|-------|
| Type | Mechanical switch / Light sensor / Pull-tab |
| Logic | Active [high/low] |
| Debounce | [X] ms in firmware |

### 2.3 Audio Output (IF-004)
| Parameter | Value |
|-----------|-------|
| Type | PWM / DAC |
| Frequency Range | [X] Hz - [Y] kHz |
| Output Level | [X] dBV |

## 3. Internal Interfaces

### 3.1 MCU to Flash Memory (IF-003)
| Signal | MCU Pin | Flash Pin | Description |
|--------|---------|-----------|-------------|
| SCK | [pin] | CLK | Clock |
| MOSI | [pin] | DI | Data In |
| MISO | [pin] | DO | Data Out |
| CS | [pin] | /CS | Chip Select |

**Protocol:** SPI Mode 0
**Clock Speed:** 10 MHz max
**Data Format:** MSB first

### 3.2 MCU to Power Supply (IF-002)
| Rail | Voltage | Current | Ripple |
|------|---------|---------|--------|
| VCC | 3.0V | [X] mA | < 50mV |

## 4. Interface Drawings
[Block diagram reference]
```

### Step 4: Allocate Requirements to Blocks

Map requirements to functional blocks:

| Requirement | Block | Notes |
|-------------|-------|-------|
| FR-001: Play audio | MCU, Flash, Speaker | Audio chain |
| FR-002: Trigger on button | MCU, Button | Input processing |
| PR-001: 5min battery life | Power, MCU | Power budget |

### Step 5: Create Budgets

**Power Budget:**
| Block | Mode | Current (mA) | Duty Cycle | Avg (mA) |
|-------|------|-------------|------------|----------|
| MCU | Active | 10 | 10% | 1.0 |
| MCU | Sleep | 0.01 | 90% | 0.009 |
| Flash | Read | 15 | 5% | 0.75 |
| Flash | Standby | 0.001 | 95% | 0.001 |
| Speaker | On | 50 | 10% | 5.0 |
| **Total** | | | | **6.76** |

Battery capacity: 220mAh (CR2032)
Estimated life: 220 / 6.76 = **32.5 hours** active

**Mass Budget (if constrained):**
| Component | Mass (g) | Notes |
|-----------|----------|-------|
| PCB | 5.0 | 50x50mm FR4 |
| Battery | 3.0 | CR2032 |
| Components | 2.0 | Estimate |
| **Total** | **10.0** | |

**Cost Budget:**
| Category | Target | Allocated |
|----------|--------|-----------|
| PCB | $1.00 | |
| Components | $3.00 | |
| Assembly | $1.00 | |
| **Total** | **$5.00** | |

### Step 6: Risk Assessment

Identify technical risks:

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Battery life insufficient | Medium | High | Optimize sleep modes |
| Audio quality poor | Low | Medium | Use proper DAC/amp |
| Size exceeds constraint | Low | High | Component selection |

### Step 7: Prepare for SRR

Create SRR package `process/reviews/SRR.md`:

```markdown
# System Requirements Review

## Project: [Name]
## Date: [date]

## Review Items

### 1. Requirements Completeness
- [ ] All stakeholder needs captured in PRD
- [ ] All requirements have unique IDs
- [ ] All requirements are verifiable
- [ ] No conflicting requirements

### 2. ConOps Validation
- [ ] All operational scenarios documented
- [ ] Failure modes identified
- [ ] User profiles defined

### 3. Interface Definition
- [ ] All external interfaces defined
- [ ] All internal interfaces defined
- [ ] Signal levels and protocols specified

### 4. Budget Allocations
- [ ] Power budget complete
- [ ] Mass budget complete (if applicable)
- [ ] Cost budget complete

### 5. Risk Assessment
- [ ] Technical risks identified
- [ ] Mitigations defined

## Action Items
| # | Action | Owner | Due |
|---|--------|-------|-----|
| | | | |

## Decision
[ ] APPROVED - Proceed to component selection
[ ] CONDITIONAL - Complete actions first
[ ] NOT APPROVED - Major rework required

## Signatures
- Technical Lead: _________________ Date: _____
- Stakeholder: _________________ Date: _____
```

## Output Summary

```
## System Design Complete

### Deliverables
- System block diagram
- Interface Control Document (ICD.md)
- Power/Mass/Cost budgets
- Requirements allocation
- Risk register

### SRR Status
Ready for System Requirements Review

### Next Steps
1. Conduct SRR with stakeholder
2. Get approval to proceed
3. Run /pcb-components for component selection
```

## Success Criteria

- [ ] Block diagram created
- [ ] All interfaces defined in ICD
- [ ] Requirements allocated to blocks
- [ ] Budgets established
- [ ] Risks documented
- [ ] SRR package ready
