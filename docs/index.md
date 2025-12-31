# PCB Engineering Process

A deterministic workflow for PCB development following NASA/DoD/IEEE systems engineering standards, adapted for small-batch manufacturing with JLCPCB.

---

## Quick Start

1. **[Engineering Process](engineering/index.md)** - Start with `00-MASTER.md`
2. Follow phases 01-10 in order
3. Complete review gates (SRR, PDR, CDR, PRR) before proceeding

---

## Documentation Structure

| Folder | Purpose |
|--------|---------|
| `engineering/` | Reusable process docs (phases, references) |
| `project/` | Project-specific docs (PRD, BOM, pin mapping) |

---

## Engineering Phases

| Phase | Document | Review Gate |
|-------|----------|-------------|
| 1 | [Init](engineering/01-init.md) | - |
| 2 | [Requirements](engineering/02-requirements.md) | - |
| 3 | [System Design](engineering/03-system-design.md) | **SRR** |
| 4 | [Components](engineering/04-components.md) | - |
| 5 | [Pin Allocation](engineering/05-pin-allocation.md) | **PDR** |
| 6 | [Schematic](engineering/06-schematic.md) | - |
| 7 | [Layout](engineering/07-layout.md) | **CDR** |
| 8 | [DFM](engineering/08-dfm.md) | - |
| 9 | [Manufacture](engineering/09-manufacture.md) | **PRR** |
| 10 | [Test](engineering/10-test.md) | - |

---

## Project: Singing Birthday Card

| Document | Description |
|----------|-------------|
| [PRD](project/PRD.md) | Product requirements |
| [Component Selection](project/component-selection.md) | BOM with LCSC parts |
| [Pin Connections](project/PIN-CONNECTIONS.md) | Complete pin mapping |
| [Status](project/status.md) | Current project status |

---

## Tooling

- **KiCad 9.0.x** - EDA suite
- **kicad-cli** - Command-line automation
- **FreeRouting** - Auto-routing
- **JLCPCB** - PCB fabrication and assembly

See [KiCad Version Notes](engineering/references/KICAD-VERSION.md) for details.
