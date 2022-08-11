import os
import json
import platform
import re
import sys
import xml.etree.ElementTree as ET
from os import walk

# -----------------------------------------------------------------------------
# Usage:
#   python generate-csv-configs.py {directory-containing-expression-maps |individual-expression-map}
#
# This script parses directories (or individual files) containing Cubase
# expression maps and generates three CSV output files:
#
# 1. all-expression-maps-and-articulations.csv - a file listing every unique
#    combination of expression map and articulation, with keyswitch trigger and
#    UACC value (UACC defaults to 127 if not available)
#
# 2. map-config.csv - a file containing just the unique expression map
#    names, allowing the user to define a custom name and order in which the
#    instrument should appear in the UI (by filling in the second and third
#    columns).
#
# 3. articulations.csv - a file containing just the unique articulations present
#    in the expression maps, sorted by the frequency in which they occurred.
#    This file allows the user to define the location each articulation
#    should occupy in the OSC controller UI, by filling in the third column.
#    This step is OPTIONAL and only required if you are using "library"
#    style articulation buttons
#
# If the output files already exist THEY WILL BE OVERWRITTEN
#
# The first file is useful for analyzing the contents of a set of Cubase Expression
# maps. The purpose of the second two are to be provided as input to the subsequent
# script (generate-osc-json-config.py) which takes the expression maps
# plus the user-provided map-config.csv and articulations.csv and generates the
# json configuration needed by the OSC cubase controller.
#
# -----------------------------------------------------------------------------

allExpressionMapFiles = []
allExpressionMapsNames = []
allArticulations = {}
articulationsByMap = {}

if len(sys.argv) != 2:
    print("Incorrect # of parameters provided")
    print("Usage:")
    print("python generate-csv-configs.py {directory-containing-expression-maps |individual-expression-map}")

expressionMapsPath = sys.argv[1]
if os.path.isdir(expressionMapsPath):
    for (dirpath, dirnames, filenames) in walk(expressionMapsPath):
        for file in filenames:
            allExpressionMapFiles.append(os.path.join(dirpath, file))
else:
    allExpressionMapFiles.append(expressionMapsPath)

pathRegex = ""
if (platform.system() == 'Windows'):
    pathRegex = '.*\\\(.*)'
else:
    pathRegex = '.*\/(.*)'

for expressionMapFile in allExpressionMapFiles:
    print("Parsing " + expressionMapFile + "...")

    m = re.search(pathRegex, expressionMapFile)
    instrumentArtMapName = m.group(1)
    articulationsByMap[instrumentArtMapName] = []
    allExpressionMapsNames.append(instrumentArtMapName)

    tree = ET.parse(expressionMapFile)
    root = tree.getroot()

    for articulationElement in root.findall(".//obj[@class='PSoundSlot']"):  # find all PSoundSlot objects
        if articulationElement.get('class') == 'PSoundSlot':  # found an articulation
            articulation = articulationElement.find(".//*[@name='s']").get('value').strip()

            if articulation not in allArticulations.keys():
                allArticulations[articulation] = 0

            allArticulations[articulation] += 1

            keySwitch = articulationElement.find(".//obj[@class='PSlotThruTrigger']/int[@name='data1']").get('value')

            uacc = 127 # default value
            if (articulationElement.find(".//obj[@class='PSlotMidiAction']/member[@name='midiMessages']//obj[@class='POutputEvent']/int[@name='data2']") is not None):
                uacc = articulationElement.find(".//obj[@class='PSlotMidiAction']/member[@name='midiMessages']//obj[@class='POutputEvent']/int[@name='data2']").get('value')

            articulationsByMap[instrumentArtMapName].append([str(articulation), str(keySwitch), str(uacc)])


# create map config to allow user to determine order and friendly name for each map
longestMapLength = len(max(allExpressionMapsNames, key=len)) + 1
mapConfig = open('map-config.csv', 'w')
mapConfig.write('ExpressionMapName' + (' ' * max(0, longestMapLength - len('ExpressionMapName'))) + (', Name (needs user input), Order (needs user input, count starting with 1)\n'))
for mapName in allExpressionMapsNames:
    mapConfig.write(mapName + (' ' * max(0, longestMapLength - len(mapName))) + ',  ,\n')

# create articulations.csv by sorting the frequency of all the unique articulations we have parsed
longestArticulationLength = len(max(allArticulations.keys(), key=len)) + 1
articulationsConfig = open('articulations.csv', 'w')
articulationsConfig.write('Articulation' + (' ' * max(0, longestArticulationLength - len('Articulation'))) + ', UI Button Location (needs user input), Frequency\n')
for art in sorted(allArticulations.items(), key=lambda item: item[1], reverse=True):
    articulationsConfig.write(art[0] + (' ' * max(0, longestArticulationLength - len(art[0]))) + ',  ,' + str(art[1]) + '\n')

# generate list of all articulations by instrument
longestInstrumentLength = len(max(articulationsByMap.keys(), key=len)) + 1
allMapsAnArts = open('all-expression-maps-and-articulations.csv', 'w')
allMapsAnArts.write('ExpressionMapName' + (' ' * max(0, longestInstrumentLength - len('ExpressionMapName'))) + ', Articulation' + (' ' * max(0, longestArticulationLength - len('Articulation'))) + ', Keyswitch, UACC\n')
for instrument in articulationsByMap.keys():
    for articulation, keyswitch, uacc in articulationsByMap[instrument]:
        allMapsAnArts.write(instrument + (' ' * max(0, longestInstrumentLength - len(instrument))) + ',' + articulation +  (' ' * max(0, longestArticulationLength - len(articulation))) + ' ,' + keyswitch + ' ,' + uacc + '\n')