var clients = []
var libraryPositionMap = {
1: 1, // ssw
2: 2, // ssb
3: 3, // sss
4: 4, // scs
5: 5, // sst
6: 27, // bbcso woods
7: 28, // bbcso brass
8: 29, // bbcso strings
9: 30, // bbcso perc
10: 8, // sa1
11: 9, // sa7
12: 7, // ar1
13: 22, // ewc
14: 6, // sas
15: 26, // bht
16: 23, // sa4 winds
17: 24, // sa4 brass
18: 25, // sa4 strings
19: 10, // sos
20: 11, // sps
21: 12, // oace
22: 13, // bdt
23: 14, // cdt
24: 24, //
25: 25, //
26: 26, //
27: 27, //
28: 28, //
29: 29, //
30: 30  //
}

app.on('open', (data, client) => {
    console.log("Client connected...")
    receive('/SET', 'library_setup_script', 0)
    if (!clients.includes(client.id)) clients.push(client.id)
})

app.on('close', (data, client)=>{
    if (clients.includes(client.id)) clients.splice(clients.indexOf(client.id))
})

module.exports = {

    init: function(){
        // this will be executed once when the osc server starts
    },

    oscInFilter:function(data){

        // Filter incoming osc messages
        var {address, args, host, port} = data

        // return a C-2 poly pressure message if receiving a track select (CC 126 on channel 7)
        if (port == 'ControlToOSC' && address == '/control' && args[0].value == 7 && args[1].value == 126 && args[2].value === 100) {
            send("midi", "VirtualMidi", '/key_pressure', 7, 0, 127)
            return
        }

        if (port == 'ControlToOSC' && address == '/key_pressure') {
            // MIDI track selected in Cubase
            var channel = args[0].value
            var note = args[1].value
            var pressure = args[2].value
            var buttonId = "button_instr_" + note
            // use channel information to select the correct instruments
            console.log("about to set library_selector_script")
            libraryPosition = libraryPositionMap[channel]
            receive('/SET', 'library_selector_script', libraryPosition)
            // select the button corresponding to the library
            console.log("about to (pre)set button " + buttonId)
            receive('/SET', buttonId, 1)
            return
        } else if (port == 'ControlToOSC' && address == '/control' && args[0].value == 8 && args[1].value == 127 && args[2].value != 0) {
            // Instrument track selected in Cubase - set corresponding library
            var library = args[2].value
            console.log("Library value = " + library)
            console.log("about to set library_selector_script")
            libraryPosition = libraryPositionMap[library]
            receive('/SET', 'library_selector_script', libraryPosition)
            return
        } else if (port == 'ControlToOSC' && address == '/control' && args[0].value == 9 && args[1].value == 127 && args[2].value != 0) {
            // Instrument track selected in Cubase - set corresponding instrument
            var instrument = args[2].value
            var buttonId = "button_instr_" + instrument
            console.log("about to set button " + buttonId)
            receive('/SET', buttonId, 1)
            receive('/SET', "art_1", 1)
            return
        }

        return {address, args, host, port}

    },

    oscOutFilter:function(data){
        // Filter outgoing osc messages
        var {address, args, host, port, clientId} = data
        // console.log("address: " + address + " host: " + host + " port: " + port)

        // same as oscInFilter

        // return data if you want the message to be and sent
        return {address, args, host, port}
    },

    unload: function(){
        // this will be executed when the custom module is reloaded
    },

}