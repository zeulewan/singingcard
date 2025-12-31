# Currently Working On

## Project: Singing Birthday Card Module

### Status: Requirements gathered, need to research chips on LCSC

### Gathered Requirements

- **Purpose**: Cheap singing birthday card module
- **Audio**: 10-20 sec, MP3 format, USB drag-and-drop upload
- **Triggers** (selectable via jumper):
  - Light sensor (LDR) - card opens, light triggers
  - Button - manual trigger option
  - Pull-tab (break-contact) - paper tab removal triggers
- **Speaker**: 23-28mm, 8 ohm
- **Battery**: CR2032 coin cell (3V, non-rechargeable)
- **Board size**: ~85x55mm (credit card), flexible
- **Volume**: Fixed (no potentiometer)
- **PCB**: Green, 2-layer
- **Quantity**: 5-10 prototypes
- **Budget**: Ultra cheap (<$3/unit target, but USB/MP3 adds cost)

### Next Steps

1. Research MP3+USB chips on LCSC (MH2024K-24SS, WT2003S, or similar)
2. Find LDR light sensor (GL5528 or similar)
3. Create kicad/specs.md with full specifications
4. Start component selection in kicad/component-selection.md

### Key Chips to Research

From earlier Perplexity research:
- **MH2024K-24SS**: MP3 decoder, USB mass storage, speaker out, ~$1-2
- **WT2003S**: USB/MP3 chip, trigger pins
- **GL5528**: LDR for light sensing (~$0.10)
- **CR2032 holder**: coin cell battery

### Files Created This Session

- README.md
- user-prompts.md
- docs/tool-setup.md
- docs/workflow-reference.md
- docs/notes.md
- .claude/skills/kicad-agent.md
- .claude/skills/pcb-requirements.md
- kicad-agent-workflow-research.md (comprehensive tool research)
- CLAUDE.md (attribution for this repo)
