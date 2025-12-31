# PCB Project Initialization

Phase 0 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-init, start new pcb, new pcb project, init pcb
- First phase of /pcb-master workflow

## Purpose

Gather stakeholder needs and create Product Requirements Document (PRD).

## Process

### Step 1: Project Identification

Ask the user:
```
What is the name of this project?
```

### Step 2: Structured Requirements Gathering

Use AskUserQuestion to gather requirements systematically:

**Question Set 1: Core Function**
```
What is the PRIMARY function of this device?
- Audio playback (speaker, buzzer, music)
- Sensing (temperature, light, motion, etc.)
- Control (motor, relay, LED)
- Communication (wireless, wired)
- Power management (charging, regulation)
- Other: [describe]
```

**Question Set 2: Power Source**
```
How will this device be powered?
- CR2032 coin cell (3V, ~220mAh)
- CR2025 coin cell (3V, ~160mAh)
- AAA batteries (1.5V each)
- AA batteries (1.5V each)
- LiPo battery (3.7V rechargeable)
- USB powered (5V)
- Mains powered (with transformer)
- Other: [specify]
```

**Question Set 3: Physical Constraints**
```
What are the size constraints?
- Credit card size (~85x54mm)
- Business card size (~90x55mm)
- Compact (~50x50mm or smaller)
- No constraints
- Custom: [specify dimensions]
```

**Question Set 4: Quantity & Cost**
```
What quantity will be produced?
- Prototype only (1-5 units)
- Small batch (10-50 units)
- Medium batch (100-500 units)
- Production (1000+ units)

What is the target unit cost?
- Under $5
- $5-15
- $15-50
- Over $50
- No constraint
```

**Question Set 5: Interfaces**
```
What interfaces are required? (Select all that apply)
- [ ] USB (charging or data)
- [ ] Audio output (speaker/headphones)
- [ ] Audio input (microphone)
- [ ] Display (LED, LCD, OLED)
- [ ] Buttons/switches
- [ ] Sensors (specify type)
- [ ] Wireless (WiFi, Bluetooth, LoRa)
- [ ] Programming/debug port
- [ ] Other: [specify]
```

**Question Set 6: Environment**
```
What is the operating environment?
- Indoor, room temperature only
- Indoor, wide temperature range
- Outdoor, weather protected
- Outdoor, fully exposed
- Other: [specify]
```

**Question Set 7: Special Requirements**
```
Any special requirements?
- [ ] Low power / battery life critical
- [ ] Small size critical
- [ ] Low cost critical
- [ ] Fast time to market
- [ ] Regulatory compliance (FCC, CE)
- [ ] Safety critical
- [ ] None
```

### Step 3: Create Directory Structure

```bash
mkdir -p requirements docs/{research,datasheets,references} \
         process/{reviews,baselines} kicad/{libs,output} tmp
```

### Step 4: Generate PRD

Create `requirements/PRD.md` using the template from PCB-SYSTEMS-ENGINEERING.md, filling in gathered information.

### Step 5: Output Summary

```
## Project Initialized: [Project Name]

### Key Requirements
- Function: [primary function]
- Power: [power source]
- Size: [dimensions]
- Quantity: [volume]
- Cost Target: [target]

### Next Steps
1. Review the PRD at requirements/PRD.md
2. Edit any incorrect information
3. Run /pcb-requirements to develop ConOps

### Files Created
- requirements/PRD.md
- requirements/ConOps.md (template)
- requirements/ICD.md (template)
- requirements/RTM.md (template)
```

## Templates to Create

### PRD.md Template
Fill in the template from PCB-SYSTEMS-ENGINEERING.md Section 6.1

### ConOps.md Template (Empty)
Fill in the template from PCB-SYSTEMS-ENGINEERING.md Section 6.2

### ICD.md Template (Empty)
Fill in the template from PCB-SYSTEMS-ENGINEERING.md Section 6.3

### RTM.md Template
```markdown
# Requirements Traceability Matrix

| Req ID | Requirement | Source | Allocated To | Verification | Status |
|--------|-------------|--------|--------------|--------------|--------|
| FR-001 | | PRD | | | Open |
```

## Success Criteria

- [ ] All key questions answered
- [ ] PRD created with all sections
- [ ] Directory structure in place
- [ ] User understands next steps
