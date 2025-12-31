# PCB Requirements Development

Phase 1 of PCB Systems Engineering Lifecycle.

## Activation
- User says: /pcb-requirements, develop requirements, conops
- After /pcb-init completes

## Purpose

Decompose PRD into detailed requirements and create Concept of Operations.

## Prerequisites

- `requirements/PRD.md` exists and is complete

## Process

### Step 1: Review PRD

Read `requirements/PRD.md` and extract:
- All stated requirements
- Implicit requirements (derived from use cases)
- Constraints and assumptions

### Step 2: Develop Operational Scenarios

Ask user about typical use cases:

**Question: User Profiles**
```
Who will use this device?
- End user (consumer)
- Technician (professional)
- Both
- Automated system (no direct user)
```

**Question: Primary Scenario**
```
Describe the most common way this device will be used:
1. How is it activated? (button, automatic, remote)
2. What happens during operation?
3. How long does typical operation last?
4. How is it deactivated?
```

**Question: Edge Cases**
```
What unusual situations might occur?
- Low battery
- Environmental extremes
- User errors
- Component failures
```

### Step 3: Create ConOps Document

Write `requirements/ConOps.md` with:

1. **System Overview** - One paragraph summary
2. **User Profiles** - Table of user types
3. **Operational Scenarios** - Step-by-step for each use case
4. **Operational Modes** - Normal, standby, error, etc.
5. **System States** - State machine if applicable
6. **Failure Modes** - What can go wrong, how detected

### Step 4: Decompose Requirements

Create detailed requirements in categories:

**Functional Requirements (FR-xxx)**
- What the system must DO
- Actions, behaviors, responses

**Performance Requirements (PR-xxx)**
- How WELL the system must perform
- Speed, accuracy, capacity, timing

**Interface Requirements (IR-xxx)**
- How system connects to external world
- Connectors, protocols, signals

**Environmental Requirements (ER-xxx)**
- Operating conditions
- Temperature, humidity, shock, vibration

**Physical Requirements (PHR-xxx)**
- Size, weight, form factor
- Mounting, enclosure

**Power Requirements (PWR-xxx)**
- Voltage, current, battery life
- Power states, consumption budgets

### Step 5: Assign Verification Methods

For each requirement, assign:
- **T** = Test (measure/observe in operation)
- **A** = Analysis (calculation/simulation)
- **I** = Inspection (visual examination)
- **D** = Demonstration (show it works)

### Step 6: Update RTM

Update `requirements/RTM.md` with all requirements:

```markdown
| ID | Requirement | Source | Verification | Status |
|----|-------------|--------|--------------|--------|
| FR-001 | System shall play audio | PRD 3.1 | T | Open |
| PR-001 | Audio shall be >70dB @ 10cm | PRD 4.1 | T | Open |
```

### Step 7: Output Summary

```
## Requirements Development Complete

### Statistics
- Functional Requirements: [count]
- Performance Requirements: [count]
- Interface Requirements: [count]
- Total Requirements: [count]

### Key Risks Identified
1. [risk 1]
2. [risk 2]

### Next Steps
1. Review ConOps at requirements/ConOps.md
2. Review RTM at requirements/RTM.md
3. Run /pcb-system-design to create ICD
```

## Requirement Writing Rules

Good requirements are:
- **Necessary** - Traceable to a need
- **Verifiable** - Can be tested/measured
- **Unambiguous** - Only one interpretation
- **Complete** - All conditions specified
- **Consistent** - No conflicts with other requirements
- **Atomic** - One requirement per statement

Bad: "The system should be fast"
Good: "The system shall respond within 100ms of trigger activation"

## Success Criteria

- [ ] ConOps document complete
- [ ] All requirements decomposed with IDs
- [ ] All requirements have verification method
- [ ] RTM populated
- [ ] User reviewed and approved
