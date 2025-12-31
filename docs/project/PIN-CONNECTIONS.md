# Pin Connections: Singing Birthday Card

Complete pin allocation and connection mapping for schematic design.

---

## System Block Diagram

```
                    CR2032 Battery (3V)
                           │
                           ▼
                    ┌──────────────┐
                    │   +3V Rail   │
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
    ┌─────────┐      ┌──────────┐      ┌─────────┐
    │  U1     │ SPI  │    U2    │      │  LS1    │
    │ISD3900  │◄────►│ W25Q16   │      │ Speaker │
    │         │      │  Flash   │      │         │
    └────┬────┘      └──────────┘      └────┬────┘
         │                                   │
         └───────────────────────────────────┘
                    SPK+/SPK-

    ┌─────────┐      ┌──────────┐      ┌─────────┐
    │   R1    │      │   SW1    │      │   J2    │
    │  LDR    │      │  Button  │      │Pull-Tab │
    │ GL5528  │      │          │      │         │
    └─────────┘      └──────────┘      └─────────┘
         │                │                 │
         └────────────────┴─────────────────┘
                    TRIGGER (GPIO)
```

---

## U1: ISD3900FYI (Audio Processor)

48-pin LQFP, LCSC: C2613393

### Power Requirements
| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| VCC/VCCa | 2.7 | 3.0 | 3.6 | V |
| Standby Current | - | 1 | - | uA |
| Playback Current | - | 15 | 25 | mA |

### Complete Pin Table

| Pin | Name | Type | Net | Connection | Notes |
|-----|------|------|-----|------------|-------|
| 1 | NC | - | - | Float | No connect |
| 2 | CSB | Output | SPI_CS | U2./CS | External flash chip select |
| 3 | DI | Input | SPI_MISO | U2.DO | Data from external flash |
| 4 | I2S_SDI/GPIO7 | I/O | - | Float/GPIO | Optional |
| 5 | I2S_SCK/GPIO6 | I/O | - | Float/GPIO | Optional |
| 6 | I2S_WS/GPIO5 | I/O | - | Float/GPIO | Optional |
| 7 | I2S_SDO/GPIO4 | I/O | - | Float/GPIO | Optional |
| 8 | NC | - | - | Float | No connect |
| 9 | NC | - | - | Float | No connect |
| 10 | VSS | Power | GND | Ground | **Digital ground** |
| 11 | VCC | Power | +3V | Battery+ | **100nF to GND** |
| 12 | VREG | Power | VREG | Regulator out | **10uF to GND** |
| 13 | MISO | Output | - | Float | Host SPI (not used in standalone) |
| 14 | SCLK | Input | - | Float | Host SPI (not used in standalone) |
| 15 | SSB | Input | - | Tie HIGH | Host SPI chip select (not used) |
| 16 | MOSI | Input | - | Float | Host SPI (not used in standalone) |
| 17 | VCCD_PWM | Power | +3V | Battery+ | **100nF to GND** |
| 18 | SPK+ | Output | SP+ | LS1.1 | Speaker + |
| 19 | VSSD_PWM | Power | GND | Ground | Speaker ground |
| 20 | SPK- | Output | SP- | LS1.2 | Speaker - |
| 21 | VCCD_PWM | Power | +3V | Battery+ | **100nF to GND** |
| 22 | NC | - | - | Float | No connect |
| 23 | NC | - | - | Float | No connect |
| 24 | NC | - | - | Float | No connect |
| 25 | INTB | Output | - | Float | Interrupt (optional) |
| 26 | RDY/BSYB | Output | - | Float | Ready/Busy (optional) |
| 27 | RESET | Input | RESET | 10k to VCC | Active low, needs pull-up |
| 28 | DO | Output | SPI_MOSI | U2.DI | Data to external flash |
| 29 | CLK | Output | SPI_SCK | U2.CLK | External flash clock |
| 30 | GPIO3 | I/O | TRIGGER | R1, SW1, J2 | **Trigger input** |
| 31 | GPIO2 | I/O | - | Float | Optional |
| 32 | GPIO1 | I/O | - | Float | Optional |
| 33 | NC | - | - | Float | No connect |
| 34 | NC | - | - | Float | No connect |
| 35 | XTALOUT | Output | - | Float | Internal oscillator used |
| 36 | XTALIN | Input | - | Float | Internal oscillator used |
| 37 | NC | - | - | Float | No connect |
| 38 | GPIO0 | I/O | - | Float | Optional |
| 39 | NC | - | - | Float | No connect |
| 40 | NC | - | - | Float | No connect |
| 41 | AUDOUT | Output | - | Float | Audio out (not used) |
| 42 | AUXOUT | Output | - | Float | Aux out (not used) |
| 43 | VCCa | Power | +3V | Battery+ | **100nF to GND** |
| 44 | VSSA | Power | GND | Ground | **Analog ground** |
| 45 | ANAOUT/MIC- | I/O | - | Float | Mic- (not used) |
| 46 | ANAIN/MIC+ | I/O | - | Float | Mic+ (not used) |
| 47 | AUXIN | Input | - | Float | Aux in (not used) |
| 48 | NC | - | - | Float | No connect |

