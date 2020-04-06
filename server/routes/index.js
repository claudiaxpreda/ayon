const Router = require('express')();

const UsersController = require('../controllers/UserController.js');
const EventsController = require('../controllers/EventsController');
Router.use('/users', UsersController);
Router.use('/events', EventsController);

module.exports = Router;
