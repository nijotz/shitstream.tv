module.exports = {
  production: {
    client: 'pg',
    connection: {
      host: process.env.PG_HOST,
      port: 5432,
      user: 'shitstream',
      database:'shitstream',
    },
    pool: {
      min: 0,
      max: 5
    }
  }
}
