#!/usr/bin/env python3
"""
Create KiCad schematic with proper net connectivity using global labels.
Parses the SKiDL netlist to understand connections.
"""

import uuid
import os
import re

def gen_uuid():
    return str(uuid.uuid4())

# Parse netlist to get connectivity
def parse_netlist(netlist_file):
    """Parse SKiDL netlist to extract nets and their connections."""
    with open(netlist_file, 'r') as f:
        content = f.read()

    nets = {}
    pin_to_net = {}  # (ref, pin) -> net_name

    # Find all nets
    net_pattern = r'\(net\s+\(code (\d+)\)\s+\(name "([^"]+)"\).*?\(class "[^"]+"\)(.*?)\)\s*(?=\(net|\)\)$)'
    for match in re.finditer(net_pattern, content, re.DOTALL):
        code, name, nodes_str = match.groups()
        nodes = []
        node_pattern = r'\(node\s+\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)'
        for node_match in re.finditer(node_pattern, nodes_str):
            ref, pin = node_match.groups()
            nodes.append({'ref': ref, 'pin': pin})
            pin_to_net[(ref, pin)] = name
        nets[name] = {'code': int(code), 'nodes': nodes}

    return nets, pin_to_net

# Read local symbol library to get pin positions
def get_symbol_pins():
    """Get pin positions for each symbol. Manually defined based on library."""
    # Pin positions relative to symbol center (x, y, angle)
    # These are approximate positions for label placement
    return {
        'ISD3900FYI': {
            # Left side pins (x=-25.4mm from center)
            '1': (-25.4, 29.21), '2': (-25.4, 26.67), '3': (-25.4, 24.13), '4': (-25.4, 21.59),
            '5': (-25.4, 19.05), '6': (-25.4, 16.51), '7': (-25.4, 13.97), '8': (-25.4, 11.43),
            '9': (-25.4, 8.89), '10': (-25.4, 6.35), '11': (-25.4, 3.81), '12': (-25.4, 1.27),
            '13': (-25.4, -1.27), '14': (-25.4, -3.81), '15': (-25.4, -6.35), '16': (-25.4, -8.89),
            '17': (-25.4, -11.43), '18': (-25.4, -13.97), '19': (-25.4, -16.51), '20': (-25.4, -19.05),
            '21': (-25.4, -21.59), '22': (-25.4, -24.13), '23': (-25.4, -26.67), '24': (-25.4, -29.21),
            # Right side pins (x=+25.4mm from center)
            '25': (25.4, -29.21), '26': (25.4, -26.67), '27': (25.4, -24.13), '28': (25.4, -21.59),
            '29': (25.4, -19.05), '30': (25.4, -16.51), '31': (25.4, -13.97), '32': (25.4, -11.43),
            '33': (25.4, -8.89), '34': (25.4, -6.35), '35': (25.4, -3.81), '36': (25.4, -1.27),
            '37': (25.4, 1.27), '38': (25.4, 3.81), '39': (25.4, 6.35), '40': (25.4, 8.89),
            '41': (25.4, 11.43), '42': (25.4, 13.97), '43': (25.4, 16.51), '44': (25.4, 19.05),
            '45': (25.4, 21.59), '46': (25.4, 24.13), '47': (25.4, 26.67), '48': (25.4, 29.21),
        },
        'W25Q16JVSSIQTR': {
            '1': (-12.7, 3.81), '2': (-12.7, 1.27), '3': (-12.7, -1.27), '4': (-12.7, -3.81),
            '5': (12.7, -3.81), '6': (12.7, -1.27), '7': (12.7, 1.27), '8': (12.7, 3.81),
        },
        'CR2032-BS-6-1': {
            '1': (-5.08, 0), '2': (5.08, 0),
        },
        'GL5528(10-20)': {
            '1': (-5.08, -1.27), '2': (5.08, -1.27),
        },
        'C': {
            '1': (0, 3.81), '2': (0, -3.81),
        },
        'R': {
            '1': (0, 3.81), '2': (0, -3.81),
        },
        'Conn_01x02_Pin': {
            '1': (5.08, 0), '2': (5.08, -2.54),
        },
        'SW_Push': {
            '1': (-5.08, 0), '2': (5.08, 0),
        },
    }

# NC pins for ISD3900FYI (pins that are not connected)
NC_PINS_U1 = ['1', '3', '4', '5', '6', '7', '8', '9', '19', '22', '23', '24', '25', '26', '28', '29', '30', '33', '34', '35', '36', '37', '39', '40', '41', '42', '45', '46', '47', '48']

# Component positions (from create_schematic.py)
COMPONENT_POS = {
    'U1': (140, 100),
    'U2': (230, 80),
    'BT1': (280, 100),
    'C1': (60, 50),
    'C2': (60, 65),
    'C3': (60, 80),
    'C4': (60, 95),
    'C5': (60, 110),
    'C6': (240, 50),
    'R1': (35, 130),
    'R2': (35, 115),
    'R3': (195, 40),
    'R4': (195, 55),
    'J1': (35, 85),
    'J2': (35, 100),
    'SW1': (195, 130),
}

# Map ref to symbol type
REF_TO_SYMBOL = {
    'U1': 'ISD3900FYI',
    'U2': 'W25Q16JVSSIQTR',
    'BT1': 'CR2032-BS-6-1',
    'R1': 'GL5528(10-20)',
    'R2': 'R', 'R3': 'R', 'R4': 'R',
    'C1': 'C', 'C2': 'C', 'C3': 'C', 'C4': 'C', 'C5': 'C', 'C6': 'C',
    'J1': 'Conn_01x02_Pin', 'J2': 'Conn_01x02_Pin',
    'SW1': 'SW_Push',
}

