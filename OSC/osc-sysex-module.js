const fs = nativeRequire('fs');
const xmljs = nativeRequire('xml-js');

var clients = []
var expressionMapsDirectory = 'E:/Projects/Cubase Projects/Expression Maps/SSO Template'
var mapFiles = []

midiPort_MCU_To_OSC = 'MCUtoOSC'
midiPort_MCU_From_OSC = 'MCUfromOSC'

// define the variables used by the track name extraction function
var trackName = ""
var pos = 72
var rootPosLCD = 72
var keepStringVal = 0
var trackNameJoined = ""
var bufferTrackName = ""
var posBuffer = 72

var expressionMapName = "" // current expression map that we are parsing
var allArticulations = {}
var defaultArticulations = [[0, 'C-2'],[1, 'C#-2'],[2, 'D-2'],[3, 'D#-2'],[4, 'E-2'],[5, 'F-2'],[6, 'F#-2'],[7, 'G-2'],[8, 'G#-2'],[9, 'A-2'],[10, 'A#-2'],[11, 'B-2'],[12, 'C-1'],[13, 'C#-1'],[14, 'D-1'],[15, 'D#-1'],[16, 'E-1'],[17, 'F-1'],[18, 'F#-1'],[19, 'G-1']] // if none defined

app.on('open', (data, client) => {
    console.log("Client connected...")
    if (!clients.includes(client.id)) clients.push(client.id)

    receive('/SET', 'library_setup_script', 0)
})

app.on('close', (data, client)=>{
    if (clients.includes(client.id)) clients.splice(clients.indexOf(client.id))
})

send('midi', midiPort_MCU_From_OSC, '/note', 1, 44, 127);

module.exports = {

    init: function(){
        // this will be executed once when the osc server starts
    },

    oscInFilter:function(data){

        // Filter incoming osc messages
        var {address, args, host, port} = data

        var inArgs = args.map(x => x.value),
            outArgs = [],
            action = ''

        if (address === '/sysex') {

            console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>sysex value received")
            let sysExVal = args[0].value

            // check to see if we have our expression map files enumerated, if not then enumerate them
            if (mapFiles.length === 0) {
                // parse the expression maps folder
                getExpressionMapFiles(expressionMapsDirectory, mapFiles)
                console.log(mapFiles)
            }
            // check to see if articulations are loaded, if not then load them
            if (Object.keys(allArticulations).length === 0) {
                // parse the expression maps folder
                parseExpressionMaps()
            }

            //Use the function getTrackName to do all the cool stuff to get the fullTrackName
            let fullTrackName = getTrackName(sysExVal)

            console.log('Received track name ' + fullTrackName)
            receive('/SET', 'setup_instrument', fullTrackName)
            if (typeof allArticulations[fullTrackName] !== 'undefined') {
                receive('/SET', 'setup_articulations_script', JSON.stringify(allArticulations[fullTrackName]))
            } else {
                receive('/SET', 'setup_articulations_script', JSON.stringify(defaultArticulations))
            }

        }
        return {address, args, host, port}

    },

    oscOutFilter:function(data){
        // Filter outgoing osc messages
        var {address, args, host, port, clientId} = data
        // console.log("address: " + address + " host: " + host + " port: " + port)

        // same as oscInFilter
        if (address == '/resetMCU') {

            console.log('MCU Reset message sent')
            send('midi', midiPort_MCU_From_OSC, '/note', 1, 44, 127);  //Send MCU command to swicth to track name sending

        }

        // return data if you want the message to be and sent
        return {address, args, host, port}
    },

    unload: function(){
        // this will be executed when the custom module is reloaded
    },
}

