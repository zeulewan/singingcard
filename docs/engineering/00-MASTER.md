# PCB Engineering Master Process

The master orchestrator document for PCB development projects. Follow phases in order, completing review gates before proceeding.

**Standard:** NASA/DoD/IEEE systems engineering adapted for JLCPCB manufacturing.

---

## Phase Documents

| Phase | Document | Description | Gate |
|-------|----------|-------------|------|
| 1 | [`01-init.md`](01-init.md) | Project initialization, PRD | - |
| 2 | [`02-requirements.md`](02-requirements.md) | ConOps, requirements decomposition | - |
| 3 | [`03-system-design.md`](03-system-design.md) | Block diagram, ICD, budgets | **SRR** |
| 4 | [`04-components.md`](04-components.md) | JLCPCB parts research, BOM | - |
| 5 | [`05-pin-allocation.md`](05-pin-allocation.md) | Datasheet analysis, pin mapping | **PDR** |
| 6 | [`06-schematic.md`](06-schematic.md) | KiCad schematic design, ERC | - |
| 7 | [`07-layout.md`](07-layout.md) | PCB routing, DRC | **CDR** |
| 8 | [`08-dfm.md`](08-dfm.md) | Design for manufacturing review | - |
| 9 | [`09-manufacture.md`](09-manufacture.md) | Gerber export, JLCPCB order | **PRR** |
| 10 | [`10-test.md`](10-test.md) | Verification, acceptance | - |

---

## Reference Documents

| Document | Description |
|----------|-------------|
| [`references/KICAD-VERSION.md`](references/KICAD-VERSION.md) | KiCad 9 formats, CLI commands |
| [`references/TOOLING-WISHLIST.md`](references/TOOLING-WISHLIST.md) | Desired automation tools |
| [`references/workflow-reference.md`](references/workflow-reference.md) | Quick command reference |
| [`references/tool-setup.md`](references/tool-setup.md) | Installed tools and versions |

---

## Tooling Requirements

| Tool | Version | Purpose |
|------|---------|---------|
| **KiCad** | 9.0.x | EDA suite (schematic, PCB, 3D) |
| **kicad-cli** | 9.0.x | Command-line automation |
| **Python** | 3.11+ | Scripting and automation |
| **FreeRouting** | 2.0.1 | Auto-routing (requires Java 21) |

**KiCad 9 Library Formats:**
- Symbols: `.kicad_sym` (single file, multiple symbols)
- Footprints: `.kicad_mod` files in `.pretty/` folders
- 3D Models: `.wrl`, `.step` in `.3dshapes/` folders

See [`references/KICAD-VERSION.md`](references/KICAD-VERSION.md) for details.

---

## 1. Lifecycle Overview

This process follows the **V-Model** approach with formal review gates. Each phase has defined entry/exit criteria, required artifacts, and a corresponding verification phase.

```
                    STAKEHOLDER NEEDS
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │  PRD    │      │ ConOps  │      │  ICD    │
    │ Phase 0 │      │ Phase 1 │      │ Phase 2 │
    └────┬────┘      └────┬────┘      └────┬────┘
         │                │                │
         └────────────────┼────────────────┘
                          │
                     ▼ SRR Gate ▼
                          │
                    ┌─────▼─────┐
                    │ Component │
                    │ Selection │
                    │  Phase 3  │
                    └─────┬─────┘
                          │
                     ▼ PDR Gate ▼
                          │
              ┌───────────┴───────────┐
              │                       │
         ┌────▼────┐             ┌────▼────┐
         │Schematic│             │   PCB   │
         │ Design  │             │ Layout  │
         │ Phase 5 │             │ Phase 7 │
         └────┬────┘             └────┬────┘
              │                       │
              └───────────┬───────────┘
                          │
                     ▼ CDR Gate ▼
                          │
                    ┌─────▼─────┐
                    │    DFM    │
                    │  Review   │
                    │  Phase 8  │
                    └─────┬─────┘
                          │
                     ▼ PRR Gate ▼
                          │
                    ┌─────▼─────┐
                    │   Order   │
                    │   PCBA    │
                    │  Phase 10 │
                    └─────┬─────┘
                          │
                    ┌─────▼─────┐
                    │   Test    │
                    │ & Verify  │
                    │ Phase 11  │
                    └─────┴─────┘
```

