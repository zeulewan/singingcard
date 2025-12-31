#!/usr/bin/env python3
"""
Create KiCad 9 schematic with proper format and connectivity.
Uses global labels for all net connections.
"""

import uuid

def gen_uuid():
    return str(uuid.uuid4())

# Component definitions
COMPONENTS = {
    'U1': {
        'name': 'ISD3900FYI',
        'value': 'ISD3900FYI',
        'footprint': 'singingcard:LQFP-48_7x7mm_P0.5mm',
        'description': 'Audio record/playback IC',
        'pins': ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',
                 '21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38',
                 '39','40','41','42','43','44','45','46','47','48'],
        'position': (120, 100),
    },
    'U2': {
        'name': 'W25Q16JVSSIQ',
        'value': 'W25Q16JVSSIQ',
        'footprint': 'singingcard:SOIC-8_5.23x5.23mm_P1.27mm',
        'description': 'SPI Flash memory',
        'pins': ['1','2','3','4','5','6','7','8'],
        'position': (220, 80),
    },
    'BT1': {
        'name': 'CR2032',
        'value': 'CR2032',
        'footprint': 'singingcard:BAT-TH_CR2032-BS-6-1',
        'description': 'CR2032 battery holder',
        'pins': ['1','2'],
        'position': (280, 100),
    },
    'R1': {
        'name': 'LDR',
        'value': 'GL5528',
        'footprint': 'singingcard:LDR_GL5528',
        'description': 'Light dependent resistor',
        'pins': ['1','2'],
        'position': (40, 50),
    },
    'R2': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'description': 'Resistor',
        'pins': ['1','2'],
        'position': (40, 70),
    },
    'R3': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'description': 'Resistor',
        'pins': ['1','2'],
        'position': (40, 90),
    },
    'R4': {
        'name': 'R',
        'value': '10k',
        'footprint': 'Resistor_SMD:R_0603_1608Metric',
        'description': 'Resistor',
        'pins': ['1','2'],
        'position': (40, 110),
    },
    'C1': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'description': 'Capacitor',
        'pins': ['1','2'],
        'position': (180, 130),
    },
    'C2': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'description': 'Capacitor',
        'pins': ['1','2'],
        'position': (195, 130),
    },
    'C3': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'description': 'Capacitor',
        'pins': ['1','2'],
        'position': (210, 130),
    },
    'C4': {
        'name': 'C',
        'value': '10uF',
        'footprint': 'Capacitor_SMD:C_0805_2012Metric',
        'description': 'Capacitor',
        'pins': ['1','2'],
        'position': (225, 130),
    },
    'C5': {
        'name': 'C',
        'value': '10uF',
        'footprint': 'Capacitor_SMD:C_0805_2012Metric',
        'description': 'Capacitor',
        'pins': ['1','2'],
        'position': (240, 130),
    },
    'C6': {
        'name': 'C',
        'value': '100nF',
        'footprint': 'Capacitor_SMD:C_0603_1608Metric',
        'description': 'Capacitor',
        'pins': ['1','2'],
        'position': (255, 80),
    },
    'J1': {
        'name': 'Conn_01x02',
        'value': 'Speaker',
        'footprint': 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
        'description': 'Speaker connector',
        'pins': ['1','2'],
        'position': (180, 60),
    },
    'J2': {
        'name': 'Conn_01x02',
        'value': 'Audio_In',
        'footprint': 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
        'description': 'Audio input connector',
        'pins': ['1','2'],
        'position': (60, 100),
    },
    'SW1': {
        'name': 'SW_Push',
        'value': 'Button',
        'footprint': 'singingcard:SW_SPST_Omron_B3S-1000',
        'description': 'Push button switch',
        'pins': ['1','2'],
        'position': (40, 130),
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
    'SP+': [('U1', '17'), ('J1', '1')],
    'SP-': [('U1', '18'), ('J1', '2')],
    'ANA_IN+': [('U1', '14'), ('J2', '1')],
    'ANA_IN-': [('U1', '15'), ('J2', '2')],
}

# NC pins for U1
NC_PINS_U1 = ['1', '3', '4', '5', '6', '7', '8', '9', '19', '22', '23', '24', '25', '26',
              '28', '29', '30', '33', '34', '35', '36', '37', '39', '40', '41', '42', '45', '46', '47', '48']

def create_lib_symbols():
    """Create embedded symbol definitions."""
    symbols = []

    # Create generic 48-pin IC symbol for ISD3900
    symbols.append(create_ic_symbol('singingcard:ISD3900FYI', 48, 'U'))

    # Create generic 8-pin IC symbol for flash
    symbols.append(create_ic_symbol('singingcard:W25Q16JVSSIQ', 8, 'U'))

    # Create 2-pin symbols
    symbols.append(create_2pin_symbol('singingcard:CR2032', 'BT'))
    symbols.append(create_2pin_symbol('singingcard:LDR', 'R'))
    symbols.append(create_2pin_symbol('singingcard:R', 'R'))
    symbols.append(create_2pin_symbol('singingcard:C', 'C'))
    symbols.append(create_2pin_symbol('singingcard:Conn_01x02', 'J'))
    symbols.append(create_2pin_symbol('singingcard:SW_Push', 'SW'))

    return '\n'.join(symbols)

def create_ic_symbol(name, num_pins, ref_prefix):
    """Create IC symbol with given number of pins."""
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
    # Add left side pins (1 to half)
    for i in range(half):
        pin_num = i + 1
        y = height/2 - 2.54 - i * 2.54
        sym += f'''				(pin passive line
					(at {-width/2 - 5.08:.2f} {y:.2f} 0)
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

    # Add right side pins (half+1 to num_pins)
    for i in range(half):
        pin_num = num_pins - i
        y = height/2 - 2.54 - i * 2.54
        sym += f'''				(pin passive line
					(at {width/2 + 5.08:.2f} {y:.2f} 180)
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
			(at {x} {y - 10} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "{comp['value']}"
			(at {x} {y - 12.54} 0)
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
    # Add pin UUIDs
    for pin in comp['pins']:
        sym += f'''		(pin "{pin}"
			(uuid "{gen_uuid()}")
		)
'''

    # Add instances section
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
    """Generate global label."""
    return f'''	(global_label "{net_name}"
		(shape bidirectional)
		(at {x} {y} {angle})
		(effects
			(font
				(size 1.27 1.27)
			)
		)
		(uuid "{gen_uuid()}")
		(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
			(at {x} {y} 0)
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
    """Generate no-connect flag."""
    return f'''	(no_connect
		(at {x} {y})
		(uuid "{gen_uuid()}")
	)
'''

def main():
    print("Creating KiCad 9 schematic...")

    project_uuid = gen_uuid()

    # Header
    sch = f'''(kicad_sch
	(version 20250114)
	(generator "create_schematic_v4.py")
	(generator_version "9.0")
	(uuid "{project_uuid}")
	(paper "A3")
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

    # Add global labels for connectivity
    label_y = 160
    for net_name in NETS:
        sch += create_global_label(net_name, 40, label_y)
        label_y += 5

    # Add no-connects for NC pins
    nc_x = 300
    nc_y = 50
    for pin in NC_PINS_U1:
        sch += create_no_connect(nc_x, nc_y)
        nc_y += 3

    sch += ')\n'

    with open('singingcard.kicad_sch', 'w') as f:
        f.write(sch)

    print(f"Created singingcard.kicad_sch")
    print(f"  - {len(COMPONENTS)} components")
    print(f"  - {len(NETS)} nets")
    print(f"  - {len(NC_PINS_U1)} no-connect flags")

if __name__ == '__main__':
    main()
