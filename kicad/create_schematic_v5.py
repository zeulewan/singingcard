#!/usr/bin/env python3
"""
Create KiCad 9 schematic with proper pin connectivity.
Places global labels directly at pin endpoints.
"""

import uuid

def gen_uuid():
    return str(uuid.uuid4())

# Symbol pin offsets from symbol center
# Format: {symbol_name: {pin_num: (dx, dy, angle)}}
# For ICs: left pins point right (angle=0), right pins point left (angle=180)
# For 2-pin: pin 1 up (270), pin 2 down (90)

def get_ic_pin_positions(num_pins):
    """Get pin positions for IC with given number of pins."""
    half = num_pins // 2
    height = max(10.16, (half + 1) * 2.54)
    width = 15.24
    positions = {}

    # Left side pins (1 to half)
    for i in range(half):
        pin_num = i + 1
        y = height/2 - 2.54 - i * 2.54
        x = -width/2 - 5.08
        positions[str(pin_num)] = (x, y, 0)

    # Right side pins (half+1 to num_pins) - numbered in reverse
    for i in range(half):
        pin_num = num_pins - i
        y = height/2 - 2.54 - i * 2.54
        x = width/2 + 5.08
        positions[str(pin_num)] = (x, y, 180)

    return positions

def get_2pin_positions():
    """Get pin positions for 2-pin symbol."""
    return {
        '1': (0, 5.08, 270),
        '2': (0, -5.08, 90),
    }

# Component definitions
COMPONENTS = {
    'U1': {
        'name': 'ISD3900FYI',
        'value': 'ISD3900FYI',
        'footprint': 'singingcard:LQFP-48_L7.0-W7.0-P0.50-LS9.0-BL',
        'description': 'Audio record/playback IC',
        'num_pins': 48,
        'position': (119.38, 99.06),  # Grid aligned
    },
    'U2': {
        'name': 'W25Q16JVSSIQ',
        'value': 'W25Q16JVSSIQ',
        'footprint': 'singingcard:SOIC-8_L5.3-W5.3-P1.27-LS8.0-BL',
        'description': 'SPI Flash memory',
        'num_pins': 8,
        'position': (220.98, 81.28),  # Grid aligned
    },
    'BT1': {
        'name': 'CR2032',
        'value': 'CR2032',
        'footprint': 'singingcard:BAT-TH_CR2032-BS-6-1',
        'description': 'CR2032 battery holder',
        'num_pins': 2,
        'position': (279.4, 99.06),  # Grid aligned
    },
    'R1': {
        'name': 'LDR',
        'value': 'GL5528',
        'footprint': 'singingcard:RES-TH_L5.1-W4.3-P3.40-D0.5',
        'description': 'Light dependent resistor',
        'num_pins': 2,
        'position': (40.64, 50.8),  # Grid aligned
    },
    'R2': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'description': 'Resistor',
        'num_pins': 2,
        'position': (60.96, 50.8),  # Grid aligned
    },
    'R3': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'description': 'Resistor',
        'num_pins': 2,
        'position': (81.28, 50.8),  # Grid aligned
    },
    'R4': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'description': 'Resistor',
        'num_pins': 2,
        'position': (101.6, 50.8),  # Grid aligned
    },
    'C1': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'description': 'Capacitor',
        'num_pins': 2,
        'position': (40.64, 139.7),
    },
    'C2': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'description': 'Capacitor',
        'num_pins': 2,
        'position': (55.88, 139.7),
    },
    'C3': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'description': 'Capacitor',
        'num_pins': 2,
        'position': (71.12, 139.7),
    },
    'C4': {
        'name': 'C',
        'value': '10uF',
        'footprint': 'Capacitor_SMD:C_0805_2012Metric',
        'description': 'Capacitor',
        'num_pins': 2,
        'position': (86.36, 139.7),
    },
    'C5': {
        'name': 'C',
        'value': '10uF',
        'footprint': 'Capacitor_SMD:C_0805_2012Metric',
        'description': 'Capacitor',
        'num_pins': 2,
        'position': (101.6, 139.7),
    },
    'C6': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'description': 'Capacitor',
        'num_pins': 2,
        'position': (251.46, 81.28),
    },
    'LS1': {
        'name': 'Speaker',
        'value': 'KLJ-01304T-08R07W',
        'footprint': 'speaker:BUZ-SMD_4P-L13.0-W13.0-P11.4-BL',
        'description': 'SMD Speaker 8ohm 700mW',
        'num_pins': 2,
        'position': (180.34, 50.8),
    },
    'J2': {
        'name': 'Conn_01x02',
        'value': 'Audio_In',
        'footprint': 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
        'description': 'Audio input connector',
        'num_pins': 2,
        'position': (60.96, 99.06),
    },
    'SW1': {
        'name': 'SW_Push',
        'value': 'Button',
        'footprint': 'Button_Switch_SMD:SW_SPST_TL3342',
        'description': 'Push button switch',
        'num_pins': 2,
        'position': (40.64, 76.2),
    },
}

