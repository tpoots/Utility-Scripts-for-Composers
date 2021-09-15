import os
import json
import platform
import re
import sys
import xml.etree.ElementTree as ET
from os import walk

# useful html color lookup https://htmlcolorcodes.com/

# sample expression map configurations:
# -----------------------------------------------------------------------------

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
# -----------------------------------------------------------------------------

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
# artButtonConfig = {
#    1: "Long",
#    2: "Long Cuivre",
#    3: "Long Stopped",
#    4: "Long Muted",
#    5: "Long Mariachi",
#    6: "Tremolo",
#    7: "Long Bells Up",
#    11: "Staccato",
#    12: "Marcato",
#    13: "Tenuto",
#    14: "Multitongue",
#    15: "Staccato Muted",
#    16: "Marcato Muted",
#    17: "Tenuto Muted",
#    18: "Staccatissimo",
#    19: "Marcato Bells Up",
#    20: "Staccatissimo Bells Up",
#    21: "Staccato Bells Up",
#    22: "Tenuto Bells Up",
#    23: "Short Muted",
#    31: "Legato",
#    41: "FX Fall",
#    42: "FX Rip",
#    43: "FX Flutter",
#    44: "Trill HT",
#    45: "Trill WT",
#    46: "FX Glissandi",
#    47: "FX Fanfare",
# }
# -----------------------------------------------------------------------------

# SSS
# artMapConfig = {
#     'SFSS Violins 1 CB D.expressionmap': {'name': 'Violins 1', 'order': 0},
#     'SFSS Violins 2 CB D.expressionmap': {'name': 'Violins 2', 'order': 1},
#     'SFSS Violas CB D.expressionmap': {'name': 'Violas', 'order': 2},
#     'SFSS Celli CB D.expressionmap': {'name': 'Celli', 'order': 3},
#     'SFSS Basses CB D.expressionmap': {'name': 'Basses', 'order': 4},
#     'SFSS Ensembles CB D.expressionmap': {'name': 'Ensembles', 'order': 5},
# }
# artButtonConfig = {
#    1: "Long",
#    2: "Long Sul Pont",
#    3: "Long Super Sul Tasto",
#    4: "Long CS",
#    5: "Long CS Blend",
#    6: "Long Flautando",
#    7: "Long CS Sul Pont",
#    8: "Long Rachm",
#    9: "Long Sul G",
#    10: "Long Sul Tasto",
#    11: "Harmonics",
#    12: "Flautando",
#    13: "Tremolo",
#    14: "Tremolo 150",
#    15: "Tremolo 150 CS",
#    16: "Tremolo 180",
#    17: "Tremolo Muted",
#    18: "Tremolo CS",
#    19: "Tremolo Sul Pont",
#    21: "Marcato",
#    22: "Pizzicato",
#    23: "Spiccato",
#    24: "Col Legno",
#    25: "Pizzicato Bartok",
#    26: "Short Brushed CS",
#    27: "Short Harmonics",
#    28: "Short Brushed",
#    29: "Short CS",
#    30: "Staccato Dig",
#    31: "Short Harmonic",
#    32: "Short Muted",
#    33: "Short Soft",
#    34: "Tenuto [0.5]",
#    35: "Marcato [1.0]",
#    41: "Legato",
#    42: "Legato Sul G",
#    43: "Legato Sul C",
#    44: "Legato Runs",
#    51: "Trill HT",
#    52: "Trill WT",
#    53: "FX",
#    54: "Trill Min3",
#    55: "Trill Maj3"
# }
# -----------------------------------------------------------------------------

# SCS
# artMapConfig = {
#     'SFCS Violins 1 CB D.expressionmap': {'name': 'Violins 1', 'order': 0},
#     'SFCS Violins 2 CB D.expressionmap': {'name': 'Violins 2', 'order': 1},
#     'SFCS Violas CB D.expressionmap': {'name': 'Violas', 'order': 2},
#     'SFCS Celli CB D.expressionmap': {'name': 'Celli', 'order': 3},
#     'SFCS Basses CB D.expressionmap': {'name': 'Basses', 'order': 4},
#     'SFCS Ensembles CB D.expressionmap': {'name': 'Ensembles', 'order': 5},
# }

