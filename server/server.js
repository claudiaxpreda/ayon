'use strict'

const express = require('express')
const session = require('express-session')
const cors = require('cors');
const promMid = require('express-prometheus-middleware');
const methodOverride = require('method-override');

require('dotenv').config()

const routes = require('./routes');
const app = express()

app.use(cors());
app.options('*', cors())

app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));

app.use(promMid({
  metricsPath: '/metrics',
  collectDefaultMetrics: true,
  requestDurationBuckets: [0.1, 0.5, 1, 1.5],
}));
app.use(methodOverride('_method'));

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

app.listen(process.env.PORT, () => console.log(`App is listening on port ${process.env.PORT}!`))