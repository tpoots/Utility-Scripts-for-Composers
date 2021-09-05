import os
import json
import re
import sys
import xml.etree.ElementTree as ET
from os import walk

# https://htmlcolorcodes.com/

artMapConfig = {
    'SFSW Piccolo Flute CB D.expressionmap': {'name': 'Piccolo Flute', 'order': 0},
    'SFSW Flute solo CB D.expressionmap': {'name': 'Flute Solo', 'order': 1},
    'SFSW Flute A2 CB D.expressionmap': {'name': 'Flutes a2', 'order': 2},
    'SFSW Alto Flute CB D.expressionmap': {'name': 'Alto Flute', 'order': 3},
    'SFSW Bass Flute CB D.expressionmap': {'name': 'Bass Flute', 'order': 4},
    'SFSW Oboe Solo CB D.expressionmap': {'name': 'Oboe Solo', 'order': 5},
    'SFSW Oboes A2 CB D.expressionmap': {'name': 'Oboes a2', 'order': 6},
    'SFSW Cor Anglais CB D.expressionmap': {'name': 'Cor Anglais', 'order': 7},
    'SFSW Clarinet Solo CB D.expressionmap': {'name': 'Clariet Solo', 'order': 8},
    'SFSW Clarinet A2 CB D.expressionmap': {'name': 'Clarinets a2', 'order': 9},
    'SFSW Bass Clarinet CB D.expressionmap': {'name': 'Bas Clarinet', 'order': 10},
    'SFSW Contrabass Clarinet CB D.expressionmap': {'name': 'Contrabass Clarinet', 'order': 11},
    'SFSW Bassoon Solo CB D.expressionmap': {'name': 'Bassoon Solo', 'order': 12},
    'SFSW Bassoon A2 CB D.expressionmap': {'name': 'Bassoons a2', 'order': 13},
    'SFSW ContraBassoon CB D.expressionmap': {'name': 'ContraBassoon', 'order': 14}
}

allExpressionMaps = []
for (dirpath, dirnames, filenames) in walk(sys.argv[1]):
    for file in filenames:
        allExpressionMaps.append(os.path.join(dirpath, file))

articulationMap = {}
# CSV output - print("InstrumentName,Articulation,Keyswitch,UACC")
for expressionMap in allExpressionMaps:
    # f = open(expressionMap, "r")
    # print(f.read())
    # print expressionMap

    m = re.search('.*\/(.*)', expressionMap)
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
            # CSV output - print(instrumentName + ',' + articulation + ',' + keySwitch + ',' + uacc)
            if (instrumentName.find('CB D') >= 0):
                config = artMapConfig.get(instrumentName)
                instrumentIndex = config.get("order")
                instrumentName = config.get("name")
                if (not instrumentIndex in articulationMap.keys()):
                    articulationMap[instrumentIndex] = {}
                    articulationMap[instrumentIndex].update({"name": instrumentName, "articulations": {}})
                articulationMap[instrumentIndex]["articulations"].update({articulation: {'keySwitch': keySwitch, 'UACC': uacc}})

    #for element in tree.iter():
    #    if (element.get('class') == "PSoundSlot"): # found an articulation
    #        print(element.attrib)

# Serializing json
json_object = json.dumps(articulationMap, indent=4)
print(json_object);