def generate_global_label(net_name, x, y, angle=0):
    """Generate a global label at the specified position."""
    # Determine shape based on net type
    if net_name in ['+3V', '+3V3', 'VCC']:
        shape = 'input'
    elif net_name in ['GND', 'VSS']:
        shape = 'input'
    else:
        shape = 'bidirectional'

    return f'''  (global_label "{net_name}"
    (shape {shape})
    (at {x} {y} {angle})
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{gen_uuid()}")
    (property "Intersheetrefs" "${{INTERSHEET_REFS}}"
      (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )'''

def generate_no_connect(x, y):
    """Generate a no-connect flag at the specified position."""
    return f'''  (no_connect
    (at {x} {y})
    (uuid "{gen_uuid()}")
  )'''

def generate_power_flag(x, y, net_name):
    """Generate a power flag symbol."""
    return f'''  (symbol
    (lib_id "power:PWR_FLAG")
    (at {x} {y} 0)
    (unit 1)
    (exclude_from_sim no)
    (in_bom no)
    (on_board yes)
    (dnp no)
    (uuid "{gen_uuid()}")
    (property "Reference" "#FLG0{1 if net_name == '+3V' else 2}"
      (at {x} {y + 3} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "PWR_FLAG"
      (at {x} {y - 2} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" ""
      (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" ""
      (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )'''

# Read the lib_symbols section from existing schematic
def get_lib_symbols():
    """Read embedded symbols from created schematic."""
    try:
        with open('singingcard.kicad_sch', 'r') as f:
            content = f.read()
        # Extract lib_symbols section
        start = content.find('(lib_symbols')
        if start == -1:
            return ''
        # Find matching close paren
        depth = 0
        for i, ch in enumerate(content[start:]):
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    return content[start:start+i+1]
        return ''
    except:
        return '  (lib_symbols\n  )'

def main():
    # Parse netlist
    if not os.path.exists('singingcard.net'):
        print("Error: singingcard.net not found")
        return

    nets, pin_to_net = parse_netlist('singingcard.net')
    print(f"Found {len(nets)} nets")
    for net_name, net_data in nets.items():
        print(f"  {net_name}: {len(net_data['nodes'])} nodes")

    symbol_pins = get_symbol_pins()

    # Start building schematic
    sch = []
    sch.append(f'''(kicad_sch
  (version 20231120)
  (generator "create_schematic_v2.py")
  (generator_version "1.0")
  (uuid "{gen_uuid()}")
  (paper "A3")
  (title_block
    (title "Singing Birthday Card Module")
    (date "2025-12-30")
    (rev "1.0")
    (comment 1 "ISD3900FYI Audio Playback")
    (comment 2 "CR2032 Powered, SPI Flash Storage")
  )
''')

    # Get lib_symbols from existing schematic
    lib_symbols = get_lib_symbols()
    if lib_symbols:
        sch.append(lib_symbols)
    else:
        sch.append('  (lib_symbols\n  )')
    sch.append('')

    # Note: The existing schematic already has the component symbols placed.
    # This script focuses on adding global labels and no-connects.
    # For a complete solution, we would need to merge with existing schematic.

    # For now, let's output the labels and no-connects that need to be added
    labels = []
    no_connects = []

    for ref, (comp_x, comp_y) in COMPONENT_POS.items():
        symbol_type = REF_TO_SYMBOL.get(ref)
        if not symbol_type:
            continue

        pins = symbol_pins.get(symbol_type, {})

        for pin, (pin_dx, pin_dy) in pins.items():
            x = comp_x + pin_dx
            y = comp_y + pin_dy

            # Check if this pin is connected to a net
            net_name = pin_to_net.get((ref, pin))

            if net_name:
                # Add global label
                angle = 180 if pin_dx < 0 else 0  # Face outward
                labels.append(generate_global_label(net_name, x, y, angle))
            elif ref == 'U1' and pin in NC_PINS_U1:
                # Add no-connect for NC pins
                no_connects.append(generate_no_connect(x, y))

    # Add power flags for +3V and GND
    # These need to be connected to the nets to indicate they're driven
    power_flags = []
    power_flags.append(generate_power_flag(280, 85, '+3V'))  # Near BT1
    power_flags.append(generate_power_flag(280, 115, 'GND'))  # Near BT1

    print(f"\nGenerated {len(labels)} global labels")
    print(f"Generated {len(no_connects)} no-connects")
    print(f"Generated {len(power_flags)} power flags")

    # Read existing schematic and merge
    try:
        with open('singingcard.kicad_sch', 'r') as f:
            existing = f.read()

        # Find the closing parenthesis and insert before it
        insert_pos = existing.rfind(')')

        new_content = existing[:insert_pos]
        new_content += '\n\n'
        for label in labels:
            new_content += label + '\n'
        new_content += '\n'
        for nc in no_connects:
            new_content += nc + '\n'
        new_content += '\n'
        for pf in power_flags:
            new_content += pf + '\n'
        new_content += '\n)'

        with open('singingcard.kicad_sch', 'w') as f:
            f.write(new_content)

        print("\nUpdated singingcard.kicad_sch with labels and no-connects")

    except Exception as e:
        print(f"Error updating schematic: {e}")

if __name__ == '__main__':
    main()