---

## 2. Review Gates

### 2.1 System Requirements Review (SRR)
**Purpose:** Confirm all requirements are complete, consistent, and verifiable.

| Entry Criteria | Exit Criteria |
|----------------|---------------|
| PRD drafted | PRD approved by stakeholder |
| ConOps drafted | ConOps validated |
| Initial ICD drafted | Interfaces defined |
| | Requirements Traceability Matrix (RTM) started |

**Required Artifacts:**
- [ ] Product Requirements Document (PRD)
- [ ] Concept of Operations (ConOps)
- [ ] Interface Control Document (ICD)
- [ ] Mass/Power/Cost budgets (initial)
- [ ] Risk register (initial)

---

### 2.2 Preliminary Design Review (PDR)
**Purpose:** Validate component selection and preliminary architecture.

| Entry Criteria | Exit Criteria |
|----------------|---------------|
| SRR complete | All components identified |
| Component research done | JLCPCB compatibility verified |
| | Datasheets collected |
| | BOM drafted |

**Required Artifacts:**
- [ ] Component Selection Matrix
- [ ] JLCPCB Parts Library validation
- [ ] Preliminary BOM with LCSC part numbers
- [ ] Preliminary schematic block diagram
- [ ] Updated risk register

---

### 2.3 Critical Design Review (CDR)
**Purpose:** Freeze detailed design before manufacturing.

| Entry Criteria | Exit Criteria |
|----------------|---------------|
| PDR complete | Schematic complete, ERC clean |
| Schematic designed | PCB layout complete, DRC clean |
| PCB routed | All design rules met |
| | BOM finalized |

**Required Artifacts:**
- [ ] Complete schematic (PDF export)
- [ ] PCB layout (Gerber preview)
- [ ] Final BOM with all LCSC parts
- [ ] Design Rule Check report (0 errors)
- [ ] Electrical Rules Check report (0 errors)
- [ ] 3D model renders

---

### 2.4 Production Readiness Review (PRR)
**Purpose:** Confirm manufacturing files are correct and complete.

| Entry Criteria | Exit Criteria |
|----------------|---------------|
| CDR complete | Gerbers generated and verified |
| DFM review done | JLCPCB order quote reviewed |
| | Assembly files validated |

**Required Artifacts:**
- [ ] Gerber files (verified in viewer)
- [ ] Drill files
- [ ] Pick-and-place file (CPL)
- [ ] BOM in JLCPCB format
- [ ] JLCPCB order screenshot/quote

---

## 3. Phase Definitions

### Phase 0: Project Initiation
**Skill:** `/pcb-init`
**Duration:** 1 session

**Activities:**
1. Gather stakeholder needs through structured questions
2. Draft Product Requirements Document (PRD)
3. Establish project scope and constraints
4. Create project directory structure

**Questions to Ask:**
- What is the primary function of this device?
- What are the physical constraints (size, weight, enclosure)?
- What is the power source (battery type, voltage)?
- What interfaces are required (USB, I2C, SPI, etc.)?
- What is the target unit cost at volume?
- What quantity will be produced?
- What is the operating environment?
- Are there regulatory requirements (FCC, CE, UL)?

---

### Phase 1: Requirements Elicitation
**Skill:** `/pcb-requirements`
**Duration:** 1-2 sessions

**Activities:**
1. Decompose PRD into technical requirements
2. Create Concept of Operations (ConOps)
3. Define use cases and operational scenarios
4. Identify interfaces with external systems

