# PCB Component Selection

Phase 3 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-components, select components, find parts, jlcpcb parts
- After SRR gate passes

## Purpose

Research, select, and validate components for JLCPCB manufacturing.

## Prerequisites

- SRR complete (PRD, ConOps, ICD approved)
- Functional requirements defined

## Process

### Step 1: Create Function-to-Component Matrix

For each function in the system, identify required component types:

```markdown
| Function | Component Type | Key Parameters |
|----------|---------------|----------------|
| Audio playback | MCU/DSP | Memory, I/O, audio DAC |
| Audio output | Speaker | Size, power, SPL |
| Power regulation | LDO/DC-DC | Vin, Vout, current |
| Storage | Flash | Capacity, interface |
```

### Step 2: JLCPCB Parts Library Search

For each component type, search JLCPCB:

**Search Strategy:**
1. Start with Basic Parts (lowest cost, always in stock)
2. If no Basic option, check Extended Parts
3. Verify stock level > order quantity + 50% margin
4. Check for multiple sources (preferred vs alternate)

**Use Perplexity/Web Search for:**
```
site:jlcpcb.com [component type] [key parameter] basic part
```

**JLCPCB Parts Library URL:**
```
https://jlcpcb.com/parts/componentSearch?searchTxt=[query]
```

### Step 3: Datasheet Analysis

For each selected component:

1. **Download datasheet** to `docs/datasheets/[part_number].pdf`
2. **Extract key information:**
   - Absolute maximum ratings
   - Recommended operating conditions
   - Pin configuration
   - Typical application circuit
   - Footprint/package dimensions

3. **Create component notes** in `docs/research/[part_number].md`:
```markdown
# [Part Number] - [Description]

## Source
- LCSC: [LCSC number]
- Category: Basic/Extended
- Stock: [quantity]
- Unit Price: [price]

## Key Specifications
- Parameter 1: value
- Parameter 2: value

## Application Notes
- Required external components
- Layout considerations
- Thermal requirements

## Risks
- [Any concerns]
```

### Step 4: Schematic Symbol & Footprint Check

For each component, verify:
- [ ] Symbol exists in JLCPCB library or create custom
- [ ] Footprint matches datasheet exactly
- [ ] 3D model available (nice to have)

If creating custom:
- Save to `kicad/libs/[project].kicad_sym`
- Save to `kicad/libs/[project].pretty/`

### Step 5: Create BOM Draft

Create `kicad/output/bom/BOM_draft.csv`:

```csv
Designator,Value,Footprint,LCSC,Quantity,Category,Unit Price,Total
U1,ISD3900FYI,LQFP-48,C123456,1,Extended,$2.50,$2.50
C1,100nF,0603,C14663,1,Basic,$0.01,$0.01
```

### Step 6: Component Selection Matrix

Create `docs/research/component-selection.md`:

```markdown
# Component Selection Matrix

## Microcontroller / Audio IC

| Option | Part Number | LCSC | Category | Price | Pros | Cons |
|--------|-------------|------|----------|-------|------|------|
| Selected | ISD3900FYI | C... | Extended | $2.50 | Built-in DAC | Complex |
| Alt 1 | ATtiny85 | C... | Basic | $0.80 | Simple | No DAC |
| Alt 2 | ESP32 | C... | Extended | $3.00 | WiFi | Overkill |

**Decision:** ISD3900FYI selected because [rationale]

## Power Regulator
[Same format]

## Speaker
[Same format]
```

### Step 7: JLCPCB Compatibility Verification

Run through checklist for each component:

```markdown
### JLCPCB Assembly Compatibility

| Component | In Library | Stock OK | Package OK | Notes |
|-----------|------------|----------|------------|-------|
| U1 | Yes | 500+ | LQFP-48 | |
| U2 | Yes | 1000+ | SOIC-8 | |
| R1 | N/A | N/A | THT | Hand solder |
```

**Package Compatibility:**
- SMD: 0201 minimum (0402+ preferred)
- QFP: 0.5mm pitch minimum
- BGA: 0.4mm pitch minimum (may need fiducials)
- THT: Not assembled by JLCPCB (hand solder required)

### Step 8: Risk Assessment

Document component risks:

```markdown
### Component Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ISD3900 stock out | Low | High | Order early, check alt |
| Speaker size conflict | Medium | Medium | Verify with 3D model |
```

### Step 9: Output Summary

```
## Component Selection Complete

### BOM Summary
- Total components: [count]
- JLCPCB Basic parts: [count]
- JLCPCB Extended parts: [count]
- Manual assembly required: [count]
- Estimated component cost: $[total]

### Key Decisions
1. [Main IC]: [selection] - [rationale]
2. [Power]: [selection] - [rationale]

### Action Items
- [ ] Download remaining datasheets
- [ ] Create custom symbols for: [list]
- [ ] Verify footprints for: [list]

### Next Steps
Run /pcb-pdr to conduct Preliminary Design Review
```

## JLCPCB Search Tips

**Finding Basic Parts:**
- Filter by "Basic Parts" in JLCPCB parts search
- Basic parts have no $3 extended fee
- Common passives (R, C) usually Basic
- Common packages (0402, 0603, 0805) usually Basic

**Stock Levels:**
- Green: Good stock (>1000)
- Yellow: Low stock (100-1000)
- Red: Very low (<100)
- Order early if using low-stock parts

**Price Breaks:**
- Check prices at different quantities
- Extended parts: $3 setup fee (once per order, not per part)

## Success Criteria

- [ ] All functions have selected components
- [ ] All components verified in JLCPCB library
- [ ] Datasheets downloaded for critical parts
- [ ] BOM draft created
- [ ] Component selection matrix documented
- [ ] Risks identified
