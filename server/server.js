'use strict'

const express = require('express')
const session = require('express-session')

const { PORT = '3000' } = process.env
const routes = require('./routes');
const app = express()

app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));

app.use(express.json());

app.use('/api', routes);

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