**Deliverables:**
- ConOps document
- Functional requirements list
- Performance requirements list
- Environmental requirements list
- Interface requirements list

---

### Phase 2: System Definition
**Skill:** `/pcb-system-design`
**Duration:** 1 session

**Activities:**
1. Create system block diagram
2. Define internal interfaces (ICD)
3. Allocate requirements to subsystems
4. Establish mass/power/cost budgets

**Deliverables:**
- System block diagram
- Interface Control Document
- Requirements allocation matrix
- Budget allocations

---

### Phase 3: Component Research & Selection
**Skill:** `/pcb-components`
**Duration:** 1-3 sessions

**Activities:**
1. Research component options for each function
2. Verify JLCPCB/LCSC availability
3. Check stock levels and lead times
4. Download and analyze datasheets
5. Create component selection matrix

**JLCPCB Compatibility Checklist:**
- [ ] Part is in JLCPCB Parts Library (Basic/Extended)
- [ ] Footprint matches JLCPCB library or custom is allowed
- [ ] Stock level > order quantity + margin
- [ ] Package is SMD (for assembly) or THT marked accordingly
- [ ] Operating temperature range meets requirements

**Deliverables:**
- Component Selection Matrix
- Datasheets (saved to docs/datasheets/)
- Preliminary BOM with LCSC numbers
- Component risk assessment

---

### Phase 4: PDR Execution
**Skill:** `/pcb-pdr`
**Duration:** 1 session

**Activities:**
1. Present component selections
2. Review preliminary architecture
3. Identify remaining risks
4. Get stakeholder approval

**Deliverables:**
- PDR presentation/document
- Stakeholder sign-off
- Action items list

---

### Phase 5: Schematic Design
**Skill:** `/pcb-schematic`
**Duration:** 2-5 sessions

**Activities:**
1. Create/import component symbols
2. Place components and draw connections
3. Add power symbols and net labels
4. Run Electrical Rules Check (ERC)
5. Annotate and review

**Design Rules:**
- Use hierarchical sheets for complex designs
- Label all power rails with voltage
- Add test points for debugging
- Include decoupling capacitors per datasheet
- Add mounting holes and connectors

**Deliverables:**
- KiCad schematic (.kicad_sch)
- ERC report (0 errors, warnings reviewed)
- Schematic PDF export
- Net list

---

### Phase 6: CDR Preparation
**Skill:** `/pcb-cdr-prep`
**Duration:** 1 session

**Activities:**
1. Final schematic review
2. Preliminary PCB stackup decision
3. Critical component placement study
4. Thermal analysis (if needed)

---

### Phase 7: PCB Layout
**Skill:** `/pcb-layout`
**Duration:** 2-5 sessions

**Activities:**
1. Set board outline and mechanical constraints
2. Place components (critical first, then others)
3. Route traces (power first, then signals)
4. Add copper pours for ground/power
5. Run Design Rules Check (DRC)
6. Generate 3D model

**JLCPCB Design Rules (2-layer, 1oz copper):**
| Parameter | Minimum | Recommended |
|-----------|---------|-------------|
| Trace width | 5 mil (0.127mm) | 6 mil (0.15mm) |
| Trace spacing | 5 mil (0.127mm) | 6 mil (0.15mm) |
| Via drill | 0.3mm | 0.3mm |
| Via pad | 0.6mm | 0.7mm |
| Via-to-trace | 5 mil | 6 mil |
| Hole-to-trace | 0.25mm | 0.3mm |
| Annular ring | 0.15mm | 0.2mm |

**Deliverables:**
- KiCad PCB (.kicad_pcb)
- DRC report (0 errors)
- 3D renders (front/back)
- Layer stackup document

---

### Phase 8: DFM Review
**Skill:** `/pcb-dfm`
**Duration:** 1 session

