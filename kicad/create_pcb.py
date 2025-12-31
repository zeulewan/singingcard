#!/usr/bin/env python3
"""
Create KiCad PCB file from netlist with footprints placed.
Properly handles KiCad 8/9 multiline S-expression format.
"""

import os
import re
import uuid
from datetime import datetime

# Board dimensions (mm)
BOARD_WIDTH = 85.0
BOARD_HEIGHT = 55.0
BOARD_ORIGIN_X = 100.0
BOARD_ORIGIN_Y = 100.0

# Footprint library paths
FOOTPRINT_LIB_PATH = os.path.abspath('libs/singingcard.pretty')
KICAD_FOOTPRINT_PATH = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'

def gen_uuid():
    return str(uuid.uuid4())

def parse_netlist(netlist_file):
    """Parse SKiDL netlist to extract components and nets."""
    with open(netlist_file, 'r') as f:
        content = f.read()

    components = []
    nets = []

    comp_pattern = r'\(comp\s+\(ref "([^"]+)"\)\s+\(value "([^"]+)"\).*?\(footprint "([^"]+)"\).*?\(tstamps "([^"]+)"\)'
    for match in re.finditer(comp_pattern, content, re.DOTALL):
        ref, value, footprint, tstamp = match.groups()
        components.append({
            'ref': ref,
            'value': value,
            'footprint': footprint,
            'uuid': tstamp
        })

    net_pattern = r'\(net\s+\(code (\d+)\)\s+\(name "([^"]+)"\).*?\(class "[^"]+"\)(.*?)\)\s*(?=\(net|\)$)'
    for match in re.finditer(net_pattern, content, re.DOTALL):
        code, name, nodes_str = match.groups()
        nodes = []
        node_pattern = r'\(node\s+\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)'
        for node_match in re.finditer(node_pattern, nodes_str):
            ref, pin = node_match.groups()
            nodes.append({'ref': ref, 'pin': pin})
        nets.append({
            'code': int(code),
            'name': name,
            'nodes': nodes
        })

    return components, nets

def place_components(components):
    """Calculate placement positions for components.

    Improved placement with more spacing to allow cleaner routing.
    Key principles:
    - U1 (MCU) in center-left area
    - U2 (SPI flash) to the right with clear path for SPI signals
    - Bypass caps close to their associated IC power pins
    - Connectors on edges
    - Button accessible but not in routing path
    """
    # Center point for main layout
    cx = BOARD_ORIGIN_X + 38  # Shift left to give room for SPI flash on right
    cy = BOARD_ORIGIN_Y + BOARD_HEIGHT/2

    positions = {
        # Main ICs
        'U1': (cx, cy, 0),  # MCU in center-left (LQFP-48 is 7x7mm)
        'U2': (cx + 28, cy - 8, 0),  # SPI flash to the right, clear routing path (SOIC-8)

        # Battery holder on far right
        'BT1': (BOARD_ORIGIN_X + BOARD_WIDTH - 18, cy, 0),  # CR2032 holder

        # Bypass capacitors - spread around U1
        'C1': (cx - 12, cy - 6, 0),   # 0603 near U1 pin 11 (+3V)
        'C2': (cx - 12, cy + 6, 0),   # 0805 near U1
        'C3': (cx + 12, cy - 6, 0),   # 0603 VREG bypass
        'C4': (cx - 6, cy - 12, 0),   # 0603 near U1 top
        'C5': (cx + 12, cy + 6, 0),   # 0805
        'C6': (cx + 28, cy + 2, 0),   # 0603 near U2/battery

        # Resistors - spread out more
        'R1': (BOARD_ORIGIN_X + 12, cy - 8, 0),    # LDR (through-hole)
        'R2': (BOARD_ORIGIN_X + 12, cy - 18, 0),   # LDR pullup - NOT rotated, more space
        'R3': (cx - 6, cy - 18, 0),    # RESET pullup - above U1
        'R4': (cx - 6, cy + 18, 0),    # CSB pullup - below U1

        # Connectors on bottom edge - spread apart to avoid routing conflicts
        'J1': (BOARD_ORIGIN_X + 15, BOARD_ORIGIN_Y + BOARD_HEIGHT - 8, 0),  # Speaker
        'J2': (BOARD_ORIGIN_X + 50, BOARD_ORIGIN_Y + BOARD_HEIGHT - 8, 0),  # Tab trigger (moved right)

        # Button on right side, away from main routing
        'SW1': (cx + 28, cy + 18, 0),  # Button near bottom right
    }

    placements = []
    for comp in components:
        ref = comp['ref']
        if ref in positions:
            x, y, rot = positions[ref]
        else:
            x = BOARD_ORIGIN_X + 10
            y = BOARD_ORIGIN_Y + 10
            rot = 0

        placements.append({
            **comp,
            'x': x,
            'y': y,
            'rotation': rot
        })

    return placements

