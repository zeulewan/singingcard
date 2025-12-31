#!/usr/bin/env python3
"""
Export KiCad PCB to Specctra DSN format for FreeRouting.
"""

import re
import os

def parse_pcb(pcb_file):
    """Parse KiCad PCB file to extract components, pads, and nets."""
    with open(pcb_file, 'r') as f:
        content = f.read()

    # Board dimensions from gr_rect Edge.Cuts
    outline_match = re.search(r'\(gr_rect\s+\(start\s+([0-9.-]+)\s+([0-9.-]+)\)\s+\(end\s+([0-9.-]+)\s+([0-9.-]+)\)', content)
    if outline_match:
        x1, y1, x2, y2 = map(float, outline_match.groups())
    else:
        x1, y1, x2, y2 = 100, 100, 185, 155

    # Extract nets
    nets = {}
    net_pattern = r'\(net\s+(\d+)\s+"([^"]*)"\)'
    for match in re.finditer(net_pattern, content):
        net_id, net_name = match.groups()
        nets[int(net_id)] = net_name if net_name else f"Net{net_id}"

    # Extract footprints and their pads
    components = []
    fp_pattern = r'\(footprint\s+"([^"]+)".*?\(uuid\s+"([^"]+)"\).*?\(at\s+([0-9.-]+)\s+([0-9.-]+)\s*([0-9.-]*)\)'

    # More comprehensive footprint extraction
    fp_blocks = re.findall(r'\(footprint "[^"]+"\s+\(layer[^)]+\)\s+\(uuid[^)]+\)\s+\(at[^)]+\).*?(?=\(footprint|\Z)', content, re.DOTALL)

    for fp_block in fp_blocks:
        # Get footprint name and position
        fp_match = re.match(r'\(footprint\s+"([^"]+)".*?\(at\s+([0-9.-]+)\s+([0-9.-]+)\s*([0-9.-]*)\)', fp_block, re.DOTALL)
        if not fp_match:
            continue

        fp_name, x, y, rot = fp_match.groups()
        x, y = float(x), float(y)
        rot = float(rot) if rot else 0

        # Get reference
        ref_match = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_block)
        ref = ref_match.group(1) if ref_match else "?"

        # Get pads - handle multiline format
        pads = []
        # Split into pad blocks
        pad_blocks = re.split(r'(?=\(pad ")', fp_block)
        for pad_block in pad_blocks:
            if not pad_block.strip().startswith('(pad "'):
                continue

            # Extract pad number
            pad_num_match = re.search(r'\(pad "(\d+)"', pad_block)
            if not pad_num_match:
                continue
            pad_num = pad_num_match.group(1)

            # Extract position
            at_match = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)', pad_block)
            if not at_match:
                continue
            px, py = float(at_match.group(1)), float(at_match.group(2))

            # Extract size
            size_match = re.search(r'\(size\s+([0-9.-]+)\s+([0-9.-]+)', pad_block)
            if not size_match:
                continue
            sx, sy = float(size_match.group(1)), float(size_match.group(2))

            # Extract net (may be on separate line)
            net_match = re.search(r'\(net\s+(\d+)\s+"([^"]*)"', pad_block)
            net_id = int(net_match.group(1)) if net_match else 0
            net_name = net_match.group(2) if net_match else ""

            pads.append({
                'num': pad_num,
                'x': px,
                'y': py,
                'size_x': sx,
                'size_y': sy,
                'net_id': net_id,
                'net_name': net_name
            })

        components.append({
            'ref': ref,
            'footprint': fp_name,
            'x': x,
            'y': y,
            'rotation': rot,
            'pads': pads
        })

    return {
        'bounds': (x1, y1, x2, y2),
        'nets': nets,
        'components': components
    }

