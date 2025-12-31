# Documentation Index

## Folder Structure

| Folder | Purpose |
|--------|---------|
| `engineering/` | General PCB engineering process (reusable across projects) |
| `project/` | Project-specific documentation |

---

## Engineering Documentation

General process and reference docs applicable to any PCB project.

| Document | Description |
|----------|-------------|
| [`engineering/PCB-SYSTEMS-ENGINEERING.md`](engineering/PCB-SYSTEMS-ENGINEERING.md) | **Master process** - V-model lifecycle, review gates |
| [`engineering/KICAD-VERSION.md`](engineering/KICAD-VERSION.md) | KiCad 9 formats, library structure, CLI commands |
| [`engineering/TOOLING-WISHLIST.md`](engineering/TOOLING-WISHLIST.md) | Desired automation tools |
| [`engineering/workflow-reference.md`](engineering/workflow-reference.md) | Quick command reference |
| [`engineering/tool-setup.md`](engineering/tool-setup.md) | Installed tools and versions |

---

## Project Documentation

Specific to this singing birthday card project.

| Document | Phase | Description |
|----------|-------|-------------|
| [`project/PRD.md`](project/PRD.md) | 0 | Product Requirements Document |
| [`project/component-selection.md`](project/component-selection.md) | 3 | BOM with LCSC parts research |
| [`project/PIN-CONNECTIONS.md`](project/PIN-CONNECTIONS.md) | 3.5 | Complete pin mapping from datasheets |
| [`project/schematic-design.md`](project/schematic-design.md) | 5 | Block diagram, interface definitions |
| [`project/status.md`](project/status.md) | - | Current project status |
| [`project/notes.md`](project/notes.md) | - | Miscellaneous learnings |
| [`project/user-prompts.md`](project/user-prompts.md) | - | User prompt history |
| [`project/research/`](project/research/) | - | Historical research documents |

---

## Skills (`.claude/skills/`)

| Skill | Phase | Description |
|-------|-------|-------------|
| `pcb-master.md` | - | Master orchestrator |
| `pcb-init.md` | 0 | Project initialization |
| `pcb-requirements.md` | 1 | Requirements gathering |
| `pcb-system-design.md` | 2 | Block diagram, ICD |
| `pcb-components.md` | 3 | JLCPCB research |
| `pcb-pin-allocation.md` | 3.5 | Datasheet analysis |
| `pcb-schematic.md` | 5 | Schematic design |
| `pcb-layout.md` | 7 | PCB routing |
| `pcb-dfm.md` | 8 | DFM review |
| `pcb-manufacture.md` | 10 | Gerber generation |
| `pcb-test.md` | 11 | Verification |
