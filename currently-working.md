# Currently Working On

## Project: Singing Birthday Card Module

### Status: Component research complete, ready for schematic design

### Design Decisions Made

1. **No USB** - Dropped USB requirement (not available on LCSC, needs 5V)
2. **SPI Programming** - Each card programmed individually via SPI programmer
3. **ISD3900FYI** - Nuvoton audio playback IC with built-in Class D amp

### Selected Components

| Component | Part | Price |
|-----------|------|-------|
| Audio IC | ISD3900FYI (C2613393) | $1.29 |
| SPI Flash | W25Q16JVSSIQ | $0.57 |
| LDR | GL5528 (C10081) | $0.04 |
| Battery Holder | CR2032-BS-6-1 (C70377) | $0.17 |
| Speaker | 23mm 8Ω 0.5W | ~$0.50 |
| Crystal + Passives | Various | ~$0.30 |
| **Total** | | **~$2.85** |

### Estimated Total Cost
- Components: ~$2.85
- PCB + Assembly: ~$1.00-1.50
- **Per-unit: ~$3.50-4.00** (slightly over $3 target)

### ISD3900FYI Key Features
- 2.7-3.6V (CR2032 compatible)
- Built-in 350mW Class D amp
- External SPI flash (Winbond 25X/25Q)
- ADPCM compression for long playback
- ~1µA standby

### Next Steps

1. [ ] Confirm exact LCSC part numbers for all components
2. [ ] Create KiCad schematic
3. [ ] Design PCB layout (~85x55mm)
4. [ ] Generate Gerbers and BOM for JLCPCB

### Key Files
- kicad/specs.md - Project specifications
- kicad/component-selection.md - Full component research and BOM