def generate_dsn(pcb_data, output_file):
    """Generate Specctra DSN file."""
    x1, y1, x2, y2 = pcb_data['bounds']
    nets = pcb_data['nets']
    components = pcb_data['components']

    # Collect all unique pad sizes for padstack generation
    pad_sizes = set()
    for comp in components:
        for pad in comp['pads']:
            # Round to avoid floating point issues
            sx = round(pad['size_x'] * 1000)  # mm to um
            sy = round(pad['size_y'] * 1000)
            pad_sizes.add((sx, sy))

    def get_padstack_name(sx, sy):
        return f"Rect[T]Pad_{sx}x{sy}_um"

    dsn = []
    dsn.append('(pcb singingcard.dsn')
    dsn.append('  (parser')
    dsn.append('    (string_quote ")')
    dsn.append('    (space_in_quoted_tokens on)')
    dsn.append('    (host_cad "KiCad")')
    dsn.append('    (host_version "8.0")')
    dsn.append('  )')
    dsn.append('  (resolution um 10)')
    dsn.append('  (unit um)')
    dsn.append('  (structure')

    # Board boundary
    dsn.append('    (boundary')
    dsn.append('      (path pcb 0')
    dsn.append(f'        {x1*1000:.0f} {y1*1000:.0f}')
    dsn.append(f'        {x2*1000:.0f} {y1*1000:.0f}')
    dsn.append(f'        {x2*1000:.0f} {y2*1000:.0f}')
    dsn.append(f'        {x1*1000:.0f} {y2*1000:.0f}')
    dsn.append(f'        {x1*1000:.0f} {y1*1000:.0f}')
    dsn.append('      )')
    dsn.append('    )')

    # Layers
    dsn.append('    (layer F.Cu')
    dsn.append('      (type signal)')
    dsn.append('      (property')
    dsn.append('        (index 0)')
    dsn.append('      )')
    dsn.append('    )')
    dsn.append('    (layer B.Cu')
    dsn.append('      (type signal)')
    dsn.append('      (property')
    dsn.append('        (index 1)')
    dsn.append('      )')
    dsn.append('    )')

    # Via
    dsn.append('    (via "Via[0-1]_600:300_um")')

    # Rule
    dsn.append('    (rule')
    dsn.append('      (width 250)')
    dsn.append('      (clearance 200)')
    dsn.append('      (clearance 200 (type default_smd))')
    dsn.append('      (clearance 50 (type smd_smd))')
    dsn.append('    )')

    dsn.append('  )')  # structure

    # Placement
    dsn.append('  (placement')
    for comp in components:
        ref = comp['ref']
        x = comp['x'] * 1000  # mm to um
        y = comp['y'] * 1000
        rot = comp['rotation']
        side = 'front'
        dsn.append(f'    (component "{comp["footprint"]}"')
        dsn.append(f'      (place {ref} {x:.0f} {y:.0f} {side} {rot:.0f}')
        dsn.append(f'      )')
        dsn.append(f'    )')
    dsn.append('  )')

    # Library (padstacks)
    dsn.append('  (library')

    # Generate padstacks for all unique pad sizes
    for sx, sy in sorted(pad_sizes):
        padstack_name = get_padstack_name(sx, sy)
        half_x = sx // 2
        half_y = sy // 2
        dsn.append(f'    (padstack "{padstack_name}"')
        dsn.append(f'      (shape (rect F.Cu -{half_x} -{half_y} {half_x} {half_y}))')
        dsn.append('      (attach off)')
        dsn.append('    )')

    # Via padstack
    dsn.append('    (padstack "Via[0-1]_600:300_um"')
    dsn.append('      (shape (circle F.Cu 600))')
    dsn.append('      (shape (circle B.Cu 600))')
    dsn.append('      (attach off)')
    dsn.append('    )')

    # Component images with correct pad sizes
    for comp in components:
        dsn.append(f'    (image "{comp["footprint"]}"')
        for pad in comp['pads']:
            px = pad['x'] * 1000
            py = pad['y'] * 1000
            sx = round(pad['size_x'] * 1000)
            sy = round(pad['size_y'] * 1000)
            padstack_name = get_padstack_name(sx, sy)
            dsn.append(f'      (pin "{padstack_name}" {pad["num"]} {px:.0f} {py:.0f})')
        dsn.append('    )')

    dsn.append('  )')  # library

    # Network
    dsn.append('  (network')

    # Group pins by net
    net_pins = {}
    for comp in components:
        for pad in comp['pads']:
            net_id = pad['net_id']
            if net_id > 0:
                if net_id not in net_pins:
                    net_pins[net_id] = []
                net_pins[net_id].append(f'{comp["ref"]}-{pad["num"]}')

    # Output nets
    for net_id, pins in net_pins.items():
        net_name = nets.get(net_id, f"Net{net_id}")
        dsn.append(f'    (net "{net_name}"')
        dsn.append(f'      (pins {" ".join(pins)})')
        dsn.append('    )')

    # Net classes
    dsn.append('    (class kicad_default "" {}'.format(' '.join(f'"{nets.get(nid, f"Net{nid}")}"' for nid in net_pins.keys())))
    dsn.append('      (circuit')
    dsn.append('        (use_via Via[0-1]_600:300_um)')
    dsn.append('      )')
    dsn.append('      (rule')
    dsn.append('        (width 250)')
    dsn.append('        (clearance 200)')
    dsn.append('      )')
    dsn.append('    )')

    dsn.append('  )')  # network

    dsn.append('  (wiring')
    dsn.append('  )')

    dsn.append(')')  # pcb

    with open(output_file, 'w') as f:
        f.write('\n'.join(dsn))

    print(f"Generated: {output_file}")
    print(f"Components: {len(components)}")
    print(f"Nets with connections: {len(net_pins)}")

def main():
    pcb_file = 'singingcard.kicad_pcb'
    dsn_file = 'singingcard.dsn'

    print("Parsing PCB file...")
    pcb_data = parse_pcb(pcb_file)

    print("Generating DSN file...")
    generate_dsn(pcb_data, dsn_file)

if __name__ == '__main__':
    main()
