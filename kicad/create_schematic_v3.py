#!/usr/bin/env python3
"""
Create complete KiCad schematic with embedded symbols and proper connectivity.
Uses global labels for all net connections to avoid complex wire routing.
"""

import uuid
import os
import re

def gen_uuid():
    return str(uuid.uuid4())

# Component definitions with their pins
COMPONENTS = {
    'U1': {
        'name': 'ISD3900FYI',
        'value': 'ISD3900FYI',
        'footprint': 'singingcard:LQFP-48_7x7mm_P0.5mm',
        'pins': {
            '2': ('SPIA', 'bidirectional'), '10': ('VCCD', 'power_in'), '11': ('VCCA', 'power_in'),
            '12': ('FT', 'output'), '13': ('XCLKO', 'output'), '14': ('ANA_IN+', 'input'),
            '15': ('ANA_IN-', 'input'), '16': ('AGNDR', 'power_in'), '17': ('SP+', 'output'),
            '18': ('SP-', 'output'), '20': ('VCCP', 'power_in'), '21': ('GPIO0', 'bidirectional'),
            '27': ('GPIO1', 'bidirectional'), '31': ('GPIO2', 'bidirectional'), '32': ('XCLK', 'input'),
            '38': ('SPI_SS', 'input'), '43': ('SPI_MOSI', 'input'), '44': ('SPI_MISO', 'output'),
        },
        'nc_pins': ['1', '3', '4', '5', '6', '7', '8', '9', '19', '22', '23', '24', '25', '26',
                    '28', '29', '30', '33', '34', '35', '36', '37', '39', '40', '41', '42', '45', '46', '47', '48'],
        'power_pins': {'10': 'VCC', '11': 'VCC', '16': 'GND', '20': 'VCC'},
        'position': (120, 100),
    },
    'U2': {
        'name': 'W25Q16JVSSIQ',
        'value': 'W25Q16JVSSIQ',
        'footprint': 'singingcard:SOIC-8_5.23x5.23mm_P1.27mm',
        'pins': {
            '1': ('/CS', 'input'), '2': ('DO', 'output'), '3': ('WP', 'input'),
            '4': ('GND', 'power_in'), '5': ('DI', 'input'), '6': ('CLK', 'input'),
            '7': ('HOLD', 'input'), '8': ('VCC', 'power_in'),
        },
        'power_pins': {'4': 'GND', '8': 'VCC'},
        'position': (220, 100),
    },
    'BT1': {
        'name': 'CR2032',
        'value': 'CR2032',
        'footprint': 'singingcard:BAT-TH_CR2032-BS-6-1',
        'pins': {
            '1': ('+', 'power_out'), '2': ('-', 'power_out'),
        },
        'power_pins': {'1': 'VCC', '2': 'GND'},
        'position': (280, 100),
    },
    'R1': {
        'name': 'GL5528',
        'value': 'LDR',
        'footprint': 'singingcard:LDR_GL5528',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (50, 60),
    },
    'R2': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (50, 80),
    },
    'R3': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (50, 100),
    },
    'R4': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (50, 120),
    },
    'C1': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (50, 145),
    },
    'C2': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (70, 145),
    },
    'C3': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (90, 145),
    },
    'C4': {
        'name': 'C',
        'value': '10uF',
        'footprint': 'Capacitor_SMD:C_0805_2012Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (110, 145),
    },
    'C5': {
        'name': 'C',
        'value': '10uF',
        'footprint': 'Capacitor_SMD:C_0805_2012Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (130, 145),
    },
    'C6': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (220, 130),
    },
    'J1': {
        'name': 'Conn_01x02',
        'value': 'Speaker',
        'footprint': 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (180, 60),
    },
    'J2': {
        'name': 'Conn_01x02',
        'value': 'USB_Audio',
        'footprint': 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (180, 80),
    },
    'SW1': {
        'name': 'SW_Push',
        'value': 'Button',
        'footprint': 'singingcard:SW_SPST_Omron_B3S-1000',
        'pins': {'1': ('1', 'passive'), '2': ('2', 'passive')},
        'position': (50, 170),
    },
}

