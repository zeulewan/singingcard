# PCB Manufacturing

Phase 10 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-manufacture, generate gerbers, order pcb, jlcpcb order
- After PRR gate passes

## Purpose

Generate production files and guide JLCPCB order process.

## Prerequisites

- CDR complete (design frozen)
- DFM review passed
- PRR approval obtained

## Process

### Step 1: Generate Gerbers

**Using Fabrication Toolkit (GUI - Recommended):**
1. Open PCB in KiCad
2. Click Fabrication Toolkit button
3. Configure:
   - [x] Auto-fill zones
   - [ ] User.1 as V-Cut (if using V-cuts)
4. Click Generate
5. Files created in `production/` folder

**Using kicad-cli (Command Line):**
```bash
# Generate Gerbers
kicad-cli pcb export gerbers \
    --output output/gerbers/ \
    --layers F.Cu,B.Cu,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste \
    --subtract-soldermask \
    --use-drill-file-origin \
    project.kicad_pcb

# Generate Drill files
kicad-cli pcb export drill \
    --output output/gerbers/ \
    --format excellon \
    --excellon-units mm \
    --excellon-zeros-format decimal \
    --drill-origin absolute \
    --generate-map \
    --map-format gerberx2 \
    project.kicad_pcb

# Create ZIP
cd output/gerbers && zip -r ../gerbers.zip *
```

### Step 2: Generate BOM

**JLCPCB BOM Format:**
```csv
Comment,Designator,Footprint,LCSC Part #
100nF,"C1,C2,C3",C_0603_1608Metric,C14663
10k,"R1,R2",R_0603_1608Metric,C25804
ISD3900FYI,U1,LQFP-48,C123456
```

**Using Fabrication Toolkit:** Auto-generated in `production/bom.csv`

**Manual export from KiCad:**
```bash
kicad-cli sch export bom --fields "Reference,Value,Footprint,LCSC" project.kicad_sch
```

Then format for JLCPCB requirements.

### Step 3: Generate Pick-and-Place (CPL)

**JLCPCB CPL Format:**
```csv
Designator,Mid X,Mid Y,Rotation,Layer
C1,125.00,121.50,0,top
U1,138.00,127.50,90,top
```

**Using Fabrication Toolkit:** Auto-generated in `production/positions.csv`

**Using kicad-cli:**
```bash
kicad-cli pcb export pos \
    --output output/positions.csv \
    --format csv \
    --units mm \
    --side front \
    --use-drill-file-origin \
    project.kicad_pcb
```

**Note:** May need column name adjustment for JLCPCB.

### Step 4: Verify Files

**Gerber Verification:**
1. Open in external viewer (gerbv, online viewer)
2. Check layer alignment
3. Verify drill positions
4. Check outline matches design

**BOM Verification:**
- [ ] All components listed
- [ ] LCSC part numbers correct
- [ ] Quantities match design
- [ ] No duplicate entries

**CPL Verification:**
- [ ] All components have positions
- [ ] Coordinates reasonable
- [ ] Rotations correct (may need adjustment)

### Step 5: Upload to JLCPCB

**Order Process:**

1. **Go to:** https://jlcpcb.com/

2. **Upload Gerbers:**
   - Click "Add Gerber File"
   - Upload `gerbers.zip`
   - Wait for processing

3. **Configure PCB Options:**
   | Option | Typical Value |
   |--------|---------------|
   | Layers | 2 |
   | Dimensions | Auto-detected |
   | PCB Qty | 5 (minimum) |
   | PCB Thickness | 1.6mm |
   | PCB Color | Green (fastest) |
   | Surface Finish | HASL (cheapest) or ENIG |
   | Copper Weight | 1oz |
   | Remove Order Number | Yes ($1.50 extra) |

4. **Enable Assembly (PCBA):**
   - Toggle "SMT Assembly"
   - Select side (Top/Bottom)
   - PCBA Qty (2-5 typical for prototype)

5. **Upload BOM and CPL:**
   - Add BOM file
   - Add CPL file
   - Click "Process BOM & CPL"

6. **Review Component Matching:**
   - Verify all parts matched
   - Fix any unmatched (search LCSC)
   - Note any shortages

7. **Component Placement Preview:**
   - Check component positions
   - Adjust rotations if needed
   - Confirm polarized components correct

8. **Review Quote:**
   - PCB cost
   - Assembly cost
   - Component cost
   - Shipping cost
   - Total

9. **Place Order:**
   - Add to cart
   - Complete checkout

### Step 6: Save Order Information

Create `process/reviews/PRR.md`:

```markdown
# Production Readiness Review

## Order Details
- Order Number: [JLCPCB order number]
- Order Date: [date]
- Quantity: [PCB qty] PCBs, [PCBA qty] assembled

## Costs
| Item | Cost |
|------|------|
| PCB fabrication | $ |
| Assembly | $ |
| Components | $ |
| Shipping | $ |
| **Total** | $ |

## Component Status
- All matched: [Yes/No]
- Substitutions: [list]
- Shortages: [list]

## Expected Delivery
- Production: [X] days
- Shipping: [X] days
- Estimated arrival: [date]

## Files Submitted
- Gerbers: gerbers.zip (SHA256: [hash])
- BOM: bom.csv
- CPL: positions.csv

## Approval
- Approved by: [name]
- Date: [date]
```

### Step 7: Track Order

JLCPCB order status stages:
1. Payment confirmed
2. PCB in production
3. PCB completed
4. Assembly in progress
5. Assembly completed
6. QC passed
7. Shipped
8. Delivered

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Gerber rejected | Missing layers | Regenerate with all layers |
| BOM mismatch | Wrong format | Use JLCPCB template |
| Part not found | Wrong LCSC number | Search LCSC directly |
| Rotation wrong | CPL offset | Adjust rotation in JLCPCB |
| Part out of stock | Stock changed | Find alternative |

## Output Summary

```
## Manufacturing Files Generated

### Files Created
- production/gerbers.zip
- production/bom.csv
- production/positions.csv

### Next Steps
1. Upload to JLCPCB
2. Configure order options
3. Review and confirm
4. Complete payment

### Order Tracking
Order submitted: [Yes/No]
Order number: [number]
Expected arrival: [date]
```

## Success Criteria

- [ ] Gerbers generated and verified
- [ ] BOM in JLCPCB format
- [ ] CPL in JLCPCB format
- [ ] Order placed successfully
- [ ] Order number recorded
