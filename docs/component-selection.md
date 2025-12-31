# Component Selection: Singing Birthday Card Module

## Approach Selected

**SPI Programming Station** - Each card's flash chip is programmed with custom audio before use.

- Audio chip: ISD3900FYI (playback only, built-in speaker amp)
- Storage: Winbond W25Q SPI flash
- Trigger: GL5528 LDR + optional button + pull-tab
- Power: CR2032 (3V)

## Research Findings

### Audio Chips - LCSC Availability

#### NOT Available on LCSC:
| Chip | Notes |
|------|-------|
| MH2024K-24SS | MP3 + USB mass storage - **NOT ON LCSC** |
| WT2003S | MP3 + USB mass storage - **NOT ON LCSC** |
| JQ6500 | Popular MP3 module - **NOT ON LCSC** |
| ISD1820 | Classic voice record chip - **NOT ON LCSC** |
| WT588D | Voice chip - **DISCONTINUED** |

#### Available on LCSC (Voice Record/Playback):
| Part Number | LCSC# | Price | Stock | Features | Voltage |
|-------------|-------|-------|-------|----------|---------|
| ISD3900FYI | C2613393 | $1.29 | 60 | I2S/SPI, 4-48kHz, playback only, ext flash | 2.7-3.6V |
| ISD3800FYI | C2613397 | $2.07 | 2 | I2S/SPI, 4-48kHz, playback only | 2.7-5.5V |
| ISD1730SY | C2613883 | $4.84 | 10 | SPI, 4-12kHz, record/playback | 2.4-5.5V |

**Note**: ISD chips are designed for voice prompts (low bitrate), not MP3 music playback. They require external flash for longer recordings and don't have USB mass storage.

### Light Sensor (LDR) - Available on LCSC
| Part Number | LCSC# | Price (10+) | Stock | Specs |
|-------------|-------|-------------|-------|-------|
| GL5528 | C125627 | $0.049 | 23,570 | 540nm, 10-20kΩ, Through-hole 3mm |
| GL5528 | C10081 | $0.039 | 10,250 | 540nm, 8-20kΩ, Through-hole 3.4mm |

**Selected**: C10081 (JCHL) - $0.039, good stock

### CR2032 Battery Holder - Available on JLCPCB Parts
| Part Number | JLCPCB# | Price (1+) | Stock | Type |
|-------------|---------|------------|-------|------|
| CR2032-BS-6-1 | C70377 | $0.17 | 48,239 | SMD |

**Selected**: C70377 - Good stock, SMD mount

### Speakers - To Be Selected
Need: 23-28mm, 8Ω, 0.5-1W
LCSC has 1,400+ speaker options but requires manual filtering.

---

## Three Possible Approaches

### Option A: Simple Voice Chip (Cheapest, No USB)
Use ISD-series or similar voice playback chip.

**Pros:**
- Works with 3V CR2032
- Available on LCSC
- ~$1-2 per chip

**Cons:**
- No USB drag-and-drop upload
- Audio must be pre-programmed via SPI programmer
- Lower audio quality (voice-optimized, not music)

**Good for:** Pre-recorded message cards where audio doesn't change

### Option B: MP3 Module from AliExpress (USB, but Not LCSC)
Source MH2024K or WT2003S module from AliExpress/Alibaba.

**Pros:**
- USB drag-and-drop MP3 upload
- Good audio quality
- Trigger pins available