**Activities:**
1. Verify all JLCPCB design rules met
2. Check component orientations for assembly
3. Verify fiducials (if required)
4. Check silkscreen readability
5. Verify tooling holes (if panelized)

**DFM Checklist:**
- [ ] All traces meet minimum width/spacing
- [ ] All vias meet minimum drill/pad size
- [ ] Board outline is closed and on Edge.Cuts layer
- [ ] No copper-to-edge violations (<0.3mm)
- [ ] Silkscreen doesn't overlap pads
- [ ] All components have reference designators
- [ ] Fiducials present (for assembly)
- [ ] Polarity markings visible on silkscreen

---

### Phase 9: PRR Execution
**Skill:** `/pcb-prr`
**Duration:** 1 session

**Activities:**
1. Generate Gerbers using Fabrication Toolkit
2. Verify Gerbers in external viewer
3. Generate BOM and CPL files
4. Upload to JLCPCB for quote
5. Review DFM feedback from JLCPCB
6. Get stakeholder approval to order

**Deliverables:**
- Gerber ZIP file
- BOM CSV (JLCPCB format)
- CPL CSV (pick-and-place)
- JLCPCB quote screenshot
- Order confirmation

---

### Phase 10: Manufacturing
**Skill:** `/pcb-manufacture`
**Duration:** External (5-15 days)

**Activities:**
1. Submit order to JLCPCB
2. Monitor order status
3. Track shipping
4. Receive and inspect boards

**Quality Inspection Checklist:**
- [ ] Board dimensions match design
- [ ] Drill holes are correct size and location
- [ ] Copper traces are clean, no shorts/opens
- [ ] Solder mask is properly applied
- [ ] Silkscreen is readable
- [ ] Components are correctly placed
- [ ] Solder joints are acceptable
- [ ] No visible defects

---

### Phase 11: Test & Verification
**Skill:** `/pcb-test`
**Duration:** 1-3 sessions

**Activities:**
1. Visual inspection
2. Continuity testing
3. Power-on test (current limiting)
4. Functional testing per test plan
5. Document results

**Test Levels:**
1. **Unit Test:** Individual component verification
2. **Integration Test:** Subsystem interaction
3. **System Test:** Full device operation
4. **Acceptance Test:** Against requirements

**Deliverables:**
- Test report
- Verification matrix (requirements vs. test results)
- Defect log (if any)
- Lessons learned

---

## 4. Configuration Management

### 4.1 Baselines

| Baseline | Established At | Contents |
|----------|---------------|----------|
| Functional | SRR | PRD, ConOps, ICD |
| Allocated | PDR | Component list, BOM draft |
| Product | CDR | Schematic, PCB, final BOM |
| As-Built | PRR | Gerbers, manufacturing files |

### 4.2 Change Control

After each baseline is established, changes require:
1. Change request documented
2. Impact analysis performed
3. Stakeholder approval
4. Implementation and verification
5. Baseline update

### 4.3 Version Numbering

- **Documents:** `DOC-XXX_v1.0.pdf`
- **Schematics:** Revision field in title block
- **PCB:** Revision field in title block + silkscreen
- **BOM:** Version in filename `BOM_v1.0.csv`

---

## 5. Directory Structure Standard

