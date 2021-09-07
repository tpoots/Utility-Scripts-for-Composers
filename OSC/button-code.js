var sectionName = id.substr(15,3)
set('section_selector_script', sectionName)
var sectionConfig = JSON.parse(JSON.stringify(get("configuration")))[sectionName]
var cc = sectionConfig["midiCC"]
send("midi:ControlToCubase", "/control", 6, cc, 100)

// --- section selector script --- //
console.log('value = ' + value)
console.log(get(id))
var sectionName = value
var sectionConfig = JSON.parse(JSON.stringify(get("configuration")))[sectionName]
var instruments = sectionConfig["instruments"]
var articulations = sectionConfig["articulations"]
var primaryColor = sectionConfig["primaryColor"]
set("button_instr_*", 0, {sync:false, send:false})
set("selectedSection", sectionName)
set("button_section_*", 0, {sync:false, send:false})
setVar("button_instr_*", "visible", 1)
// set up articulation selector buttons
for (let i = 1; i <= 60; i++) {
    if (typeof articulations[i] !== "undefined") {
        setVar("art_" + i, "visible", 1)
        setVar("art_" + i, "color", "#C0C0C0")
        setVar("art_" + i, "label", articulations[i])
        setVar("art_" + i, "enabled", 0)
    } else {
        setVar("art_" + i, "visible", 0)
    }
}
// set up instrument selector buttons
for (let i = 1; i <= 19; i++) {
    if (typeof instruments[i-1] !== "undefined") {
        setVar("button_instr_" + i, "visible", 1)
        setVar("button_instr_" + i, "color", primaryColor)
        setVar("button_instr_" + i, "label", instruments[i-1]["name"])
    } else {
        setVar("button_instr_" + i, "visible", 0)
    }
}

// --- instrument selector buttons --- //
set("button_instr_*", 0, {sync:false, send:false})
var buttonIndex = id.substr(13,2)-1
var myInstrumentName = getProp("this", "label")
var section = get("selectedSection")
var sectionConfig = JSON.parse(JSON.stringify(get("configuration")))[section]
var secondaryColor = sectionConfig["secondaryColor"]
var articulations = sectionConfig["instruments"][buttonIndex]["articulations"]
if (get(id) === 1) {
    set("art_*", 0, {sync:false, send:false}) // deselect all articulation buttons
    for (let i = 0; i < 60; i++) {
    var buttonId = "art_" + i
    var buttonLabel = getVar(buttonId, "label")
    if (typeof articulations[buttonLabel] !== "undefined") {
        var keyswitch = articulations[buttonLabel]["keySwitch"]
        setVar(buttonId, "color", secondaryColor)
        setVar(buttonId, "enabled", 1)
        setVar(buttonId, "keyswitch", keyswitch)
    } else {
        setVar(buttonId, "color", "#C0C0C0")
        setVar(buttonId, "enabled", 0)
        setVar(buttonId, "keyswitch", 0)
    }
}
} else {
    set("art_*", 0, {sync:false, send:false}) // deselect all articulation buttons
    for (let i = 0; i < 60; i++) {
        var buttonId = "art_" + i
        setVar(buttonId, "color", "#C0C0C0")
        setVar(buttonId, "enabled", 0)
        setVar(buttonId, "keyswitch", 0)
    }
}

// --- articulation selector buttons --- //
set("art_*", 0, {sync:false, send:false})
if (get(id) === 1) {
    let keyswitch = getVar(id, "keyswitch")
    console.log("Sending " + keyswitch)
    send("midi:VirtualMidi", "/note", 1, keyswitch, 100) // sends note "on" to channel 1, note defined by the variable, and velocity = 100
    send("midi:VirtualMidi", "/note", 1, keyswitch, 0) // sends note "off" using velocity = 0
} else {
}

// --- scratchpad --- //
send("midi:VirtualMidi", "/note", 1, 50, 100)
send("midi:VirtualMidi", "/note", 1, 50, 0)
