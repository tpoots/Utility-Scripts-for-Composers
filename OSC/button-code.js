// -- show all button -- //
send("midi:ControlToCubase", "/control", 6, 99, 100)
// -- end show all button -- //

// -- hide all button -- //
send("midi:ControlToCubase", "/control", 7, 99, 100)
// -- end hide all button --//

// --- library selector buttons --- //
let libraryId = getVar(id, "libraryId")
var libraryConfig = JSON.parse(JSON.stringify(get("configuration")))[libraryId]
var cc = libraryConfig["midiCC"]
send("midi:ControlToCubase", "/control", 6, cc, 100)
// --- end library selector buttons --- //

// --- library hide buttons --- //
let libraryId = getVar(id, "libraryId")
var libraryConfig = JSON.parse(JSON.stringify(get("configuration")))[libraryId]
var cc = libraryConfig["midiCC"]
set("button_library_*", 0, {sync:false, send:false})
setVar("button_instr_*", "visible", 0)
setVar("art_*", "visible", 0)
send("midi:ControlToCubase", "/control", 7, cc, 100)
// --- end library hide buttons --- //

// --- articulation selector buttons --- //
set("art_*", 0, {sync:false, script: false, send:false})
var myId = getProp("this", "id")
if (get(myId) === 1) {
    let keyswitch = getVar(id, "keyswitch")
    if (typeof(keyswitch) !== "undefined") {
        console.log("Sending KS: " + keyswitch)
        send("midi:VirtualMidi", "/note", 1, keyswitch, 100) // sends note "on" to channel 1, note defined by the variable, and velocity = 100
        send("midi:VirtualMidi", "/note", 1, keyswitch, 0) // sends note "off" using velocity = 0
    }
} else {
}
// --- end articulation selector buttons --- //

// --- cc faders (onValue) --- //
var mic_level = Math.round(value)
var cc =  getVar("this", "cc")
console.log("Sending " + mic_level + " to CC " + cc)
send("midi:ControlToCubase", "/control", 1, cc, mic_level)
// --- end cc faders --- //

// --- cc max buttons --- //
var buttonIndex = id.substr(7,2)
set("cc_fader_" + buttonIndex, 127)
// --- end cc max buttons ---//

// --- cc min buttons --- //
var buttonIndex = id.substr(7,2)
set("cc_fader_" + buttonIndex, 0)
// --- end cc min buttons ---//

// --- setup the instrument --- //
var mapName = value
var libraryId = mapName.substr(0,3).toLowerCase()
var config = JSON.parse(JSON.stringify(get("configuration")))
var color = '#3366ff' // default color
if (typeof  config[libraryId] !== 'undefined') {
    // library-specific config exists so use those configuration values
    color = config[libraryId]['primaryColor']
}
// set the color of the articulation buttons to the library color
setVar('art_*', "color", color)

// set up the label and color of the articulation header
set("label_artics*", mapName, {sync:false, script: false, send:false})
setVar('label_artics', "color", color)

// set up CC faders
if (typeof config[libraryId] !== 'undefined' && typeof config[libraryId]['ccConfig'] !== 'undefined') {
    var ccConfig = config[libraryId]['ccConfig']
    // hide all CC UI elements
    setVar("cc_max_*", "visible", 0)
    setVar("cc_fader_*", "visible", 0)
    setVar("cc_min_*", "visible", 0)
    setVar("cc_only_*", "visible", 0)
    setVar("cc_id_*", "visible", 0)
    setVar("cc_label_*", "visible", 0)
    // show only those set up for the library
    for (let i = 1; i <= 20; i++) {
        if (typeof ccConfig[i] !== "undefined") {
            setVar("cc_fader_" + i, "cc", ccConfig[i].cc)
            setVar("cc_id_" + i, "name", "CC " + ccConfig[i].cc)
            setVar("cc_label_" + i, "name", ccConfig[i].name)
            // show CC UI element
             setVar("cc_max_" + i, "visible", 1)
             setVar("cc_fader_" + i, "visible", 1)
             setVar("cc_min_" + i, "visible", 1)
             setVar("cc_only_" + i, "visible", 1)
             setVar("cc_id_" + i, "visible", 1)
             setVar("cc_label_" + i, "visible", 1)
        }
    }
} else {
    console.log("setting up default CC faders")
    // show all CC UI elements
    setVar("cc_max_*", "visible", 1)
    setVar("cc_fader_*", "visible", 1)
    setVar("cc_min_*", "visible", 1)
    setVar("cc_only_*", "visible", 1)
    setVar("cc_id_*", "visible", 1)
    setVar("cc_label_*", "visible", 1)
    for (let i = 1; i<= 20; i++) {
        var cc = 20+i
        setVar("cc_fader_" + i, "cc", cc)
        setVar("cc_id_" + i, "name", "CC " + cc)
        setVar("cc_label_" + i, "name", "CC " + cc)
    }
}
// --- end setup the instrument --- //

// --- setup the articulations --- //
var artMap = JSON.parse(value)
setVar("art_*", "visible", 0)
set("art_*", 0, {sync:false, script: false, send:false})

var index = 1
for (var art in artMap) {
    var buttonId = "art_" + index
    setVar(buttonId, "label", artMap[art][1])
    setVar(buttonId, "enabled", 1)
    setVar(buttonId, "keyswitch", parseInt(artMap[art][0]))
    setVar(buttonId, "visible", 1)
    index += 1
}
// --- end setup the articulations --- //

// --- library setup script --- //
var config = JSON.parse(JSON.stringify(get("configuration")))
var index = 1
for (var id in config) {
    console.log(id)
    var libraryConfig = config[id]
    var buttonId = "button_library_" + index
    var hideButtonId = "hide_lib_" + index
    setVar(buttonId, "label", libraryConfig["name"])
    setVar(buttonId, "color", libraryConfig["primaryColor"])
    setVar(hideButtonId, "color", libraryConfig["primaryColor"])
    setVar(buttonId, "libraryId", id)
    setVar(hideButtonId, "libraryId", id)
    setVar(buttonId, "visible", 1)
    setVar(hideButtonId, "visible", 1)
    index += 1
}
for (var i = index; i <= 30; i++) {
    setVar('button_library_' + i, "visible", 0)
    setVar('hide_lib_' + i, "visible", 0)
}
for (let i = 1; i <= 60; i++) {
        setVar("art_" + i, "visible", 0)
}
// --- end library setup script --- //
