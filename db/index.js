'use strict'
const knexConfig = require('../knexfile').production
const knex = require('knex')(knexConfig)

class DB {
  constructor() {
    knex.select().from('video').then(function(stuff) {
      console.log(stuff)
      console.log('hi')
    }, function(e) {
      console.log(e)
    })
  }
}

module.exports = knex
