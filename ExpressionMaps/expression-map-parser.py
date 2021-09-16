import os
import json
import platform
import re
import sys
import xml.etree.ElementTree as ET
from os import walk

print("\nThis script is deprecated, use generate-csv-configs.py to create CSV dumps of expression maps, or generate-osc-json-config.py to create OSC json config")
exit(0)

allExpressionMaps = []
articulationMap = {}

expressionMapsPath = sys.argv[1]
csvFlag = False
if len(sys.argv) > 2:
    if sys.argv[2] == "--csv":
        csvFlag = True

if csvFlag:
    print("ExpressionMapName, Articulation, Keyswitch, UACC")

pathRegex = ""
if (platform.system() == 'Windows'):
    pathRegex = '.*\\\(.*)'
else:
    pathRegex = '.*\/(.*)'

for (dirpath, dirnames, filenames) in walk(expressionMapsPath):
    for file in filenames:
        allExpressionMaps.append(os.path.join(dirpath, file))

if "artButtonConfig" in globals():
    articulationMap = {"articulations": artButtonConfig}

articulationMap.update({"instruments": {}})

for expressionMap in allExpressionMaps:
    m = re.search(pathRegex, expressionMap)
    instrumentArtMapName = m.group(1)

    tree = ET.parse(expressionMap)
    root = tree.getroot()

    for articulationElement in root.findall(".//obj[@class='PSoundSlot']"): # find all PSoundSlot objects
        if articulationElement.get('class') == 'PSoundSlot': # found an articulation
            articulation = articulationElement.find(".//*[@name='s']").get('value').strip()
            # this is less general: articulation = articulationElement.find(".//*[@name='description']").get('value').strip()
            
            keySwitch = articulationElement.find(".//obj[@class='PSlotThruTrigger']/int[@name='data1']").get('value')
            uacc = 127
            if (articulationElement.find(".//obj[@class='PSlotMidiAction']/member[@name='midiMessages']//obj[@class='POutputEvent']/int[@name='data2']")  is not None):
                uacc = articulationElement.find(".//obj[@class='PSlotMidiAction']/member[@name='midiMessages']//obj[@class='POutputEvent']/int[@name='data2']").get('value')

            # --- CSV output ---
            if csvFlag:
                print(instrumentArtMapName + ',' + str(articulation) + ',' + str(keySwitch) + ',' + str(uacc))
            # --- CSV Output ---
            else:
                config = artMapConfig.get(instrumentArtMapName)
                instrumentIndex = config.get("order")
                instrumentName = config.get("name")
                if not instrumentIndex in articulationMap["instruments"].keys():
                    articulationMap["instruments"][instrumentIndex] = {}
                    articulationMap["instruments"][instrumentIndex].update({"name": instrumentName, "articulations": {}})
                    # update the list of all articulations as well so we have a full list for the library
                articulationMap["instruments"][instrumentIndex]["articulations"].update({articulation: {'keySwitch': keySwitch, 'UACC': uacc}})
                json_object = json.dumps(articulationMap, indent=4)
                print(json_object)