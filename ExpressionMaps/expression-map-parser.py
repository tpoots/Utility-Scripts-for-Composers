import os
import json
import re
import sys
import xml.etree.ElementTree as ET
from os import walk

# https://htmlcolorcodes.com/

# SSW
# artMapConfig = {
#     'SFSW Piccolo Flute CB D.expressionmap': {'name': 'Piccolo Flute', 'order': 0},
#     'SFSW Flute solo CB D.expressionmap': {'name': 'Flute Solo', 'order': 1},
#     'SFSW Flute A2 CB D.expressionmap': {'name': 'Flutes a2', 'order': 2},
#     'SFSW Alto Flute CB D.expressionmap': {'name': 'Alto Flute', 'order': 3},
#     'SFSW Bass Flute CB D.expressionmap': {'name': 'Bass Flute', 'order': 4},
#     'SFSW Oboe Solo CB D.expressionmap': {'name': 'Oboe Solo', 'order': 5},
#     'SFSW Oboes A2 CB D.expressionmap': {'name': 'Oboes a2', 'order': 6},
#     'SFSW Cor Anglais CB D.expressionmap': {'name': 'Cor Anglais', 'order': 7},
#     'SFSW Clarinet Solo CB D.expressionmap': {'name': 'Clariet Solo', 'order': 8},
#     'SFSW Clarinet A2 CB D.expressionmap': {'name': 'Clarinets a2', 'order': 9},
#     'SFSW Bass Clarinet CB D.expressionmap': {'name': 'Bas Clarinet', 'order': 10},
#     'SFSW Contrabass Clarinet CB D.expressionmap': {'name': 'Contrabass Clarinet', 'order': 11},
#     'SFSW Bassoon Solo CB D.expressionmap': {'name': 'Bassoon Solo', 'order': 12},
#     'SFSW Bassoon A2 CB D.expressionmap': {'name': 'Bassoons a2', 'order': 13},
#     'SFSW ContraBassoon CB D.expressionmap': {'name': 'ContraBassoon', 'order': 14}
# }
# artButtonConfig = {
#     1: "Long",
#     2: "Harmonics",
#     3: "Long Hollow",
#     4: "Long Overblown",
#     11: "Staccato",
#     12: "Marcato",
#     13: "Tenuto",
#     14: "Multitongue",
#     15: "Marcato Sforzando",
#     16: "Short Overblown",
#     21: "Legato",
#     22: "Legato (Detached)",
#     31: "Trill HT",
#     32: "Trill WT",
#     33: "FX Flutter",
#     34: "FX Fall",
#     35: "FX Rip"
# }

# SSB
# artMapConfig = {
#     'SFSB Horn Solo CB D.expressionmap': {'name': 'Horn Solo', 'order': 0},
#     'SFSB Horns A2 CB D.expressionmap': {'name': 'Horns a2', 'order': 1},
#     'SFSB Horns A6 CB D.expressionmap': {'name': 'Horns a6', 'order': 2},
#     'SFSB Trumpet Solo CB D.expressionmap': {'name': 'Trumpet Solo', 'order': 3},
#     'SFSB Trumpet A2 CB D.expressionmap': {'name': 'Trumpets a2', 'order': 4},
#     'SFSB Trumpet A6 CB D.expressionmap': {'name': 'Trumpets a6', 'order': 5},
#     'SFSB Tenor Trombone Solo CB D.expressionmap': {'name': 'Tenor Trombone Solo', 'order': 6},
#     'SFSB Tenor Trombone A2 CB D.expressionmap': {'name': 'Tenor Trombones a2', 'order': 7},
#     'SFSB Trombone A6 CB D.expressionmap': {'name': 'Trombones a6', 'order': 8},
#     'SFSB Bass Trombone Solo CB D.expressionmap': {'name': 'Bass Trombone Solo', 'order': 9},
#     'SFSB Bass Trombone A2 CB D.expressionmap': {'name': 'Bass Trombones a2', 'order': 10},
#     'SFSB Cimbasso Solo CB D.expressionmap': {'name': 'Cimbasso Solo', 'order': 11},
#     'SFSB Cimbassi A2 CB D.expressionmap': {'name': 'Cimbassi a2', 'order': 12},
#     'SFSB Contra Trombone Solo CB D.expressionmap': {'name': 'Contra Trombone Solo', 'order': 13},
#     'SFSB Tuba Solo CB D.expressionmap': {'name': 'Tuba Solo', 'order': 14},
#     'SFSB Contrabass Tuba Solo CB D.expressionmap': {'name': 'Contrabass Tuba Solo', 'order': 15}
# }
#
# artButtonConfig = {
# 1: "Long",
# 2: "Long Cuivre",
# 3: "Long Stopped",
# 4: "Long Muted",
# 5: "Long Mariachi",
# 6: "Tremolo",
# 7: "Long Bells Up",
# 11: "Staccato",
# 12: "Marcato",
# 13: "Tenuto",
# 14: "Multitongue",
# 15: "Staccato Muted",
# 16: "Marcato Muted",
# 17: "Tenuto Muted",
# 18: "Staccatissimo",
# 19: "Marcato Bells Up",
# 20: "Staccatissimo Bells Up",
# 21: "Staccato Bells Up",
# 22: "Tenuto Bells Up",
# 23: "Short Muted",
# 31: "Legato",
# 41: "FX Fall",
# 42: "FX Rip",
# 43: "FX Flutter",
# 44: "Trill HT",
# 45: "Trill WT",
# 46: "FX Glissandi",
# 47: "FX Fanfare",
# }

