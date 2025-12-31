#!/usr/bin/env python3
"""
Import FreeRouting SES file traces into KiCad PCB.
"""

import re
import uuid

def gen_uuid():
    return str(uuid.uuid4())

def parse_ses(ses_file):
    """Parse SES file to extract routes."""
    with open(ses_file, 'r') as f:
        content = f.read()

    routes = []
    vias = []

    # Find network_out section - simpler approach
    idx = content.find('(network_out')
    if idx < 0:
        print("No network_out section found")
        return routes, vias

    # Extract everything from network_out to the end
    network_content = content[idx:]

    # Parse each net - net name can contain special chars like +
    # Find all (net ... ) blocks
    depth = 0
    start = None
    net_blocks = []

    i = 0
    while i < len(network_content):
        if network_content[i:i+5] == '(net ':
            if depth == 0:
                start = i
            depth += 1
        if network_content[i] == '(':
            if depth > 0:
                depth += 1
        if network_content[i] == ')':
            if depth > 0:
                depth -= 1
                if depth == 1:  # Back to net level
                    # Check if next char after whitespace is not ( - end of net
                    j = i + 1
                    while j < len(network_content) and network_content[j] in ' \n\t':
                        j += 1
                    if j >= len(network_content) or network_content[j] != '(':
                        net_blocks.append(network_content[start:i+1])
                        depth = 0
                        start = None
        i += 1

    # Simpler approach: split on (net and process
    net_sections = re.split(r'(?=\(net\s+)', network_content)

    for net_section in net_sections:
        if not net_section.strip().startswith('(net'):
            continue

        # Extract net name
        net_match = re.match(r'\(net\s+([^\s\n]+)', net_section)
        if not net_match:
            continue
        net_name = net_match.group(1)

        # Parse wires - multiline format
        wire_pattern = r'\(wire\s*\n?\s*\(path\s+([A-Za-z.]+)\s+(\d+)\s*\n?([\s\d.-]+)\)\s*\)'
        for wire_match in re.finditer(wire_pattern, net_section, re.DOTALL):
            layer = wire_match.group(1)
            width = int(wire_match.group(2))
            coords_str = wire_match.group(3).strip()
            # Parse coordinates (may be on multiple lines)
            coords = [float(x) for x in coords_str.split()]

            # Convert coordinates (um to mm)
            # SES uses resolution um 10, so values are in 0.1um
            # Actually it says (resolution um 10) meaning 10 units = 1 um
            # So divide by 10000 to get mm (10 * 1000)
            points = []
            for j in range(0, len(coords), 2):
                x = coords[j] / 10000.0
                y = coords[j+1] / 10000.0
                points.append((x, y))

            if len(points) >= 2:
                routes.append({
                    'net': net_name,
                    'layer': layer,
                    'width': width / 10000.0,
                    'points': points
                })

        # Parse vias
        via_pattern = r'\(via\s+"([^"]+)"\s+([\d.-]+)\s+([\d.-]+)\s*\)'
        for via_match in re.finditer(via_pattern, net_section):
            via_type = via_match.group(1)
            x = float(via_match.group(2)) / 10000.0
            y = float(via_match.group(3)) / 10000.0
            vias.append({
                'net': net_name,
                'x': x,
                'y': y,
                'type': via_type
            })

    return routes, vias

def add_routes_to_pcb(pcb_file, routes, vias, output_file):
    """Add routes and vias to PCB file."""
    with open(pcb_file, 'r') as f:
        content = f.read()

    # Find net codes in PCB
    net_codes = {}
    net_pattern = r'\(net\s+(\d+)\s+"([^"]*)"\)'
    for match in re.finditer(net_pattern, content):
        code, name = match.groups()
        net_codes[name] = int(code)

    # Build tracks section
    tracks = []
    for route in routes:
        net_name = route['net']
        net_code = net_codes.get(net_name, 0)
        layer = route['layer']
        width = route['width']
        points = route['points']

        # Create segments between consecutive points
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            tracks.append(f'''  (segment
    (start {x1:.4f} {y1:.4f})
    (end {x2:.4f} {y2:.4f})
    (width {width:.4f})
    (layer "{layer}")
    (net {net_code})
    (uuid "{gen_uuid()}")
  )''')

    # Build vias section
    via_strs = []
    for via in vias:
        net_name = via['net']
        net_code = net_codes.get(net_name, 0)
        x, y = via['x'], via['y']
        # Standard via size
        via_strs.append(f'''  (via
    (at {x:.4f} {y:.4f})
    (size 0.6)
    (drill 0.3)
    (layers "F.Cu" "B.Cu")
    (net {net_code})
    (uuid "{gen_uuid()}")
  )''')

    # Insert tracks before closing paren
    # Find position before last )
    last_paren = content.rfind(')')
    new_content = content[:last_paren]

    # Add tracks and vias
    if tracks:
        new_content += '\n\n'
        new_content += '\n'.join(tracks)

    if via_strs:
        new_content += '\n\n'
        new_content += '\n'.join(via_strs)

    new_content += '\n)'

    # Write output
    with open(output_file, 'w') as f:
        f.write(new_content)

    print(f"Added {len(tracks)} track segments and {len(via_strs)} vias")

def main():
    ses_file = 'singingcard_routed.ses'
    pcb_file = 'singingcard.kicad_pcb'
    output_file = 'singingcard_routed.kicad_pcb'

    print("Parsing SES file...")
    routes, vias = parse_ses(ses_file)
    print(f"Found {len(routes)} wire paths and {len(vias)} vias")

    print("Adding routes to PCB...")
    add_routes_to_pcb(pcb_file, routes, vias, output_file)

    print(f"Generated: {output_file}")

if __name__ == '__main__':
    main()