### ISD3900 Power Pin Summary
| Pin | Name | Capacitor |
|-----|------|-----------|
| 11 | VCC | 100nF |
| 12 | VREG | 10uF (regulator output) |
| 17 | VCCD_PWM | 100nF |
| 21 | VCCD_PWM | 100nF |
| 43 | VCCa | 100nF |

**Total decoupling: 4x 100nF + 1x 10uF**

### ISD3900 External Flash Interface (to W25Q16)
| Signal | ISD3900 Pin | Direction | Flash Pin | Notes |
|--------|-------------|-----------|-----------|-------|
| CSB | 2 | Out | U2.1 (/CS) | Flash chip select |
| DI | 3 | In | U2.2 (DO) | Data from flash |
| DO | 28 | Out | U2.5 (DI) | Data to flash |
| CLK | 29 | Out | U2.6 (CLK) | Flash clock |

**Note:** Pins 13-16 (MISO, SCLK, SSB, MOSI) are the HOST SPI interface for external MCU control. In standalone mode with internal oscillator, these are not used.

---

## U2: W25Q16JVSSIQ (SPI Flash)

8-pin SOIC, LCSC: C131024

### Specifications
| Parameter | Value |
|-----------|-------|
| Capacity | 16 Mbit (2 MB) |
| Voltage | 2.7V - 3.6V |
| SPI Clock | Up to 133 MHz |
| Current (read) | 4 mA typ |
| Current (standby) | 1 uA typ |

### Pin Table (SOIC-8)

| Pin | Name | Type | Net | Connection | Notes |
|-----|------|------|-----|------------|-------|
| 1 | /CS | Input | SPI_CS | U1.15 | Active low chip select |
| 2 | DO (IO1) | Output | SPI_MISO | U1.13 | Data out |
| 3 | /WP (IO2) | Input | +3V | Pull HIGH | Disable write protect |
| 4 | GND | Power | GND | Ground | |
| 5 | DI (IO0) | Input | SPI_MOSI | U1.16 | Data in |
| 6 | CLK | Input | SPI_SCK | U1.14 | SPI clock |
| 7 | /HOLD (IO3) | Input | +3V | Pull HIGH | Disable hold |
| 8 | VCC | Power | +3V | Battery+ | **100nF to GND** |

### W25Q16 Notes
- Pins 3 and 7 must be tied HIGH to disable write protect and hold functions
- 100nF decoupling required on VCC

---

## LS1: KLJ-01304T-08R07W (Speaker)

4-pin SMD speaker, 8 ohm, 0.7W

### Pin Table

| Pin | Name | Net | Connection |
|-----|------|-----|------------|
| 1 | + | SP+ | U1.18 (SPK+) |
| 2 | - | SP- | U1.20 (SPK-) |
| 3 | (mounting) | - | Mechanical |
| 4 | (mounting) | - | Mechanical |

**Note:** Differential output from ISD3900 Class D amplifier (SPK+/SPK-)

---

## R1: GL5528 (Light Dependent Resistor)

Through-hole photoresistor, LCSC: C10081

### Specifications
| Parameter | Value |
|-----------|-------|
| Light resistance (10 lux) | 10-20 kOhm |
| Dark resistance | > 1 MOhm |
| Max voltage | 150V DC |
| Spectral peak | 540nm (green) |
| Response time | ~30ms |

### Connection

```
+3V ──┬── R1 (GL5528) ──┬── GND
      │                 │
      └── R2 (10k) ─────┴── TRIGGER (GPIO30)
```

Voltage divider:
- Dark: TRIGGER ~ 0V (LDR high resistance)
- Light: TRIGGER ~ VCC * (10k / (10k + LDR))
- At 10 lux (10-20k LDR): ~1.0-1.5V

---

## SW1: TL3342 (Tactile Switch)

4-pin SPST momentary switch

### Connection

```
TRIGGER ────── SW1 ────── GND
```

Active low - pressing connects TRIGGER to GND.

---

## J2: Pull-Tab Connector

2-pin header for pull-tab trigger

### Connection

```
TRIGGER ────── J2.1
GND     ────── J2.2
```

