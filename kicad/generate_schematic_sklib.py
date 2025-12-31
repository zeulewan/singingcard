from collections import defaultdict
from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

from skidl.pin import pin_types

SKIDL_lib_version = '0.0.1'

generate_schematic = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'ISD3900FYI', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'ISD3900FYI'}), 'ref_prefix':'U', 'fplist':['singingcard:LQFP-48_L7.0-W7.0-P0.50-LS9.0-BL'], 'footprint':'singingcard:LQFP-48_L7.0-W7.0-P0.50-LS9.0-BL', 'keywords':'', 'description':'', 'datasheet':'', 'pins':[
            Pin(num='1',name='NC',func=pin_types.UNSPEC),
            Pin(num='2',name='CSB',func=pin_types.UNSPEC),
            Pin(num='3',name='DI',func=pin_types.UNSPEC),
            Pin(num='4',name='I2S_SDI/GPIO7',func=pin_types.UNSPEC),
            Pin(num='5',name='I2S_SCK/GPIO6',func=pin_types.UNSPEC),
            Pin(num='6',name='I2S_WS/GPIO5',func=pin_types.UNSPEC),
            Pin(num='7',name='I2S_SDO/GPIO4',func=pin_types.UNSPEC),
            Pin(num='8',name='NC',func=pin_types.UNSPEC),
            Pin(num='9',name='NC',func=pin_types.UNSPEC),
            Pin(num='10',name='VSS',func=pin_types.UNSPEC),
            Pin(num='11',name='VCC',func=pin_types.UNSPEC),
            Pin(num='12',name='VREG',func=pin_types.UNSPEC),
            Pin(num='13',name='MISO',func=pin_types.UNSPEC),
            Pin(num='14',name='SCLK',func=pin_types.UNSPEC),
            Pin(num='15',name='SSB',func=pin_types.UNSPEC),
            Pin(num='16',name='MOSI',func=pin_types.UNSPEC),
            Pin(num='17',name='VCCD_PWM',func=pin_types.UNSPEC),
            Pin(num='18',name='SPK+',func=pin_types.UNSPEC),
            Pin(num='19',name='VSSD_PWM',func=pin_types.UNSPEC),
            Pin(num='20',name='SPK-',func=pin_types.UNSPEC),
            Pin(num='21',name='VCCD_PWM',func=pin_types.UNSPEC),
            Pin(num='22',name='NC',func=pin_types.UNSPEC),
            Pin(num='23',name='NC',func=pin_types.UNSPEC),
            Pin(num='24',name='NC',func=pin_types.UNSPEC),
            Pin(num='25',name='INTB',func=pin_types.UNSPEC),
            Pin(num='26',name='RDY/BSYB',func=pin_types.UNSPEC),
            Pin(num='27',name='RESET',func=pin_types.UNSPEC),
            Pin(num='28',name='DO',func=pin_types.UNSPEC),
            Pin(num='29',name='CLK',func=pin_types.UNSPEC),
            Pin(num='30',name='GPIO3',func=pin_types.UNSPEC),
            Pin(num='31',name='GPIO2',func=pin_types.UNSPEC),
            Pin(num='32',name='GPIO1',func=pin_types.UNSPEC),
            Pin(num='33',name='NC',func=pin_types.UNSPEC),
            Pin(num='34',name='NC',func=pin_types.UNSPEC),
            Pin(num='35',name='XTALOUT',func=pin_types.UNSPEC),
            Pin(num='36',name='XTALIN',func=pin_types.UNSPEC),
            Pin(num='37',name='NC',func=pin_types.UNSPEC),
            Pin(num='38',name='GPIO0',func=pin_types.UNSPEC),
            Pin(num='39',name='NC',func=pin_types.UNSPEC),
            Pin(num='40',name='NC',func=pin_types.UNSPEC),
            Pin(num='41',name='AUDOUT',func=pin_types.UNSPEC),
            Pin(num='42',name='AUXOUT',func=pin_types.UNSPEC),
            Pin(num='43',name='VCCa',func=pin_types.UNSPEC),
            Pin(num='44',name='VSSA',func=pin_types.UNSPEC),
            Pin(num='45',name='ANAOUT/MIC-',func=pin_types.UNSPEC),
            Pin(num='46',name='ANAIN/MIC+',func=pin_types.UNSPEC),
            Pin(num='47',name='AUXIN',func=pin_types.UNSPEC),
            Pin(num='48',name='NC',func=pin_types.UNSPEC)], 'unit_defs':[] }),
        Part(**{ 'name':'W25Q16JVSSIQTR', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'W25Q16JVSSIQTR'}), 'ref_prefix':'U', 'fplist':['singingcard:SOIC-8_L5.3-W5.3-P1.27-LS8.0-BL'], 'footprint':'singingcard:SOIC-8_L5.3-W5.3-P1.27-LS8.0-BL', 'keywords':'', 'description':'', 'datasheet':'https://lcsc.com/product-detail/FLASH_W25Q16JVSSIQTR_C131025.html', 'pins':[
            Pin(num='1',name='/CS',func=pin_types.UNSPEC),
            Pin(num='2',name='DO/IO1',func=pin_types.UNSPEC),
            Pin(num='3',name='IO2',func=pin_types.UNSPEC),
            Pin(num='4',name='GND',func=pin_types.UNSPEC),
            Pin(num='5',name='DI/IO0',func=pin_types.UNSPEC),
            Pin(num='6',name='CLK',func=pin_types.UNSPEC),
            Pin(num='7',name='IO3',func=pin_types.UNSPEC),
            Pin(num='8',name='VCC',func=pin_types.UNSPEC)], 'unit_defs':[] }),
        Part(**{ 'name':'CR2032-BS-6-1', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'CR2032-BS-6-1'}), 'ref_prefix':'B', 'fplist':['singingcard:BAT-TH_CR2032-BS-6-1'], 'footprint':'singingcard:BAT-TH_CR2032-BS-6-1', 'keywords':'', 'description':'', 'datasheet':'https://lcsc.com/product-detail/Battery-Holders-Clips-Contacts_Button-battery-holder-CR2032_C70377.html', 'pins':[
            Pin(num='1',name='1',func=pin_types.INPUT),
            Pin(num='2',name='2',func=pin_types.INPUT)], 'unit_defs':[] }),
        Part(**{ 'name':'GL5528(10-20)', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'GL5528(10-20)'}), 'ref_prefix':'R', 'fplist':['singingcard:RES-TH_L5.1-W4.3-P3.40-D0.5'], 'footprint':'singingcard:RES-TH_L5.1-W4.3-P3.40-D0.5', 'keywords':'', 'description':'', 'datasheet':'https://lcsc.com/product-detail/Photoresistors_GL5528-10-20-NO-RHOS_C10081.html', 'pins':[
            Pin(num='2',name='2',func=pin_types.INPUT),
            Pin(num='1',name='1',func=pin_types.INPUT)], 'unit_defs':[] }),
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'R'}), 'ref_prefix':'R', 'fplist':[''], 'footprint':'Resistor_SMD:R_0603_1608Metric', 'keywords':'R res resistor', 'description':'Resistor', 'datasheet':'~', 'pins':[
            Pin(num='1',name='~',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='~',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'C', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'C'}), 'ref_prefix':'C', 'fplist':[''], 'footprint':'Capacitor_SMD:C_0603_1608Metric', 'keywords':'cap capacitor', 'description':'Unpolarized capacitor', 'datasheet':'~', 'pins':[
            Pin(num='1',name='~',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='~',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'Conn_01x02', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'Conn_01x02'}), 'ref_prefix':'J', 'fplist':[''], 'footprint':'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical', 'keywords':'connector', 'description':'Generic connector, single row, 01x02, script generated (kicad-library-utils/schlib/autogen/connector/)', 'datasheet':'~', 'pins':[
            Pin(num='1',name='Pin_1',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='Pin_2',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'SW_Push', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'SW_Push'}), 'ref_prefix':'SW', 'fplist':[''], 'footprint':'Button_Switch_SMD:SW_SPST_TL3342', 'keywords':'switch normally-open pushbutton push-button', 'description':'Push button switch, generic, two pins', 'datasheet':'~', 'pins':[
            Pin(num='1',name='1',func=pin_types.PASSIVE),
            Pin(num='2',name='2',func=pin_types.PASSIVE)], 'unit_defs':[] })])