```
project-name/
├── CLAUDE.md              # Project-specific AI instructions
├── README.md              # Project overview
├── .gitignore
│
├── docs/                  # Documentation learned
│   ├── research/          # Research notes, web findings
│   ├── datasheets/        # Component datasheets (PDF)
│   └── references/        # Standards, app notes
│
├── process/               # Systems engineering
│   ├── reviews/           # SRR, PDR, CDR, PRR documents
│   ├── baselines/         # Frozen configuration snapshots
│   └── skills/            # Phase-specific skill files
│
├── requirements/          # Requirements documents
│   ├── PRD.md             # Product Requirements Document
│   ├── ConOps.md          # Concept of Operations
│   ├── ICD.md             # Interface Control Document
│   └── RTM.md             # Requirements Traceability Matrix
│
├── kicad/                 # KiCad project files
│   ├── project.kicad_pro  # KiCad project
│   ├── project.kicad_sch  # Schematic
│   ├── project.kicad_pcb  # PCB layout
│   ├── libs/              # Custom libraries
│   │   ├── project.kicad_sym
│   │   └── project.pretty/
│   └── output/            # Generated files
│       ├── gerbers/
│       ├── bom/
│       └── images/
│
├── images/                # Auto-generated by GitHub Action
│   ├── sch.svg
│   ├── pcbf.svg
│   ├── pcbb.svg
│   └── board.step
│
├── tmp/                   # NOT TRACKED - temporary workspace
│   ├── latest_render.png  # Latest inspection image
│   └── notes.txt          # Scratch notes
│
└── firmware/              # If applicable
    └── src/
```

---

## 6. Required Documents

### 6.1 Product Requirements Document (PRD)

```markdown
# Product Requirements Document: [Project Name]

## 1. Purpose
[One paragraph describing what this product does]

## 2. Stakeholders
| Role | Name | Contact |
|------|------|---------|

## 3. Functional Requirements
| ID | Requirement | Priority | Verification |
|----|-------------|----------|--------------|
| FR-001 | | | |

## 4. Performance Requirements
| ID | Requirement | Value | Tolerance | Verification |
|----|-------------|-------|-----------|--------------|
| PR-001 | | | | |

## 5. Physical Requirements
| Parameter | Value | Notes |
|-----------|-------|-------|
| Dimensions | | |
| Weight | | |
| Enclosure | | |

## 6. Environmental Requirements
| Parameter | Min | Typ | Max |
|-----------|-----|-----|-----|
| Operating Temp | | | |
| Storage Temp | | | |
| Humidity | | | |

## 7. Power Requirements
| Parameter | Value | Notes |
|-----------|-------|-------|
| Source | | |
| Voltage | | |
| Current (avg) | | |
| Current (peak) | | |
| Battery Life | | |

## 8. Interface Requirements
| Interface | Type | Description |
|-----------|------|-------------|

## 9. Cost Targets
| Item | Target | Notes |
|------|--------|-------|
| Unit cost (1) | | |
| Unit cost (100) | | |
| Unit cost (1000) | | |

## 10. Schedule
| Milestone | Target Date |
|-----------|-------------|

## 11. Constraints
-
-

## 12. Assumptions
-
-
```

### 6.2 Concept of Operations (ConOps)

```markdown
# Concept of Operations: [Project Name]

## 1. System Overview
[Description of the system and its purpose]

## 2. User Profiles
| User Type | Description | Frequency of Use |
|-----------|-------------|------------------|

## 3. Operational Scenarios

### Scenario 1: [Name]
1. User action
2. System response
3. ...

### Scenario 2: [Name]
...

## 4. Operational Modes
| Mode | Description | Transitions |
|------|-------------|-------------|

## 5. System States
[State diagram or description]

## 6. Failure Modes
| Failure | Detection | Response |
|---------|-----------|----------|
```

### 6.3 Interface Control Document (ICD)

```markdown
# Interface Control Document: [Project Name]

## 1. External Interfaces

### 1.1 Power Interface
| Parameter | Value |
|-----------|-------|
| Connector | |
| Voltage | |
| Current | |

### 1.2 [Interface Name]
...

## 2. Internal Interfaces

### 2.1 [Subsystem A] to [Subsystem B]
| Signal | Direction | Type | Description |
|--------|-----------|------|-------------|
```

---

## 7. Skill Invocation Map

The master skill `/pcb-master` orchestrates all phases:

