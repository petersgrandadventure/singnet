import AgiCrowdsaleContract from './AgiCrowdsale.json'

const contract = require('truffle-contract')
const { web3 } = window

const AgiCrowdsale = contract(AgiCrowdsaleContract)

AgiCrowdsale.setProvider(web3.currentProvider)

const contractInstance = AgiCrowdsale.at("0xddd78c1a0eb35ab17cf54385604ef75bc6cfec8e")

export default contractInstance