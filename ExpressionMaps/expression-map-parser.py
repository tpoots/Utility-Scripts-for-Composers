import os
import re
import sys
import xml.etree.ElementTree as ET
from os import walk

allExpressionMaps = []
for (dirpath, dirnames, filenames) in walk(sys.argv[1]):
    for file in filenames:
        allExpressionMaps.append(os.path.join(dirpath, file))

print allExpressionMaps

print("InstrumentName,Articulation,Keyswitch,UACC")
for expressionMap in allExpressionMaps:
    # f = open(expressionMap, "r")
    # print(f.read())
    # print expressionMap

    m = re.search('.*\/(.*).expressionmap', expressionMap)
    instrumentName = m.group(1)

    tree = ET.parse(expressionMap)
    root = tree.getroot()

    lastArticulation = ''
    lastUACC = 0
    lastMidiKeywitch = 0
    #for articulationElement in root.findall(".//obj[@class='PSoundSlot']"):
    #    print(articulationElement.attrib)

    # print('------------')

    for articulationElement in root.findall(".//obj[@class='PSoundSlot']"): # find all PSoundSlot objects
        if articulationElement.get('class') == 'PSoundSlot': # found an articulation
            #for element in articulationElement.iter():
            #    print(element.attrib)
            articulation = articulationElement.find(".//*[@name='description']").get('value')
            keySwitch = articulationElement.find(".//obj[@class='PSlotThruTrigger']/int[@name='data1']").get('value')
            uacc = articulationElement.find(".//obj[@class='PSlotMidiAction']/member[@name='midiMessages']//obj[@class='POutputEvent']/int[@name='data2']").get('value')
            # print('articulation: ' + articulation)
            # print('keyswitch: ' + keySwitch)
            # print('uacc: ' + uacc)
            # print('------------')
            print(instrumentName + ',' + articulation + ',' + keySwitch + ',' + uacc)

    #for element in tree.iter():
    #    if (element.get('class') == "PSoundSlot"): # found an articulation
    #        print(element.attrib)