function getTrackName(sysExVal) {

    var nameDone = false

    var d = sysExVal.split(" ").slice(6).map(x => parseInt(x, 16)) // slices off the front 6 elements, x => parseInt(x, 16) converts the rest from Hex to Int then .map creates the array d[]

    pos = d[0] // first byte -> position // hex to int

    text = d.slice(1).map(x => String.fromCharCode(x)) // these are the new characters which are updated on the console, the rest -> updated characters
    if (pos < 29) {
        return trackNameJoined
    }

    text.pop() // drop sysex closing byte
    trackName = text.join('')

    // MCU only sends what it needs so you need to buffer the previous name and use parts of that
    // Check the length of the new name vs the buffer
    nameLengthCheck = bufferTrackName.length - trackName.length

    // MCU sends some sysex data to tell the screen where to start showing the new characters
    // This is related to the root position on the screen which is 72

    // Check if root position matches the position where the characters are to be placed
    charFromStart = pos - rootPosLCD

    var lengthCheck = charFromStart + trackName.length

    if (lengthCheck < 29) {

        let newEndLength = 29 - charFromStart - trackName.length

        newEnd = bufferTrackName.substring(bufferTrackName.length - newEndLength)

    } else { newEnd = "" }

    if (pos == 72) {       // Full length name received

        trackNameJoined = trackName + newEnd
        bufferTrackName = trackNameJoined
        posBuffer = pos

        nameDone = true

    } else if (pos > posBuffer && posBuffer == 72 && nameDone == false) {

        keepStringVal = pos - posBuffer  // new name follows a full string text

        var prevTrackKeep = bufferTrackName.substring(0, keepStringVal)

        trackNameJoined = prevTrackKeep + trackName + newEnd
        bufferTrackName = trackNameJoined
        posBuffer = pos
        nameDone = true
    } else {
        keepStringVal = pos - rootPosLCD  // new name follows a full string text

        var prevTrackKeep = bufferTrackName.substring(0, keepStringVal)

        trackNameJoined = prevTrackKeep + trackName + newEnd
        bufferTrackName = trackNameJoined
        posBuffer = pos
        nameDone = true
    }


    // MCU will sometimes send the characters (MIDI) as part of the track name
    // so you need to strip these out
    const findMidiTag = '(';

    var posMidiTag = trackNameJoined.search("\\(M");
    var posBrackTag = trackNameJoined.search("\\(");
    var trackNameJoinedTrim = ""


    if (posBrackTag == trackNameJoined.length - 1) {
        trackNameJoinedTrim = trackNameJoined.substring(0, (posBrackTag - 1))
        trackNameJoined = trackNameJoinedTrim
    }

    if (posMidiTag > -1) {

        trackNameJoinedTrim = trackNameJoined.substring(0, (posMidiTag - 1))

        trackNameJoined = trackNameJoinedTrim

    }

    // trim off all the spaces at the end
    trackNameJoined = trackNameJoined.trimEnd();

    return trackNameJoined
}

async function parseExpressionMaps() {
    for (const mapFileName of mapFiles) {

        let mapFile =  mapFileName.split('\\').pop().split('/').pop().split('.')[0]
        const data = fs.readFileSync(mapFileName)
        var converted = xmljs.xml2js(data, {compact: false, spaces: 4})
        converted['elements'][0]['elements'].forEach(parseElements)
    }
}

function parseElements(item, index, arr) {

  var articulations = []
  if (item['attributes']['name'] === 'name') {
    expressionMapName = item['attributes']['value']
    console.log('Parsing articulations for ' + expressionMapName)
  }
  if (item['attributes']['name'] === 'slots') {
    articulations = parsePSoundSlots(item['elements'])
    console.log('articulations = ' + articulations)
    allArticulations[expressionMapName] = articulations
  }

}

function parsePSoundSlots(elements) {
  var articulations = []
  elements.forEach(element => {
    if (element['name'] === 'list') {
      // found the list of articulations
      element['elements'].forEach(e => {
        articulations.push(parseSlot(e))
      })
    }
  })
  return articulations.sort(compareNumbers)
}

function parseSlot(soundSlot) {
  var name = ""
  var keySwitch = ""
  soundSlot['elements'].forEach(element => {
    if (element['attributes']['name'] === 'name') {
      name = element['elements'][0]['attributes']['value']
    }
    if (element['attributes']['name'] === 'remote') {
      element['elements'].forEach(subElement => {
        if (subElement['attributes']['name'] === 'data1') {
          keySwitch = subElement['attributes']['value']
        }
      })
    }
  })
  return [keySwitch, name]
}

function compareNumbers(a, b) {
//  console.log('sorting a: ' + a + ' vs b: ' + b)
  return a[0] - b[0];
}

var getExpressionMapFiles = function(dir, files){
    fs.readdirSync(dir).forEach(function(file){
        var subpath = dir + '/' + file;
        if(fs.lstatSync(subpath).isDirectory()){
            getExpressionMapFiles(subpath, files);
        } else {
            if (file.indexOf('.expressionmap') != -1) {
                files.push(dir + '/' + file);
            }
        }
    });
}