# Net connections (ref, pin) pairs
NETS = {
    '+3V': [('BT1', '1'), ('U1', '10'), ('U1', '11'), ('U1', '20'), ('U2', '8'),
            ('C1', '1'), ('C2', '1'), ('C3', '1'), ('C4', '1'), ('C5', '1'), ('C6', '1'),
            ('R2', '1'), ('R3', '1'), ('R4', '1'), ('U2', '3'), ('U2', '7')],
    'GND': [('BT1', '2'), ('U1', '16'), ('U2', '4'),
            ('C1', '2'), ('C2', '2'), ('C3', '2'), ('C4', '2'), ('C5', '2'), ('C6', '2'),
            ('R1', '2'), ('SW1', '2')],
    'GPIO0': [('U1', '21'), ('R1', '1'), ('R2', '2')],
    'GPIO1': [('U1', '27'), ('SW1', '1')],
    'GPIO2': [('U1', '31'), ('R3', '2')],
    'RESET': [('U1', '12'), ('R4', '2')],
    'SPI_CS': [('U1', '38'), ('U2', '1')],
    'SPI_MOSI': [('U1', '43'), ('U2', '5')],
    'SPI_MISO': [('U1', '44'), ('U2', '2')],
    'SPI_CLK': [('U1', '32'), ('U2', '6')],
    'SP+': [('U1', '17'), ('LS1', '1')],
    'SP-': [('U1', '18'), ('LS1', '2')],
    'ANA_IN+': [('U1', '14'), ('J2', '1')],
    'ANA_IN-': [('U1', '15'), ('J2', '2')],
}

# NC pins for U1 (not connected to any net)
NC_PINS_U1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '13', '19', '22', '23', '24', '25', '26',
              '28', '29', '30', '33', '34', '35', '36', '37', '39', '40', '41', '42', '45', '46', '47', '48']

def get_pin_world_position(ref, pin_num):
    """Get world position of a pin."""
    comp = COMPONENTS[ref]
    cx, cy = comp['position']

    if comp['num_pins'] == 2:
        pin_offsets = get_2pin_positions()
    else:
        pin_offsets = get_ic_pin_positions(comp['num_pins'])

    if pin_num in pin_offsets:
        dx, dy, angle = pin_offsets[pin_num]
        return (cx + dx, cy + dy, angle)
    return None

def create_lib_symbols():
    """Create embedded symbol definitions."""
    symbols = []

    # Create IC symbols
    symbols.append(create_ic_symbol('singingcard:ISD3900FYI', 48, 'U'))
    symbols.append(create_ic_symbol('singingcard:W25Q16JVSSIQ', 8, 'U'))

    # Create 2-pin symbols
    for name in ['CR2032', 'LDR', 'R', 'C', 'Conn_01x02', 'SW_Push', 'Speaker']:
        ref = 'BT' if name == 'CR2032' else ('R' if name in ['LDR', 'R'] else ('C' if name == 'C' else ('J' if name == 'Conn_01x02' else ('LS' if name == 'Speaker' else 'SW'))))
        symbols.append(create_2pin_symbol(f'singingcard:{name}', ref))

    return '\n'.join(symbols)

def create_ic_symbol(name, num_pins, ref_prefix):
    """Create IC symbol with pins."""
    half = num_pins // 2
    height = max(10.16, (half + 1) * 2.54)
    width = 15.24

    sym = f'''		(symbol "{name}"
			(pin_names
				(offset 1.016)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "{ref_prefix}"
				(at 0 {height/2 + 2.54:.2f} 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "{name.split(':')[1]}"
				(at 0 {-height/2 - 2.54:.2f} 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "{name.split(':')[1]}_1_1"
				(rectangle
					(start {-width/2:.2f} {height/2:.2f})
					(end {width/2:.2f} {-height/2:.2f})
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
'''

    # Add pins
    for i in range(half):
        pin_num = i + 1
        y = height/2 - 2.54 - i * 2.54
        x = -width/2 - 5.08
        sym += f'''				(pin passive line
					(at {x:.2f} {y:.2f} 0)
					(length 5.08)
					(name "{pin_num}"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "{pin_num}"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
'''

    for i in range(half):
        pin_num = num_pins - i
        y = height/2 - 2.54 - i * 2.54
        x = width/2 + 5.08
        sym += f'''				(pin passive line
					(at {x:.2f} {y:.2f} 180)
					(length 5.08)
					(name "{pin_num}"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "{pin_num}"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
'''

    sym += '''			)
		)'''
    return sym

