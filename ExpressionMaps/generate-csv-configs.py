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
# expression maps and generates two CSV output files:
#
# 1. map-config.csv - a file listing every unique combination of expression
#    map and articulation, with keyswitch trigger and UACC value
#
# 2. articulations.csv - a file containing just the unique articulations present
#    in the expression maps, sorted by the frequency in which they occurred
#
# if the output files already exist THEY WILL BE OVERWRITTEN
#
# These files are useful for analyzing the contents of a set of Cubase Expression
# maps. However their main purpose is to be provided as input to the subsequent
# script (generate-osc-json-configuration.py) which takes the expression maps
# plus the user-provided map-config.csv and articulations.csv and generates the
# json configuration needed by the OSC cubase controller.
#
# -----------------------------------------------------------------------------

allExpressionMaps = []
allArticulations = {}

if len(sys.argv) != 2:
    print("Incorrect # of parameters provided")
    print("Usage:")
    print("python generate-csv-configs.py {directory-containing-expression-maps |individual-expression-map}")

expressionMapsPath = sys.argv[1]
if os.path.isdir(expressionMapsPath):
    for (dirpath, dirnames, filenames) in walk(expressionMapsPath):
        for file in filenames:
            allExpressionMaps.append(os.path.join(dirpath, file))
else:
    allExpressionMaps.append(expressionMapsPath)

mapConfig = open('map-config.csv', 'w')
mapConfig.write("Library Name (needs user input), ExpressionMapName, Articulation, Keyswitch, UACC\n")

articulationsConfig = open('articulations.csv', 'w')
articulationsConfig.write('UI Button Location (needs user input), Articulation, Frequency')

pathRegex = ""
if (platform.system() == 'Windows'):
    pathRegex = '.*\\\(.*)'
else:
    pathRegex = '.*\/(.*)'

for expressionMap in allExpressionMaps:
    print("Parsing " + expressionMap + "...")

    m = re.search(pathRegex, expressionMap)
    instrumentArtMapName = m.group(1)

    tree = ET.parse(expressionMap)
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

            mapConfig.write(' ,' + instrumentArtMapName + ',' + str(articulation) + ',' + str(keySwitch) + ',' + str(uacc) + '\n')

# create articulations.csv by sorting the frequency of all the unique articulations we have parsed
for art in sorted(allArticulations.items(), key=lambda item: item[1], reverse=True):
    articulationsConfig.write(' ,' + art[0] + ',' + str(art[1]) + '\n')