Pull-tab removes to break connection, triggering playback.

---

## Passive Components

| Ref | Value | Package | Net 1 | Net 2 | Purpose |
|-----|-------|---------|-------|-------|---------|
| C1 | 100nF | 0603 | +3V | GND | U1.VCC decoupling |
| C2 | 10uF | 0805 | VREG | GND | U1.VREG bulk |
| C3 | 1uF | 0603 | +3V | GND | General filtering |
| C4 | 100nF | 0603 | +3V | GND | U1.VCCD decoupling |
| C5 | 10uF | 0805 | +3V | GND | Bulk capacitor |
| C6 | 100nF | 0603 | +3V | GND | U2.VCC decoupling |
| R1 | GL5528 | THT | +3V | TRIGGER | LDR (light sensor) |
| R2 | 10k | 0603 | TRIGGER | GND | Pull-down for LDR divider |
| R3 | 10k | 0603 | +3V | RESET | Reset pull-up |
| R4 | 10k | 0603 | - | - | Spare |

---

## Net List Summary

| Net Name | Source | Destinations | Purpose |
|----------|--------|--------------|---------|
| +3V | BT1+ | U1.11,17,21,43, U2.3,7,8, R1, R3, C1-6 | 3V power |
| GND | BT1- | U1.10,19,44, U2.4, R2, SW1, J2.2, C1-6 | Ground |
| VREG | U1.12 | C2 | Internal regulator |
| SPI_MOSI | U1.28 (DO) | U2.5 (DI) | Data to flash |
| SPI_MISO | U2.2 (DO) | U1.3 (DI) | Data from flash |
| SPI_SCK | U1.29 (CLK) | U2.6 (CLK) | Flash clock |
| SPI_CS | U1.2 (CSB) | U2.1 (/CS) | Flash chip select |
| SP+ | U1.18 | LS1.1 | Speaker + |
| SP- | U1.20 | LS1.2 | Speaker - |
| TRIGGER | U1.30 | R1, R2, SW1, J2.1 | Trigger input |
| RESET | U1.27 | R3 | Reset with pull-up |

---

## Power Budget

| Component | Mode | Current (mA) | Duty | Avg (mA) |
|-----------|------|--------------|------|----------|
| U1 ISD3900 | Playback | 15 | 10% | 1.5 |
| U1 ISD3900 | Standby | 0.001 | 90% | 0.0009 |
| U2 W25Q16 | Read | 4 | 5% | 0.2 |
| U2 W25Q16 | Standby | 0.001 | 95% | 0.001 |
| **Total Average** | | | | **~1.7** |

CR2032 capacity: 220 mAh
**Estimated standby life:** 220 / 0.002 = **>4 years**
**Estimated active life:** 220 / 1.7 = **~130 hours** continuous play

---

## Signal Routing Priority

1. **Power (+3V, GND)** - Wide traces (0.3mm+), short paths, star ground
2. **SPI bus** - Keep together, max 25mm length at 10MHz
3. **Speaker (SP+/SP-)** - Differential pair, away from sensitive signals
4. **Trigger** - Can be long, not speed-critical
5. **Reset** - Short to pull-up resistor

---

## Design Checklist

### Power
- [x] All VCC pins identified (U1: 11,17,21,43; U2: 8)
- [x] All GND pins identified (U1: 10,19,44; U2: 4)
- [x] Decoupling capacitors assigned (4x 100nF + 2x 10uF)
- [x] VREG output capacitor (10uF on pin 12)

### SPI Interface
- [x] MOSI connected (U1.16 → U2.5)
- [x] MISO connected (U2.2 → U1.13)
- [x] SCK connected (U1.14 → U2.6)
- [x] CS connected (U1.15 → U2.1)
- [x] W25Q16 /WP tied HIGH (pin 3)
- [x] W25Q16 /HOLD tied HIGH (pin 7)

### Trigger Input
- [x] GPIO30 selected for trigger
- [x] LDR voltage divider designed
- [x] Button connected
- [x] Pull-tab connector included

### Speaker
- [x] Differential output (SPK+/SPK-)
- [x] 4-pin speaker footprint

### Unused Pins
- [x] NC pins floating (per datasheet)
- [x] Unused GPIO pins floating
- [x] I2C pins (CSB, DI) tied appropriately
- [x] Crystal pins floating (internal oscillator)

---

## Open Questions (Resolved)

1. **Crystal needed?** NO - ISD3900 has internal oscillator
2. **LDR pull-up or pull-down?** PULL-DOWN (R2 to GND)
3. **Reset circuit?** 10k pull-up to VCC
4. **Speaker coupling capacitor?** NO - Class D differential output
