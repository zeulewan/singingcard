# KiCad Version Notes

This project uses **KiCad 9.0.x** (December 2025).

---

## Library Formats (KiCad 8/9)

| Type | Extension | Container | Notes |
|------|-----------|-----------|-------|
| **Symbols** | `.kicad_sym` | Single file | One file can contain multiple symbols |
| **Footprints** | `.kicad_mod` | `.pretty/` folder | One file per footprint in a `.pretty` directory |
| **3D Models** | `.wrl`, `.step` | Any folder | Typically in `.3dshapes/` directory |
| **Schematic** | `.kicad_sch` | - | S-expression format, version 20250114 for KiCad 9 |
| **PCB** | `.kicad_pcb` | - | S-expression format |
| **Project** | `.kicad_pro` | - | JSON format in KiCad 6+, S-expression before |

---

## Library Table System

KiCad uses library tables to locate libraries:

| File | Scope | Purpose |
|------|-------|---------|
| `fp-lib-table` | Project/Global | Maps footprint library nicknames to paths |
| `sym-lib-table` | Project/Global | Maps symbol library nicknames to paths |

### Path Variables

| Variable | Meaning |
|----------|---------|
| `${KIPRJMOD}` | Project directory (relative paths) |
| `${KICAD9_SYMBOL_DIR}` | Global KiCad symbol libraries |
| `${KICAD9_FOOTPRINT_DIR}` | Global KiCad footprint libraries |
| `${KICAD9_3DMODEL_DIR}` | Global KiCad 3D models |

**Always use `${KIPRJMOD}` for project-local libraries** to ensure portability.

---

## Key Changes from KiCad 7

1. **Fields in Footprints** (KiCad 8+)
   - Footprints now have named fields like symbols
   - Default fields: Reference, Value, Footprint, Datasheet, Description
   - Fields sync between schematic and PCB

2. **File Format Versions**
   - KiCad 9 schematic version: 20250114
   - KiCad 9 PCB version: 20250114
   - Older KiCad versions cannot open files saved in newer versions

3. **Embedded Symbols in Schematic**
   - KiCad 8+ schematics contain `lib_symbols` section
   - All used symbols are embedded in the schematic file
   - Schematic is self-contained (doesn't require external symbol libraries)

4. **Library Upgrade Command**
   ```bash
   kicad-cli fp upgrade --force libs/project.pretty
   kicad-cli sym upgrade libs/project.kicad_sym
   ```

---

## Project Library Structure

```
project/
├── kicad/
│   ├── libs/
│   │   ├── project.kicad_sym          # Symbol library
│   │   └── project.pretty/            # Footprint library folder
│   │       ├── Component1.kicad_mod
│   │       └── Component2.kicad_mod
│   ├── 3dmodels/ or libs/project.3dshapes/
│   │   ├── Component1.wrl
│   │   └── Component1.step
│   ├── fp-lib-table                   # Footprint library config
│   ├── sym-lib-table                  # Symbol library config
│   ├── project.kicad_pro              # Project file
│   ├── project.kicad_sch              # Schematic
│   └── project.kicad_pcb              # PCB
```

---

## Importing from LCSC/EasyEDA

The `easyeda2kicad` tool imports components from LCSC:

```bash
easyeda2kicad --lcsc_id CXXXXXX --full --output libs/project.kicad_sym
```

**Important:** EasyEDA exports older format files. Upgrade after import:

```bash
kicad-cli fp upgrade --force libs/project.pretty
```

---

## CLI Commands (KiCad 9)

### Rendering
```bash
kicad-cli pcb render --output image.png --side top project.kicad_pcb
kicad-cli pcb render --perspective --rotate "45,0,45" project.kicad_pcb
```

### Design Checks
```bash
kicad-cli sch erc --output erc.json --format json project.kicad_sch
kicad-cli pcb drc --output drc.json --format json project.kicad_pcb
```

### Export
```bash
kicad-cli pcb export gerbers --output gerbers/ project.kicad_pcb
kicad-cli pcb export drill --output gerbers/ project.kicad_pcb
kicad-cli pcb export pos --output positions.csv project.kicad_pcb
kicad-cli pcb export step --output model.step project.kicad_pcb
```

---

## Compatibility Notes

- **Read-only formats**: Eagle, Altium, CADSTAR (can open, cannot save)
- **Legacy KiCad**: `.mod` files (KiCad 4 and earlier) are read-only
- **Forward compatibility**: None - newer files won't open in older KiCad
- **Backward compatibility**: KiCad 9 can open KiCad 4+ files

---

## References

- [KiCad Documentation](https://docs.kicad.org/9.0/en/)
- [KiCad Library Conventions](https://klc.kicad.org)
- [KiCad CLI Reference](https://docs.kicad.org/9.0/en/cli/cli.html)
