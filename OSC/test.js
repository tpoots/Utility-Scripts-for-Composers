const xmljs = require('xml-js');
const fs = require('fs');


const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
  const data = fs.readFileSync('./SST Cello ~.expressionmap');
//  var json = xmljs.xml2json(data, {compact: false, spaces: 4});
//  console.log(json)
    var converted = xmljs.xml2js(data, {compact: false, spaces: 4});
    converted['elements'][0]['elements'].forEach(parseElements)
});

function parseElements(item, index, arr) {
  if (item['attributes']['name'] === 'name') {
    var expressionMapName = item['attributes']['value']
    console.log(expressionMapName)
  }
  if (item['attributes']['name'] === 'slots') {
    parsePSoundSlots(item['elements'])
  }
}

function parsePSoundSlots(elements) {
  elements.forEach(element => {
    if (element['name'] === 'list') {
      // found the list of articulations
      element['elements'].forEach(parseSlot)
    }
  })
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
  console.log('Name: ' + name + ' Keyswitch: ' + keySwitch)
}