# Net connections from SKiDL netlist
NETS = {
    '+3V': [('BT1', '1'), ('U1', '10'), ('U1', '11'), ('U1', '20'), ('U2', '8'),
            ('C1', '1'), ('C2', '1'), ('C3', '1'), ('C4', '1'), ('C5', '1'), ('C6', '1'),
            ('R2', '1'), ('R3', '1'), ('R4', '1'), ('U2', '3'), ('U2', '7')],
    'GND': [('BT1', '2'), ('U1', '16'), ('U2', '4'),
            ('C1', '2'), ('C2', '2'), ('C3', '2'), ('C4', '2'), ('C5', '2'), ('C6', '2'),
            ('SW1', '2')],
    'GPIO0_LDR': [('U1', '21'), ('R1', '1'), ('R2', '2')],
    'GPIO1_BTN': [('U1', '27'), ('SW1', '1')],
    'GPIO2_TAB': [('U1', '31'), ('R3', '2')],
    'RESET': [('U1', '12'), ('R4', '2')],
    'SPI_CS': [('U1', '38'), ('U2', '1')],
    'SPI_MOSI': [('U1', '43'), ('U2', '5')],
    'SPI_MISO': [('U1', '44'), ('U2', '2')],
    'SPI_SCK': [('U1', '32'), ('U2', '6')],
    'N$1': [('U1', '17'), ('J1', '1')],  # SP+ to speaker
    'N$2': [('U1', '18'), ('J1', '2')],  # SP- to speaker
    'ANA_IN+': [('U1', '14'), ('J2', '1')],  # Audio input
    'ANA_IN-': [('U1', '15'), ('J2', '2')],  # Audio input
    'XCLKO': [('U1', '13')],  # Crystal out - not connected
    'LDR_GND': [('R1', '2')],  # LDR to ground - add to GND
    'VREG': [('U1', '2')],  # Voltage regulator bypass
}