**Cons:**
- Not available on LCSC (can't do JLCPCB SMT assembly)
- Requires 4.5-5V (NOT compatible with single CR2032)
- Need boost converter or 2x CR2032 in series
- Module cost: ~$1-2 from China

**Good for:** DIY projects where you source modules separately

### Option C: Hybrid PCB + Module
Design PCB with LDR, triggers, battery holder, and space to solder an MP3 module.

**Pros:**
- Can use JLCPCB for PCB fab
- Flexibility to source audio module separately
- Works with existing $1-2 MP3 modules from China

**Cons:**
- Two-stage assembly (PCB + module)
- Still needs 2x CR2032 or LiPo for 5V module
- Total cost likely >$3/unit

---

## Recommendation

Given the requirements, I recommend **reconsidering one of these constraints**:

1. **Drop USB requirement** → Use ISD chip with pre-programmed audio
2. **Change battery to 2x CR2032 or small LiPo** → Can use USB-capable MP3 chip
3. **Accept non-LCSC sourcing** → Buy MH2024K modules from AliExpress

## Next Steps

User decision needed:
- [ ] Which approach to pursue?
- [ ] Is pre-programmed audio acceptable? (no USB)
- [ ] Can we use 2x batteries or different power source?
- [ ] Is non-LCSC module sourcing acceptable?

---

## Final Parts List (BOM)

| Component | Part Number | LCSC/JLCPCB | Qty | Unit Price | Notes |
|-----------|-------------|-------------|-----|------------|-------|
| Audio IC | ISD3900FYI | C2613393 | 1 | $1.29 | 48-LQFP, 2.7-3.6V, built-in Class D amp |
| SPI Flash | W25Q16JVSSIQ | TBD | 1 | $0.57 | 16Mbit, 2.7-3.6V, SOIC-8 |
| LDR | GL5528 | C10081 | 1 | $0.04 | Light sensor, through-hole |
| Battery Holder | CR2032-BS-6-1 | C70377 | 1 | $0.17 | SMD |
| Speaker | 23mm 8Ω 0.5W | LCSC (TBD) | 1 | $0.45-0.82 | Electromagnetic |
| Crystal | 11.2896MHz | TBD | 1 | ~$0.15 | For audio timing |
| Tactile Switch | 6x6mm | TBD | 1 | ~$0.02 | Optional button trigger |
| Capacitors | 0.1uF, 10uF, etc | TBD | ~5 | ~$0.05 | Decoupling, audio |
| Resistors | Various | TBD | ~4 | ~$0.02 | LDR divider, etc |
| **Subtotal** | | | | **~$2.85** | Components only |

### PCB Cost Estimate
- PCB fab: ~$0.50-1.00/unit at qty 10 (JLCPCB)
- SMT assembly: ~$0.50/unit (extended parts fee)

**Estimated Total: ~$3.50-4.00/unit** (slightly over $3 target)

---

## ISD3900FYI Key Features

From datasheet:
- **Voltage**: 2.7-3.6V (works with 3V CR2032)
- **Speaker output**: Built-in Class D, 350mW @ 3.3V into 8Ω
- **Audio format**: ADPCM (4-bit) or PCM (12-bit)
- **Sample rates**: 8-48kHz
- **Storage**: Up to 128Mbit external SPI flash (64 min @ 8kHz ADPCM)
- **Standby**: ~1µA
- **Package**: LQFP-48 (7x7mm)

### Flash Storage Calculation
W25Q16 = 16Mbit = 2MB storage

| Sample Rate | Compression | Duration |
|------------|-------------|----------|
| 8kHz | 4-bit ADPCM | ~8 min |
| 16kHz | 4-bit ADPCM | ~4 min |
| 32kHz | 8-bit PCM | ~1 min |
| 48kHz | 8-bit PCM | ~40 sec |

For 10-20 second audio at decent quality (16-32kHz), W25Q16 is plenty.

---

## SPI Programming Setup

To program custom audio for each card:

1. **Hardware needed**:
   - CH341A USB programmer (~$5) OR
   - Raspberry Pi with SPI interface

2. **Software**:
   - Nuvoton ISD-DMK tools for audio conversion
   - flashrom or similar for SPI flash programming

3. **Process**:
   - Convert MP3/WAV to ISD ADPCM format
   - Program flash chip via SPI
   - Assemble card with programmed flash

---

## Next Steps

- [ ] Confirm exact LCSC part numbers for all components
- [ ] Create KiCad schematic
- [ ] Design PCB layout (~85x55mm)
- [ ] Generate Gerbers and BOM
- [ ] Order prototype batch from JLCPCB
