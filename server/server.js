'use strict'

const express = require('express')

const { PORT = '8080' } = process.env
const app = express()

app.get('/', (req, res) => {
  res.send('Welcome to homepage')
})

app.get('/api/events', (req, res) => {
  res.send('See your events')
})

app.post('/api/events', (req, res) => {
  res.send('request to add one event')
})

app.listen(PORT, () => console.log(`App is listening on port ${PORT}!`))