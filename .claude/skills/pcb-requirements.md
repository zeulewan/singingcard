---
name: pcb-requirements
description: Interview user to gather complete PCB project requirements. Use when user wants to start a new PCB project or says "new project", "design a board", "make a PCB", etc.
---

# PCB Requirements Gathering

Thoroughly interview the user to capture all PCB project requirements before any design work begins. Ask questions using AskUserQuestion tool until nothing is ambiguous.

## When to Use

Trigger this skill when user:
- Wants to design a new PCB
- Says "new project", "make a board", "design a PCB"
- Provides vague requirements that need clarification

## Interview Process

Ask questions in phases. Use AskUserQuestion with multiple choice where possible. Follow up on anything unclear.

### Phase 1: Project Overview

Ask these first:
1. **What does this board do?** (main purpose/application)
2. **What's the end use?** (consumer product, prototype, one-off, hobby, commercial)
3. **Any existing design to reference?** (Arduino, dev board, previous version)

### Phase 2: Core Components

Ask about key parts:
1. **Main processor/MCU?** (ESP32, STM32, ATmega, RP2040, none)
2. **Wireless?** (WiFi, Bluetooth, LoRa, Zigbee, none)
3. **Sensors needed?** (temperature, motion, light, pressure, etc.)
4. **Displays?** (OLED, LCD, LED indicators, none)
5. **Connectors?** (USB-C, USB-A, JST, headers, screw terminals)
6. **Any specific ICs you want to use?**

### Phase 3: Power

1. **Input power source?** (USB 5V, battery, external supply, multiple)
2. **Battery type if applicable?** (LiPo, 18650, coin cell, AA/AAA)
3. **Voltage rails needed?** (3.3V, 5V, 12V, multiple)
4. **Estimated current draw?** (low <100mA, medium <500mA, high >500mA)
5. **Need battery charging on board?**

### Phase 4: I/O & Interfaces

1. **GPIO pins needed?** (how many, what for)
2. **Communication interfaces?** (I2C, SPI, UART, CAN)
3. **Analog inputs/outputs?**
4. **PWM outputs?** (motors, LEDs, buzzers)
5. **External connections?** (buttons, switches, external sensors)

### Phase 5: Physical Constraints

1. **Board size?** (specific dimensions, or "as small as possible", or "doesn't matter")
2. **Shape constraints?** (rectangular, must fit enclosure, mounting holes)
3. **Height restrictions?** (low profile needed?)
4. **Mounting?** (standoffs, screws, snap-fit, none)

### Phase 6: Environment & Reliability

1. **Operating environment?** (indoor, outdoor, high temp, moisture)
2. **Expected lifespan?** (prototype only, years of use)
3. **Compliance needs?** (FCC, CE, UL - usually not for prototypes)

### Phase 7: Fabrication & Budget

1. **Layer count preference?** (2-layer cheaper, 4-layer for complex)
2. **Quantity?** (5, 10, 20, 100+)
3. **Budget range?** (cheap prototype <$50, mid $50-150, flexible)
4. **Timeline?** (ASAP, 1-2 weeks, flexible)
5. **Manufacturer preference?** (JLCPCB default, PCBWay, other)
6. **Need assembly?** (bare boards only, or SMT assembly)

### Phase 8: Aesthetic Preferences

1. **Solder mask color?** (green, black, white, blue, red, purple)
2. **Silkscreen color?** (white, black)
3. **Surface finish?** (HASL lead-free default, ENIG for fine pitch)
4. **Any branding/logo to include?**

## Follow-up Questions

After initial answers, probe deeper:
- "You mentioned [X], can you tell me more about..."
- "What happens if [component] isn't available?"
- "Is [feature] required or nice-to-have?"
- "Any features you explicitly DON'T want?"

## Output

After gathering all requirements, create `kicad/specs.md` with:

```markdown
# Project: [Name]

## Overview
- Purpose:
- Application:
- Reference designs:

## Components
- MCU:
- Wireless:
- Sensors:
- Connectors:
- Other ICs:

## Power
- Input:
- Rails needed:
- Battery:
- Current estimate:

## I/O
- GPIO:
- Interfaces:
- External connections:

## Physical
- Size:
- Shape:
- Mounting:

## Fabrication
- Layers:
- Quantity:
- Budget:
- Timeline:
- Assembly:
- Colors:

## Notes
[Any other details]

## Open Questions
[Anything still unclear]
```

## Important

- Don't assume anything - ask
- Offer sensible defaults when user says "I don't know"
- Flag anything that seems contradictory
- Confirm understanding before proceeding to design
