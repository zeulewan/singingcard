# PCB Design for Manufacturing Review

Phase 8 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-dfm, dfm check, manufacturing review
- After PCB layout complete

## Purpose

Verify PCB design meets JLCPCB manufacturing requirements before generating production files.

## Prerequisites

- PCB layout complete
- DRC passes with 0 errors
- 3D model reviewed

## DFM Checklist

### 1. Board Dimensions

- [ ] Board outline is closed polygon on Edge.Cuts
- [ ] Minimum size: 5mm x 5mm
- [ ] Maximum size: 400mm x 500mm
- [ ] No internal cutouts violate minimum rules
- [ ] Corners have appropriate radius (if required)

### 2. Copper Layers

**Trace Width & Spacing:**

| Copper | Min Width | Min Spacing | Status |
|--------|-----------|-------------|--------|
| 1oz external | 5mil (0.127mm) | 5mil (0.127mm) | [ ] |
| 1oz internal | 3.5mil (0.09mm) | 3.5mil (0.09mm) | [ ] |
| 2oz external | 8mil (0.2mm) | 8mil (0.2mm) | [ ] |

**Copper Pour:**
- [ ] No isolated copper islands (or intentionally left)
- [ ] Thermal relief on pads (not direct connect unless intended)
- [ ] Pour clearance meets minimum spacing

**Copper-to-Edge:**
- [ ] Minimum 0.3mm from copper to board edge
- [ ] V-score lines have appropriate copper clearance

### 3. Drill/Via

| Parameter | Min Value | Design Value | Status |
|-----------|-----------|--------------|--------|
| Via drill (2L) | 0.3mm | | [ ] |
| Via drill (4L+) | 0.2mm | | [ ] |
| Via pad (2L) | 0.6mm | | [ ] |
| Via pad (4L+) | 0.45mm | | [ ] |
| PTH drill min | 0.15mm | | [ ] |
| PTH drill max | 6.3mm | | [ ] |
| NPTH drill min | 0.5mm | | [ ] |
| Hole-to-hole | 0.25mm | | [ ] |
| Hole-to-trace | 0.25mm | | [ ] |

**Via Tenting:**
- [ ] Decide: tented (covered by solder mask) or open
- [ ] Tented vias reduce risk of shorts from solder

### 4. Solder Mask

- [ ] Solder mask expansion appropriate (typically 0.05mm)
- [ ] No mask slivers (thin strips between pads)
- [ ] Mask bridge between fine-pitch pads (check 0.5mm pitch and below)
- [ ] Mask color selected (green fastest/cheapest)

### 5. Silkscreen

- [ ] Minimum line width: 0.15mm (0.2mm preferred)
- [ ] Minimum text height: 0.8mm (1.0mm preferred)
- [ ] No silkscreen on pads
- [ ] No silkscreen on exposed copper
- [ ] Reference designators readable
- [ ] Polarity markings present for polarized components
- [ ] Pin 1 indicators visible

**Silkscreen Conflicts:**
- Enable "Subtract soldermask from silkscreen" in plot settings
- Or manually adjust silkscreen graphics

### 6. Component Placement (for Assembly)

**Orientation:**
- [ ] All components on designated side(s)
- [ ] Consistent IC orientation (pin 1 direction)
- [ ] Components accessible for rework

**Spacing:**
- [ ] Minimum component-to-component spacing met
- [ ] Minimum component-to-edge spacing met
- [ ] Tall components don't shadow shorter ones

**Fiducials (for fine-pitch assembly):**
- [ ] Fiducials present if using 0.5mm pitch or finer
- [ ] Minimum 3 fiducials (recommended: 4 corners + near fine-pitch)
- [ ] Fiducial size: 1mm pad with 2mm clearance

### 7. Special Features

**Slots:**
- [ ] Minimum slot width: 0.65mm (metallized), 1.0mm (non-metallized)
- [ ] Slot length ≥ 2x width (ideally 2.5x)

**Edge Plating:**
- [ ] If needed, properly specified

**Castellated Holes:**
- [ ] If needed, minimum half-hole size 0.6mm

### 8. Layer Alignment

- [ ] All layers use same origin
- [ ] Drill file origin matches Gerber origin
- [ ] Outline on Edge.Cuts layer only

## DFM Review Process

### Step 1: Run Final DRC

Verify 0 errors:
```
Inspect → Design Rules Checker
```

### Step 2: Check Clearances

Use KiCad's clearance measurement:
```
Inspect → Measure (Ctrl+M)
```

Verify:
- Trace-to-trace clearance
- Trace-to-via clearance
- Trace-to-edge clearance

### Step 3: Review Layer by Layer

View each layer independently:
1. F.Cu - Check routing, pours
2. B.Cu - Check routing, ground pour
3. F.Silkscreen - Check readability
4. B.Silkscreen - Check if needed
5. F.Mask - Check pad exposure
6. Edge.Cuts - Check outline is closed

### Step 4: 3D Model Final Check

- [ ] All components present
- [ ] No component collisions
- [ ] Mounting holes clear
- [ ] Connectors accessible
- [ ] Board fits intended enclosure

### Step 5: Generate Test Gerbers

Generate preliminary Gerbers for review:
```bash
kicad-cli pcb export gerbers --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,Edge.Cuts project.kicad_pcb
```

### Step 6: View in External Gerber Viewer

Use one of:
- gerbv (open source)
- Online viewer at JLCPCB
- KiCad's built-in Gerber viewer

Check:
- [ ] All layers align correctly
- [ ] No missing features
- [ ] Board outline correct
- [ ] Drill file matches via/hole positions

## Common DFM Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| Trace too close to edge | Board rejected | Move trace inward |
| Acid trap | Etching problem | Round corners |
| Copper sliver | Lifting copper | Merge or remove |
| Missing mask | Unwanted solder | Add mask |
| Silkscreen on pad | Solder issue | Move silkscreen |
| No fiducials | Assembly alignment | Add fiducials |

## Output Summary

```
## DFM Review Complete

### Results
- Trace/space violations: [count]
- Drill violations: [count]
- Mask violations: [count]
- Silkscreen issues: [count]

### Required Fixes
1. [Description] - [Location]
2. [Description] - [Location]

### Ready for Production
[ ] Yes - proceed to /pcb-manufacture
[ ] No - fix issues first

### Files Generated
- tmp/dfm_gerbers/ (for review)
```

## Success Criteria

- [ ] All DFM checks pass
- [ ] Gerbers verified in external viewer
- [ ] No manufacturing warnings expected
- [ ] Ready for PRR gate
