const Router = require('express')();

const UsersController = require('../controllers/UserController.js');
const EventsController = require('../controllers/EventsController');
const TodosController = require('../controllers/TodosController');
const ActivitiesController = require('../controllers/ActivitiesController');


Router.use('/users', UsersController);
Router.use('/events', EventsController)
Router.use('/todolists', TodosController)
Router.use('/activities', ActivitiesController)
module.exports = Router;
