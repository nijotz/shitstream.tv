'use strict'

const Server = require('./server')
const Producer = require('./producer')
const DB = require('./db')
const Veejay = require('./veejay')

const producer = new Producer()
producer.start()

new Server()
setTimeout(() => new DB(), 1000)
//setInterval(() => console.log('hi'), 1000)