# artButtonConfig = {
#    1: 'Long',
#    2: 'Long Flautando',
#    3: 'Long Sul Pont',
#    4: 'Long CS',
#    5: 'Long CS Sul Pont',
#    6: 'Long Sul Pont Dist',
#    7: 'Long Sul Tasto',
#    8: 'Long Sul G',
#    9: 'Long Sul C',
#    10: 'Harmonics',
#    11: 'Tremolo',
#    12: 'Tremolo 150Bpm',
#    13: 'Tremolo 180Bpm',
#    14: 'Tremolo CS',
#    15: 'Tremolo Sul Pont',
#    16: 'Tremolo CS Sul Pont',
#    21: 'Staccato',
#    22: 'Spiccato',
#    23: 'Marcato',
#    24: 'Pizzicato',
#    25: 'Pizzicato Bartok',
#    26: 'Col Legno',
#    27: 'Short CS',
#    28: 'Staccato Dig',
#    29: 'Spiccato Feathered',
#    31: 'Legato',
#    32: 'Legato CS',
#    33: 'Legato Fast',
#    34: 'Legato Flautando',
#    35: 'Legato Portamento',
#    36: 'Legato Sul Pont',
#    37: 'Legato Tremolo',
#    38: 'Legato Runs',
#    39: 'Legato Bowed',
#    40: 'Legato Sul G',
#    41: 'Legato Sul C',
#    42: 'Legato CS Port',
#    43: 'Legato Flautando Port',
#    51: 'Trill HT',
#    52: 'Trill WT',
#    53: 'Trill Min3',
#    54: 'Trill Perf4',
#    55: 'FX',
#    56: 'FX Run',
#    57: 'FX Slides',
#    58: 'FX Tense Longer',
#    59: 'FX Disco Fall',
#    60: 'FX Disco Upwards'
# }
# -----------------------------------------------------------------------------

# Solo Strings
# artMapConfig = {
#     'SFSOS Violin (Virtuoso) CB D.expressionmap': {'name': 'Violin (Virtuoso)', 'order': 0},
#     'SFSOS Violin (1st Desk) CB D.expressionmap': {'name': 'Violin (1st Desk)', 'order': 1},
#     'SFSOS Violin (Progressive) CB D.expressionmap': {'name': 'Violin (Progressive)', 'order': 2},
#     'SFSOS Viola CB D.expressionmap': {'name': 'Viola', 'order': 3},
#     'SFSOS Cello CB D.expressionmap': {'name': 'Cello', 'order': 4},
#     'SFSOS Bass CB D.expressionmap': {'name': 'Bass', 'order': 5}
# }
#
# artButtonConfig = {
#     1: 'Long',
#     2: 'Long Flautando',
#     3: 'Long Sul Pont',
#     4: 'Long CS',
#     5: 'Long Super Sul Tasto',
#     6: 'Harmonics',
#     7: 'Tremolo',
#     11: 'Spiccato',
#     12: 'Staccato',
#     13: 'Pizzicato',
#     14: 'Pizzicato Bartok',
#     15: 'Col Legno',
#     16: 'Short Brushed Baroque CS',
#     17: 'Spiccato Brushed CS',
#     18: 'Spiccato Brushed Baroque',
#     21: 'Legato',
#     31: 'Trill HT',
#     32: 'Trill WT',
# }
# -----------------------------------------------------------------------------

# Albion Solstice
# artMapConfig = {
#     'SFA7 b - The Elders Strings Traditional Sextet CB Direction - No Mtr.expressionmap': {'name': 'Elders Trad Sextet', 'order': 0},
#     'SFA7 b - The Elders Strings Traditional Sextet Motors CB Direction.expressionmap': {'name': 'Elders Trad Motors', 'order': 1},
#     'SFA7 a - The Elders Strings Classic Octet CB Direction - No Motors.expressionmap': {'name': 'Elders Classic Octet', 'order': 2},
#     'SFA7 a - The Elders Strings Classic Octet Motors CB Direction.expressionmap': {'name': 'Elders Classic Motors', 'order': 3},
#     'SFA7 c - The Elders Strings Bass D.expressionmap': {'name': 'Elders Bass', 'order': 4},
#     'SFA7 The Callers Brass+Winds CB D - No Motors.expressionmap': {'name': 'Callers Brass & Winds', 'order': 5},
#     'SFA7 The Callers Brass+Winds Motors CB D.expressionmap': {'name': 'Callers B&W Motors', 'order': 6},
#     'SFA7 The Mystics Pipes D.expressionmap': {'name': 'Mystics Pipes', 'order': 7},
#     'SFA7 a - BLAG  - Main Techniques D.expressionmap': {'name': 'Blaggards', 'order': 8},
#     'SFA7 e - BLAG - Bellows D.expressionmap': {'name': 'Blaggards Bellows', 'order': 9},
#     'SFA7 d - BLAG - Bellows+Strings D.expressionmap': {'name': 'Blaggards Bellows & Strings', 'order': 10},
#     'SFA7 b - BLAG  - Drones D ~.expressionmap': {'name': 'Blaggards Drones', 'order': 11},
#     'SFA7 c - BLAG  - Drones Hurdy Gurdy D ~.expressionmap': {'name': 'Blaggards Hurdy Gurdy Drones', 'order': 12},
#     'SFA7 f - BLAG - Plucked D.expressionmap': {'name': 'Blaggards Plucked', 'order': 13},
#     'SFA7 a - HOST - Main Techniques D ~.expressionmap': {'name': 'Hosts', 'order': 14},
#     'SFA7 b - HOST - Motors+Effects D ~.expressionmap': {'name': 'Hosts Motors & FX', 'order': 15},
#     'SFA7 a - Generator Trio CB D.expressionmap': {'name': 'Generator Trio', 'order': 16},
#     'SFA7 a - Generator Trio Motors CB D.expressionmap': {'name': 'Generator Trio Motors', 'order': 17},
#     'SFA7 a - GUT - Main Techniques D ~ -SL.expressionmap': {'name': 'Gut Circle', 'order': 18},
#     'SFA7 b - GUT - Motors D ~.expressionmap': {'name': 'Gut Circle Motors', 'order': 19},
#     'SFA7 a - NURS - Main techniques D.expressionmap': {'name': 'Nursery', 'order': 20},
#     'SFA7 b- NURS - Motors D ~.expressionmap': {'name': 'Nursery Motors', 'order': 21}
# }
# -----------------------------------------------------------------------------