def create_lib_symbol(name, pins, is_power=False):
    """Create an embedded symbol definition."""
    # Calculate symbol size based on number of pins
    num_pins = len(pins)
    height = max(5.08, (num_pins + 1) * 2.54)
    width = 15.24

    # Start symbol
    sym = f'''    (symbol "{name}"
      (pin_names (offset 1.016))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "U"
        (at 0 {height/2 + 2.54} 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "{name}"
        (at 0 {-height/2 - 2.54} 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "{name}_1_1"
        (rectangle (start {-width/2} {height/2}) (end {width/2} {-height/2})
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
'''

    # Add pins
    pin_y = height/2 - 2.54
    for pin_num, (pin_name, pin_type) in sorted(pins.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
        pin_type_kicad = {
            'input': 'input',
            'output': 'output',
            'bidirectional': 'bidirectional',
            'passive': 'passive',
            'power_in': 'power_in',
            'power_out': 'power_out',
        }.get(pin_type, 'bidirectional')

        # Alternate pins left and right
        pin_idx = list(pins.keys()).index(pin_num)
        if pin_idx % 2 == 0:
            x = -width/2 - 2.54
            angle = 0
        else:
            x = width/2 + 2.54
            angle = 180
        y = height/2 - 2.54 - (pin_idx // 2) * 2.54

        sym += f'''        (pin {pin_type_kicad} line
          (at {x} {y} {angle})
          (length 2.54)
          (name "{pin_name}" (effects (font (size 1.016 1.016))))
          (number "{pin_num}" (effects (font (size 1.016 1.016))))
        )
'''

    sym += '''      )
    )
'''
    return sym

def create_simple_symbol(name, ref_prefix, num_pins=2, vertical=True):
    """Create a simple 2-pin symbol (R, C, etc)."""
    if num_pins == 2:
        sym = f'''    (symbol "{name}"
      (pin_numbers hide)
      (pin_names hide)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "{ref_prefix}"
        (at 2.54 0 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )
      (property "Value" "{name}"
        (at 2.54 -2.54 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "{name}_1_1"
        (rectangle (start -1.016 2.54) (end 1.016 -2.54)
          (stroke (width 0.254) (type default))
          (fill (type none))
        )
        (pin passive line
          (at 0 5.08 270)
          (length 2.54)
          (name "1" (effects (font (size 1.016 1.016))))
          (number "1" (effects (font (size 1.016 1.016))))
        )
        (pin passive line
          (at 0 -5.08 90)
          (length 2.54)
          (name "2" (effects (font (size 1.016 1.016))))
          (number "2" (effects (font (size 1.016 1.016))))
        )
      )
    )
'''
    return sym

def create_power_symbol(name, is_gnd=False):
    """Create a power symbol (+3V3 or GND)."""
    if is_gnd:
        sym = f'''    (symbol "{name}"
      (power)
      (pin_numbers hide)
      (pin_names (offset 0) hide)
      (exclude_from_sim no)
      (in_bom no)
      (on_board yes)
      (property "Reference" "#PWR"
        (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Value" "{name}"
        (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "{name}_1_1"
        (polyline
          (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
          (stroke (width 0) (type default))
          (fill (type outline))
        )
        (pin power_in line
          (at 0 0 270)
          (length 0)
          (name "{name}" (effects (font (size 1.016 1.016))))
          (number "1" (effects (font (size 1.016 1.016))))
        )
      )
    )
'''
    else:
        sym = f'''    (symbol "{name}"
      (power)
      (pin_numbers hide)
      (pin_names (offset 0) hide)
      (exclude_from_sim no)
      (in_bom no)
      (on_board yes)
      (property "Reference" "#PWR"
        (at 0 3.81 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Value" "{name}"
        (at 0 3.81 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "{name}_1_1"
        (polyline
          (pts (xy 0 0) (xy 0 1.27) (xy -1.27 1.27) (xy 0 2.54) (xy 1.27 1.27) (xy 0 1.27))
          (stroke (width 0) (type default))
          (fill (type outline))
        )
        (pin power_in line
          (at 0 0 90)
          (length 0)
          (name "{name}" (effects (font (size 1.016 1.016))))
          (number "1" (effects (font (size 1.016 1.016))))
        )
      )
    )
'''
    return sym

def generate_symbol_instance(ref, comp, lib_name):
    """Generate a symbol instance in the schematic."""
    x, y = comp['position']

    sym = f'''  (symbol
    (lib_id "{lib_name}")
    (at {x} {y} 0)
    (unit 1)
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (dnp no)
    (uuid "{gen_uuid()}")
    (property "Reference" "{ref}"
      (at {x} {y - 10} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{comp['value']}"
      (at {x} {y - 12.54} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "{comp['footprint']}"
      (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" ""
      (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
'''

    # Add pin connections
    for pin_num in comp['pins']:
        sym += f'''    (pin "{pin_num}"
      (uuid "{gen_uuid()}")
    )
'''

    sym += '''  )
'''
    return sym

def generate_global_label(net_name, x, y, angle=0):
    """Generate a global label."""
    if net_name in ['+3V', 'VCC', '+3V3']:
        shape = 'input'
    elif net_name in ['GND', 'VSS']:
        shape = 'input'
    else:
        shape = 'bidirectional'

    return f'''  (global_label "{net_name}"
    (shape {shape})
    (at {x} {y} {angle})
    (effects (font (size 1.27 1.27)))
    (uuid "{gen_uuid()}")
    (property "Intersheetrefs" "${{INTERSHEET_REFS}}"
      (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )
'''

def generate_no_connect(x, y):
    """Generate a no-connect flag."""
    return f'''  (no_connect
    (at {x} {y})
    (uuid "{gen_uuid()}")
  )
'''

def main():
    print("Creating KiCad schematic with embedded symbols...")

    # Build lib_symbols section
    lib_symbols = ['  (lib_symbols']

    # Add power symbols
    lib_symbols.append(create_power_symbol('singingcard:+3V', is_gnd=False))
    lib_symbols.append(create_power_symbol('singingcard:GND', is_gnd=True))

    # Add component symbols
    unique_symbols = {}
    for ref, comp in COMPONENTS.items():
        name = comp['name']
        if name not in unique_symbols:
            if name in ['R', 'C']:
                unique_symbols[name] = create_simple_symbol(f"singingcard:{name}", name[0])
            elif name in ['Conn_01x02', 'SW_Push']:
                unique_symbols[name] = create_simple_symbol(f"singingcard:{name}", ref[0])
            else:
                unique_symbols[name] = create_lib_symbol(f"singingcard:{name}", comp['pins'])

    for sym in unique_symbols.values():
        lib_symbols.append(sym)

    lib_symbols.append('  )')

    # Build schematic
    sch = f'''(kicad_sch
  (version 20231120)
  (generator "create_schematic_v3.py")
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

'''

    # Add lib_symbols
    sch += '\n'.join(lib_symbols) + '\n\n'

    # Add symbol instances
    for ref, comp in COMPONENTS.items():
        lib_name = f"singingcard:{comp['name']}"
        sch += generate_symbol_instance(ref, comp, lib_name)

    # Add global labels for each net connection
    # Track pin positions for label placement
    label_count = 0
    for net_name, connections in NETS.items():
        for ref, pin in connections:
            if ref in COMPONENTS:
                comp = COMPONENTS[ref]
                x, y = comp['position']
                # Offset for label placement
                label_x = x + 20 + (label_count % 3) * 5
                label_y = y + (label_count // 3) * 3
                sch += generate_global_label(net_name, label_x, label_y)
                label_count += 1

    # Add no-connects for NC pins on U1
    if 'U1' in COMPONENTS:
        comp = COMPONENTS['U1']
        x, y = comp['position']
        for pin in comp.get('nc_pins', []):
            nc_x = x + 25
            nc_y = y + int(pin) * 0.5
            sch += generate_no_connect(nc_x, nc_y)

    sch += ')\n'

    # Write schematic
    with open('singingcard.kicad_sch', 'w') as f:
        f.write(sch)

    print(f"Created singingcard.kicad_sch")
    print(f"  - {len(COMPONENTS)} component instances")
    print(f"  - {len(NETS)} nets with global labels")
    print(f"  - No-connect flags for NC pins")

if __name__ == '__main__':
    main()
