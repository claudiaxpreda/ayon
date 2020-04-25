const mongoose = require('mongoose');

(async () => {
  try {
    await mongoose.connect(`mongodb://${process.env.DBHOST}:${process.env.DBPORT}/ayondb`, {
        useNewUrlParser: true,
        useUnifiedTopology: true
      });
    console.log("Db connected");
  } catch (e) {
    console.trace(e);
  }
})();

mongoose.set('useCreateIndex', true);
mongoose.set('useFindAndModify', false);

const Users = require('./models/Users.js');
const Events = require('./models/Events.js');
const Todos = require('./models/Todos.js');



module.exports = {
  Users,
  Events,
  Todos
}
