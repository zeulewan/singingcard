# PCB Development Master Orchestrator

Master skill for PCB development following systems engineering lifecycle.

## Activation
- User says: /pcb-master, /pcb, start pcb project, pcb workflow
- User wants to develop a PCB from scratch

## Overview

This skill orchestrates the complete PCB development lifecycle from requirements through manufacturing. It follows NASA/DoD/IEEE systems engineering standards adapted for JLCPCB manufacturing.

## Lifecycle Phases

```
Phase 0: Project Initiation ─────► /pcb-init
    │
    ▼ [PRD Created]
Phase 1: Requirements ───────────► /pcb-requirements
    │
    ▼ [ConOps Complete]
Phase 2: System Design ──────────► /pcb-system-design
    │
    ▼ [SRR Gate - Stakeholder Approval Required]
Phase 3: Component Selection ────► /pcb-components
    │
    ▼ [PDR Gate - Stakeholder Approval Required]
Phase 5: Schematic Design ───────► /pcb-schematic
    │
    ▼ [Schematic Complete]
Phase 7: PCB Layout ─────────────► /pcb-layout
    │
    ▼ [CDR Gate - Stakeholder Approval Required]
Phase 8: DFM Review ─────────────► /pcb-dfm
    │
    ▼ [PRR Gate - Stakeholder Approval Required]
Phase 10: Manufacturing ─────────► /pcb-manufacture
    │
    ▼ [Boards Received]
Phase 11: Test & Verify ─────────► /pcb-test
```

## Phase Detection

Determine current project phase by checking for artifacts:

| Check | If Missing | Phase |
|-------|------------|-------|
| `requirements/PRD.md` | Create it | Phase 0 |
| `requirements/ConOps.md` | Create it | Phase 1 |
| `requirements/ICD.md` | Create it | Phase 2 |
| `process/reviews/SRR.md` | Conduct SRR | SRR Gate |
| `docs/datasheets/*.pdf` or component matrix | Research | Phase 3 |
| `process/reviews/PDR.md` | Conduct PDR | PDR Gate |
| `kicad/*.kicad_sch` (valid) | Create schematic | Phase 5 |
| `kicad/*.kicad_pcb` (routed) | Route PCB | Phase 7 |
| `process/reviews/CDR.md` | Conduct CDR | CDR Gate |
| `kicad/output/gerbers/*.zip` | Generate gerbers | Phase 8-9 |
| `process/reviews/PRR.md` | Conduct PRR | PRR Gate |

## Instructions

### On First Invocation (New Project)

1. **Assess Current State**
   - Check if project structure exists
   - Identify which artifacts are present
   - Determine current phase

2. **Present Status**
   ```
   ## PCB Project Status

   **Current Phase:** [Phase Name]
   **Next Action:** [What needs to happen]

   ### Completed Artifacts
   - [x] PRD
   - [ ] ConOps
   ...

   ### Pending Reviews
   - [ ] SRR (System Requirements Review)
   - [ ] PDR (Preliminary Design Review)
   - [ ] CDR (Critical Design Review)
   - [ ] PRR (Production Readiness Review)
   ```

3. **Invoke Appropriate Sub-Skill**
   - Based on phase, invoke the corresponding skill
   - Pass context about what's already done

### For Continuing Projects

1. Read existing artifacts to understand context
2. Identify blockers or missing information
3. Propose next steps with clear options

### Review Gates (Human Checkpoints)

At each review gate, STOP and require explicit human approval:

**SRR Gate:**
```
## System Requirements Review

Before proceeding to component selection, please confirm:

1. [ ] PRD accurately captures your needs
2. [ ] ConOps scenarios are realistic
3. [ ] Interfaces are correctly defined
4. [ ] Budget allocations are acceptable

Reply "SRR APPROVED" to proceed, or list changes needed.
```

**PDR Gate:**
```
## Preliminary Design Review

Before proceeding to schematic design, please confirm:

1. [ ] Component selections are acceptable
2. [ ] All parts available in JLCPCB library
3. [ ] BOM cost is within budget
4. [ ] Technical risks are acceptable

Reply "PDR APPROVED" to proceed, or list changes needed.
```

**CDR Gate:**
```
## Critical Design Review

Before generating manufacturing files, please confirm:

1. [ ] Schematic has been reviewed
2. [ ] PCB layout has been reviewed
3. [ ] 3D model looks correct
4. [ ] BOM is complete and accurate

Reply "CDR APPROVED" to proceed, or list changes needed.
```

**PRR Gate:**
```
## Production Readiness Review

Before ordering, please confirm:

1. [ ] Gerbers verified in viewer
2. [ ] JLCPCB quote is acceptable
3. [ ] Assembly options are correct
4. [ ] Ready to spend money

Reply "PRR APPROVED" and "ORDER" to proceed.
```

## Project Structure Creation

If no structure exists, create:

```bash
mkdir -p requirements docs/{research,datasheets,references} \
         process/{reviews,baselines} kicad/{libs,output} tmp
```

Create template files:
- `requirements/PRD.md` - From template
- `requirements/ConOps.md` - From template
- `requirements/ICD.md` - From template
- `requirements/RTM.md` - Requirements Traceability Matrix

## Sub-Skills Reference

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `/pcb-init` | Project setup, PRD drafting | PRD.md, directory structure |
| `/pcb-requirements` | ConOps, requirements decomposition | ConOps.md, requirements list |
| `/pcb-system-design` | Block diagram, ICD | ICD.md, block diagram |
| `/pcb-components` | JLCPCB research, BOM | Component matrix, BOM draft |
| `/pcb-schematic` | KiCad schematic creation | .kicad_sch, ERC clean |
| `/pcb-layout` | PCB routing | .kicad_pcb, DRC clean |
| `/pcb-dfm` | Design for manufacturing check | DFM report |
| `/pcb-manufacture` | Order generation | Gerbers, BOM, CPL |
| `/pcb-test` | Verification planning | Test plan, results |

## Error Recovery

If something goes wrong:
1. Check the most recent baseline in `process/baselines/`
2. Identify what changed since baseline
3. Propose rollback or fix

## Notes

- Always save inspection images to `tmp/` for user review
- Reference the master document: `process/PCB-SYSTEMS-ENGINEERING.md`
- Update RTM when requirements change
- Keep risk register current
