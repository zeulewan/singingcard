# Documentation Index

Master reference linking each PCB development phase to its documentation.

**Process Reference:** [`../process/PCB-SYSTEMS-ENGINEERING.md`](../process/PCB-SYSTEMS-ENGINEERING.md)

---

## Phase Documents

| Phase | Document | Description |
|-------|----------|-------------|
| **0. Requirements** | [`PRD.md`](PRD.md) | Product Requirements Document - project specs |
| **1. ConOps** | *Not yet created* | Concept of Operations - usage scenarios |
| **2. System Design** | [`schematic-design.md`](schematic-design.md) | Block diagram and interface definitions |
| **3. Component Selection** | [`component-selection.md`](component-selection.md) | BOM with LCSC parts research |
| **3.5. Pin Allocation** | [`PIN-CONNECTIONS.md`](PIN-CONNECTIONS.md) | Complete pin mapping from datasheets |
| **5. Schematic** | `../kicad/*.kicad_sch` | KiCad schematic files |
| **7. PCB Layout** | `../kicad/*.kicad_pcb` | KiCad PCB files |
| **8. DFM Review** | *Generated at runtime* | DRC/ERC reports |
| **10. Manufacturing** | `../kicad/jlcpcb/` | Gerbers, BOM, CPL files |

---

## Reference Documents

| Document | Description |
|----------|-------------|
| [`tool-setup.md`](tool-setup.md) | Installed tools and versions |
| [`workflow-reference.md`](workflow-reference.md) | Quick command reference |
| [`notes.md`](notes.md) | Miscellaneous learnings |
| [`status.md`](status.md) | Current project status |

---

## Process Documents

| Document | Description |
|----------|-------------|
| [`../process/PCB-SYSTEMS-ENGINEERING.md`](../process/PCB-SYSTEMS-ENGINEERING.md) | Master process definition |
| [`../process/TOOLING-WISHLIST.md`](../process/TOOLING-WISHLIST.md) | Desired automation tools |
| [`../process/user-prompts.md`](../process/user-prompts.md) | User prompt history |
| [`../process/research/`](../process/research/) | Historical research documents |

---

## Skills (Claude Code)

Project-level skills in `.claude/skills/`:

| Skill | Description |
|-------|-------------|
| `kicad-agent.md` | Main KiCad automation workflow |
| `pcb-requirements.md` | Requirements gathering interview |
| `kicad-ci-debug.md` | CI/CD debugging |

User-level skills in `~/.claude/skills/pcb-*/`:

| Skill | Phase |
|-------|-------|
| `/pcb-master` | Orchestrator |
| `/pcb-init` | Phase 0: Project initialization |
| `/pcb-requirements` | Phase 1: ConOps, requirements |
| `/pcb-system-design` | Phase 2: Block diagram, ICD |
| `/pcb-components` | Phase 3: JLCPCB research |
| `/pcb-pin-allocation` | Phase 3.5: Datasheet analysis |
| `/pcb-schematic` | Phase 5: Schematic design |
| `/pcb-layout` | Phase 7: PCB routing |
| `/pcb-dfm` | Phase 8: DFM review |
| `/pcb-manufacture` | Phase 10: Gerber generation |
| `/pcb-test` | Phase 11: Verification |
