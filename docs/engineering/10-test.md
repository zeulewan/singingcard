# PCB Test & Verification

Phase 11 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-test, test board, verify pcb, bring up
- After boards received from manufacturing

## Purpose

Verify manufactured PCBs meet requirements through systematic testing.

## Prerequisites

- PCBs received from JLCPCB
- Test equipment available
- Requirements Traceability Matrix (RTM) ready

## Test Levels

Following V-Model, testing proceeds from component to system level:

```
Requirements ◄─────────────────────────────► Acceptance Test
     │                                              ▲
     ▼                                              │
System Design ◄────────────────────────────► System Test
     │                                              ▲
     ▼                                              │
Subsystem Design ◄─────────────────────────► Integration Test
     │                                              ▲
     ▼                                              │
Component Design ◄─────────────────────────► Unit Test
```

## Process

### Step 1: Incoming Inspection

**Visual Inspection Checklist:**
- [ ] Correct quantity received
- [ ] Board dimensions match design
- [ ] No visible damage (cracks, scratches)
- [ ] Solder mask intact
- [ ] Silkscreen legible
- [ ] Copper traces clean (no shorts/opens visible)
- [ ] Components present (if assembled)
- [ ] Component orientation correct
- [ ] Solder joints acceptable

**Take photos and save to `tmp/inspection/`**

**Defects Found:**
| Item | Location | Severity | Action |
|------|----------|----------|--------|
| | | | |

### Step 2: Bare Board Testing (if applicable)

If boards are not assembled:

**Continuity Testing:**
- [ ] Power rails continuous end-to-end
- [ ] No shorts between VCC and GND
- [ ] Critical signal paths continuous

**Isolation Testing:**
- [ ] Power rails isolated from each other
- [ ] Signal paths isolated from power

### Step 3: Power-On Test (First Article)

**CRITICAL: Use current-limited power supply**

**Pre-Power Checklist:**
- [ ] Visual inspection complete
- [ ] No obvious shorts
- [ ] Correct polarity marked
- [ ] Current limit set (50-100mA initially)

**Power-On Procedure:**
1. Connect current-limited supply
2. Set voltage to minimum, slowly increase to nominal
3. Monitor current draw
4. Check for:
   - Smoke or burning smell (STOP immediately)
   - Excessive current (compare to expected)
   - Correct voltage at test points
   - No hot components

**Initial Power Measurements:**
| Measurement | Expected | Actual | Status |
|-------------|----------|--------|--------|
| Input current (idle) | | | |
| VCC voltage | | | |
| 3V3 rail (if present) | | | |
| Current (active) | | | |

### Step 4: Unit Testing

Test individual functional blocks:

**Power Supply:**
- [ ] Input voltage range
- [ ] Output voltage accuracy
- [ ] Load regulation
- [ ] Ripple voltage (if measurable)

**Microcontroller/IC:**
- [ ] Oscillator running (scope on XTAL)
- [ ] Reset behavior
- [ ] I/O pins toggle correctly
- [ ] Programming interface works

**Communication Interfaces:**
- [ ] SPI/I2C signals present
- [ ] Correct timing (if scope available)
- [ ] Device responds to commands

**Sensors:**
- [ ] Responds to stimulus
- [ ] Values in expected range

**Output Devices:**
- [ ] LED illuminates
- [ ] Speaker produces sound
- [ ] Motor runs (if applicable)

### Step 5: Integration Testing

Test interactions between subsystems:

**Test Cases:**
| ID | Description | Steps | Expected Result | Actual | Status |
|----|-------------|-------|-----------------|--------|--------|
| IT-001 | | | | | |
| IT-002 | | | | | |

### Step 6: System Testing

Test complete system operation:

**Functional Tests:**
Map to Functional Requirements (FR-xxx):

| Req ID | Requirement | Test Method | Result | Status |
|--------|-------------|-------------|--------|--------|
| FR-001 | | | | |
| FR-002 | | | | |

