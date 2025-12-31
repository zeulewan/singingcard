#!/usr/bin/env python3
"""
Create KiCad schematic file with all components for the singing birthday card.
Uses KiCad 8/9 schematic format with embedded symbol definitions.
"""

import uuid
import os
import re

def gen_uuid():
    return str(uuid.uuid4())

# Read the local symbol library
def read_local_symbols():
    """Read symbols from the local singingcard.kicad_sym library."""
    lib_path = 'libs/singingcard.kicad_sym'
    if not os.path.exists(lib_path):
        return {}

    with open(lib_path, 'r') as f:
        content = f.read()

    symbols = {}
    # Parse each symbol from the library
    depth = 0
    in_symbol = False
    symbol_content = []
    symbol_name = None

    for line in content.split('\n'):
        stripped = line.strip()

        if stripped.startswith('(symbol "') and depth == 1:
            # Start of a symbol definition
            match = re.match(r'\(symbol "([^"]+)"', stripped)
            if match:
                symbol_name = match.group(1)
                symbol_content = [line]
                in_symbol = True
        elif in_symbol:
            symbol_content.append(line)

        depth += line.count('(') - line.count(')')

        if in_symbol and depth == 1:
            # End of symbol
            symbols[symbol_name] = '\n'.join(symbol_content)
            in_symbol = False
            symbol_name = None
            symbol_content = []

    return symbols

# Standard KiCad symbols (embedded definitions)
STANDARD_SYMBOLS = {
    'Device:C': '''    (symbol "Device:C"
      (pin_numbers hide)
      (pin_names
        (offset 0.254) hide)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "C"
        (at 0.635 2.54 0)
        (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "C"
        (at 0.635 -2.54 0)
        (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" ""
        (at 0.9652 -3.81 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Description" "Unpolarized capacitor"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "ki_keywords" "cap capacitor"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "ki_fp_filters" "C_*"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "C_0_1"
        (polyline
          (pts (xy -2.032 -0.762) (xy 2.032 -0.762))
          (stroke (width 0.508) (type default))
          (fill (type none)))
        (polyline
          (pts (xy -2.032 0.762) (xy 2.032 0.762))
          (stroke (width 0.508) (type default))
          (fill (type none))))
      (symbol "C_1_1"
        (pin passive line
          (at 0 3.81 270)
          (length 2.794)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line
          (at 0 -3.81 90)
          (length 2.794)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))))''',

    'Device:R': '''    (symbol "Device:R"
      (pin_numbers hide)
      (pin_names
        (offset 0) hide)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "R"
        (at 2.032 0 90)
        (effects (font (size 1.27 1.27))))
      (property "Value" "R"
        (at 0 0 90)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" ""
        (at -1.778 0 90)
        (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Description" "Resistor"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "ki_keywords" "R res resistor"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "ki_fp_filters" "R_*"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "R_0_1"
        (rectangle
          (start -1.016 -2.54)
          (end 1.016 2.54)
          (stroke (width 0.254) (type default))
          (fill (type none))))
      (symbol "R_1_1"
        (pin passive line
          (at 0 3.81 270)
          (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line
          (at 0 -3.81 90)
          (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))))''',

    'Switch:SW_Push': '''    (symbol "Switch:SW_Push"
      (pin_numbers hide)
      (pin_names
        (offset 1.016) hide)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "SW"
        (at 1.27 6.35 0)
        (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "SW_Push"
        (at 0 -1.524 0)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" ""
        (at 0 5.08 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~"
        (at 0 5.08 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Description" "Push button switch, generic, two pins"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "ki_keywords" "switch normally-open pushbutton push-button"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "SW_Push_0_1"
        (circle
          (center -2.032 0)
          (radius 0.508)
          (stroke (width 0) (type default))
          (fill (type none)))
        (polyline
          (pts (xy 0 1.27) (xy 0 3.048))
          (stroke (width 0) (type default))
          (fill (type none)))
        (polyline
          (pts (xy 2.54 1.27) (xy -2.54 1.27))
          (stroke (width 0) (type default))
          (fill (type none)))
        (circle
          (center 2.032 0)
          (radius 0.508)
          (stroke (width 0) (type default))
          (fill (type none)))
        (pin passive line
          (at -5.08 0 0)
          (length 2.54)
          (name "1" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line
          (at 5.08 0 180)
          (length 2.54)
          (name "2" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))))''',

    'Connector:Conn_01x02_Pin': '''    (symbol "Connector:Conn_01x02_Pin"
      (pin_names
        (offset 1.016) hide)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "J"
        (at 0 2.54 0)
        (effects (font (size 1.27 1.27))))
      (property "Value" "Conn_01x02_Pin"
        (at 0 -5.08 0)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Description" "Generic connector, single row, 01x02"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "ki_keywords" "connector"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "Conn_01x02_Pin_1_1"
        (polyline
          (pts (xy 1.27 -2.54) (xy 0.8636 -2.54))
          (stroke (width 0.1524) (type default))
          (fill (type none)))
        (polyline
          (pts (xy 1.27 0) (xy 0.8636 0))
          (stroke (width 0.1524) (type default))
          (fill (type none)))
        (rectangle
          (start 0.8636 -2.413)
          (end 0 -2.667)
          (stroke (width 0.1524) (type default))
          (fill (type outline)))
        (rectangle
          (start 0.8636 0.127)
          (end 0 -0.127)
          (stroke (width 0.1524) (type default))
          (fill (type outline)))
        (pin passive line
          (at 5.08 0 180)
          (length 3.81)
          (name "Pin_1" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line
          (at 5.08 -2.54 180)
          (length 3.81)
          (name "Pin_2" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))))''',

    'power:+3V3': '''    (symbol "power:+3V3"
      (power)
      (pin_names
        (offset 0))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "#PWR"
        (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+3V3"
        (at 0 3.556 0)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Description" "Power symbol creates a global label with name +3V3"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "ki_keywords" "global power"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "+3V3_0_1"
        (polyline
          (pts (xy -0.762 1.27) (xy 0 2.54))
          (stroke (width 0) (type default))
          (fill (type none)))
        (polyline
          (pts (xy 0 0) (xy 0 2.54))
          (stroke (width 0) (type default))
          (fill (type none)))
        (polyline
          (pts (xy 0 2.54) (xy 0.762 1.27))
          (stroke (width 0) (type default))
          (fill (type none))))
      (symbol "+3V3_1_1"
        (pin power_in line
          (at 0 0 90)
          (length 0)
          (name "+3V3" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))))''',

    'power:GND': '''    (symbol "power:GND"
      (power)
      (pin_names
        (offset 0))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "#PWR"
        (at 0 -6.35 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Value" "GND"
        (at 0 -3.81 0)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Description" "Power symbol creates a global label with name GND"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "ki_keywords" "global power"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "GND_0_1"
        (polyline
          (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
          (stroke (width 0) (type default))
          (fill (type none))))
      (symbol "GND_1_1"
        (pin power_in line
          (at 0 0 270)
          (length 0)
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))))''',
}

