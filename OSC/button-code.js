// --- section setup script --- //
var config = JSON.parse(JSON.stringify(get("configuration")))
console.log(config)
for (let i = 1; i <= 6; i++) {
    var sectionConfig = config[i]
    var sectionId = sectionConfig["id"]
    var buttonId = "button_section_" + i
    setVar(buttonId, "label", sectionConfig["name"])
    setVar(buttonId, "color", sectionConfig["primaryColor"])
}
// clear the buttons and articulation sections since nothing is selected yet
for (let i = 1; i <= 25; i++) {
    setVar("button_instr_" + i, "visible", 0)
}
for (let i = 1; i <= 60; i++) {
        setVar("art_" + i, "visible", 0)
}
// --- end section setup script --- //

// --- section selector buttons --- //
var sectionId = id.substr(15,1)
set('section_selector_script', sectionId)
var sectionConfig = JSON.parse(JSON.stringify(get("configuration")))[sectionId]
var cc = sectionConfig["midiCC"]
send("midi:ControlToCubase", "/control", 6, cc, 100)
// --- end section selector buttons --- //


// --- section selector script --- //
var sectionId = value
var sectionConfig = JSON.parse(JSON.stringify(get("configuration")))[sectionId]
var instruments = sectionConfig["instruments"]
var articulations = sectionConfig["articulations"]
var primaryColor = sectionConfig["primaryColor"]
var articulationConfig = sectionConfig["articulationConfig"]
set("button_instr_*", 0, {sync:false, send:false})
set("selectedSection", sectionId)
set("button_section_*", 0, {sync:false, send:false})
setVar("button_instr_*", "visible", 1)
if (articulationConfig == "perInstrument") {
    // set up articulation selector buttons only when the instrument is selected
    for (let i = 1; i <= 60; i++) {
        setVar("art_" + i, "visible", 0)
    }
} else {
    // set up articulation selector buttons using library-level articulation definitions
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
}
// set up instrument selector buttons
for (let i = 1; i <= 25; i++) {
    if (typeof instruments[i-1] !== "undefined") {
        setVar("button_instr_" + i, "visible", 1)
        setVar("button_instr_" + i, "color", primaryColor)
        setVar("button_instr_" + i, "label", instruments[i-1]["name"])
    } else {
        setVar("button_instr_" + i, "visible", 0)
    }
}
// --- end section selector script --- //


// --- instrument selector buttons --- //
set("button_instr_*", 0, {sync:false, send:false})
var buttonIndex = id.substr(13,2)-1
var myInstrumentName = getProp("this", "label")
var section = get("selectedSection")
var sectionConfig = JSON.parse(JSON.stringify(get("configuration")))[section]
var primaryColor = sectionConfig["primaryColor"]
var articulations = sectionConfig["instruments"][buttonIndex]["articulations"]
var articulationConfig = sectionConfig["articulationConfig"]
if (get(id) === 1) {
    if (articulationConfig == "perInstrument") {

    } else {
        set("art_*", 0, {sync:false, send:false}) // deselect all articulation buttons
        for (let i = 0; i < 60; i++) {
            var buttonId = "art_" + i
            var buttonLabel = getVar(buttonId, "label")
            if (typeof articulations[buttonLabel] !== "undefined") {
                var keyswitch = articulations[buttonLabel]["keySwitch"]
                setVar(buttonId, "color", primaryColor)
                setVar(buttonId, "enabled", 1)
                setVar(buttonId, "keyswitch", keyswitch)
            } else {
                setVar(buttonId, "color", "#C0C0C0")
                setVar(buttonId, "enabled", 0)
                setVar(buttonId, "keyswitch", 0)
            }
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
// --- end instrument selector buttons --- //


// --- articulation selector buttons --- //
set("art_*", 0, {sync:false, send:false})
if (get(id) === 1) {
    let keyswitch = getVar(id, "keyswitch")
    console.log("Sending " + keyswitch)
    send("midi:VirtualMidi", "/note", 1, keyswitch, 100) // sends note "on" to channel 1, note defined by the variable, and velocity = 100
    send("midi:VirtualMidi", "/note", 1, keyswitch, 0) // sends note "off" using velocity = 0
} else {
}
// --- end articulation selector buttons --- //


// --- scratchpad --- //
send("midi:VirtualMidi", "/note", 1, 50, 100)
send("midi:VirtualMidi", "/note", 1, 50, 0)
