module.exports = {

    init: function(){
        // this will be executed once when the osc server starts
    },

    oscInFilter:function(data){

        // Filter incoming osc messages
        var {address, args, host, port} = data
        console.log("starting processing")
        console.log("host: " + host  + " port: " + port + " address: " + address + " args[0]: " + args[0].value + " args[1]: " + args[1].value + " args[2]: " + args[2].value)

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
            if (channel == 1) {
                // woodwinds section
                receive('/SET', 'section_selector_script', 'ssw')
            } else if (channel == 2) {
                // brass section
                receive('/SET', 'section_selector_script', 'ssb')
            }
            console.log("PP " + note + " on channel " + channel)
            receive('/SET', buttonId, 1)
            return
        }

        // if (address === '/control' && args[0].value === 7 && args[1].value === 126 && args[2].value === 100) {
        //    // received a track selector message so probe for instrument information
        //    send(host, port, '/key_pressure', 1, 127, 101)
        //    console.log("sent poly pressure 127")
        //    return
        // }

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