# SSS
artMapConfig = {
    'SFSS Violins 1 CB D.expressionmap': {'name': 'Violins 1', 'order': 0},
    'SFSS Violins 2 CB D.expressionmap': {'name': 'Violins 2', 'order': 1},
    'SFSS Violas CB D.expressionmap': {'name': 'Violas', 'order': 2},
    'SFSS Celli CB D.expressionmap': {'name': 'Celli', 'order': 3},
    'SFSS Basses CB D.expressionmap': {'name': 'Basses', 'order': 4},
    'SFSS Ensembles CB D.expressionmap': {'name': 'Ensembles', 'order': 5},
}

artButtonConfig = {
1: "Long",
2: "Long Sul Pont",
3: "Long Super Sul Tasto",
4: "Long CS",
5: "Long CS Blend",
6: "Long Flautando",
7: "Long CS Sul Pont",
8: "Long Rachm",
9: "Long Sul G",
10: "Long Sul Tasto",
11: "Harmonics",
12: "Flautando",
13: "Tremolo",
14: "Tremolo 150",
15: "Tremolo 150 CS",
16: "Tremolo 180",
17: "Tremolo Muted",
18: "Tremolo CS",
19: "Tremolo Sul Pont",
21: "Marcato",
22: "Pizzicato",
23: "Spiccato",
24: "Col Legno",
25: "Pizzicato Bartok",
26: "Short Brushed CS",
27: "Short Harmonics",
28: "Short Brushed",
29: "Short CS",
30: "Staccato Dig",
31: "Short Harmonic",
32: "Short Muted",
33: "Short Soft",
34: "Tenuto [0.5]",
35: "Marcato [1.0]",
41: "Legato",
42: "Legato Sul G",
43: "Legato Sul C",
44: "Legato Runs",
51: "Trill HT",
52: "Trill WT",
53: "FX",
54: "Trill Min3",
55: "Trill Maj3"
}

allExpressionMaps = []
for (dirpath, dirnames, filenames) in walk(sys.argv[1]):
    for file in filenames:
        allExpressionMaps.append(os.path.join(dirpath, file))

articulationMap = {"articulations": artButtonConfig}
articulationMap.update({"instruments": {}})

for expressionMap in allExpressionMaps:
    # f = open(expressionMap, "r")
    # print(f.read())
    # print expressionMap

    m = re.search('.*\/(.*)', expressionMap)
    instrumentArtMapName = m.group(1)

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
            # print(instrumentArtMapName + ',' + articulation + ',' + keySwitch + ',' + uacc)
            if (instrumentArtMapName.find('CB D') >= 0):
                config = artMapConfig.get(instrumentArtMapName)
                instrumentIndex = config.get("order")
                instrumentName = config.get("name")
                if (not instrumentIndex in articulationMap["instruments"].keys()):
                    articulationMap["instruments"][instrumentIndex] = {}
                    articulationMap["instruments"][instrumentIndex].update({"name": instrumentName, "articulations": {}})
                    # update the list of all articulations as well so we have a full list for the section
                articulationMap["instruments"][instrumentIndex]["articulations"].update({articulation: {'keySwitch': keySwitch, 'UACC': uacc}})

    #for element in tree.iter():
    #    if (element.get('class') == "PSoundSlot"): # found an articulation
    #        print(element.attrib)

# Serializing json
json_object = json.dumps(articulationMap, indent=4)
print(json_object);