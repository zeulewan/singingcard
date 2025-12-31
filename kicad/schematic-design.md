# Schematic Design: Singing Birthday Card

## Block Diagram

```
                    +3V (CR2032)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      ISD3900FYI                              │
│                                                              │
│  SPI Flash Interface          │    Speaker Output            │
│  ─────────────────            │    ─────────────             │
│  MOSI (pin 16) ◄──────────────┼──► W25Q16 DI (pin 5)        │
│  MISO (pin 13) ◄──────────────┼──► W25Q16 DO (pin 2)        │  SPK+ (pin 18) ──►┌────────┐
│  SCLK (pin 14) ◄──────────────┼──► W25Q16 CLK (pin 6)       │                    │ Speaker │
│  SSB  (pin 15) ◄──────────────┼──► W25Q16 /CS (pin 1)       │  SPK- (pin 20) ──►│  8Ω    │
│                               │                              │                    └────────┘
│  GPIO (Triggers)              │                              │
│  ─────────────────            │                              │
│  GPIO0 (pin 38) ◄────────────[R]── LDR (GL5528)             │
│  GPIO1 (pin 32) ◄────────────[SW]── Button (optional)        │
│  GPIO2 (pin 31) ◄────────────[J]── Pull-tab (optional)       │
│                               │                              │
│  Power                        │                              │
│  ─────                        │                              │
│  VCC  (pin 11) ◄──────────────┼── +3V                        │
│  VREG (pin 12) ── 1µF ── GND  │                              │
│  VSS  (pin 10) ◄──────────────┼── GND                        │
│  VCCA (pin 43) ◄──────────────┼── +3V (with 0.1µF to GND)    │
│  VSSA (pin 44) ◄──────────────┼── GND                        │
│                               │                              │
│  Clock (Internal oscillator used - no external crystal)      │
│  XTALIN (pin 36) ── NC or GND │                              │
│  XTALOUT (pin 35) ── NC       │                              │
│                               │                              │
└─────────────────────────────────────────────────────────────┘
```

## Pin Connections

### ISD3900FYI (U1) - 48-LQFP

| Pin | Name | Connection | Notes |
|-----|------|------------|-------|
| 1 | NC | - | |
| 2 | CSB | Pull-up 10k to VCC | SPI chip select (active low) |
| 3 | DI | SPI data in from MCU | Not used (playback only) |
| 4-7 | I2S/GPIO4-7 | NC | I2S not used |
| 8-9 | NC | - | |
| 10 | VSS | GND | Digital ground |
| 11 | VCC | +3V | Digital power |
| 12 | VREG | 1µF to GND | Internal regulator output |
| 13 | MISO | W25Q16 DO (pin 2) | Flash data out |
| 14 | SCLK | W25Q16 CLK (pin 6) | Flash clock |
| 15 | SSB | W25Q16 /CS (pin 1) | Flash chip select |
| 16 | MOSI | W25Q16 DI (pin 5) | Flash data in |
| 17 | VCCD_PWM | +3V | PWM power |
| 18 | SPK+ | Speaker + | Speaker output |
| 19 | VSSD_PWM | GND | PWM ground |
| 20 | SPK- | Speaker - | Speaker output |
| 21 | VCCD_PWM | +3V | PWM power (tied to pin 17) |
| 22-24 | NC | - | |
| 25 | INTB | NC or pull-up | Interrupt output |
| 26 | RDY/BSYB | NC or pull-up | Ready/busy output |
| 27 | RESET | Pull-up 10k to VCC | Active low reset |
| 28 | DO | NC | SPI data out (not used) |
| 29 | CLK | NC | SPI clock in (not used) |
| 30-32 | GPIO3-1 | Trigger inputs | GPIO1/2 for button/pull-tab |
| 33-34 | NC | - | |
| 35 | XTALOUT | NC | Using internal oscillator |
| 36 | XTALIN | NC or 80k to GND | Internal oscillator |
| 37 | NC | - | |
| 38 | GPIO0 | LDR voltage divider | Light sensor input |
| 39-40 | NC | - | |
| 41 | AUDOUT | NC | Line out (not used) |
| 42 | AUXOUT | NC | Aux out (not used) |
| 43 | VCCA | +3V (0.1µF to GND) | Analog power |
| 44 | VSSA | GND | Analog ground |
| 45 | ANAOUT/MIC- | NC | Not used |
| 46 | ANAIN/MIC+ | NC | Not used |
| 47 | AUXIN | NC | Not used |
| 48 | NC | - | |

### W25Q16JVSSIQ (U2) - SOIC-8

| Pin | Name | Connection |
|-----|------|------------|
| 1 | /CS | ISD3900 SSB (pin 15) |
| 2 | DO | ISD3900 MISO (pin 13) |
| 3 | IO2 | Pull-up 10k to VCC (or NC) |
| 4 | GND | GND |
| 5 | DI | ISD3900 MOSI (pin 16) |
| 6 | CLK | ISD3900 SCLK (pin 14) |
| 7 | IO3 | Pull-up 10k to VCC (or NC) |
| 8 | VCC | +3V |

### CR2032 Battery Holder (B1)

| Pin | Connection |
|-----|------------|
| + | +3V rail |
| - | GND |

### GL5528 LDR (R1)

Voltage divider configuration:
```
+3V ── [10k] ── GPIO0 (pin 38) ── [LDR] ── GND
```
When light hits LDR, resistance drops, voltage at GPIO0 rises.

### Speaker (LS1) - 8Ω 0.5W

| Connection | ISD3900 Pin |
|------------|-------------|
| Speaker + | SPK+ (pin 18) |
| Speaker - | SPK- (pin 20) |

### Optional Tactile Switch (SW1)

```
GPIO1 (pin 32) ── [10k pull-up] ── +3V
           └──── [Switch] ──── GND
```

### Optional Pull-Tab Contact (J1)

```
GPIO2 (pin 31) ── [10k pull-up] ── +3V
           └──── [Tab contact] ── GND
```
When tab is inserted, contact is broken (high). When tab is pulled, contact closes (low → trigger).

## Decoupling Capacitors

| Location | Value | Notes |
|----------|-------|-------|
| VCC (pin 11) | 0.1µF + 10µF | Close to pin |
| VREG (pin 12) | 1µF | Regulator output |
| VCCA (pin 43) | 0.1µF | Analog power |
| VCCD_PWM (pin 17,21) | 10µF | PWM power |
| W25Q16 VCC | 0.1µF | Close to pin |

## Power Budget

| Component | Current (typical) | Current (max) |
|-----------|------------------|---------------|
| ISD3900 (standby) | 1µA | - |
| ISD3900 (playback) | 30mA | 50mA |
| ISD3900 (speaker) | - | 150mA |
| W25Q16 (read) | 5mA | 15mA |
| **Total (playback)** | ~40mA | ~200mA |

CR2032 capacity: ~220mAh
Estimated playback time: ~5-10 hours continuous (but greeting cards are used briefly)

## Trigger Logic

The ISD3900 can be configured via SPI to trigger playback on GPIO edges:
- GPIO0: Rising edge (light detected)
- GPIO1: Falling edge (button pressed)
- GPIO2: Falling edge (tab pulled)

Jumper selection can be done by enabling/disabling the corresponding GPIO pull-ups or connections.