# Component definitions with schematic positions
COMPONENTS = {
    'U1': {
        'lib': 'singingcard',
        'symbol': 'ISD3900FYI',
        'value': 'ISD3900FYI',
        'footprint': 'singingcard:LQFP-48_L7.0-W7.0-P0.50-LS9.0-BL',
        'x': 140, 'y': 100,
    },
    'U2': {
        'lib': 'singingcard',
        'symbol': 'W25Q16JVSSIQTR',
        'value': 'W25Q16JVSSIQ',
        'footprint': 'singingcard:SOIC-8_L5.3-W5.3-P1.27-LS8.0-BL',
        'x': 230, 'y': 80,
    },
    'BT1': {
        'lib': 'singingcard',
        'symbol': 'CR2032-BS-6-1',
        'value': 'CR2032',
        'footprint': 'singingcard:BAT-TH_CR2032-BS-6-1',
        'x': 280, 'y': 100,
    },
    'C1': {
        'lib': 'Device',
        'symbol': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'x': 80, 'y': 60,
    },
    'C2': {
        'lib': 'Device',
        'symbol': 'C',
        'value': '10uF',
        'footprint': 'Capacitor_SMD:C_0805_2012Metric',
        'x': 80, 'y': 80,
    },
    'C3': {
        'lib': 'Device',
        'symbol': 'C',
        'value': '1uF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'x': 80, 'y': 100,
    },
    'C4': {
        'lib': 'Device',
        'symbol': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'x': 80, 'y': 120,
    },
    'C5': {
        'lib': 'Device',
        'symbol': 'C',
        'value': '10uF',
        'footprint': 'Capacitor_SMD:C_0805_2012Metric',
        'x': 80, 'y': 140,
    },
    'C6': {
        'lib': 'Device',
        'symbol': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'x': 250, 'y': 60,
    },
    'R1': {
        'lib': 'singingcard',
        'symbol': 'GL5528(10-20)',
        'value': 'GL5528',
        'footprint': 'singingcard:RES-TH_L5.1-W4.3-P3.40-D0.5',
        'x': 50, 'y': 160,
    },
    'R2': {
        'lib': 'Device',
        'symbol': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'x': 50, 'y': 140,
    },
    'R3': {
        'lib': 'Device',
        'symbol': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'x': 200, 'y': 50,
    },
    'R4': {
        'lib': 'Device',
        'symbol': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'x': 200, 'y': 70,
    },
    'J1': {
        'lib': 'Connector',
        'symbol': 'Conn_01x02_Pin',
        'value': 'Speaker',
        'footprint': 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
        'x': 50, 'y': 80,
    },
    'J2': {
        'lib': 'Connector',
        'symbol': 'Conn_01x02_Pin',
        'value': 'Pull-Tab',
        'footprint': 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
        'x': 50, 'y': 100,
    },
    'SW1': {
        'lib': 'Switch',
        'symbol': 'SW_Push',
        'value': 'Button',
        'footprint': 'Button_Switch_SMD:SW_SPST_TL3342',
        'x': 200, 'y': 140,
    },
}