# Albion One
# artMapConfig = {
#     'SFA1 Wood High CB D.expressionmap': {'name': 'Woods High', 'order': 0},
#     'SFA1 Wood Low CB D.expressionmap': {'name': 'Woods Low', 'order': 1},
#     'SFA1 Brass High CB D.expressionmap': {'name': 'Brass High', 'order': 2},
#     'SFA1 Brass Mid CB D.expressionmap': {'name': 'Brass Mid', 'order': 3},
#     'SFA1 Brass Low CB D.expressionmap': {'name': 'Brass Low', 'order': 4},
#     'SFA1 Strings CB D.expressionmap': {'name': 'Strings', 'order': 5},
#     'SFA1 Strings CS legato D.expressionmap': {'name': 'Strings CS Legato', 'order': 6},
#     'SFA1 Strings High Runs D ~.expressionmap': {'name': 'Strings High Runs', 'order': 7},
#     'SFA1 Strings Low Runs D ~.expressionmap': {'name': 'Strings Low Runs', 'order': 8}
# }
# -----------------------------------------------------------------------------

# Abbey Road Orchestral Foundations
# artMapConfig = {
#     'SFARF High Woods D.expressionmap': {'name': 'High Woods', 'order': 0},
#     'SFARF Low Woods D.expressionmap': {'name': 'Low Woods', 'order': 1},
#     'SFARF Horns D.expressionmap': {'name': 'Horns', 'order': 2},
#     'SFARF Trumpets D.expressionmap': {'name': 'Trumpets', 'order': 3},
#     'SFARF Low Brass D.expressionmap': {'name': 'Low Brass', 'order': 4},
#     'SFARF High Strings D.expressionmap': {'name': 'High Strings', 'order': 5},
#     'SFARF Low Strings D.expressionmap': {'name': 'Low Strings', 'order': 6},
#     'SFARF Orchestra D.expressionmap': {'name': 'Orchestra', 'order': 7}
# }
#
# artButtonConfig = {
#     1: 'Long',
#     2: 'Long CS',
#     3: 'Tremolo',
#     11: 'Marcato',
#     12: 'Staccato',
#     13: 'Staccatissimo',
#     14: 'Spiccato',
#     15: 'Tenuto',
#     21: 'Swell Shorter',
#     22: 'Swell Med',
#     23: 'Swell Longer'
# }
# -----------------------------------------------------------------------------

# Eric Whitacre Choir
artMapConfig = {
    'SFEWC Soprano All In One D ~.expressionmap': {'name': 'Sopranos', 'order': 0},
    'SFEWC Alto All In One D ~.expressionmap': {'name': 'Altos', 'order': 1},
    'SFEWC Tenor All In One D ~.expressionmap': {'name': 'Tenors', 'order': 2},
    'SFEWC Bass All In One D ~.expressionmap': {'name': 'Basses', 'order': 3},
    'SFEWC Tutti All In One D ~.expressionmap': {'name': 'Tutti', 'order': 4},

    'SFEWC Tutti All Evolutions Simple D ~.expressionmap': {'name': 'Tutti Evos Simple', 'order': 5},
    'SFEWC Tutti All Evolutions Rhythmic D ~.expressionmap': {'name': 'Tutti Evos Rhythmic', 'order': 6},
    'SFEWC Tutti All Evolutions Clashes D ~.expressionmap': {'name': 'Tutti Evos Clashes', 'order': 7},
    'SFEWC Tutti All Evolutions Dynamic D ~.expressionmap': {'name': 'Tutti Evos Dynamic', 'order': 8},
    'SFEWC Tutti All Evolutions Special D ~.expressionmap': {'name': 'Tutti Evos Special', 'order': 9}

}

# -----------------------------------------------------------------------------

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