def create_2pin_symbol(name, ref_prefix):
    """Create 2-pin symbol."""
    sym = f'''		(symbol "{name}"
			(pin_names
				(offset 1.016)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "{ref_prefix}"
				(at 2.54 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "{name.split(':')[1]}"
				(at 2.54 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "{name.split(':')[1]}_1_1"
				(rectangle
					(start -1.27 2.54)
					(end 1.27 -2.54)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(pin passive line
					(at 0 5.08 270)
					(length 2.54)
					(name "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -5.08 90)
					(length 2.54)
					(name "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
		)'''
    return sym

def create_symbol_instance(ref, comp, project_uuid):
    """Generate symbol instance."""
    x, y = comp['position']
    lib_name = f"singingcard:{comp['name']}"
    comp_uuid = gen_uuid()

    # Get list of pins
    if comp['num_pins'] == 2:
        pins = ['1', '2']
    else:
        pins = [str(i) for i in range(1, comp['num_pins'] + 1)]

    sym = f'''	(symbol
		(lib_id "{lib_name}")
		(at {x} {y} 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{comp_uuid}")
		(property "Reference" "{ref}"
			(at {x} {y - 12} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "{comp['value']}"
			(at {x} {y - 15} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "{comp['footprint']}"
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Datasheet" ""
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Description" "{comp['description']}"
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
'''
    for pin in pins:
        sym += f'''		(pin "{pin}"
			(uuid "{gen_uuid()}")
		)
'''

    sym += f'''		(instances
			(project "singingcard"
				(path "/{project_uuid}"
					(reference "{ref}")
					(unit 1)
				)
			)
		)
	)
'''
    return sym

def create_global_label(net_name, x, y, angle=0):
    """Generate global label at exact position."""
    # Convert angle to proper orientation
    # angle from pin indicates direction pin points, we want opposite
    label_angle = (angle + 180) % 360
    return f'''	(global_label "{net_name}"
		(shape bidirectional)
		(at {x:.2f} {y:.2f} {label_angle})
		(effects
			(font
				(size 1.27 1.27)
			)
		)
		(uuid "{gen_uuid()}")
		(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
			(at {x:.2f} {y:.2f} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
	)
'''

def create_no_connect(x, y):
    """Generate no-connect flag at exact position."""
    return f'''	(no_connect
		(at {x:.2f} {y:.2f})
		(uuid "{gen_uuid()}")
	)
'''

def main():
    print("Creating KiCad 9 schematic with proper connectivity...")

    project_uuid = gen_uuid()

    # Header
    sch = f'''(kicad_sch
	(version 20250114)
	(generator "create_schematic_v5.py")
	(generator_version "9.0")
	(uuid "{project_uuid}")
	(paper "A4")
	(title_block
		(title "Singing Birthday Card Module")
		(date "2025-12-30")
		(rev "1.0")
		(comment 1 "ISD3900FYI Audio Playback")
		(comment 2 "CR2032 Powered, SPI Flash Storage")
	)
	(lib_symbols
{create_lib_symbols()}
	)

'''

    # Add symbol instances
    for ref, comp in COMPONENTS.items():
        sch += create_symbol_instance(ref, comp, project_uuid)

    # Add global labels at pin locations
    labels_added = 0
    for net_name, connections in NETS.items():
        for ref, pin in connections:
            if ref in COMPONENTS:
                pos = get_pin_world_position(ref, pin)
                if pos:
                    x, y, angle = pos
                    sch += create_global_label(net_name, x, y, angle)
                    labels_added += 1

    # Add no-connects at NC pin locations
    nc_added = 0
    for pin in NC_PINS_U1:
        pos = get_pin_world_position('U1', pin)
        if pos:
            x, y, angle = pos
            sch += create_no_connect(x, y)
            nc_added += 1

    sch += ')\n'

    with open('singingcard.kicad_sch', 'w') as f:
        f.write(sch)

    print(f"Created singingcard.kicad_sch")
    print(f"  - {len(COMPONENTS)} components")
    print(f"  - {labels_added} global labels")
    print(f"  - {nc_added} no-connect flags")

if __name__ == '__main__':
    main()