| Phase | Skill | Trigger Condition |
|-------|-------|-------------------|
| 0 | `/pcb-init` | New project |
| 1 | `/pcb-requirements` | After PRD draft |
| 2 | `/pcb-system-design` | After ConOps |
| 3 | `/pcb-components` | After SRR |
| 4 | `/pcb-pdr` | Components selected |
| 5 | `/pcb-schematic` | After PDR |
| 6 | `/pcb-cdr-prep` | Schematic complete |
| 7 | `/pcb-layout` | After CDR prep |
| 8 | `/pcb-dfm` | Layout complete |
| 9 | `/pcb-prr` | DFM clean |
| 10 | `/pcb-manufacture` | After PRR |
| 11 | `/pcb-test` | Boards received |

---

## 8. JLCPCB Integration

### 8.1 Parts Library Categories

| Category | Description | Cost Impact |
|----------|-------------|-------------|
| Basic | Standard parts, always in stock | Lowest |
| Extended | Specialty parts, usually in stock | +$3 fee |
| Consignment | Customer provides parts | Handling fee |

### 8.2 Assembly Constraints

- **Minimum component size:** 0201 (imperial)
- **Maximum component height:** 5mm (standard), 8mm (large)
- **Minimum pitch:** 0.4mm (BGA), 0.5mm (QFP)
- **Sides:** Top-only or top+bottom (extra cost)
- **Fiducials:** Required for fine-pitch (< 0.5mm)

### 8.3 File Format Requirements

**Gerbers:**
- Format: RS-274X
- Extension: Standard (e.g., `.gtl`, `.gbl`)
- Layers: F.Cu, B.Cu, F.Mask, B.Mask, F.Silkscreen, B.Silkscreen, Edge.Cuts

**Drill:**
- Format: Excellon
- Units: Metric (mm)

**BOM:**
- Format: CSV
- Columns: Designator, Footprint, Quantity, Value, LCSC Part #

**CPL:**
- Format: CSV
- Columns: Designator, Mid X, Mid Y, Rotation, Layer

---

## 9. Claude Code Limitations & Workarounds

| Limitation | Workaround |
|------------|------------|
| Cannot open KiCad GUI | Generate scripts, user executes in KiCad |
| Fabrication Toolkit requires GUI | User runs in KiCad, or use kicad-cli |
| Cannot view images directly | Export to tmp/, user confirms |
| DSN export not in kicad-cli | Use KiCad's Python with pcbnew module |
| FreeRouting requires Java 21 | Install via homebrew, specify path |
| Cannot upload to JLCPCB | Generate files, user uploads |

---

## 10. References

- NASA Systems Engineering Handbook (NASA/SP-2016-6105)
- NASA Procedural Requirements NPR 7123.1
- DoD Instruction 5000.88 - Engineering of Defense Systems
- IEEE 1220-2005 - Systems Engineering
- ISO/IEC/IEEE 29148:2018 - Requirements Engineering
- JLCPCB Capabilities: https://jlcpcb.com/capabilities/pcb-capabilities

---

## Appendix A: Checklists

### A.1 SRR Checklist
- [ ] PRD complete with all sections
- [ ] All requirements have unique IDs
- [ ] All requirements are verifiable
- [ ] ConOps reviewed by stakeholder
- [ ] Interfaces identified
- [ ] Risks documented

### A.2 PDR Checklist
- [ ] All functions have component selections
- [ ] All parts verified in JLCPCB library
- [ ] Datasheets downloaded and reviewed
- [ ] BOM draft with LCSC numbers
- [ ] Block diagram complete
- [ ] Risks updated

### A.3 CDR Checklist
- [ ] Schematic complete
- [ ] ERC passes with 0 errors
- [ ] PCB layout complete
- [ ] DRC passes with 0 errors
- [ ] BOM finalized
- [ ] 3D model reviewed

### A.4 PRR Checklist
- [ ] Gerbers generated
- [ ] Gerbers verified in external viewer
- [ ] BOM in JLCPCB format
- [ ] CPL in JLCPCB format
- [ ] JLCPCB quote reviewed
- [ ] Stakeholder approval obtained
