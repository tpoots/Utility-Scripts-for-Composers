module.exports = {

    init: function(){
        // this will be executed once when the osc server starts
    },

    oscInFilter:function(data){
        // Filter incoming osc messages

        var {address, args, host, port} = data

        console.log("oscInFilter: address = " + address + ", args = " + args + ", host = " + host + ", port = " + port)
        console.log("----")
        return {address, args, host, port}

    },

    oscOutFilter:function(data){
        // Filter outgoing osc messages

        var {address, args, host, port, clientId} = data
        console.log("oscOutFilter: address = " + address + ", args = " + args + ", host = " + host + ", port = " + port)
        console.log("----")

        // same as oscInFilter

        // return data if you want the message to be and sent
        return {address, args, host, port}
    },

    unload: function(){
        // this will be executed when the custom module is reloaded
    },

}