**Performance Tests:**
Map to Performance Requirements (PR-xxx):

| Req ID | Requirement | Test Method | Target | Result | Status |
|--------|-------------|-------------|--------|--------|--------|
| PR-001 | | | | | |

### Step 7: Environmental Testing (If Required)

**Temperature Testing:**
- [ ] Function at minimum temperature
- [ ] Function at maximum temperature
- [ ] No damage after temperature cycling

**Other Environmental:**
- [ ] Humidity (if specified)
- [ ] Vibration (if specified)
- [ ] Drop test (if specified)

### Step 8: Acceptance Testing

Final verification against all requirements:

**Update Requirements Traceability Matrix:**

| Req ID | Verified | Method | Evidence | Date |
|--------|----------|--------|----------|------|
| FR-001 | Yes/No | T/A/I/D | | |
| FR-002 | Yes/No | T/A/I/D | | |

**Verification Methods:**
- T = Test (measured)
- A = Analysis (calculated)
- I = Inspection (visual)
- D = Demonstration (observed)

### Step 9: Document Results

Create Test Report `process/reviews/TEST-REPORT.md`:

```markdown
# Test Report: [Project Name]

## Summary
- Test Date: [date]
- Tester: [name]
- Units Tested: [count]
- Pass: [count]
- Fail: [count]

## Test Configuration
- Power Supply: [model]
- Multimeter: [model]
- Other Equipment: [list]

## Results Summary

### Functional Requirements
| Req ID | Result |
|--------|--------|
| FR-001 | PASS/FAIL |

### Performance Requirements
| Req ID | Target | Result | Status |
|--------|--------|--------|--------|
| PR-001 | | | PASS/FAIL |

## Defects Found
| ID | Description | Severity | Resolution |
|----|-------------|----------|------------|
| | | | |

## Conclusions
[Summary of test results and recommendations]

## Approval
- Tested by: [name]
- Reviewed by: [name]
- Date: [date]
```

### Step 10: Lessons Learned

Document improvements for next revision:

```markdown
## Lessons Learned

### What Worked Well
1.
2.

### What Could Be Improved
1.
2.

### Design Changes for Next Revision
1.
2.
```

## Test Equipment Recommendations

| Equipment | Purpose | Minimum Spec |
|-----------|---------|--------------|
| Multimeter | Voltage, current, resistance | 3.5 digit |
| Power Supply | Controlled power | Current limiting |
| Oscilloscope | Signal analysis | 50MHz, 2ch |
| Logic Analyzer | Digital debug | 8ch, 24MHz |
| Programmer | MCU programming | Device-specific |

## Common First-Board Issues

| Symptom | Likely Cause | Check |
|---------|--------------|-------|
| No power | Solder bridge, open | Visual, continuity |
| High current | Short circuit | Remove ICs, test rails |
| Chip hot | Wrong orientation | Check pin 1 |
| No clock | Crystal circuit | ESR of caps, layout |
| SPI/I2C fail | Wrong pull-ups | Signal integrity |
| Noise | Decoupling | Add/improve caps |

## Output Summary

```
## Testing Complete

### Results
- Units tested: [count]
- Passed: [count]
- Failed: [count]

### Requirements Verification
- Functional: [X]/[Y] passed
- Performance: [X]/[Y] met
- Overall: [PASS/CONDITIONAL/FAIL]

### Next Steps
[ ] Project complete - celebrate!
[ ] Minor fixes - create issue list
[ ] Major rework - plan revision

### Documentation
- Test report: process/reviews/TEST-REPORT.md
- RTM updated: requirements/RTM.md
- Lessons learned: process/reviews/LESSONS-LEARNED.md
```

## Success Criteria

- [ ] All units inspected
- [ ] Power-on test completed
- [ ] All requirements verified
- [ ] Test report documented
- [ ] Defects logged
- [ ] Lessons learned captured
