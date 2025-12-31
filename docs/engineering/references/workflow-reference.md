# Workflow Quick Reference

## 1. Component Selection

```bash
# Import component from LCSC by part number
easyeda2kicad --full --lcsc_id=C12345

# Output: easyeda2kicad.kicad_sym, easyeda2kicad.pretty/, easyeda2kicad.3dshapes/
```

## 2. Design Rule Check

```bash
# Run DRC on PCB
kicad-cli pcb drc --output drc_report.json --format json project.kicad_pcb

# Run ERC on schematic
kicad-cli sch erc --output erc_report.json --format json project.kicad_sch
```

## 3. Visual Inspection

```bash
# 3D raytraced render (top)
kicad-cli pcb render --output render_top.png --side top --width 2048 --height 2048 project.kicad_pcb

# 3D raytraced render (bottom)
kicad-cli pcb render --output render_bottom.png --side bottom project.kicad_pcb

# Gerber to PNG
gerbv -x png -o output.png -D 600 -a file.gbr
```

## 4. Auto-Routing

```bash
# Export DSN for FreeRouting
kicad-cli pcb export dsn --output board.dsn project.kicad_pcb

# Run FreeRouting (requires JAR)
java -jar freerouting.jar -de board.dsn -do board.ses

# Import SES back to KiCad (via GUI or MCP)
```

## 5. Fabrication Files

```bash
# Export Gerbers
kicad-cli pcb export gerbers --output gerbers/ project.kicad_pcb

# Export drill files
kicad-cli pcb export drill --output gerbers/ project.kicad_pcb

# Using KiBot (comprehensive)
kibot -c kibot.yaml -b project.kicad_pcb
```

## 6. BOM Generation

```bash
# Interactive HTML BOM
generate_interactive_bom --dest-dir output/ project.kicad_pcb

# XML BOM via CLI
kicad-cli sch export bom --output bom.xml project.kicad_sch
```

## 7. 3D Model Export

```bash
# STEP file (for CAD)
kicad-cli pcb export step --output model.step project.kicad_pcb

# GLB file (for 3D viewers)
kicad-cli pcb export glb --output model.glb project.kicad_pcb
```

## 8. SVG Export

```bash
# Schematic to SVG
kicad-cli sch export svg --output svg_output/ project.kicad_sch

# PCB to SVG
kicad-cli pcb export svg --output board.svg project.kicad_pcb
```

## KiBot Configuration Example

```yaml
# kibot.yaml
kibot:
  version: 1

preflight:
  run_erc: true
  run_drc: true
  check_zone_fills: true

outputs:
  - name: gerbers
    type: gerber
    dir: output/gerbers
    layers:
      - F.Cu
      - B.Cu
      - F.SilkS
      - B.SilkS
      - F.Mask
      - B.Mask
      - Edge.Cuts

  - name: drill
    type: excellon
    dir: output/gerbers

  - name: bom
    type: bom
    dir: output

  - name: position
    type: position
    dir: output
    format: CSV
```
