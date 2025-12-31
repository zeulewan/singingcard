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
| [`KICAD-VERSION.md`](KICAD-VERSION.md) | **KiCad 9 version notes, library formats, CLI commands** |
| [`tool-setup.md`](tool-setup.md) | Installed tools and versions |
| [`workflow-reference.md`](workflow-reference.md) | Quick command reference |
| [`notes.md`](notes.md) | Miscellaneous learnings |
| [`status.md`](status.md) | Current project status |

---

## Process Documents

| Document | Description |
|----------|-------------|
| [`process/PCB-SYSTEMS-ENGINEERING.md`](process/PCB-SYSTEMS-ENGINEERING.md) | Master process definition |
| [`process/TOOLING-WISHLIST.md`](process/TOOLING-WISHLIST.md) | Desired automation tools |
| [`process/user-prompts.md`](process/user-prompts.md) | User prompt history |
| [`process/research/`](process/research/) | Historical research documents |

---

## Skills (Claude Code)

Project-level skills in `.claude/skills/`:

| Skill | Phase | Description |
|-------|-------|-------------|
| `pcb-master.md` | - | Master orchestrator, invokes other skills |
| `pcb-init.md` | 0 | Project initialization |
| `pcb-requirements.md` | 1 | ConOps, requirements gathering |
| `pcb-system-design.md` | 2 | Block diagram, ICD |
| `pcb-components.md` | 3 | JLCPCB research, BOM |
| `pcb-pin-allocation.md` | 3.5 | Datasheet analysis, pin mapping |
| `pcb-schematic.md` | 5 | Schematic design |
| `pcb-layout.md` | 7 | PCB routing |
| `pcb-dfm.md` | 8 | DFM review |
| `pcb-manufacture.md` | 10 | Gerber generation |
| `pcb-test.md` | 11 | Verification |
| `kicad-agent.md` | - | Legacy: Full KiCad workflow |
| `kicad-ci-debug.md` | - | CI/CD debugging |
