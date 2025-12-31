# Currently Working On

## Project: Singing Birthday Card Module

### Status: Schematic complete, PCB needs routing

### Design Decisions Made

1. **No USB** - Dropped USB requirement (not available on LCSC, needs 5V)
2. **SPI Programming** - Each card programmed individually via SPI programmer
3. **ISD3900FYI** - Nuvoton audio playback IC with built-in Class D amp
4. **4-pin Speaker** - KLJ-01304T-08R07W SMD speaker with proper symbol

### Completed Tasks

- [x] Component research and selection
- [x] KiCad schematic design (A5 page, compact layout)
- [x] Symbol library with embedded symbols
- [x] PCB layout (components placed)
- [x] 3D models configured

### Pending Tasks

1. [ ] **Route PCB traces** - Open in KiCad, use File > Export > Specctra DSN, run FreeRouting, import SES
2. [ ] Run DRC check
3. [ ] Generate Gerbers and BOM for JLCPCB
4. [ ] Order prototype batch

### PCB Routing Instructions

1. Open `kicad/singingcard.kicad_pcb` in KiCad
2. File > Export > Specctra DSN
3. Run FreeRouting: `java -jar freerouting.jar`
4. Load DSN, autoroute, export SES
5. In KiCad: File > Import > Specctra Session
6. Run DRC to verify

### Key Files

- `kicad/create_schematic_v5.py` - Schematic generator script
- `kicad/singingcard.kicad_sch` - KiCad schematic
- `kicad/singingcard.kicad_pcb` - KiCad PCB layout
- `kicad/specs.md` - Project specifications
- `kicad/component-selection.md` - Full component research and BOM
