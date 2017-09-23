'use strict'

const IPFS = require('ipfs')

const node = new IPFS()

node.on('ready', () => {
  // Your node is now ready to use \o/
  console.log('🚀  Your node is now ready to use')
  
  node.files.add({
    path: 'hello.txt',
  }, (err, result) => {
    if (err) return console.error(err)
    //File added!
    console.log('\nAdded file:', result[0].path, result[0].hash)
    console.log('Shutting down in 2 seconds')
    // stopping a node
    setTimeout(
      () => node.stop(() => console.log('💥  node is now offline ')),
      2000,
    )
  })
})