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
            if (channel == 1) {
                // woodwinds section
                receive('/SET', 'section_selector_script', 'ssw')
            } else if (channel == 2) {
                // brass section
                receive('/SET', 'section_selector_script', 'ssb')
            } else if (channel == 3) {
                // symphonic strings section
                receive('/SET', 'section_selector_script', 'sss')
            } else if (channel == 4) {
                // chamber strings section
                receive('/SET', 'section_selector_script', 'scs')
            } else if (channel == 5) {
                // solo strings section
                receive('/SET', 'section_selector_script', 'sst')
            }
            receive('/SET', buttonId, 1)
            return
        }

        return {address, args, host, port}

    },

    oscOutFilter:function(data){
        // Filter outgoing osc messages
        console.log("detected outgoing osc message")

        var {address, args, host, port, clientId} = data
        console.log("address: " + address + " host: " + host + " port: " + port)

        // same as oscInFilter

        // return data if you want the message to be and sent
        return {address, args, host, port}
    },

    unload: function(){
        // this will be executed when the custom module is reloaded
    },

}