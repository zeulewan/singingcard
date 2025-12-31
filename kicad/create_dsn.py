#!/usr/bin/env python3
"""
Generate DSN file for FreeRouting from KiCad netlist and PCB.
"""

import os
import re
import sys

# Board dimensions (mm) - same as create_pcb.py
BOARD_WIDTH = 85.0
BOARD_HEIGHT = 55.0
BOARD_ORIGIN_X = 100.0
BOARD_ORIGIN_Y = 100.0

# Convert mm to um (DSN uses micrometers)
def mm_to_um(mm):
    return int(mm * 1000)

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

def get_component_positions():
    """Component positions from create_pcb.py (converted to um)"""
    cx = BOARD_ORIGIN_X + 38
    cy = BOARD_ORIGIN_Y + BOARD_HEIGHT/2

    positions = {
        'U1': (mm_to_um(cx), mm_to_um(cy), 0),
        'U2': (mm_to_um(cx + 22), mm_to_um(cy - 18), 0),
        'BT1': (mm_to_um(BOARD_ORIGIN_X + BOARD_WIDTH - 15), mm_to_um(cy), 0),
        'C1': (mm_to_um(cx - 12), mm_to_um(cy - 6), 0),
        'C2': (mm_to_um(cx - 12), mm_to_um(cy + 6), 0),
        'C3': (mm_to_um(cx + 12), mm_to_um(cy - 6), 0),
        'C4': (mm_to_um(cx - 6), mm_to_um(cy - 12), 0),
        'C5': (mm_to_um(cx + 12), mm_to_um(cy + 6), 0),
        'C6': (mm_to_um(cx + 22), mm_to_um(cy - 10), 0),
        'R1': (mm_to_um(BOARD_ORIGIN_X + 12), mm_to_um(cy - 8), 0),
        'R2': (mm_to_um(BOARD_ORIGIN_X + 12), mm_to_um(cy - 18), 0),
        'R3': (mm_to_um(cx - 6), mm_to_um(cy - 18), 0),
        'R4': (mm_to_um(cx - 6), mm_to_um(cy + 18), 0),
        'LS1': (mm_to_um(BOARD_ORIGIN_X + 15), mm_to_um(cy + 10), 0),
        'J2': (mm_to_um(BOARD_ORIGIN_X + 50), mm_to_um(BOARD_ORIGIN_Y + BOARD_HEIGHT - 8), 0),
        'SW1': (mm_to_um(cx + 28), mm_to_um(cy + 18), 0),
    }
    return positions

def generate_dsn(components, nets, output_file):
    """Generate DSN file for FreeRouting."""
    positions = get_component_positions()

    # Board boundary in um
    x1 = mm_to_um(BOARD_ORIGIN_X)
    y1 = mm_to_um(BOARD_ORIGIN_Y)
    x2 = mm_to_um(BOARD_ORIGIN_X + BOARD_WIDTH)
    y2 = mm_to_um(BOARD_ORIGIN_Y + BOARD_HEIGHT)

    dsn_parts = []

    # Header
    dsn_parts.append(f'''(pcb singingcard.dsn
  (parser
    (string_quote ")
    (space_in_quoted_tokens on)
    (host_cad "KiCad")
    (host_version "9.0")
  )
  (resolution um 10)
  (unit um)
  (structure
    (boundary
      (path pcb 0
        {x1} {y1}
        {x2} {y1}
        {x2} {y2}
        {x1} {y2}
        {x1} {y1}
      )
    )
    (layer F.Cu
      (type signal)
      (property
        (index 0)
      )
    )
    (layer B.Cu
      (type signal)
      (property
        (index 1)
      )
    )
    (via "Via[0-1]_600:300_um")
    (rule
      (width 250)
      (clearance 200)
      (clearance 200 (type default_smd))
      (clearance 50 (type smd_smd))
    )
  )''')

    # Placement
    dsn_parts.append('  (placement')

    for comp in components:
        ref = comp['ref']
        footprint = comp['footprint']
        if ref in positions:
            x, y, rot = positions[ref]
        else:
            x, y, rot = x1 + 10000, y1 + 10000, 0

        dsn_parts.append(f'''    (component "{footprint}"
      (place {ref} {x} {y} front {rot}
      )
    )''')

    dsn_parts.append('  )')

    # Library (simplified - FreeRouting will read padstacks from component defs)
    dsn_parts.append('''  (library
    (padstack "Via[0-1]_600:300_um"
      (shape
        (circle F.Cu 600)
      )
      (shape
        (circle B.Cu 600)
      )
      (attach off)
    )
  )''')

    # Network
    dsn_parts.append('  (network')

    for net in nets:
        net_name = net['name']
        if not net_name:
            continue

        dsn_parts.append(f'    (net "{net_name}"')
        dsn_parts.append('      (pins')
        for node in net['nodes']:
            dsn_parts.append(f'        {node["ref"]}-{node["pin"]}')
        dsn_parts.append('      )')
        dsn_parts.append('    )')

    dsn_parts.append('''    (class "Default"
      (circuit
        (use_via Via[0-1]_600:300_um)
      )
      (rule
        (width 250)
        (clearance 200)
      )
    )
  )''')

    # Wiring (empty for initial routing)
    dsn_parts.append('  (wiring')
    dsn_parts.append('  )')

    dsn_parts.append(')')

    with open(output_file, 'w') as f:
        f.write('\n'.join(dsn_parts))

    print(f"Generated: {output_file}")

def main():
    print("Parsing netlist...")
    components, nets = parse_netlist('singingcard.net')
    print(f"Found {len(components)} components and {len(nets)} nets")

    print("Generating DSN file...")
    generate_dsn(components, nets, 'singingcard_new.dsn')

if __name__ == '__main__':
    main()
