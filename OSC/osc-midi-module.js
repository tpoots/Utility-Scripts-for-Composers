app.on('open', (data, client) => {
    console.log("Client connected...")
    receive('/SET', 'section_setup_script', 0)
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
            var channel = args[0].value
            var note = args[1].value
            var pressure = args[2].value
            var buttonId = "button_instr_" + note
            // use channel information to select the correct instruments
            receive('/SET', 'section_selector_script', channel)
            // select the button corresponding to the section
            receive('/SET', buttonId, 1)
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