def get_lib_id(comp):
    """Get the library ID for a component."""
    return f"{comp['lib']}:{comp['symbol']}"

def generate_lib_symbols(local_symbols):
    """Generate the lib_symbols section."""
    result = ['  (lib_symbols']

    # Add standard symbols
    for lib_id, symbol_def in STANDARD_SYMBOLS.items():
        result.append(symbol_def)

    # Add local symbols with proper prefixes
    for symbol_name, symbol_def in local_symbols.items():
        # Convert local symbol to embedded format
        # Change 'symbol "X"' to 'symbol "singingcard:X"'
        modified = symbol_def.replace(f'(symbol "{symbol_name}"', f'    (symbol "singingcard:{symbol_name}"')
        # Ensure proper indentation
        lines = modified.split('\n')
        indented = []
        for line in lines:
            if line.strip():
                # Add proper indentation
                if not line.startswith('    '):
                    indented.append('    ' + line)
                else:
                    indented.append(line)
        result.append('\n'.join(indented))

    result.append('  )')
    return '\n'.join(result)

def generate_symbol_instance(ref, comp, uuid_str):
    """Generate a symbol instance for the schematic."""
    x, y = comp['x'], comp['y']
    lib_id = get_lib_id(comp)
    value = comp['value']
    footprint = comp['footprint']

    return f'''  (symbol
    (lib_id "{lib_id}")
    (at {x} {y} 0)
    (unit 1)
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (dnp no)
    (uuid "{uuid_str}")
    (property "Reference" "{ref}"
      (at {x} {y - 8} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{value}"
      (at {x} {y + 8} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "{footprint}"
      (at {x} {y + 10} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" ""
      (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )'''

def generate_power_symbol(ref, symbol_type, x, y, uuid_str):
    """Generate a power symbol instance."""
    if symbol_type == '+3V3':
        lib_id = 'power:+3V3'
        value = '+3V3'
    else:
        lib_id = 'power:GND'
        value = 'GND'

    return f'''  (symbol
    (lib_id "{lib_id}")
    (at {x} {y} 0)
    (unit 1)
    (exclude_from_sim no)
    (in_bom no)
    (on_board yes)
    (dnp no)
    (uuid "{uuid_str}")
    (property "Reference" "{ref}"
      (at {x} {y + 3} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "{value}"
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

def generate_schematic():
    """Generate the complete KiCad schematic."""
    local_symbols = read_local_symbols()

    sch = []

    # Header
    sch.append(f'''(kicad_sch
  (version 20231120)
  (generator "create_schematic.py")
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

    # Add lib_symbols section
    sch.append(generate_lib_symbols(local_symbols))
    sch.append('')

    # Track power symbol references
    pwr_num = 1

    # Add power symbols for the schematic
    power_symbols = [
        ('#PWR01', '+3V3', 280, 70),
        ('#PWR02', 'GND', 280, 130),
    ]

    for ref, sym_type, x, y in power_symbols:
        sch.append(generate_power_symbol(ref, sym_type, x, y, gen_uuid()))
        sch.append('')

    # Add component symbols
    for ref, comp in COMPONENTS.items():
        sch.append(generate_symbol_instance(ref, comp, gen_uuid()))
        sch.append('')

    # Add a text note
    sch.append(f'''  (text "SINGING BIRTHDAY CARD MODULE\\n\\nU1: ISD3900FYI Audio IC\\nU2: W25Q16 SPI Flash\\nBT1: CR2032 Battery\\n\\nNets are connected via net labels"
    (exclude_from_sim no)
    (at 25 30 0)
    (effects (font (size 1.5 1.5)) (justify left top))
    (uuid "{gen_uuid()}")
  )''')

    sch.append('')
    sch.append(')')

    return '\n'.join(sch)

def main():
    schematic = generate_schematic()

    with open('singingcard.kicad_sch', 'w') as f:
        f.write(schematic)

    print("Generated: singingcard.kicad_sch")
    print(f"Components: {len(COMPONENTS)}")

if __name__ == '__main__':
    main()
