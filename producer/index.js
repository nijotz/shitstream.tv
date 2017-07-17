const request = require('request-promise-native')
const { URL } = require('url')
const db = require('../db')
const util = require('util')
const exec = util.promisify(require('child_process').exec)

//this logger could be wrapped to make it nicer to work with.
const logger = require('bunyan').createLogger({
  name: 'producer',
  path: '/var/log/shitstream.log'
})

const dlRegex = /\[download\] Destination: (\S*)/

class Producer {
  start() {
    return this.update()
  }

  async getYoutubePosts() {
    try {
      return request('http://infoforcefeed.shithouse.tv/data/all').then((payload) => {
        return JSON.parse(payload).filter((el) => 
          /https?:\/\/(?:www\.)?youtube\.com\/watch\?/.test(el.url)
        )
      })
    } catch(e) {
      logger.error('ran into error while scraping youtube videos', {
        error: e
      })
      return []
    }
  }

  async update() {
    // this could be broken out a little more
    const posts = await this.getYoutubePosts()
    const existingKeys = await db.select('key').from('video')
    const keySet = new Set(existingKeys)
    const newPosts = await posts.filter((post) => {
      const key = new URL(post.url).searchParams.get('v')
      return !keySet.has(key)
    })

    for(let i = 0; i < newPosts.length; i++) {
      const post = newPosts[i]
      const key = new URL(post.url).searchParams.get('v')
      const dlString = `youtube-dl --max-filesize 500M --id -i --download-archive shitstream-downloads http://www.youtube.com/watch?v=${key}`

      try {
        // try to download
        const output = await exec(dlString)
        const matches = dlRegex.exec(output.stdout)
        const filename = matches && matches[1]

        await db.transaction(function insertVideo(trx) {
          // try to insert a video entry
          return trx.insert({
            filename: filename || key + '.mp4',
            origin: {
              created_at: post.created_at,
              person: post.person,
              title: post.title
            },
            key: key
          }, '*').into('video').then((video) => {
            // try to insert a weight entry for the new video
            return db('weight').insert({
              video_id: video.id,
              weight: 1
            })
          })
        })
      } catch (e) {
        // XXX: the file can download and the insert can fail, the video
        // should be cleaned up or the entry should be retried in that
        // case
        logger.error('ran into error while creating video entry', {
          error: e
        })
      }
    }

    // wait 30 minutes
    // enable/disable this?
    setTimeout(this.update.bind(this), 30*60*1000)
  }
}
module.exports = Producer
