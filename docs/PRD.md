# Project: Singing Birthday Card Module

## Overview
- **Purpose**: Cheap module to play audio when birthday card opens
- **Application**: Gift/novelty, hidden inside greeting cards
- **Reference**: Commercial singing cards, ISD1820 modules

## Components (To Research)
- **Audio IC**: MP3 decoder with USB upload (MH2024K-24SS or WT2003S)
- **Speaker**: 23-28mm, 8 ohm, 0.5-1W
- **Light sensor**: LDR (GL5528) for open-card detection
- **Button**: Optional tactile switch
- **Pull-tab switch**: Break-contact mechanism

## Power
- **Input**: CR2032 coin cell (3V)
- **Current estimate**: <100mA during playback
- **No charging**: disposable battery

## Triggers (Jumper Selectable)
1. Light sensor - detects card opening
2. Button - manual press
3. Pull-tab - paper tab removal completes circuit

## Physical
- **Size**: ~85x55mm (credit card), flexible
- **Shape**: Rectangular
- **Mounting**: Glued/taped inside card

## Fabrication
- **Layers**: 2
- **Quantity**: 5-10 prototypes
- **Budget**: <$3/unit target
- **Assembly**: JLCPCB SMT
- **Solder mask**: Green
- **Silkscreen**: White
- **Finish**: HASL lead-free

## Open Questions
- [ ] Exact MP3 chip selection (check LCSC stock)
- [ ] Speaker driver - built into chip or need amp?
- [ ] USB connector - Micro or USB-C?
