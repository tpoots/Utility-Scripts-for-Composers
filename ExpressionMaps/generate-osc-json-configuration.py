import csv
import os
import json
import platform
import re
import sys
import xml.etree.ElementTree as ET
from os import walk

# -----------------------------------------------------------------------------
# Usage:
#   python generate-osc-json-configuration.py {directory-containing-expression-maps |individual-expression-map}
#
# This script parses directories (or individual files) containing Cubase
# expression maps and generates two JSON objects that can be used by the OSC
# Cubase Controller: "instruments" and "articulations". These must be copied
# into the library configuration you are creating for the OSC controller.
#
# Please note that the library configuration lives in a variable called
# "configuration" within the OSC session itself, but it is highly recommended
# that you keep a reference copy of the JSON config in a separate file for
# easier editing. Such a file (with examples) is already provided in
# "configuration.json". Please reference that file to see what fields are
# required to be defined for each library
#
# -----------------------------------------------------------------------------


allExpressionMaps = []
articulationMap = {}
insMapConfig = {}


pathRegex = ""
if (platform.system() == 'Windows'):
    pathRegex = '.*\\\(.*)'
else:
    pathRegex = '.*\/(.*)'

if len(sys.argv) != 3:
    print("Incorrect # of parameters provided")
    print("Usage:")
    print("python generate-osc-json-configuration.py {directory-containing-expression-maps |individual-expression-map} {articulation button style: either \"perInstrument\" or \"library\"}")
    exit(1)

expressionMapsPath = sys.argv[1]
articulationStyle = sys.argv[2]

if articulationStyle != 'library' and articulationStyle != 'perInstrument':
    print("You must define an articulation button style, either \"library\" or \"perInstrument\"")
    print("Usage:")
    print("python generate-osc-json-configuration.py {directory-containing-expression-maps |individual-expression-map} {articulation button style: either \"perInstrument\" or \"library\"}")
    exit(1)

if os.path.isdir(expressionMapsPath):
    for (dirpath, dirnames, filenames) in walk(expressionMapsPath):
        for file in filenames:
            allExpressionMaps.append(os.path.join(dirpath, file))
else:
    allExpressionMaps.append(expressionMapsPath)

# read in the map-config.csv
reader = csv.reader(open('map-config.csv', 'r'))
headers = next(reader)
for row in reader:
    insName, mapName, order = row[0].strip(), row[1].strip(), int(row[2].strip())
    insMapConfig[insName] = {'name': mapName, 'order': order}

print(insMapConfig)


if articulationStyle == 'library':
    reader = csv.reader(open('articulations.csv', 'r'))
    headers = next(reader)
    artButtonConfig = {int(rows[2]): rows[0] for rows in reader}
    articulationMap = {"articulations": artButtonConfig}

articulationMap.update({"instruments": {}})

for expressionMap in allExpressionMaps:
    m = re.search(pathRegex, expressionMap)
    instrumentArtMapName = m.group(1)

    tree = ET.parse(expressionMap)
    root = tree.getroot()

    for articulationElement in root.findall(".//obj[@class='PSoundSlot']"):  # find all PSoundSlot objects
        if articulationElement.get('class') == 'PSoundSlot':  # found an articulation
            articulation = articulationElement.find(".//*[@name='s']").get('value').strip()
            # this is less general: articulation = articulationElement.find(".//*[@name='description']").get('value').strip()

            keySwitch = articulationElement.find(".//obj[@class='PSlotThruTrigger']/int[@name='data1']").get('value')
            uacc = 127
            if (articulationElement.find(".//obj[@class='PSlotMidiAction']/member[@name='midiMessages']//obj[@class='POutputEvent']/int[@name='data2']") is not None):
                uacc = articulationElement.find(".//obj[@class='PSlotMidiAction']/member[@name='midiMessages']//obj[@class='POutputEvent']/int[@name='data2']").get('value')

            config = insMapConfig.get(instrumentArtMapName)
            instrumentIndex = config.get("order")
            instrumentName = config.get("name")

            if not instrumentIndex in articulationMap["instruments"].keys():
                articulationMap["instruments"][instrumentIndex] = {}
                articulationMap["instruments"][instrumentIndex].update({"name": instrumentName, "articulations": {}})
                # update the list of all articulations as well so we have a full list for the library
            articulationMap["instruments"][instrumentIndex]["articulations"].update({articulation: {'keySwitch': keySwitch, 'UACC': uacc}})


json_object = json.dumps(articulationMap, indent=4)
print(json_object)