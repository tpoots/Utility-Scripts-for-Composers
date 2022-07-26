// --- library setup script --- //
var config = JSON.parse(JSON.stringify(get("configuration")))
for (var i in config) {
    console.log(i)
    var libraryConfig = config[i]
    var libraryId = libraryConfig["id"]
    var buttonId = "button_library_" + i
    var hideButtonId = "hide_lib_" + i
    setVar(buttonId, "label", libraryConfig["name"])
    setVar(buttonId, "color", libraryConfig["primaryColor"])
    setVar(hideButtonId, "color", libraryConfig["primaryColor"])
}
// clear the buttons and articulation panels since nothing is selected yet
for (let i = 1; i <= 25; i++) {
    setVar("button_instr_" + i, "visible", 0)
}
for (let i = 1; i <= 60; i++) {
        setVar("art_" + i, "visible", 0)
}
// --- end library setup script --- //

// -- show all button -- //
send("midi:ControlToCubase", "/control", 6, 99, 100)
// -- end show all button -- //

// -- hide all button -- //
send("midi:ControlToCubase", "/control", 7, 99, 100)
// -- end hide all button --//

// --- library selector buttons --- //
var libraryId = id.substr(15,2)
set('library_selector_script', libraryId)
var libraryConfig = JSON.parse(JSON.stringify(get("configuration")))[libraryId]
var cc = libraryConfig["midiCC"]
send("midi:ControlToCubase", "/control", 6, cc, 100)
// --- end library selector buttons --- //

// --- library hide buttons --- //
var libraryId = id.substr(9,2)
var libraryConfig = JSON.parse(JSON.stringify(get("configuration")))[libraryId]
var cc = libraryConfig["midiCC"]
set("button_instr_*", 0, {sync:false, send:false})
set("button_library_*", 0, {sync:false, send:false})
setVar("button_instr_*", "visible", 0)
setVar("art_*", "visible", 0)
send("midi:ControlToCubase", "/control", 7, cc, 100)
// --- end library hide buttons --- //

// --- library selector script --- //
var libraryId = value
var libraryConfig = JSON.parse(JSON.stringify(get("configuration")))[libraryId]
var instruments = libraryConfig["instruments"]
var articulations = libraryConfig["articulations"]
var primaryColor = libraryConfig["primaryColor"]
var articulationConfig = libraryConfig["articulationConfig"]
console.log("libraryId = " + value)
set("button_instr_*", 0, {sync:false, script: false, send:false})
set("selectedLibrary", libraryId)
set("button_library_*", 0, {sync:false, script: false, send:false})
//setVar("button_instr_*", "visible", 1)
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
// set default selected articulation to first slot
// set("art_1", 1, {sync:true, send:true})
// --- end library selector script --- //


// --- instrument selector buttons --- //
set("button_instr_*", 0, {sync:false, script: false, send:false})
var buttonIndex = id.substr(13,2)-1
var library = get("selectedLibrary")
var libraryConfig = JSON.parse(JSON.stringify(get("configuration")))[library]
var primaryColor = libraryConfig["primaryColor"]
var articulations = libraryConfig["instruments"][buttonIndex]["articulations"]
var articulationConfig = libraryConfig["articulationConfig"]
if (get(id) === 1) {
    // instrument button is selected
    if (articulationConfig == "perInstrument") {
        // clear all articulation buttons first
        for (let i = 1; i <= 60; i++) {
            setVar("art_" + i, "visible", 0)
        }
        var index = 1
        for (var art in articulations) {
            var buttonId = "art_" + index
            setVar(buttonId, "label", art)
            setVar(buttonId, "color", primaryColor)
            setVar(buttonId, "enabled", 1)
            setVar(buttonId, "keyswitch", articulations[art]["keySwitch"])
            setVar(buttonId, "visible", 1)
            index += 1
         }
    } else {
        set("art_*", 0, {sync:false, script: false, send:false}) // deselect all articulation buttons
        for (let i = 1; i <= 60; i++) {
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
    // instrument button is un-selected
    if (articulationConfig == "perInstrument") {
        for (let i = 1; i <= 60; i++) {
            setVar("art_" + i, "visible", 0)
        }
    } else {
        set("art_*", 0, {sync:false, send:false}) // deselect all visible articulation buttons
        for (let i = 1; i <= 60; i++) {
            var buttonId = "art_" + i
            setVar(buttonId, "color", "#C0C0C0")
            setVar(buttonId, "enabled", 0)
            setVar(buttonId, "keyswitch", 0)
        }
    }
}
// --- end instrument selector buttons --- //


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