def parse_sexp(text):
    """Simple S-expression parser that handles nested parentheses."""
    # Find matching paren for each opening paren
    stack = []
    pairs = {}
    for i, ch in enumerate(text):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            if stack:
                start = stack.pop()
                pairs[start] = i
    return pairs

def extract_footprint_content(fp_file, ref, value, x, y, rot, fp_uuid, net_by_ref_pin, footprint_str):
    """Extract and transform footprint for PCB embedding."""
    with open(fp_file, 'r') as f:
        content = f.read()

    # Find the content inside the top-level (footprint ...)
    first_paren = content.find('(')
    if first_paren == -1:
        return None

    # Parse to find the inner content
    pairs = parse_sexp(content)
    last_paren = pairs.get(first_paren)
    if last_paren is None:
        return None

    # Get inner content (after first line up to last paren)
    first_newline = content.find('\n', first_paren)
    inner_content = content[first_newline:last_paren].strip()

    # Build the new footprint with our header
    result = []
    result.append(f'  (footprint "{footprint_str}"')
    result.append(f'    (layer "F.Cu")')
    result.append(f'    (uuid "{fp_uuid}")')
    result.append(f'    (at {x} {y} {rot})')

    # Process inner content line by line
    lines = inner_content.split('\n')
    in_property_ref = False
    in_property_val = False
    skip_until_close = 0
    current_pad = None
    pad_content = []

    for line in lines:
        stripped = line.strip()

        # Skip version and generator lines
        if stripped.startswith('(version') or stripped.startswith('(generator'):
            continue

        # Skip the layer line (we added our own)
        if stripped.startswith('(layer "F.Cu")') and '(' not in stripped[1:]:
            continue

        # Handle property Reference - replace with our ref
        if '(property "Reference"' in stripped:
            result.append(f'    (property "Reference" "{ref}"')
            in_property_ref = True
            skip_until_close = 1
            continue

        if in_property_ref:
            if '(' in stripped:
                skip_until_close += stripped.count('(')
            if ')' in stripped:
                skip_until_close -= stripped.count(')')
            if skip_until_close <= 0:
                in_property_ref = False
                result.append(f'      (at 0 -3 {rot})')
                result.append(f'      (layer "F.SilkS")')
                result.append(f'      (uuid "{gen_uuid()}")')
                result.append(f'      (effects (font (size 1 1) (thickness 0.15)))')
                result.append(f'    )')
            continue

        # Handle property Value - replace with our value
        if '(property "Value"' in stripped:
            result.append(f'    (property "Value" "{value}"')
            in_property_val = True
            skip_until_close = 1
            continue

        if in_property_val:
            if '(' in stripped:
                skip_until_close += stripped.count('(')
            if ')' in stripped:
                skip_until_close -= stripped.count(')')
            if skip_until_close <= 0:
                in_property_val = False
                result.append(f'      (at 0 3 {rot})')
                result.append(f'      (layer "F.Fab")')
                result.append(f'      (uuid "{gen_uuid()}")')
                result.append(f'      (effects (font (size 1 1) (thickness 0.15)))')
                result.append(f'    )')
            continue

        # Skip other property definitions
        if '(property "Datasheet"' in stripped or '(property "Description"' in stripped:
            skip_until_close = 1
            continue

        if skip_until_close > 0:
            if '(' in stripped:
                skip_until_close += stripped.count('(')
            if ')' in stripped:
                skip_until_close -= stripped.count(')')
            continue

        # Handle pads - add net info
        if stripped.startswith('(pad "'):
            # Extract pad number
            pad_match = re.match(r'\(pad "(\d+)"', stripped)
            if pad_match:
                current_pad = pad_match.group(1)
                pad_content = [line]
                continue

        if current_pad is not None:
            pad_content.append(line)
            if stripped == ')':
                # End of pad, add net info if needed
                key = (ref, current_pad)
                if key in net_by_ref_pin:
                    net_code, net_name = net_by_ref_pin[key]
                    # Insert net before closing paren
                    pad_content.insert(-1, f'\t\t(net {net_code} "{net_name}")')
                for pad_line in pad_content:
                    result.append('  ' + pad_line)
                current_pad = None
                pad_content = []
            continue

        # Copy other content with proper indentation
        if stripped:
            result.append('  ' + line)

    result.append('  )')

    return '\n'.join(result)

def load_footprint(footprint_str, ref, value, x, y, rot, fp_uuid, net_by_ref_pin):
    """Load footprint file and convert to PCB embedded format."""
    if ':' in footprint_str:
        lib, fp_name = footprint_str.split(':', 1)
    else:
        lib = 'unknown'
        fp_name = footprint_str

    if lib == 'singingcard':
        fp_path = FOOTPRINT_LIB_PATH
    else:
        fp_path = os.path.join(KICAD_FOOTPRINT_PATH, f"{lib}.pretty")

    fp_file = os.path.join(fp_path, f"{fp_name}.kicad_mod")

    if not os.path.exists(fp_file):
        print(f"Warning: Footprint not found: {fp_file}")
        return None

    return extract_footprint_content(fp_file, ref, value, x, y, rot, fp_uuid, net_by_ref_pin, footprint_str)

def generate_pcb(components, nets, placements):
    """Generate KiCad PCB file content."""

    now = datetime.now().strftime("%Y-%m-%d")

    # Create net lookup
    net_by_ref_pin = {}
    for net in nets:
        for node in net['nodes']:
            key = (node['ref'], node['pin'])
            net_by_ref_pin[key] = (net['code'], net['name'])

    pcb_parts = []

    # Header
    pcb_parts.append(f'''(kicad_pcb
  (version 20240108)
  (generator "pcbnew")
  (generator_version "8.0")
  (general
    (thickness 1.6)
    (legacy_teardrops no)
  )
  (paper "A4")
  (title_block
    (title "Singing Birthday Card Module")
    (date "{now}")
    (rev "1.0")
    (comment 1 "ISD3900FYI Audio Playback")
    (comment 2 "CR2032 Powered")
  )
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (42 "Eco1.User" user "User.Eco1")
    (43 "Eco2.User" user "User.Eco2")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
    (50 "User.1" user)
    (51 "User.2" user)
    (52 "User.3" user)
    (53 "User.4" user)
    (54 "User.5" user)
    (55 "User.6" user)
    (56 "User.7" user)
    (57 "User.8" user)
    (58 "User.9" user)
  )
  (setup
    (pad_to_mask_clearance 0)
    (allow_soldermask_bridges_in_footprints no)
    (pcbplotparams
      (layerselection 0x00010fc_ffffffff)
      (plot_on_all_layers_selection 0x0000000_00000000)
      (disableapertmacros no)
      (usegerberextensions no)
      (usegerberattributes yes)
      (usegerberadvancedattributes yes)
      (creategerberjobfile yes)
      (dashed_line_dash_ratio 12.000000)
      (dashed_line_gap_ratio 3.000000)
      (svgprecision 4)
      (plotframeref no)
      (viasonmask no)
      (mode 1)
      (useauxorigin no)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15.000000)
      (pdf_front_fp_property_popups yes)
      (pdf_back_fp_property_popups yes)
      (dxfpolygonmode yes)
      (dxfimperialunits yes)
      (dxfusepcbnewfont yes)
      (psnegative no)
      (psa4output no)
      (plotreference yes)
      (plotvalue yes)
      (plotfptext yes)
      (plotinvisibletext no)
      (sketchpadsonfab no)
      (subtractmaskfromsilk no)
      (outputformat 1)
      (mirror no)
      (drillshape 1)
      (scaleselection 1)
      (outputdirectory "")
    )
  )''')

    # Add nets
    pcb_parts.append('')
    pcb_parts.append('  (net 0 "")')
    for net in nets:
        pcb_parts.append(f'  (net {net["code"]} "{net["name"]}")')

    # Add board outline
    x1 = BOARD_ORIGIN_X
    y1 = BOARD_ORIGIN_Y
    x2 = BOARD_ORIGIN_X + BOARD_WIDTH
    y2 = BOARD_ORIGIN_Y + BOARD_HEIGHT

    pcb_parts.append(f'''
  (gr_rect
    (start {x1} {y1})
    (end {x2} {y2})
    (stroke
      (width 0.15)
      (type default)
    )
    (fill none)
    (layer "Edge.Cuts")
    (uuid "{gen_uuid()}")
  )''')

    # Add footprints
    for place in placements:
        fp_content = load_footprint(
            place['footprint'],
            place['ref'],
            place['value'],
            place['x'],
            place['y'],
            place['rotation'],
            place['uuid'],
            net_by_ref_pin
        )
        if fp_content:
            pcb_parts.append('')
            pcb_parts.append(fp_content)

    pcb_parts.append('')
    pcb_parts.append(')')

    return '\n'.join(pcb_parts)

def main():
    print("Parsing netlist...")
    components, nets = parse_netlist('singingcard.net')
    print(f"Found {len(components)} components and {len(nets)} nets")

    print("Calculating component placement...")
    placements = place_components(components)

    print("Generating PCB file...")
    pcb_content = generate_pcb(components, nets, placements)

    with open('singingcard.kicad_pcb', 'w') as f:
        f.write(pcb_content)

    print("Generated: singingcard.kicad_pcb")
    print(f"Board size: {BOARD_WIDTH}mm x {BOARD_HEIGHT}mm")

if __name__ == '__main__':
    main()
